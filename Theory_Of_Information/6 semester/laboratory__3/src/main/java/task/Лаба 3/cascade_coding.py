import customtkinter as ctk
from tkinter import filedialog, messagebox
import numpy as np
import os
from PIL import Image, ImageTk
import time

# Импортируем наши модули
from utils import (
    load_image, save_image, image_to_binary, binary_to_image,
    introduce_errors, introduce_errors_per_pixel, save_intermediate_data, clear_intermediate_data
)
from block_coder import BlockCoder
from conv_coder import ConvolutionalCoder
from interleaver import BlockInterleaver

# Настройки приложения
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CascadeCodingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title("Каскадное кодирование изображений")
        self.geometry("1200x800")
        
        # Переменные
        self.input_image_path = ""
        self.img_array = None
        self.output_decoded_path = "output_decoded.png"
        self.output_noisy_path = "output_noisy.png"
        self.intermediate_data_file = "intermediate_data.txt"
        self.error_rate = 0.01  # 1% ошибок
        
        # Инициализация кодеров
        self.block_coder = BlockCoder()
        self.conv_coder = ConvolutionalCoder()
        self.interleaver = BlockInterleaver()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Очистка файла с промежуточными данными
        clear_intermediate_data(self.intermediate_data_file)
        
    def create_widgets(self):
        # Основной контейнер - три колонки
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Левая колонка - параметры кодирования
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Центральная колонка - изображения
        center_frame = ctk.CTkFrame(main_frame)
        center_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Правая колонка - результаты и журнал
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # === Левая колонка ===
        left_label = ctk.CTkLabel(left_frame, text="Параметры кодирования", font=("Arial", 16, "bold"))
        left_label.pack(pady=10)
        
        # Выбор изображения
        image_frame = ctk.CTkFrame(left_frame)
        image_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(image_frame, text="Изображение:").pack(anchor="w")
        
        image_button_frame = ctk.CTkFrame(image_frame)
        image_button_frame.pack(fill="x", pady=5)
        
        self.image_path_label = ctk.CTkLabel(image_button_frame, text="Не выбрано")
        self.image_path_label.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(image_button_frame, text="Выбрать...", command=self.load_image_dialog).pack(side="right")
        
        # Параметры блочного кода
        block_frame = ctk.CTkFrame(left_frame)
        block_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(block_frame, text="Блочный код:").pack(anchor="w")
        
        matrix_frame = ctk.CTkFrame(block_frame)
        matrix_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(matrix_frame, text="Матрица порождающая (G) или проверочная (H):").pack(anchor="w")
        self.matrix_text = ctk.CTkTextbox(matrix_frame, height=100)
        self.matrix_text.pack(fill="x", pady=5)
        self.matrix_text.insert("1.0", "1101\n1011\n0111")  # Пример матрицы Хэмминга (7,4)
        
        matrix_type_frame = ctk.CTkFrame(block_frame)
        matrix_type_frame.pack(fill="x", pady=5)
        
        self.matrix_type_var = ctk.StringVar(value="G")
        ctk.CTkRadioButton(matrix_type_frame, text="Порождающая (G)", variable=self.matrix_type_var, value="G").pack(side="left", padx=10)
        ctk.CTkRadioButton(matrix_type_frame, text="Проверочная (H)", variable=self.matrix_type_var, value="H").pack(side="left", padx=10)
        
        ctk.CTkButton(block_frame, text="Настроить блочный код", command=self.setup_block_code).pack(fill="x", pady=5)
        
        # Параметры сверточного кода
        conv_frame = ctk.CTkFrame(left_frame)
        conv_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(conv_frame, text="Сверточный код:").pack(anchor="w")
        
        ctk.CTkLabel(conv_frame, text="Сумматоры (каждый на новой строке):").pack(anchor="w")
        self.poly_text = ctk.CTkTextbox(conv_frame, height=100)
        self.poly_text.pack(fill="x", pady=5)
        self.poly_text.insert("1.0", "0,1,2\n0,2")  # Пример сумматоров для rate 1/2, K=3
        
        conv_options_frame = ctk.CTkFrame(conv_frame)
        conv_options_frame.pack(fill="x", pady=5)
        
        self.verbose_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(conv_options_frame, text="Подробный вывод Витерби", variable=self.verbose_var).pack(side="left", padx=10)
        
        ctk.CTkButton(conv_frame, text="Настроить сверточный код", command=self.setup_conv_code).pack(fill="x", pady=5)
        
        # Параметры ошибок
        error_frame = ctk.CTkFrame(left_frame)
        error_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(error_frame, text="Параметры ошибок:").pack(anchor="w")
        
        error_slider_frame = ctk.CTkFrame(error_frame)
        error_slider_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(error_slider_frame, text="Вероятность ошибки:").pack(side="left")
        
        self.error_slider = ctk.CTkSlider(error_slider_frame, from_=0, to=0.2, number_of_steps=20)
        self.error_slider.pack(side="left", fill="x", expand=True, padx=10)
        self.error_slider.set(0.01)  # 1% по умолчанию
        
        self.error_label = ctk.CTkLabel(error_slider_frame, text="1%")
        self.error_label.pack(side="right")
        
        self.error_slider.configure(command=self.update_error_label)
        
        # Кнопка запуска
        ctk.CTkButton(left_frame, text="Выполнить каскадное кодирование", font=("Arial", 14, "bold"), 
                     command=self.run_cascade_coding, height=40).pack(fill="x", padx=10, pady=20)
        
        # === Центральная колонка ===
        center_label = ctk.CTkLabel(center_frame, text="Изображения", font=("Arial", 16, "bold"))
        center_label.pack(pady=10)
        
        # Исходное изображение
        original_frame = ctk.CTkFrame(center_frame)
        original_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(original_frame, text="Исходное изображение:").pack(anchor="w")
        
        self.original_image_label = ctk.CTkLabel(original_frame, text="")
        self.original_image_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Закодированное изображение
        decoded_frame = ctk.CTkFrame(center_frame)
        decoded_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(decoded_frame, text="Декодированное изображение:").pack(anchor="w")
        
        self.decoded_image_label = ctk.CTkLabel(decoded_frame, text="")
        self.decoded_image_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Зашумленное изображение
        noisy_frame = ctk.CTkFrame(center_frame)
        noisy_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(noisy_frame, text="Изображение с шумом (без кодирования):").pack(anchor="w")
        
        self.noisy_image_label = ctk.CTkLabel(noisy_frame, text="")
        self.noisy_image_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === Правая колонка ===
        right_label = ctk.CTkLabel(right_frame, text="Результаты", font=("Arial", 16, "bold"))
        right_label.pack(pady=10)
        
        # Информация о кодировании
        info_frame = ctk.CTkFrame(right_frame)
        info_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(info_frame, text="Параметры блочного кода:").pack(anchor="w")
        
        block_info_frame = ctk.CTkFrame(info_frame)
        block_info_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(block_info_frame, text="n:").pack(side="left")
        self.n_label = ctk.CTkLabel(block_info_frame, text="-")
        self.n_label.pack(side="left", padx=5)
        
        ctk.CTkLabel(block_info_frame, text="k:").pack(side="left", padx=10)
        self.k_label = ctk.CTkLabel(block_info_frame, text="-")
        self.k_label.pack(side="left", padx=5)
        
        ctk.CTkLabel(block_info_frame, text="dmin:").pack(side="left", padx=10)
        self.dmin_label = ctk.CTkLabel(block_info_frame, text="-")
        self.dmin_label.pack(side="left", padx=5)
        
        ctk.CTkLabel(block_info_frame, text="t:").pack(side="left", padx=10)
        self.t_label = ctk.CTkLabel(block_info_frame, text="-")
        self.t_label.pack(side="left", padx=5)
        
        # Журнал выполнения
        log_frame = ctk.CTkFrame(right_frame)
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(log_frame, text="Журнал выполнения:").pack(anchor="w")
        
        self.log_text = ctk.CTkTextbox(log_frame, height=400, wrap="word")
        self.log_text.pack(fill="both", expand=True, pady=5)
        
        # Кнопки управления журналом
        log_button_frame = ctk.CTkFrame(right_frame)
        log_button_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkButton(log_button_frame, text="Очистить журнал", command=self.clear_log).pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(log_button_frame, text="Сохранить журнал", command=self.save_log).pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(log_button_frame, text="Открыть промежуточные данные", command=self.open_intermediate_data).pack(side="left", padx=5, fill="x", expand=True)
    
    def load_image_dialog(self):
        """Диалог выбора изображения"""
        filename = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*")]
        )
        
        if filename:
            self.input_image_path = filename
            self.image_path_label.configure(text=os.path.basename(filename))
            
            # Загружаем и отображаем изображение
            self.img_array = load_image(filename)
            if self.img_array is not None:
                self.display_image(self.img_array, self.original_image_label)
                self.log("Изображение загружено: " + os.path.basename(filename))
                self.log(f"Размер: {self.img_array.shape[1]}x{self.img_array.shape[0]}, каналов: {self.img_array.shape[2]}")
            else:
                self.log("Ошибка при загрузке изображения", error=True)
    
    def setup_block_code(self):
        """Настройка блочного кода"""
        try:
            matrix_text = self.matrix_text.get("1.0", "end-1c")
            matrix = matrix_text.split("\n")
            
            # Проверка матрицы
            matrix_type = self.matrix_type_var.get()
            
            if not matrix:
                raise ValueError("Матрица не введена")
                
            for row in matrix:
                if not all(bit in ['0', '1'] for bit in row):
                    raise ValueError("Матрица должна содержать только 0 и 1")
            
            # Настройка блочного кода
            result = self.block_coder.setup_code(matrix, matrix_type)
            
            if result:
                # Обновляем информацию о блочном коде
                self.n_label.configure(text=str(self.block_coder.n))
                self.k_label.configure(text=str(self.block_coder.k))
                self.dmin_label.configure(text=str(self.block_coder.dmin))
                self.t_label.configure(text=str(self.block_coder.t))
                
                self.log(f"Блочный код настроен: ({self.block_coder.n}, {self.block_coder.k})")
                self.log(f"dmin = {self.block_coder.dmin}, t = {self.block_coder.t}")
            else:
                self.log("Ошибка при настройке блочного кода", error=True)
        
        except Exception as e:
            self.log(f"Ошибка при настройке блочного кода: {str(e)}", error=True)
            messagebox.showerror("Ошибка", str(e))
    
    def setup_conv_code(self):
        """Настройка сверточного кода"""
        try:
            poly_text = self.poly_text.get("1.0", "end-1c")
            
            # Разбор сумматоров
            polynomials = []
            for line in poly_text.split("\n"):
                if line.strip():
                    try:
                        poly = [int(x) for x in line.split(",")]
                        polynomials.append(poly)
                    except:
                        raise ValueError(f"Некорректный формат сумматора: {line}")
            
            if not polynomials:
                raise ValueError("Сумматоры не введены")
                
            # Настройка сверточного кода
            self.conv_coder.set_polynomials(polynomials)
            self.conv_coder.set_verbose(self.verbose_var.get())
            
            self.log(f"Сверточный код настроен: {len(polynomials)} сумматоров")
            self.log(f"Сумматоры: {polynomials}")
            
        except Exception as e:
            self.log(f"Ошибка при настройке сверточного кода: {str(e)}", error=True)
            messagebox.showerror("Ошибка", str(e))
    
    def update_error_label(self, value):
        """Обновление метки с вероятностью ошибки"""
        self.error_rate = float(value)
        percent = int(self.error_rate * 100)
        self.error_label.configure(text=f"{percent}%")
    
    def run_cascade_coding(self):
        """Выполнение каскадного кодирования"""
        if self.img_array is None:
            messagebox.showwarning("Предупреждение", "Сначала выберите изображение")
            return
            
        if self.block_coder.n == 0 or self.block_coder.k == 0:
            messagebox.showwarning("Предупреждение", "Сначала настройте блочный код")
            return
            
        if not self.conv_coder.polynomials:
            messagebox.showwarning("Предупреждение", "Сначала настройте сверточный код")
            return
        
        try:
            # Очистка журнала и промежуточных данных
            self.clear_log()
            clear_intermediate_data(self.intermediate_data_file)
            
            self.log("Начало каскадного кодирования...")
            self.log(f"Вероятность ошибки: {self.error_rate:.2%}")
            
            # 1. Преобразование изображения в бинарные данные
            self.log("1. Преобразование изображения в бинарный вид...")
            start_time = time.time()
            binary_rows = image_to_binary(self.img_array)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            save_intermediate_data("Бинарные строки изображения:", self.intermediate_data_file)
            for i, row in enumerate(binary_rows[:3]):  # Сохраняем только первые 3 строки для примера
                save_intermediate_data(f"Строка {i} (первые 100 бит): {row[:100]}...", self.intermediate_data_file)
            
            # 2. Блочное кодирование (строка за строкой)
            self.log("2. Блочное кодирование...")
            start_time = time.time()
            encoded_block_rows = []
            for i, row in enumerate(binary_rows):
                encoded_row = self.block_coder.encode(row)
                encoded_block_rows.append(encoded_row)
                if i < 3:  # Сохраняем только первые 3 строки для примера
                    save_intermediate_data(f"Строка {i} после блочного кодирования (первые 100 бит): {encoded_row[:100]}...", self.intermediate_data_file)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 3. Перемежение (строка за строкой)
            self.log("3. Перемежение...")
            start_time = time.time()
            interleaved_rows = []
            for i, row in enumerate(encoded_block_rows):
                # Определяем размер перемежителя для строки
                rows, cols = self.interleaver.calculate_dimensions(len(row))
                self.interleaver.set_dimensions(rows, cols)
                
                # Перемежение
                interleaved_row = self.interleaver.interleave(row)
                interleaved_rows.append((interleaved_row, rows, cols))  # Сохраняем размеры для деперемежения
                
                if i < 3:  # Сохраняем только первые 3 строки для примера
                    save_intermediate_data(f"Строка {i} после перемежения (размер {rows}x{cols}, первые 100 бит): {interleaved_row[:100]}...", self.intermediate_data_file)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 4. Сверточное кодирование
            self.log("4. Сверточное кодирование...")
            start_time = time.time()
            conv_encoded_rows = []
            for i, (row, _, _) in enumerate(interleaved_rows):
                conv_encoded_row = self.conv_coder.convolutional_encode(row)
                conv_encoded_rows.append(conv_encoded_row)
                if i < 3:  # Сохраняем только первые 3 строки для примера
                    save_intermediate_data(f"Строка {i} после сверточного кодирования (первые 100 бит): {conv_encoded_row[:100]}...", self.intermediate_data_file)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 5. Внесение ошибок
            self.log("5. Внесение ошибок...")
            start_time = time.time()
            noisy_rows = []
            for i, row in enumerate(conv_encoded_rows):
                noisy_row = introduce_errors_per_pixel(row, self.error_rate)
                noisy_rows.append(noisy_row)
                if i < 3:  # Сохраняем только первые 3 строки для примера
                    save_intermediate_data(f"Строка {i} после внесения ошибок (первые 100 бит): {noisy_row[:100]}...", self.intermediate_data_file)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # --- Декодирование ---
            self.log("--- Начало декодирования ---")
            
            # 6. Сверточное декодирование
            self.log("6. Сверточное декодирование...")
            start_time = time.time()
            conv_decoded_rows = []
            for i, row in enumerate(noisy_rows):
                conv_decoded_row = self.conv_coder.viterbi_decode(row)
                conv_decoded_rows.append(conv_decoded_row)
                if i < 3:  # Сохраняем только первые 3 строки для примера
                    save_intermediate_data(f"Строка {i} после сверточного декодирования (первые 100 бит): {conv_decoded_row[:100]}...", self.intermediate_data_file)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 7. Деперемежение
            self.log("7. Деперемежение...")
            start_time = time.time()
            deinterleaved_rows = []
            for i, (row, interleaved_info) in enumerate(zip(conv_decoded_rows, interleaved_rows)):
                # Распаковываем данные перемежителя
                _, rows, cols = interleaved_info
                
                # Убеждаемся, что длина строки соответствует размеру перемежителя
                if len(row) != rows * cols:
                    # Обрезаем или дополняем
                    if len(row) > rows * cols:
                        row = row[:rows * cols]
                    else:
                        row = row + '0' * (rows * cols - len(row))
                
                self.interleaver.set_dimensions(rows, cols)
                deinterleaved_row = self.interleaver.deinterleave(row)
                deinterleaved_rows.append(deinterleaved_row)
                
                if i < 3:  # Сохраняем только первые 3 строки для примера
                    save_intermediate_data(f"Строка {i} после деперемежения (первые 100 бит): {deinterleaved_row[:100]}...", self.intermediate_data_file)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 8. Блочное декодирование
            self.log("8. Блочное декодирование...")
            start_time = time.time()
            decoded_rows = []
            for i, row in enumerate(deinterleaved_rows):
                decoded_row = self.block_coder.decode(row)
                
                # Проверяем, что длина декодированной строки соответствует длине исходной
                if len(decoded_row) < len(binary_rows[i]):
                    # Дополняем нулями
                    decoded_row = decoded_row + '0' * (len(binary_rows[i]) - len(decoded_row))
                elif len(decoded_row) > len(binary_rows[i]):
                    # Обрезаем
                    decoded_row = decoded_row[:len(binary_rows[i])]
                
                decoded_rows.append(decoded_row)
                
                if i < 3:  # Сохраняем только первые 3 строки для примера
                    save_intermediate_data(f"Строка {i} после блочного декодирования (первые 100 бит): {decoded_row[:100]}...", self.intermediate_data_file)
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 9. Преобразование бинарных данных обратно в изображение
            self.log("9. Восстановление изображения...")
            start_time = time.time()
            decoded_img_array = binary_to_image(decoded_rows, self.img_array.shape[0], self.img_array.shape[1])
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 10. Создание зашумленного изображения (без кодирования)
            self.log("10. Создание изображения с шумом (без кодирования)...")
            start_time = time.time()
            # Вносим ошибки в исходные бинарные данные
            noisy_uncoded_rows = []
            for row in binary_rows:
                noisy_uncoded_row = introduce_errors_per_pixel(row, self.error_rate)
                noisy_uncoded_rows.append(noisy_uncoded_row)
            
            noisy_img_array = binary_to_image(noisy_uncoded_rows, self.img_array.shape[0], self.img_array.shape[1])
            self.log(f"   Завершено за {time.time() - start_time:.2f} сек.")
            
            # 11. Сохранение и отображение результатов
            self.log("11. Сохранение результатов...")
            save_image(decoded_img_array, self.output_decoded_path)
            save_image(noisy_img_array, self.output_noisy_path)
            
            # Отображение изображений
            self.display_image(decoded_img_array, self.decoded_image_label)
            self.display_image(noisy_img_array, self.noisy_image_label)
            
            self.log("Каскадное кодирование завершено успешно!")
            self.log(f"Декодированное изображение сохранено в {self.output_decoded_path}")
            self.log(f"Зашумленное изображение сохранено в {self.output_noisy_path}")
            self.log(f"Промежуточные данные сохранены в {self.intermediate_data_file}")
            
        except Exception as e:
            self.log(f"Ошибка при выполнении каскадного кодирования: {str(e)}", error=True)
            import traceback
            traceback.print_exc()
            messagebox.showerror("Ошибка", str(e))
    
    def display_image(self, img_array, label):
        """Отображение изображения в метке"""
        try:
            # Преобразуем массив numpy в изображение PIL
            img = Image.fromarray(img_array.astype(np.uint8))
            
            # Определяем размер контейнера
            container_width = label.winfo_width()
            container_height = label.winfo_height()
            
            # Если контейнер еще не отрисован, используем примерные значения
            if container_width <= 1:
                container_width = 300
            if container_height <= 1:
                container_height = 200
            
            # Масштабируем изображение, сохраняя пропорции
            img_width, img_height = img.size
            scale = min(container_width / img_width, container_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Преобразуем в формат, понятный Tkinter
            tk_img = ImageTk.PhotoImage(img_resized)
            
            # Сохраняем ссылку на изображение (иначе оно будет удалено сборщиком мусора)
            label.image = tk_img
            
            # Обновляем метку
            label.configure(image=tk_img)
            
        except Exception as e:
            print(f"Ошибка при отображении изображения: {str(e)}")
    
    def log(self, message, error=False):
        """Добавление сообщения в журнал"""
        self.log_text.insert("end", message + "\n")
        if error:
            self.log_text.insert("end", "ОШИБКА: " + message + "\n", "error")
        self.log_text.see("end")  # Прокрутка до конца
        
        # Обновляем интерфейс
        self.update()
    
    def clear_log(self):
        """Очистка журнала"""
        self.log_text.delete("1.0", "end")
    
    def save_log(self):
        """Сохранение журнала в файл"""
        filename = filedialog.asksaveasfilename(
            title="Сохранить журнал",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.log_text.get("1.0", "end"))
                messagebox.showinfo("Информация", f"Журнал сохранен в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении журнала: {str(e)}")
    
    def open_intermediate_data(self):
        """Открытие файла с промежуточными данными"""
        if os.path.exists(self.intermediate_data_file):
            try:
                os.startfile(self.intermediate_data_file)
            except:
                messagebox.showinfo("Информация", f"Файл {self.intermediate_data_file} существует, но не может быть открыт автоматически.")
        else:
            messagebox.showinfo("Информация", "Файл с промежуточными данными не существует. Сначала выполните кодирование.")

if __name__ == "__main__":
    app = CascadeCodingApp()
    app.mainloop() 