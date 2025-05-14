import cv2
import numpy as np
import pickle
import zlib
import os
import time
import math
from datetime import datetime
from tqdm import tqdm
from .frame_processor import FrameProcessor

class VideoDecoder:
    """Класс для декодирования видео, сжатого с использованием DCT"""
    
    def __init__(self, input_file, verbose=False):
        """
        Инициализация декодера видео
        
        :param input_file: Входной сжатый файл
        :param verbose: Флаг подробного вывода
        """
        self.input_file = input_file
        self.verbose = verbose
        self.frame_processor = FrameProcessor()
        self.metadata = {}
        self.start_time = None
        self.processed_frames = 0
        self.original_size = 0
        self.decompressed_size = 0

    def _format_size(self, size_bytes):
        """Format size in human readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    def _print_progress_header(self):
        """Вывод заголовка с информацией о декодировании"""
        if not self.verbose:
            return
            
        print("\n" + "=" * 70)
        print(f"{' ДЕКОДИРОВАНИЕ ВИДЕО ':=^70}")
        print("=" * 70)
        print(f"{'Входной файл:':<15} {os.path.basename(self.input_file)}")
        print(f"{'Разрешение:':<15} {self.width}x{self.height}")
        print(f"{'Кадров:':<15} {self.total_frames} ({self.fps:.2f} к/с)")
        print(f"{'Качество:':<15} {self.quality}/100")
        print("-" * 70)
        self.start_time = time.time()

    def _print_progress(self, current_frame, total_frames, frame_size):
        """
        Вывод информации о прогрессе декодирования
        
        :param current_frame: Текущий обрабатываемый кадр
        :param total_frames: Общее количество кадров
        :param frame_size: Размер текущего кадра в байтах
        """
        if not self.verbose:
            return
            
        elapsed = time.time() - self.start_time
        fps = current_frame / elapsed if elapsed > 0 else 0
        remaining = (total_frames - current_frame) / fps if fps > 0 else 0
        
        # Очистка предыдущего вывода
        print("\r" + " " * 100, end="")
        
        # Отрисовка прогресс-бара
        bar_length = 40
        progress = current_frame / total_frames
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # Формирование строки статуса
        status = (
            f"\r[Кадр {current_frame:4d}/{total_frames}] |{bar}| "
            f"{progress*100:5.1f}% | "
            f"{fps:.1f} к/с | "
            f"Осталось: {remaining:.1f}с"
        )
        print(status, end="")
        
        if current_frame == total_frames:
            print("\n" + "-" * 70)
            print(f"{'Затрачено времени:':<20} {elapsed:.2f} сек")
            print(f"{'Средняя скорость:':<20} {total_frames/elapsed:.2f} к/с" if elapsed > 0 else "")
            print("=" * 70 + "\n")

    def _load_metadata(self, file):
        """
        Загрузка метаданных видео из файла
        
        :param file: Файловый объект для чтения
        """
        self.metadata = pickle.load(file)
        self.fps = self.metadata.get('fps', 30)
        self.width = self.metadata.get('width', 640)
        self.height = self.metadata.get('height', 480)
        self.total_frames = self.metadata.get('total_frames', 0)
        self.quality = self.metadata.get('quality', 50)
        self.keyframe_interval = self.metadata.get('keyframe_interval', 10)

    def _read_next_frame(self, file):
        """Read the next frame from the compressed file"""
        # Read frame size (4 bytes)
        size_bytes = file.read(4)
        if not size_bytes:
            return None
            
        frame_size = int.from_bytes(size_bytes, byteorder='big')
        if frame_size == 0:
            return None
            
        # Read compressed frame data
        compressed_data = file.read(frame_size)
        if not compressed_data or len(compressed_data) != frame_size:
            return None
            
        # Decompress and deserialize the frame
        return pickle.loads(zlib.decompress(compressed_data))

    def decode(self, output_file):
        """
        Декодирование видеофайла и сохранение в указанный файл
        
        :param output_file: Путь для сохранения декодированного видео
        :return: Количество обработанных кадров
        """
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Входной файл не найден: {self.input_file}")

        # Чтение метаданных и кадров
        with open(self.input_file, 'rb') as f:
            # Загрузка метаданных
            self._load_metadata(f)
            
            # Вывод заголовка
            self._print_progress_header()
            
            # Инициализация видеопотока для записи
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(
                output_file, 
                fourcc, 
                self.fps, 
                (self.width, self.height)
            )
            
            prev_frame = None
            frame_count = 0
            total_frames = self.total_frames
            
            # Инициализация индикатора прогресса
            pbar = None if self.verbose else tqdm(total=total_frames, desc="Декодирование", unit="кадр")
            
            # Чтение и обработка каждого кадра
            while True:
                frame_data = self._read_next_frame(f)
                if frame_data is None:
                    break
                
                # Распаковка кадра
                frame = self.frame_processor.decompress_frame(frame_data, prev_frame)
                
                # Запись кадра в выходной файл
                out.write(frame)
                frame_count += 1
                
                # Обновление предыдущего кадра, если это ключевой кадр
                if frame_data.get('is_keyframe', False):
                    prev_frame = frame
                
                # Обновление прогресса
                if self.verbose:
                    self._print_progress(frame_count, total_frames, frame.nbytes)
                elif pbar:
                    pbar.update(1)
        if pbar:
            pbar.close()
            
        # Print final summary if not in verbose mode
        if not self.verbose and frame_count > 0:
            elapsed = time.time() - self.start_time if hasattr(self, 'start_time') and self.start_time else 0
            print(f"\nDecoded {frame_count} frames in {elapsed:.2f} seconds ({frame_count/elapsed:.2f} fps)" if elapsed > 0 else "")
            
        return frame_count