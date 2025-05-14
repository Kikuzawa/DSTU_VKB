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
        try:
            # Сохраняем текущую позицию в файле
            start_pos = file.tell()
            
            # Пытаемся прочитать первые несколько байт для отладки
            debug_bytes = file.read(100)
            if not debug_bytes:
                raise ValueError("Файл пуст")
                
            # Возвращаемся в начало файла
            file.seek(start_pos)
            
            # Читаем размер метаданных
            size_bytes = file.read(4)
            if not size_bytes or len(size_bytes) != 4:
                raise ValueError(f"Неверный формат файла: не удалось прочитать размер метаданных. Первые байты: {debug_bytes[:20]}")
                
            metadata_size = int.from_bytes(size_bytes, byteorder='big')
            if metadata_size <= 0:
                raise ValueError(f"Неверный размер метаданных: {metadata_size}")
                
            # Читаем метаданные
            metadata_bytes = file.read(metadata_size)
            if not metadata_bytes or len(metadata_bytes) != metadata_size:
                raise ValueError(f"Не удалось прочитать метаданные: неверный размер данных. Ожидалось {metadata_size}, получено {len(metadata_bytes) if metadata_bytes else 0}")
                
            # Пробуем десериализовать метаданные
            try:
                self.metadata = pickle.loads(metadata_bytes)
            except Exception as pickle_error:
                # Выводим отладочную информацию о первых байтах метаданных
                debug_hex = ' '.join(f'{b:02x}' for b in metadata_bytes[:min(20, len(metadata_bytes))])
                raise ValueError(f"Ошибка десериализации метаданных: {str(pickle_error)}. Первые байты (hex): {debug_hex}")
            
            # Проверяем, что метаданные - это словарь
            if not isinstance(self.metadata, dict):
                raise ValueError(f"Ожидался словарь метаданных, получен {type(self.metadata)}")
            
            # Извлекаем основные параметры
            self.fps = self.metadata.get('fps', 30)
            self.width = self.metadata.get('width', 640)
            self.height = self.metadata.get('height', 480)
            self.total_frames = self.metadata.get('total_frames', 0)
            self.quality = self.metadata.get('quality', 50)
            self.keyframe_interval = self.metadata.get('keyframe_interval', 10)
            
            # Выводим отладочную информацию
            if self.verbose:
                print(f"Загружены метаданные: {self.metadata}")
            
        except Exception as e:
            # Добавляем дополнительную информацию об ошибке
            error_msg = f"Ошибка при загрузке метаданных: {str(e)}"
            if self.verbose:
                import traceback
                error_msg += f"\n\nТрассировка:\n{traceback.format_exc()}"
            raise Exception(error_msg)

    def _read_next_frame(self, file):
        """
        Чтение следующего кадра из сжатого файла
        
        :param file: Файловый объект для чтения
        :return: Словарь с данными кадра или None, если достигнут конец файла
        """
        try:
            # Читаем размер данных кадра (4 байта)
            size_bytes = file.read(4)
            if not size_bytes:
                if self.verbose:
                    print("Достигнут конец файла при чтении размера кадра")
                return None
                
            if len(size_bytes) != 4:
                raise ValueError(f"Не удалось прочитать размер кадра: получено {len(size_bytes)} байт вместо 4")
                
            frame_size = int.from_bytes(size_bytes, byteorder='big')
            if frame_size <= 0:
                if self.verbose:
                    print(f"Обнаружен нулевой размер кадра: {frame_size}")
                return None
            
            if self.verbose:
                print(f"Чтение кадра размером {frame_size} байт")
                
            # Читаем сжатые данные кадра
            compressed_data = file.read(frame_size)
            if not compressed_data:
                if self.verbose:
                    print("Не удалось прочитать данные кадра: файл закончился")
                return None
                
            if len(compressed_data) != frame_size:
                raise ValueError(f"Неверный размер данных кадра: ожидалось {frame_size} байт, получено {len(compressed_data)} байт")
            
            # Распаковываем и десериализуем кадр
            try:
                decompressed_data = zlib.decompress(compressed_data)
                frame_data = pickle.loads(decompressed_data)
                
                if self.verbose and isinstance(frame_data, dict):
                    frame_info = {
                        'is_keyframe': frame_data.get('is_keyframe', False),
                        'data_size': len(decompressed_data),
                        'compressed_size': frame_size
                    }
                    print(f"Прочитан кадр: {frame_info}")
                
                return frame_data
                
            except zlib.error as e:
                raise Exception(f"Ошибка распаковки данных кадра: {str(e)}")
            except pickle.PickleError as e:
                raise Exception(f"Ошибка десериализации кадра: {str(e)}")
                
        except Exception as e:
            error_msg = f"Ошибка при чтении кадра: {str(e)}"
            if self.verbose:
                import traceback
                error_msg += f"\n\nТрассировка:\n{traceback.format_exc()}"
            raise Exception(error_msg)

    def decode(self, output_file):
        """
        Декодирование видеофайла и сохранение в указанный файл
        
        :param output_file: Путь для сохранения декодированного видео
        :return: Количество обработанных кадров
        """
        if self.verbose:
            print(f"Начало декодирования файла: {self.input_file}")
            print(f"Целевой файл: {output_file}")
        
        frame_count = 0
        pbar = None
        out = None
        
        try:
            # Открываем файл для чтения
            with open(self.input_file, 'rb') as f:
                if self.verbose:
                    print("Файл успешно открыт для чтения")
                
                # Загружаем метаданные
                self._load_metadata(f)
                
                if self.verbose:
                    print(f"Метаданные загружены: {self.metadata}")
                
                # Создаем объект VideoWriter
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_file, fourcc, self.fps, (self.width, self.height))
                
                if not out.isOpened():
                    raise Exception(f"Не удалось создать выходной файл: {output_file}")
                
                if self.verbose:
                    print(f"Создан VideoWriter с параметрами: fps={self.fps}, размер={self.width}x{self.height}")
                
                # Вывод заголовка
                self._print_progress_header()
                
                # Инициализируем индикатор прогресса
                if not self.verbose:
                    pbar = tqdm(total=self.total_frames, desc="Декодирование", unit="кадр")
                
                prev_frame = None
                
                # Читаем и обрабатываем кадры
                while True:
                    if self.verbose and frame_count % 10 == 0:
                        print(f"Обработка кадра {frame_count}")
                    
                    # Читаем следующий кадр
                    frame_data = self._read_next_frame(f)
                    if frame_data is None:
                        if self.verbose:
                            print("Достигнут конец файла")
                        break
                    
                    # Декомпрессируем кадр
                    try:
                        frame = self.frame_processor.decompress_frame(frame_data, prev_frame)
                    except Exception as e:
                        raise Exception(f"Ошибка при декомпрессии кадра {frame_count}: {str(e)}")
                    
                    # Проверяем размер кадра
                    if frame is not None and (frame.shape[0] != self.height or frame.shape[1] != self.width):
                        if self.verbose:
                            print(f"Предупреждение: несоответствие размера кадра. Ожидалось {self.width}x{self.height}, получено {frame.shape[1]}x{frame.shape[0]}")
                        frame = cv2.resize(frame, (self.width, self.height))
                    
                    # Записываем кадр в выходной файл
                    if frame is not None:
                        out.write(frame)
                    
                    # Обновляем предыдущий кадр, если это ключевой кадр
                    if frame_data.get('is_keyframe', False):
                        prev_frame = frame
                    
                    # Обновляем счетчик кадров и прогресс
                    frame_count += 1
                    if self.verbose:
                        self._print_progress(frame_count, self.total_frames, frame.nbytes if frame is not None else 0)
                    elif pbar:
                        pbar.update(1)
                
        except Exception as e:
            error_msg = f"Ошибка при декодировании видео: {str(e)}"
            if self.verbose:
                import traceback
                error_msg += f"\n\nТрассировка:\n{traceback.format_exc()}"
            raise Exception(error_msg)
            
        finally:
            # Закрываем ресурсы
            if out is not None:
                out.release()
                if self.verbose:
                    print(f"Освобождены ресурсы VideoWriter. Обработано кадров: {frame_count}")
            
            if pbar is not None:
                pbar.close()
        
        # Выводим итоговую статистику, если не используется подробный вывод
        if not self.verbose and frame_count > 0:
            elapsed = time.time() - self.start_time if hasattr(self, 'start_time') and self.start_time else 0
            if elapsed > 0:
                print(f"\nДекодировано {frame_count} кадров за {elapsed:.2f} сек ({frame_count/elapsed:.2f} к/с)")
        
        return frame_count