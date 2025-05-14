import cv2
import numpy as np
import pickle
import zlib
import time
import os
from datetime import datetime
from tqdm import tqdm
from .frame_processor import FrameProcessor, BLOCK_SIZE
from config import *

class VideoEncoder:
    """Класс для кодирования видео с использованием DCT-сжатия"""
    
    def __init__(self, output_file, quality=50, keyframe_interval=10, verbose=False):
        """
        Инициализация кодировщика видео
        
        :param output_file: Выходной файл для сохранения
        :param quality: Качество сжатия (1-100)
        :param keyframe_interval: Интервал между ключевыми кадрами
        :param verbose: Флаг подробного вывода
        """
        self.output_file = output_file
        self.quality = quality
        self.keyframe_interval = keyframe_interval
        self.verbose = verbose
        self.frame_processor = FrameProcessor()
        self.start_time = None
        self.total_frames = 0
        self.processed_frames = 0
        self.original_size = 0
        self.compressed_size = 0
        self.metadata = {}
        # Инициализация атрибутов для хранения информации о видео
        self.width = 0
        self.height = 0
        self.fps = 0

    def _save_metadata(self, file):
        """
        Сохранение метаданных видео в файл
        
        :param file: Файловый объект для записи
        """
        # Сохраняем все необходимые метаданные
        self.metadata = {
            'fps': self.fps,
            'width': self.width,
            'height': self.height,
            'total_frames': self.total_frames,
            'quality': self.quality,
            'keyframe_interval': self.keyframe_interval,
            'version': '1.0',
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if self.verbose:
            print(f"Сохранение метаданных: {self.metadata}")
        
        try:
            # Сериализуем метаданные в байты
            metadata_bytes = pickle.dumps(self.metadata)
            
            if self.verbose:
                print(f"Размер сериализованных метаданных: {len(metadata_bytes)} байт")
                print(f"Первые 20 байт (hex): {' '.join(f'{b:02x}' for b in metadata_bytes[:20])}")
            
            # Записываем размер метаданных и сами метаданные
            file.write(len(metadata_bytes).to_bytes(4, byteorder='big'))
            file.write(metadata_bytes)
            file.flush()  # Убедимся, что данные записаны на диск
            
            if self.verbose:
                print("Метаданные успешно записаны в файл")
                
        except Exception as e:
            error_msg = f"Ошибка при сохранении метаданных: {str(e)}"
            if self.verbose:
                import traceback
                error_msg += f"\n\nТрассировка:\n{traceback.format_exc()}"
            raise Exception(error_msg)

    def _format_size(self, size_bytes):
        """
        Форматирование размера в удобочитаемый вид
        
        :param size_bytes: Размер в байтах
        :return: Строка с отформатированным размером
        """
        if size_bytes == 0:
            return "0 Б"
        size_names = ("Б", "КБ", "МБ", "ГБ", "ТБ")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    def _print_progress_header(self, metadata):
        """
        Вывод заголовка с информацией о кодировании
        
        :param metadata: Словарь с метаданными видео
        """
        if not self.verbose:
            return
            
        print("\n" + "=" * 70)
        print(f"{' КОДИРОВАНИЕ ВИДЕО ':=^70}")
        print("=" * 70)
        print(f"{'Входной файл:':<15} {os.path.basename(self.input_file)}")
        print(f"{'Выходной файл:':<15} {os.path.basename(self.output_file)}")
        print(f"{'Разрешение:':<15} {metadata['width']}x{metadata['height']}")
        print(f"{'Кадров:':<15} {metadata['total_frames']} ({metadata['fps']:.2f} к/с)")
        print(f"{'Качество:':<15} {self.quality}/100")
        print(f"{'Ключ. кадры:':<15} Каждый {self.keyframe_interval}-й кадр")
        print(f"{'Размер блока:':<15} {BLOCK_SIZE}x{BLOCK_SIZE}")
        print("-" * 70)
        self.start_time = time.time()

    def _print_progress(self, current_frame, total_frames, frame_size, compressed_size):
        """
        Вывод информации о прогрессе кодирования
        
        :param current_frame: Текущий обрабатываемый кадр
        :param total_frames: Общее количество кадров
        :param frame_size: Размер текущего кадра в байтах
        :param compressed_size: Размер сжатого кадра в байтах
        """
        if not self.verbose:
            return
            
        elapsed = time.time() - self.start_time
        fps = current_frame / elapsed if elapsed > 0 else 0
        remaining = (total_frames - current_frame) / fps if fps > 0 else 0
        
        # Обновление счетчиков размера
        self.original_size += frame_size
        self.compressed_size += compressed_size
        compression_ratio = (self.original_size / self.compressed_size) if self.compressed_size > 0 else 0
        
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
            f"Осталось: {remaining:.1f}с | "
            f"Сжатие: {compression_ratio:.2f}×"
        )
        print(status, end="")
        
        if current_frame == total_frames:
            print("\n" + "-" * 70)
            print(f"{'Исходный размер:':<20} {self._format_size(self.original_size)}")
            print(f"{'Сжатый размер:':<20} {self._format_size(self.compressed_size)}")
            print(f"{'Степень сжатия:':<20} {compression_ratio:.2f}×")
            print(f"{'Затрачено времени:':<20} {elapsed:.2f} сек")
            print(f"{'Средняя скорость:':<20} {total_frames/elapsed:.2f} к/с" if elapsed > 0 else "")
            print("=" * 70 + "\n")

    def _save_to_file(self, frames_data):
        """
        Сохранение сжатых данных в файл
        
        :param frames_data: Список сжатых кадров
        """
        try:
            with open(self.output_file, 'wb') as f:
                # Сохраняем метаданные (они уже содержат все необходимые поля)
                self._save_metadata(f)
                
                # Обработка и сохранение каждого кадра
                for frame in frames_data:
                    frame_bytes = pickle.dumps(frame)
                    compressed_data = zlib.compress(frame_bytes)
                    f.write(len(compressed_data).to_bytes(4, byteorder='big'))
                    f.write(compressed_data)
                    
        except Exception as e:
            if os.path.exists(self.output_file):
                os.remove(self.output_file)
            raise Exception(f"Ошибка при сохранении файла: {str(e)}")
        
        # Расчет статистики сжатия
        original_size = sum(frame.nbytes for frame in frames_data if hasattr(frame, 'nbytes'))
        compressed_size = os.path.getsize(self.output_file)
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
        
        if self.verbose:
            elapsed = time.time() - self.start_time if self.start_time else 0
            print(f"\n{'Файл сохранен:':<20} {os.path.basename(self.output_file)}")
            print(f"{'Исходное видео:':<20} {self._format_size(original_size)}")
            print(f"{'Сжатый размер:':<20} {self._format_size(compressed_size)}")
            print(f"{'Финальное сжатие:':<20} {compression_ratio:.2f}×")
            if elapsed > 0:
                print(f"{'Затрачено времени:':<20} {elapsed:.2f} сек")
                print(f"{'Средняя скорость:':<20} {self.total_frames/elapsed:.2f} к/с")
            print("=" * 70 + "\n")

    def encode(self, video_path):
        """
        Кодирование видеофайла
        
        :param video_path: Путь к исходному видеофайлу
        :return: Список сжатых кадров
        """
        self.input_file = video_path
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Не удалось открыть видеофайл: {video_path}")
            
        # Инициализация атрибутов видео
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Получение общего количества кадров
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Сохранение метаданных видео
        metadata = {
            'fps': self.fps,
            'width': self.width,
            'height': self.height,
            'total_frames': total_frames,
            'quality': self.quality,
            'keyframe_interval': self.keyframe_interval,
            'block_size': BLOCK_SIZE,
            'version': '1.0',
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        frames_data = []
        prev_frame = None
        frame_count = 0
        self.total_frames = total_frames
        self.processed_frames = 0
        self.original_size = 0
        self.compressed_size = 0

        # Вывод заголовка
        self._print_progress_header(metadata)

        # Обработка кадров
        pbar = None if self.verbose else tqdm(total=total_frames, desc="Обработка", unit="кадр")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Определяем, является ли кадр ключевым
            is_keyframe = (frame_count % self.keyframe_interval == 0) or (prev_frame is None)
            
            # Обработка кадра
            compressed_frame = self.frame_processor.compress_frame(
                frame, prev_frame, is_keyframe, self.quality
            )
            
            # Расчет размеров кадра
            frame_size = frame.nbytes
            compressed_size = len(pickle.dumps(compressed_frame))
            
            frames_data.append(compressed_frame)
            prev_frame = frame if is_keyframe else prev_frame
            frame_count += 1
            self.processed_frames = frame_count
            
            # Обновление прогресса
            if self.verbose:
                self._print_progress(frame_count, total_frames, frame_size, compressed_size)
            elif pbar:
                pbar.update(1)

        # Освобождение ресурсов
        cap.release()
        if pbar:
            pbar.close()

        # Сохранение в файл
        self._save_to_file(frames_data)
        
        # Вывод итоговой статистики, если не используется подробный вывод
        if not self.verbose and frame_count > 0:
            elapsed = time.time() - self.start_time if hasattr(self, 'start_time') and self.start_time else 0
            if elapsed > 0:
                print(f"\nЗакодировано {frame_count} кадров за {elapsed:.2f} сек ({frame_count/elapsed:.2f} к/с)")
            print(f"Исходный размер: {self._format_size(self.original_size)}")
            print(f"Сжатый размер: {self._format_size(self.compressed_size)}")
            print(f"Степень сжатия: {self.original_size/self.compressed_size if self.compressed_size > 0 else 0:.2f}×")
        
        return frames_data