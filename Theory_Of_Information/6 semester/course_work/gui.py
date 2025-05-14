import sys
import os
import time
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QFileDialog, QLabel, QSlider, QTextEdit, QSplitter,
                           QGroupBox, QSizePolicy, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon, QTextCursor

from core.encoder import VideoEncoder
from core.decoder import VideoDecoder

class VideoPlayer(QWidget):
    """Виджет для отображения видео"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 360)
        
        # Основной макет
        layout = QVBoxLayout()
        
        # Метка для отображения кадра
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        
        # Метка с информацией о видео
        self.info_label = QLabel("Видео не загружено")
        self.info_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.video_label, 1)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
        
        # Параметры видео
        self.cap = None
        self.frame_count = 0
        self.fps = 30
        self.duration = 0
        
    def load_video(self, video_path):
        """Загрузка видеофайла"""
        if self.cap is not None:
            self.cap.release()
            
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            return False
            
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.duration = self.frame_count / self.fps if self.fps > 0 else 0
        
        # Обновляем информацию о видео
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.info_label.setText(f"{os.path.basename(video_path)}\n{width}x{height} | {self.fps:.2f} FPS | {self.duration:.2f} сек")
        
        return True
    
    def get_frame(self, frame_num):
        """Получение кадра по номеру"""
        if self.cap is None:
            return None
            
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None
    
    def display_frame(self, frame):
        """Отображение кадра в QLabel"""
        if frame is None:
            return
            
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Масштабируем изображение под размер виджета с сохранением пропорций
        scaled_pixmap = QPixmap.fromImage(q_img).scaled(
            self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(scaled_pixmap)
    
    def closeEvent(self, event):
        """Очистка ресурсов при закрытии"""
        if self.cap is not None:
            self.cap.release()


class VideoProcessor(QThread):
    """Поток для обработки видео"""
    progress = pyqtSignal(int, int, str)  # текущий кадр, всего кадров, сообщение
    progress_percent = pyqtSignal(int)  # процент выполнения
    finished = pyqtSignal(bool, str)  # успех, сообщение
    log_message = pyqtSignal(str)  # сообщение в лог
    
    def __init__(self, operation, input_file, output_file, quality=50):
        super().__init__()
        self.operation = operation  # 'encode' или 'decode'
        self.input_file = input_file
        self.output_file = output_file
        self.quality = quality
        self.is_running = True
    
    def run(self):
        """Запуск обработки"""
        try:
            if self.operation == 'encode':
                self._encode()
            else:
                self._decode()
        except Exception as e:
            self.finished.emit(False, f"Ошибка: {str(e)}")
    
    def _encode(self):
        """Кодирование видео"""
        try:
            # Сохраняем путь к входному файлу как атрибут
            self.input_file = os.path.abspath(self.input_file)
            
            # Создаем экземпляр кодировщика
            encoder = VideoEncoder(
                output_file=self.output_file,
                quality=self.quality,
                verbose=False  # Отключаем стандартный вывод прогресса
            )
            
            # Получаем информацию о видео
            cap = cv2.VideoCapture(self.input_file)
            if not cap.isOpened():
                raise ValueError(f"Не удалось открыть видеофайл: {self.input_file}")
                
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            
            # Устанавливаем разрешение в кодировщик
            encoder.width = width
            encoder.height = height
            
            self.log_message.emit(f"Начато кодирование видео")
            self.log_message.emit(f"Всего кадров: {total_frames}")
            self.log_message.emit(f"Разрешение: {width}x{height}")
            self.log_message.emit(f"FPS: {fps:.2f}")
            self.log_message.emit(f"Качество: {self.quality}")
            self.log_message.emit("-" * 50)
            
            # Создаем кастомный tqdm-подобный объект для вывода прогресса
            class ProgressTracker:
                def __init__(self, total, progress_callback, log_callback):
                    self.total = total
                    self.processed = 0
                    self.progress_callback = progress_callback
                    self.log_callback = log_callback
                    self.last_log_time = time.time()
                    self.last_log_frame = 0
                
                def update(self, current_frame=1):
                    self.processed = current_frame
                    progress = int((self.processed / self.total) * 100)
                    self.progress_callback(min(progress, 100))
                    
                    # Логируем каждую секунду или при значительном изменении кадра
                    current_time = time.time()
                    if current_time - self.last_log_time >= 1.0 or current_frame - self.last_log_frame >= 100:
                        self.log_callback(f"Обработка кадра {current_frame}/{self.total} ({progress}%)")
                        self.last_log_time = current_time
                        self.last_log_frame = current_frame
            
            # Создаем трекер прогресса и сохраняем как атрибут
            self.progress_tracker = ProgressTracker(
                total_frames, 
                lambda p: self.progress_percent.emit(p),
                lambda msg: self.log_message.emit(msg)
            )
            
            # Переопределяем метод _print_progress в кодировщике
            original_print_progress = encoder._print_progress
            
            def custom_print_progress(self, current_frame, total_frames, frame_size, compressed_size):
                self.progress_tracker.update(current_frame + 1)  # current_frame начинается с 0
                
            # Подменяем метод вывода прогресса
            encoder._print_progress = custom_print_progress.__get__(encoder, VideoEncoder)
            # Сохраняем ссылку на трекер в кодировщике
            encoder.progress_tracker = self.progress_tracker
            
            # Запускаем кодирование и замеряем время
            start_time = time.time()
            encoder.encode(self.input_file)
            
            # Восстанавливаем оригинальный метод
            encoder._print_progress = original_print_progress
            
            elapsed = time.time() - start_time
            self.log_message.emit("-" * 50)
            self.log_message.emit(f"Кодирование успешно завершено!")
            self.log_message.emit(f"Затрачено времени: {elapsed:.1f} сек")
            if elapsed > 0:
                self.log_message.emit(f"Средняя скорость: {total_frames/elapsed:.2f} к/с")
            self.finished.emit(True, "Кодирование успешно завершено")
            
        except Exception as e:
            self.log_message.emit(f"Ошибка при кодировании: {str(e)}")
            self.finished.emit(False, f"Ошибка кодирования: {str(e)}")
    
    def _wrap_encode(self, encode_func):
        """Обертка для отслеживания прогресса кодирования"""
        def wrapper(encoder_self, video_path):
            try:
                # Получаем общее количество кадров из видео
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    self.progress_percent.emit(0)
                    return
                    
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()
                
                # Запускаем кодирование
                self.progress_percent.emit(0)
                
                # Вызываем оригинальный метод
                result = encode_func(video_path)
                
                # Устанавливаем 100% по завершении
                self.progress_percent.emit(100)
                return result
                
            except Exception as e:
                self.log_message.emit(f"Ошибка в обертке кодирования: {str(e)}")
                raise
                
        return wrapper
    
    def _decode(self):
        """Декодирование видео"""
        if not os.path.exists(self.input_file):
            self.finished.emit(False, f"Файл не найден: {self.input_file}")
            return
            
        # Сохраняем путь к входному файлу как атрибут
        self.input_file = os.path.abspath(self.input_file)
            
        decoder = VideoDecoder(
            input_file=self.input_file,
            verbose=True
        )
        
        # Перехватываем вывод в консоль для отображения в логе
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            decoder.decode(self.output_file)
            
            # Получаем вывод из буфера
            log_output = sys.stdout.getvalue()
            self.log_message.emit(log_output)
            
            self.finished.emit(True, "Декодирование успешно завершено")
        except Exception as e:
            self.finished.emit(False, f"Ошибка декодирования: {str(e)}")
        finally:
            sys.stdout = old_stdout
    
    def stop(self):
        """Остановка обработки"""
        self.is_running = False


class VideoComparisonApp(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сравнение видео")
        self.setMinimumSize(1200, 800)
        
        # Переменные
        self.source_video = None
        self.processed_video = None
        self.temp_processed_file = "temp_processed.mp4"
        self.current_frame = 0
        # Управление воспроизведением
        self.is_playing = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer_interval = 33  # ~30 FPS по умолчанию
        self.timer.setInterval(self.timer_interval)
        
        # Инициализация UI
        self.init_ui()
        
        # Обработчик видео
        self.video_processor = None
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Главный виджет и макет
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Разделитель для левой и правой панелей
        splitter = QSplitter(Qt.Horizontal)
        
        # Левая панель - видео
        left_panel = QVBoxLayout()
        
        # Группа для исходного видео
        source_group = QGroupBox("Исходное видео")
        source_layout = QVBoxLayout()
        self.source_player = VideoPlayer()
        source_layout.addWidget(self.source_player)
        source_group.setLayout(source_layout)
        
        # Группа для обработанного видео
        processed_group = QGroupBox("Обработанное видео")
        processed_layout = QVBoxLayout()
        self.processed_player = VideoPlayer()
        processed_layout.addWidget(self.processed_player)
        processed_group.setLayout(processed_layout)
        
        left_panel.addWidget(source_group, 1)
        left_panel.addWidget(processed_group, 1)
        
        # Правая панель - управление и логи
        right_panel = QVBoxLayout()
        
        # Группа управления
        control_group = QGroupBox("Управление")
        control_layout = QVBoxLayout()
        
        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        
        # Кнопка выбора файла
        self.select_btn = QPushButton("Выбрать видео")
        self.select_btn.clicked.connect(self.select_video)
        
        # Качество сжатия
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Качество (1-100):")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(1)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(80)
        self.quality_value = QLabel("80")
        self.quality_slider.valueChanged.connect(lambda v: self.quality_value.setText(str(v)))
        
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_value)
        
        # Кнопки кодирования/декодирования и загрузки
        btn_layout = QHBoxLayout()
        
        # Кнопки кодирования/декодирования
        encode_decode_layout = QHBoxLayout()
        self.encode_btn = QPushButton("Кодировать")
        self.encode_btn.clicked.connect(self.start_encoding)
        self.decode_btn = QPushButton("Декодировать")
        self.decode_btn.clicked.connect(self.start_decoding)
        
        encode_decode_layout.addWidget(self.encode_btn)
        encode_decode_layout.addWidget(self.decode_btn)
        
        # Кнопка добавления видео для сравнения
        self.add_compare_btn = QPushButton("Добавить для сравнения")
        self.add_compare_btn.clicked.connect(self.add_video_for_comparison)
        self.add_compare_btn.setToolTip("Добавить видео для сравнения без кодирования/декодирования")
        
        # Добавляем все кнопки в основной макет
        btn_layout.addLayout(encode_decode_layout)
        btn_layout.addWidget(self.add_compare_btn)
        
        # Кнопки управления воспроизведением
        play_controls = QHBoxLayout()
        self.play_btn = QPushButton("▶")
        self.play_btn.clicked.connect(self.toggle_play)
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.clicked.connect(self.stop_playback)
        
        play_controls.addWidget(self.play_btn)
        play_controls.addWidget(self.stop_btn)
        
        # Ползунок перемотки
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.sliderMoved.connect(self.seek_video)
        
        control_layout.addWidget(self.select_btn)
        control_layout.addLayout(quality_layout)
        control_layout.addLayout(btn_layout)
        control_layout.addLayout(play_controls)
        control_layout.addWidget(self.position_slider)
        control_layout.addWidget(self.progress_bar)
        control_group.setLayout(control_layout)
        
        # Группа логов
        log_group = QGroupBox("Логи")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        
        right_panel.addWidget(control_group)
        right_panel.addWidget(log_group, 1)
        
        # Создаем виджеты для левой и правой панелей
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        right_widget.setMaximumWidth(400)
        
        # Добавляем виджеты в разделитель
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([800, 400])
        
        # Устанавливаем главный макет
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Обновляем состояние кнопок
        self.update_buttons_state()
    
    def log(self, message):
        """Добавление сообщения в лог"""
        self.log_text.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        # Прокрутка вниз
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def select_video(self):
        """Выбор видеофайла"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите видеофайл", "", 
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)"
        )
        
        if file_name:
            self.source_video = file_name
            self.log(f"Выбран файл: {file_name}")
            
            # Загружаем видео в проигрыватель
            if self.source_player.load_video(file_name):
                self.log(f"Загружено видео: {os.path.basename(file_name)}")
                self.log(f"Разрешение: {self.source_player.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{self.source_player.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
                self.log(f"Частота кадров: {self.source_player.fps:.2f} FPS")
                self.log(f"Длительность: {self.source_player.duration:.2f} сек")
                
                # Сбрасываем ползунок
                self.position_slider.setMaximum(self.source_player.frame_count - 1)
                self.position_slider.setValue(0)
                
                # Показываем первый кадр
                self.show_frame(0)
            else:
                self.log("Ошибка загрузки видео")
                self.source_video = None
        
        self.update_buttons_state()
    
    def start_encoding(self):
        """Запуск кодирования видео"""
        if not self.source_video:
            return
            
        output_file, _ = QFileDialog.getSaveFileName(
            self, "Сохранить сжатое видео", "", "Video Files (*.vid);;All Files (*)"
        )
        
        if not output_file:
            return
            
        if not output_file.endswith('.vid'):
            output_file += '.vid'
            
        quality = self.quality_slider.value()
        self.log(f"Начало кодирования с качеством {quality}...")
        
        # Отключаем кнопки на время обработки
        self.set_processing_state(True)
        
        # Запускаем кодирование в отдельном потоке
        self.video_processor = VideoProcessor(
            'encode', self.source_video, output_file, quality
        )
        self.video_processor.finished.connect(self.on_processing_finished)
        self.video_processor.log_message.connect(self.log)
        self.video_processor.progress_percent.connect(self.update_progress)
        self.video_processor.start()
    
    def start_decoding(self):
        """Запуск декодирования видео"""
        # Запрашиваем файл с расширением .vid для декодирования
        input_file, _ = QFileDialog.getOpenFileName(
            self, "Выберите сжатый файл (.vid)", "", "Compressed Video Files (*.vid);;All Files (*)"
        )
        
        if not input_file:
            return
            
        # Проверяем расширение файла
        if not input_file.lower().endswith('.vid'):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите файл с расширением .vid")
            return
            
        output_file, _ = QFileDialog.getSaveFileName(
            self, "Сохранить декодированное видео", "", "Video Files (*.mp4);;All Files (*)"
        )
        
        if not output_file:
            return
            
        if not output_file.lower().endswith(('.mp4', '.avi', '.mov')):
            output_file += '.mp4'
            
        self.log(f"Начало декодирования файла: {os.path.basename(input_file)}")
        
        # Отключаем кнопки на время обработки
        self.set_processing_state(True)
        
        # Запускаем декодирование в отдельном потоке
        self.video_processor = VideoProcessor(
            'decode', input_file, output_file, self.quality_slider.value()
        )
        self.video_processor.finished.connect(self.on_processing_finished)
        self.video_processor.log_message.connect(self.log)
        self.video_processor.progress_percent.connect(self.update_progress)
        self.video_processor.start()
    
    def on_processing_finished(self, success, message):
        """Обработка завершения обработки видео"""
        self.log(message)
        
        if success:
            if self.video_processor.operation == 'encode':
                # После кодирования загружаем обработанное видео
                self.processed_player.load_video(self.video_processor.output_file)
                self.log("Обработанное видео загружено для сравнения")
            elif self.video_processor.operation == 'decode':
                # После декодирования загружаем декодированное видео во второй проигрыватель
                self.processed_player.load_video(self.video_processor.output_file)
                self.log("Декодированное видео загружено для сравнения")
                
                # Если исходное видео не загружено, загружаем его тоже
                if not self.source_video and hasattr(self.video_processor, 'input_file'):
                    self.source_player.load_video(self.video_processor.input_file)
                    self.log(f"Исходное видео загружено: {os.path.basename(self.video_processor.input_file)}")
        
        # Обновляем состояние кнопок
        self.set_processing_state(False)
        self.update_buttons_state()
        
        # Очищаем ссылку на процессор
        self.video_processor = None
    
    def update_progress(self, percent):
        """Обновление прогресс-бара"""
        self.progress_bar.setValue(percent)
        self.progress_bar.setFormat(f"{percent}%")
        
        # Если обработка завершена, сбрасываем прогресс через 2 секунды
        if percent == 100:
            QTimer.singleShot(2000, lambda: self.progress_bar.reset())
            QTimer.singleShot(2000, lambda: self.progress_bar.setFormat("%p%"))
    
    def set_processing_state(self, processing):
        """Установка состояния обработки"""
        if processing:
            self.progress_bar.setValue(0)
        else:
            self.progress_bar.setValue(100)
    
    def toggle_play(self):
        """Включение/выключение воспроизведения"""
        if not self.source_video:
            return
            
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_btn.setText("❚❚")
            # Устанавливаем интервал таймера на основе FPS видео
            if hasattr(self.source_player, 'fps') and self.source_player.fps > 0:
                self.timer_interval = max(1, int(1000 / self.source_player.fps))
                self.timer.setInterval(self.timer_interval)
            self.timer.start()
        else:
            self.play_btn.setText("▶")
            self.timer.stop()
    
    def stop_playback(self):
        """Остановка воспроизведения"""
        self.is_playing = False
        self.play_btn.setText("▶")
        self.timer.stop()
        self.show_frame(0)
    
    def seek_video(self, frame_num):
        """Переход к определенному кадру"""
        self.show_frame(frame_num)
    
    def show_frame(self, frame_num):
        """Отображение кадра в обоих проигрывателях"""
        if not self.source_video:
            return
            
        # Обновляем текущий кадр
        self.current_frame = frame_num
        self.position_slider.setValue(frame_num)
        
        # Показываем кадр в исходном видео
        source_frame = self.source_player.get_frame(frame_num)
        if source_frame is not None:
            self.source_player.display_frame(source_frame)
        
        # Показываем кадр в обработанном видео, если оно загружено
        if self.processed_player.cap is not None:
            processed_frame = self.processed_player.get_frame(frame_num)
            if processed_frame is not None:
                self.processed_player.display_frame(processed_frame)
    
    def update_frames(self):
        """Обновление кадров при воспроизведении"""
        if not self.source_video:
            return
            
        self.current_frame += 1
        
        # Проверяем, не достигли ли конца видео
        if self.current_frame >= self.source_player.frame_count:
            self.current_frame = 0
            if self.processed_player.cap is not None:
                self.processed_player.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        self.show_frame(self.current_frame)
    
    def add_video_for_comparison(self):
        """Добавление видео для сравнения"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите видео для сравнения", "", 
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)"
        )
        
        if file_name:
            # Загружаем видео во второй проигрыватель
            if self.processed_player.load_video(file_name):
                self.log(f"Видео для сравнения загружено: {os.path.basename(file_name)}")
                
                # Если исходное видео не загружено, загружаем его тоже
                if not self.source_video:
                    self.source_player.load_video(file_name)
                    self.source_video = file_name
                    self.log(f"Исходное видео загружено: {os.path.basename(file_name)}")
                
                # Обновляем состояние кнопок
                self.update_buttons_state()
            else:
                self.log("Ошибка загрузки видео для сравнения")
    
    def update_buttons_state(self):
        """Обновление состояния кнопок"""
        has_video = self.source_video is not None
        is_processing = hasattr(self, 'video_processor') and self.video_processor is not None and self.video_processor.isRunning()
        
        self.encode_btn.setEnabled(has_video and not is_processing)
        self.decode_btn.setEnabled(not is_processing)  # Разрешаем декодирование без исходного видео
        self.add_compare_btn.setEnabled(not is_processing)
        self.select_btn.setEnabled(not is_processing)
        self.play_btn.setEnabled(has_video and not is_processing)
        self.stop_btn.setEnabled(has_video and not is_processing)
        self.position_slider.setEnabled(has_video and not is_processing)
        self.quality_slider.setEnabled(not is_processing)
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        # Останавливаем таймер
        if self.timer.isActive():
            self.timer.stop()
        
        # Останавливаем обработку видео, если она выполняется
        if hasattr(self, 'video_processor') and self.video_processor and self.video_processor.isRunning():
            self.video_processor.terminate()
            self.video_processor.wait()
        
        # Закрываем видео
        if self.source_player.cap is not None:
            self.source_player.cap.release()
        
        if self.processed_player.cap is not None:
            self.processed_player.cap.release()
        
        event.accept()


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль
    app.setStyle('Fusion')
    
    # Создаем и показываем главное окно
    window = VideoComparisonApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
