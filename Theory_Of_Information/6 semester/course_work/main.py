import cv2
import numpy as np
from skimage.measure import block_reduce


def dct_compress(block, quality=10):
    """Применяет ДКП и квантование к блоку 8x8"""
    # ДКП
    dct_block = cv2.dct(block.astype(np.float32))

    # Простое квантование (зануляем высокие частоты)
    rows, cols = dct_block.shape
    for i in range(rows):
        for j in range(cols):
            if i + j > 8:  # Порог для сохранения низких частот
                dct_block[i, j] = 0
            else:
                dct_block[i, j] = np.round(dct_block[i, j] / quality) * quality

    return dct_block


def process_frame(frame, prev_frame=None, block_size=8):
    """Обрабатывает кадр с ДКП и разностным кодированием"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    if prev_frame is None:
        # Первый кадр - обрабатываем целиком
        processed = np.zeros_like(gray, dtype=np.float32)
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = gray[y:y + block_size, x:x + block_size]
                if block.shape == (block_size, block_size):
                    processed[y:y + block_size, x:x + block_size] = dct_compress(block)
        return processed, gray

    else:
        # Разностное кодирование
        delta = gray.astype(np.int16) - prev_frame.astype(np.int16)

        # Обрабатываем разницу
        processed = np.zeros_like(gray, dtype=np.float32)
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = delta[y:y + block_size, x:x + block_size]
                if block.shape == (block_size, block_size):
                    processed[y:y + block_size, x:x + block_size] = dct_compress(block.astype(np.float32))

        # Восстанавливаем кадр
        reconstructed = np.clip(processed + prev_frame, 0, 255).astype(np.uint8)
        return reconstructed, gray


def compress_video(input_path, output_path, show_preview=False):
    """Основная функция компрессии видео"""
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)

    prev_frame = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, current_gray = process_frame(frame, prev_frame)
        prev_frame = current_gray

        out.write(processed_frame)
        frame_count += 1

        if show_preview:
            cv2.imshow('Compressed', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Compression complete! {frame_count} frames processed.")


# Использование
if __name__ == "__main__":
    input_video = "input.mp4"
    output_video = "compressed.mp4"
    compress_video(input_video, output_video, show_preview=True)