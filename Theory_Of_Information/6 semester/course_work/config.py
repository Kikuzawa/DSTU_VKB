import numpy as np

def create_quantization_matrix(size, quality_scale=1.0):
    """Create a quantization matrix with adjustable quality"""
    # Base quantization matrix (similar to JPEG but for 16x16)
    base = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61, 70, 80, 85, 90, 95, 100, 105, 110],
        [12, 12, 14, 19, 26, 58, 60, 55, 60, 65, 70, 75, 80, 85, 90, 95],
        [14, 13, 16, 24, 40, 57, 69, 56, 55, 60, 65, 70, 75, 80, 85, 90],
        [14, 17, 22, 29, 51, 87, 80, 62, 60, 55, 60, 65, 70, 75, 80, 85],
        [18, 22, 37, 56, 68, 109, 103, 77, 65, 60, 55, 60, 65, 70, 75, 80],
        [24, 35, 55, 64, 81, 104, 113, 92, 70, 65, 60, 55, 60, 65, 70, 75],
        [49, 64, 78, 87, 103, 121, 120, 101, 75, 70, 65, 60, 55, 60, 65, 70],
        [72, 92, 95, 98, 112, 100, 103, 99, 80, 75, 70, 65, 60, 55, 60, 65],
        [70, 80, 85, 90, 95, 100, 105, 110, 85, 80, 75, 70, 65, 60, 55, 60],
        [60, 65, 70, 75, 80, 85, 90, 95, 90, 85, 80, 75, 70, 65, 60, 55],
        [55, 60, 65, 70, 75, 80, 85, 90, 95, 90, 85, 80, 75, 70, 65, 60],
        [60, 55, 60, 65, 70, 75, 80, 85, 90, 95, 90, 85, 80, 75, 70, 65],
        [65, 60, 55, 60, 65, 70, 75, 80, 85, 90, 95, 90, 85, 80, 75, 70],
        [70, 65, 60, 55, 60, 65, 70, 75, 80, 85, 90, 95, 90, 85, 80, 75],
        [75, 70, 65, 60, 55, 60, 65, 70, 75, 80, 85, 90, 95, 90, 85, 80],
        [80, 75, 70, 65, 60, 55, 60, 65, 70, 75, 80, 85, 90, 95, 90, 85]
    ], dtype=np.float32)
    
    # Apply quality scaling
    if quality_scale < 1.0:
        quality_scale = 1.0
    
    # Scale the matrix based on quality
    scaled = np.maximum(1, base * quality_scale)
    
    return scaled

# Block size (16x16 for better compression)
BLOCK_SIZE = 16
# Keyframe every 30 frames (1 second for 30fps video)
KEYFRAME_INTERVAL = 30
# Chroma subsampling (4:2:0)
CHROMA_SUBSAMPLING = True