import cv2
import numpy as np
from config import (
    BLOCK_SIZE,
    KEYFRAME_INTERVAL,
    CHROMA_SUBSAMPLING,
    create_quantization_matrix
)

class FrameProcessor:
    @staticmethod
    def _get_quantization_matrix(quality, is_chroma=False):
        """Get quantization matrix based on quality"""
        # Higher quality = lower values = less quantization
        if quality <= 10:
            scale = 5.0
        elif quality <= 30:
            scale = 3.0
        elif quality <= 50:
            scale = 2.0
        elif quality <= 70:
            scale = 1.5
        else:
            scale = 1.0
            
        # Chroma channels can use more aggressive quantization
        if is_chroma:
            scale *= 1.5
            
        return create_quantization_matrix(BLOCK_SIZE, scale)

    @staticmethod
    def _process_block(block, is_chroma=False, quality=50):
        """Process a single block with DCT and quantization"""
        # Get quantization matrix for this quality level
        q_matrix = FrameProcessor._get_quantization_matrix(quality, is_chroma)
        
        # Apply DCT
        dct_block = cv2.dct(block.astype(np.float32))
        
        # Apply quantization
        quantized = np.round(dct_block / q_matrix).astype(np.int16)
        
        # Zero out high-frequency coefficients (zigzag order)
        # More aggressive zeroing for higher compression
        zero_threshold = BLOCK_SIZE * (1.5 - (quality / 100))
        for i in range(BLOCK_SIZE):
            for j in range(BLOCK_SIZE):
                if i + j >= zero_threshold:
                    quantized[i,j] = 0
                    
        # Remove very small values (they're likely noise)
        quantized[np.abs(quantized) < 2] = 0
        
        return quantized

    @staticmethod
    def _inverse_process_block(block, is_chroma=False, quality=50):
        """Inverse process for a single block"""
        # Get the same quantization matrix used for encoding
        q_matrix = FrameProcessor._get_quantization_matrix(quality, is_chroma)
        
        # Apply inverse quantization and IDCT
        dequantized = block * q_matrix
        return cv2.idct(dequantized.astype(np.float32))

    @staticmethod
    def _apply_rle(block):
        """Apply Run-Length Encoding to a block"""
        # Flatten the block in zigzag order
        flat = []
        for i in range(BLOCK_SIZE + BLOCK_SIZE - 1):
            if i % 2 == 0:  # Up-right direction
                x = min(i, BLOCK_SIZE - 1)
                y = i - x
                while x >= 0 and y < BLOCK_SIZE:
                    flat.append(block[x, y])
                    x -= 1
                    y += 1
            else:  # Down-left direction
                y = min(i, BLOCK_SIZE - 1)
                x = i - y
                while y >= 0 and x < BLOCK_SIZE:
                    flat.append(block[x, y])
                    x += 1
                    y -= 1
        
        # Simple RLE
        rle = []
        count = 1
        for i in range(1, len(flat)):
            if flat[i] == flat[i-1] and count < 255:
                count += 1
            else:
                rle.extend([count, flat[i-1]])
                count = 1
        rle.extend([count, flat[-1]])
        
        return rle

    @staticmethod
    def _process_channel(channel, quality, is_keyframe, prev_channel=None, is_chroma=False):
        """Process a single color channel"""
        height, width = channel.shape
        
        # For chroma subsampling
        if CHROMA_SUBSAMPLING and is_chroma:
            # Downsample chroma channels (4:2:0)
            channel = cv2.resize(channel, (width//2, height//2), interpolation=cv2.INTER_AREA)
            
        # Process in blocks
        blocks = []
        for y in range(0, channel.shape[0], BLOCK_SIZE):
            for x in range(0, channel.shape[1], BLOCK_SIZE):
                block = channel[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
                if block.shape[0] == BLOCK_SIZE and block.shape[1] == BLOCK_SIZE:
                    if is_keyframe or prev_channel is None:
                        # I-frame: process directly
                        processed_block = FrameProcessor._process_block(
                            block, is_chroma, quality)
                    else:
                        # P-frame: process difference from previous frame
                        prev_block = prev_channel[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
                        if prev_block.shape == (BLOCK_SIZE, BLOCK_SIZE):
                            diff = block.astype(np.float32) - prev_block.astype(np.float32)
                            processed_block = FrameProcessor._process_block(
                                diff, is_chroma, quality)
                        else:
                            # If shapes don't match, process as I-frame
                            processed_block = FrameProcessor._process_block(
                                block, is_chroma, quality)
                    
                    # Apply RLE to the block
                    rle_block = FrameProcessor._apply_rle(processed_block)
                    blocks.append(rle_block)
        
        return blocks

    @staticmethod
    def _decode_rle(rle_data):
        """Decode RLE data back to block"""
        # Reconstruct flat array from RLE
        flat = []
        for i in range(0, len(rle_data), 2):
            count = rle_data[i]
            value = rle_data[i+1]
            flat.extend([value] * count)
        
        # Reconstruct block from zigzag order
        block = np.zeros((BLOCK_SIZE, BLOCK_SIZE), dtype=np.int16)
        idx = 0
        for i in range(BLOCK_SIZE + BLOCK_SIZE - 1):
            if i % 2 == 0:  # Up-right direction
                x = min(i, BLOCK_SIZE - 1)
                y = i - x
                while x >= 0 and y < BLOCK_SIZE and idx < len(flat):
                    block[x, y] = flat[idx]
                    x -= 1
                    y += 1
                    idx += 1
            else:  # Down-left direction
                y = min(i, BLOCK_SIZE - 1)
                x = i - y
                while y >= 0 and x < BLOCK_SIZE and idx < len(flat):
                    block[x, y] = flat[idx]
                    x += 1
                    y -= 1
                    idx += 1
        
        return block

    @staticmethod
    def _reconstruct_channel(compressed_blocks, quality, is_keyframe, prev_channel, width, height, is_chroma=False):
        """Reconstruct a single color channel"""
        # For chroma subsampling
        if CHROMA_SUBSAMPLING and is_chroma:
            width, height = width//2, height//2
            
        # Create empty channel
        channel = np.zeros((height, width), dtype=np.float32)
        
        block_idx = 0
        block_size = BLOCK_SIZE
        
        # Handle case where we might have a partial block at the edges
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                if block_idx < len(compressed_blocks):
                    # Get RLE data for this block
                    rle_data = compressed_blocks[block_idx]
                    
                    # Decode RLE and get the block
                    block = FrameProcessor._decode_rle(rle_data)
                    
                    # Apply inverse DCT with the same settings used for encoding
                    recon_block = FrameProcessor._inverse_process_block(block, is_chroma, quality)
                    
                    # Handle block reconstruction
                    block_h, block_w = recon_block.shape
                    target_h = min(block_size, height - y)
                    target_w = min(block_size, width - x)
                    
                    if is_keyframe or prev_channel is None:
                        # For I-frames, just use the reconstructed block
                        channel[y:y+target_h, x:x+target_w] = recon_block[:target_h, :target_w]
                    else:
                        # For P-frames, add the difference to the previous frame
                        prev_block = prev_channel[y:y+target_h, x:x+target_w]
                        channel[y:y+target_h, x:x+target_w] = recon_block[:target_h, :target_w] + prev_block
                    
                    block_idx += 1
        
        # For chroma subsampling, upsample back to original size
        if CHROMA_SUBSAMPLING and is_chroma:
            channel = cv2.resize(channel, (width*2, height*2), interpolation=cv2.INTER_LINEAR)
        
        return np.clip(channel, 0, 255).astype(np.uint8)

    @staticmethod
    def compress_frame(frame, prev_frame, is_keyframe, quality):
        """Compress a single frame"""
        if frame.ndim == 2:  # Grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # Convert to YCrCb color space (better for compression)
        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)
        
        # Get previous frame channels if available
        prev_channels = None
        if prev_frame is not None and not is_keyframe:
            prev_ycrcb = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2YCrCb)
            prev_y, prev_cr, prev_cb = cv2.split(prev_ycrcb)
            prev_channels = [prev_y, prev_cr, prev_cb]
        
        # Process Y channel (luminance) with higher quality
        compressed_y = FrameProcessor._process_channel(
            y, quality, is_keyframe, 
            prev_channels[0] if prev_channels else None,
            is_chroma=False
        )
        
        # Process Cr and Cb channels (chrominance) with more aggressive compression
        compressed_cr = FrameProcessor._process_channel(
            cr, quality, is_keyframe,
            prev_channels[1] if prev_channels else None,
            is_chroma=True
        )
        
        compressed_cb = FrameProcessor._process_channel(
            cb, quality, is_keyframe,
            prev_channels[2] if prev_channels else None,
            is_chroma=True
        )
        
        # Get frame dimensions
        height, width = frame.shape[:2]

        return {
            'channels': [compressed_y, compressed_cr, compressed_cb],
            'is_keyframe': is_keyframe,
            'quality': quality,
            'height': height,
            'width': width
        }

    @staticmethod
    def decompress_frame(compressed_data, prev_frame):
        """Decompress a single frame"""
        # Get previous frame channels if available
        prev_channels = None
        if prev_frame is not None and not compressed_data['is_keyframe']:
            prev_ycrcb = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2YCrCb)
            prev_y, prev_cr, prev_cb = cv2.split(prev_ycrcb)
            prev_channels = [prev_y, prev_cr, prev_cb]
        
        # Get frame dimensions from metadata
        height = compressed_data['height']
        width = compressed_data['width']
        quality = compressed_data['quality']
        is_keyframe = compressed_data['is_keyframe']
        
        # Reconstruct Y channel (luminance)
        y_blocks = compressed_data['channels'][0]
        y = FrameProcessor._reconstruct_channel(
            y_blocks, quality, is_keyframe,
            prev_channels[0] if prev_channels else None,
            width, height, is_chroma=False
        )
        
        # Reconstruct Cr and Cb channels (chrominance)
        cr_blocks = compressed_data['channels'][1]
        cr = FrameProcessor._reconstruct_channel(
            cr_blocks, quality, is_keyframe,
            prev_channels[1] if prev_channels else None,
            width, height, is_chroma=True
        )
        
        cb_blocks = compressed_data['channels'][2]
        cb = FrameProcessor._reconstruct_channel(
            cb_blocks, quality, is_keyframe,
            prev_channels[2] if prev_channels else None,
            width, height, is_chroma=True
        )
        
        # Merge channels and convert back to BGR
        ycrcb = cv2.merge([y, cr, cb])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)