import customtkinter as ctk
import numpy as np
import random
import re
import time
from datetime import datetime
from tkinter import messagebox
from helpful_utils import text_to_binary, binary_to_text


class CodingBlock:
    def __init__(self, parent):
        self.parent = parent
        self.n = 7  # Общее количество бит в кодовом слове (по умолчанию 7)
        self.k = 4  # Количество информационных бит (по умолчанию 4)
        self.H_matrix = None  # Проверочная матрица
        self.G_matrix = None  # Порождающая матрица
        self.error_correction_capability = 1  # Начальное количество исправляемых ошибок

    def create_widgets(self, parent_frame):
        # Создание основного фрейма
        self.main_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Для контента
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Заголовок модуля с подчеркиванием
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        title_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(title_frame,
                                        text="Адаптивная система с блочным кодом",
                                        font=ctk.CTkFont(size=24, weight="bold"),
                                        text_color="White")
        self.title_label.grid(row=0, column=0, pady=(0, 5))

        title_underline = ctk.CTkFrame(title_frame, height=2, fg_color=self.parent.accent_color)
        title_underline.grid(row=1, column=0, sticky="ew", padx=100)

        # Создаем основной контейнер для содержимого
        content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_container.grid(row=1, column=0, sticky="nsew")
        content_container.grid_rowconfigure(1, weight=1)  # Для основного контента
        content_container.grid_columnconfigure(0, weight=1)

        # Создаем верхнюю панель для параметров
        top_panel = ctk.CTkFrame(content_container, fg_color=self.parent.sidebar_color, corner_radius=10)
        top_panel.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        top_panel.grid_columnconfigure(2, weight=1)  # Для растягивания

        # Параметры кода в сетке
        params_grid = ctk.CTkFrame(top_panel, fg_color="transparent")
        params_grid.pack(fill="x", padx=20, pady=10)

        self.params_label = ctk.CTkLabel(params_grid,
                                         text="Параметры кода:",
                                         font=ctk.CTkFont(size=16, weight="bold"),
                                         text_color=self.parent.text_color)
        self.params_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

        # n параметр
        n_frame = ctk.CTkFrame(params_grid, fg_color="transparent")
        n_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.n_label = ctk.CTkLabel(n_frame,
                                    text="n (длина кодового слова):",
                                    font=ctk.CTkFont(size=14))
        self.n_label.pack(side="left", padx=(0, 10))

        self.n_entry = ctk.CTkEntry(n_frame, width=60, height=32,
                                    font=ctk.CTkFont(size=14))
        self.n_entry.pack(side="left")
        self.n_entry.insert(0, str(self.n))

        # k параметр
        k_frame = ctk.CTkFrame(params_grid, fg_color="transparent")
        k_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.k_label = ctk.CTkLabel(k_frame,
                                    text="k (информационные биты):",
                                    font=ctk.CTkFont(size=14))
        self.k_label.pack(side="left", padx=(0, 10))

        self.k_entry = ctk.CTkEntry(k_frame, width=60, height=32,
                                    font=ctk.CTkFont(size=14))
        self.k_entry.pack(side="left")
        self.k_entry.insert(0, str(self.k))

        # Кнопка генерации матрицы
        self.matrix_button = ctk.CTkButton(params_grid,
                                           text="Сгенерировать матрицу",
                                           command=self.generate_matrix,
                                           height=32,
                                           font=ctk.CTkFont(size=14),
                                           fg_color=self.parent.accent_color,
                                           hover_color="#1f7a2f")
        self.matrix_button.grid(row=1, column=2, padx=20, pady=5)

        # Информация о корректирующей способности
        self.info_label = ctk.CTkLabel(params_grid,
                                       text=f"Текущая корректирующая способность: {self.error_correction_capability} ошибок",
                                       font=ctk.CTkFont(size=14),
                                       text_color="#666666")
        self.info_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="w")

        # Создаем контейнер для основного контента
        main_content = ctk.CTkFrame(content_container, fg_color="transparent")
        main_content.grid(row=1, column=0, sticky="nsew", pady=5)
        main_content.grid_columnconfigure(0, weight=2)  # Левая колонка шире
        main_content.grid_columnconfigure(1, weight=1)  # Правая колонка уже
        main_content.grid_rowconfigure(0, weight=1)

        # === ЛЕВАЯ КОЛОНКА ===
        left_column = ctk.CTkFrame(main_content, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(10, 5))
        left_column.grid_rowconfigure(1, weight=1)  # Для поля результатов
        left_column.grid_columnconfigure(0, weight=1)

        # Левая панель для ввода
        left_panel = ctk.CTkFrame(left_column, fg_color=self.parent.sidebar_color, corner_radius=10)
        left_panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.input_label = ctk.CTkLabel(left_panel,
                                        text="Исходный текст:",
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        text_color=self.parent.text_color)
        self.input_label.pack(padx=10, pady=(10, 5), anchor="w")

        self.input_text = ctk.CTkTextbox(left_panel,
                                         height=120,  # Уменьшенная высота
                                         font=ctk.CTkFont(size=14),
                                         fg_color="white",
                                         border_color=self.parent.accent_color,
                                         border_width=1,
                                         text_color=self.parent.text_color)
        self.input_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопки управления вводом
        input_buttons = ctk.CTkFrame(left_panel, fg_color="transparent")
        input_buttons.pack(fill="x", padx=10, pady=(0, 10))

        self.load_button = ctk.CTkButton(input_buttons,
                                         text="Загрузить из файла",
                                         command=self.load_text,
                                         height=28,  # Уменьшенная высота
                                         font=ctk.CTkFont(size=12),
                                         fg_color=self.parent.accent_color,
                                         hover_color="#1f7a2f")
        self.load_button.pack(side="left", padx=(0, 5))

        self.clear_button = ctk.CTkButton(input_buttons,
                                          text="Очистить",
                                          command=lambda: self.input_text.delete("1.0", "end"),
                                          height=28,  # Уменьшенная высота
                                          font=ctk.CTkFont(size=12),
                                          fg_color="#cccccc",
                                          hover_color="#bbbbbb",
                                          text_color="#333333")
        self.clear_button.pack(side="left", padx=5)

        # Правая панель для результатов
        right_panel = ctk.CTkFrame(left_column, fg_color=self.parent.sidebar_color, corner_radius=10)
        right_panel.grid(row=1, column=0, sticky="nsew")
        right_panel.grid_rowconfigure(1, weight=1)  # Для текстового поля
        right_panel.grid_columnconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(right_panel,
                                         text="Результаты:",
                                         font=ctk.CTkFont(size=16, weight="bold"),
                                         text_color=self.parent.text_color)
        self.result_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.result_text = ctk.CTkTextbox(right_panel,
                                          font=ctk.CTkFont(size=14),
                                          fg_color="white",
                                          border_color=self.parent.accent_color,
                                          border_width=1,
                                          text_color=self.parent.text_color)
        self.result_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        # === ПРАВАЯ КОЛОНКА ===
        right_column = ctk.CTkFrame(main_content, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(5, 10))
        right_column.grid_rowconfigure(1, weight=1)  # Для матриц
        right_column.grid_columnconfigure(0, weight=1)

        # Панель операций
        operations_panel = ctk.CTkFrame(right_column, fg_color=self.parent.sidebar_color, corner_radius=10)
        operations_panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        operations_label = ctk.CTkLabel(operations_panel,
                                        text="Операции:",
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        text_color=self.parent.text_color)
        operations_label.pack(padx=10, pady=(10, 5), anchor="w")

        buttons_frame = ctk.CTkFrame(operations_panel, fg_color="transparent")
        buttons_frame.pack(padx=10, pady=(0, 10), fill="x")

        # Кнопки операций (теперь в два ряда)
        top_buttons = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        top_buttons.pack(fill="x", pady=(0, 5))

        self.encode_button = ctk.CTkButton(top_buttons,
                                           text="Кодировать",
                                           command=self.encode_text,
                                           height=28,
                                           font=ctk.CTkFont(size=12),
                                           fg_color=self.parent.accent_color,
                                           hover_color="#1f7a2f")
        self.encode_button.pack(side="left", padx=(0, 5), expand=True, fill="x")

        self.noise_button = ctk.CTkButton(top_buttons,
                                          text="Внести ошибки",
                                          command=self.add_noise,
                                          height=28,
                                          font=ctk.CTkFont(size=12),
                                          fg_color="#cccccc",
                                          hover_color="#bbbbbb",
                                          text_color="#333333")
        self.noise_button.pack(side="left", padx=(0, 5), expand=True, fill="x")

        bottom_buttons = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        bottom_buttons.pack(fill="x")

        self.decode_button = ctk.CTkButton(bottom_buttons,
                                           text="Декодировать",
                                           command=self.decode_text,
                                           height=28,
                                           font=ctk.CTkFont(size=12),
                                           fg_color=self.parent.accent_color,
                                           hover_color="#1f7a2f")
        self.decode_button.pack(side="left", padx=(0, 5), expand=True, fill="x")

        self.adapt_button = ctk.CTkButton(bottom_buttons,
                                          text="Адаптировать код",
                                          command=self.adapt_code,
                                          state="disabled",
                                          height=28,
                                          font=ctk.CTkFont(size=12),
                                          fg_color="#cccccc",
                                          hover_color="#bbbbbb",
                                          text_color="#333333")
        self.adapt_button.pack(side="left", padx=(0, 5), expand=True, fill="x")

        # Панели для матриц
        matrices_frame = ctk.CTkFrame(right_column, fg_color="transparent")
        matrices_frame.grid(row=1, column=0, sticky="nsew")
        matrices_frame.grid_rowconfigure(0, weight=1)  # Для матрицы G
        matrices_frame.grid_rowconfigure(1, weight=1)  # Для матрицы H
        matrices_frame.grid_columnconfigure(0, weight=1)

        # Панель для матрицы G
        g_matrix_panel = ctk.CTkFrame(matrices_frame, fg_color=self.parent.sidebar_color, corner_radius=10)
        g_matrix_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        g_matrix_panel.grid_rowconfigure(1, weight=1)  # Для текстового поля
        g_matrix_panel.grid_columnconfigure(0, weight=1)

        g_matrix_label = ctk.CTkLabel(g_matrix_panel,
                                      text="Порождающая матрица G:",
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      text_color=self.parent.text_color)
        g_matrix_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.g_matrix_text = ctk.CTkTextbox(g_matrix_panel,
                                            font=ctk.CTkFont(family="Courier", size=12),
                                            fg_color="white",
                                            border_color=self.parent.accent_color,
                                            border_width=1,
                                            text_color=self.parent.text_color)
        self.g_matrix_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        # Панель для матрицы H
        h_matrix_panel = ctk.CTkFrame(matrices_frame, fg_color=self.parent.sidebar_color, corner_radius=10)
        h_matrix_panel.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        h_matrix_panel.grid_rowconfigure(1, weight=1)  # Для текстового поля
        h_matrix_panel.grid_columnconfigure(0, weight=1)

        h_matrix_label = ctk.CTkLabel(h_matrix_panel,
                                      text="Проверочная матрица H:",
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      text_color=self.parent.text_color)
        h_matrix_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.h_matrix_text = ctk.CTkTextbox(h_matrix_panel,
                                            font=ctk.CTkFont(family="Courier", size=12),
                                            fg_color="white",
                                            border_color=self.parent.accent_color,
                                            border_width=1,
                                            text_color=self.parent.text_color)
        self.h_matrix_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    def load_text(self):
        text = self.parent.load_text_from_file()
        if text:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", text)

    def generate_matrix(self):
        operation_start_time = time.time()
        operation_start_dt = datetime.fromtimestamp(operation_start_time)

        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"""============================================================
OPERATION: Генерация матриц блочного кода
START TIME: {operation_start_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
============================================================\n\n""")

        try:
            # --- Шаг 1: Валидация параметров ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 1: Валидация параметров кода
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Проверка корректности введенных параметров n и k.\n")

            try:
                self.n = int(self.n_entry.get())
                self.k = int(self.k_entry.get())

                if self.n <= self.k:
                    messagebox.showerror("Ошибка", "n должно быть больше k")
                    self.result_text.insert("end", "Результат: Ошибка - n должно быть больше k.\n")
                    step_end_time = time.time()
                    self.result_text.insert("end",
                                            f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                    return

                if 2 ** (self.n - self.k) < 2 * self.n + 1:
                    self.result_text.insert("end",
                                            "Предупреждение: при данных параметрах (n, k) не гарантируется исправление 2 ошибок.\n")

                self.result_text.insert("end", f"Параметры валидны: n={self.n}, k={self.k}\n")
                step_end_time = time.time()
                self.result_text.insert("end",
                                        f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")
            except ValueError:
                messagebox.showerror("Ошибка", "Параметры должны быть целыми числами")
                self.result_text.insert("end", "Результат: Ошибка - параметры должны быть целыми числами.\n")
                step_end_time = time.time()
                self.result_text.insert("end",
                                        f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                return

            # --- Шаг 2: Генерация матриц ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 2: Генерация матриц кода
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Генерация порождающей (G) и проверочной (H) матриц.\n")

            max_attempts = 10
            for attempt in range(max_attempts):
                # Генерируем порождающую матрицу G
                I_k = np.eye(self.k, dtype=int)
                P = np.random.randint(0, 2, size=(self.k, self.n - self.k))
                self.G_matrix = np.hstack((I_k, P))

                # Генерируем проверочную матрицу H
                P_t = P.T
                I_nk = np.eye(self.n - self.k, dtype=int)
                self.H_matrix = np.hstack((P_t, I_nk))

                # Определяем корректирующую способность кода
                min_d = self.calculate_min_distance()
                self.error_correction_capability = (min_d - 1) // 2

                # Проверяем, достигли ли мы требуемого минимального расстояния
                if self.error_correction_capability >= 2:
                    break

            self.result_text.insert("end", f"Матрицы сгенерированы за {attempt + 1} попыток\n")
            self.result_text.insert("end", f"Минимальное расстояние кода: {min_d}\n")
            self.result_text.insert("end", f"Корректирующая способность: {self.error_correction_capability} ошибок\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 3: Отображение матриц ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 3: Отображение матриц
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Форматирование матриц для отображения в интерфейсе.\n")

            # Формируем строковое представление матриц
            G_str = ""
            for row in self.G_matrix:
                G_str += ' '.join(map(str, row)) + '\n'

            H_str = ""
            for row in self.H_matrix:
                H_str += ' '.join(map(str, row)) + '\n'

            # Вывод матриц в отдельные текстовые поля
            self.g_matrix_text.delete("1.0", "end")
            self.g_matrix_text.insert("1.0", G_str)

            self.h_matrix_text.delete("1.0", "end")
            self.h_matrix_text.insert("1.0", H_str)

            self.result_text.insert("end", "Матрицы успешно отображены в интерфейсе\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 4: Обновление интерфейса ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 4: Обновление интерфейса
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Обновление информации о корректирующей способности.\n")

            self.info_label.configure(
                text=f"Текущая корректирующая способность: {self.error_correction_capability} ошибок")
            messagebox.showinfo("Успех", f"Матрицы блочного кода ({self.n}, {self.k}) успешно сгенерированы")

            self.result_text.insert("end", "Интерфейс успешно обновлен\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

        except Exception as e:
            self.result_text.insert("end", f"КРИТИЧЕСКАЯ ОШИБКА: {str(e)}\n")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

        finally:
            operation_end_time = time.time()
            self.result_text.insert("end", f"""============================================================
OPERATION COMPLETED: Генерация матриц блочного кода
END TIME: {datetime.fromtimestamp(operation_end_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
TOTAL DURATION: {operation_end_time - operation_start_time:.3f} seconds
============================================================\n""")

    def calculate_min_distance(self):
        """Вычисляет минимальное расстояние Хэмминга для кода"""
        # Для небольших значений k можно непосредственно вычислить все кодовые слова
        if self.k <= 10:  # Ограничение для предотвращения ошибок при больших k
            # Генерируем все возможные кодовые слова
            all_messages = [format(i, f'0{self.k}b') for i in range(2 ** self.k)]
            codewords = []

            for msg in all_messages:
                # Преобразуем сообщение в массив бит
                msg_bits = np.array([int(bit) for bit in msg])

                # Умножаем на порождающую матрицу по модулю 2
                codeword = np.remainder(np.dot(msg_bits, self.G_matrix), 2)
                codewords.append(codeword)

            # Находим минимальное расстояние между всеми парами кодовых слов
            min_distance = float('inf')
            for i in range(len(codewords)):
                for j in range(i + 1, len(codewords)):
                    # Вычисляем расстояние Хэмминга (количество различающихся позиций)
                    distance = np.sum(codewords[i] != codewords[j])
                    if distance < min_distance:
                        min_distance = distance

            return min_distance if min_distance != float('inf') else 0
        else:
            # Для больших k используем аппроксимацию
            return max(3, self.n - self.k)

    def encode_text(self):
        operation_start_time = time.time()
        operation_start_dt = datetime.fromtimestamp(operation_start_time)

        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"""============================================================
OPERATION: Кодирование текста блочным кодом
START TIME: {operation_start_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
============================================================\n\n""")

        try:
            # --- Шаг 1: Проверка матриц ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 1: Проверка матриц кода
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Проверка наличия сгенерированных матриц кода.\n")

            if self.G_matrix is None:
                messagebox.showerror("Ошибка", "Сначала сгенерируйте матрицу кода")
                self.result_text.insert("end", "Результат: Ошибка - матрицы кода не сгенерированы.\n")
                step_end_time = time.time()
                self.result_text.insert("end",
                                        f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                return

            self.result_text.insert("end", "Матрицы кода присутствуют.\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 2: Получение входного текста ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 2: Получение входного текста
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Чтение текста из поля ввода.\n")

            input_text = self.input_text.get("1.0", "end-1c")
            if not input_text:
                messagebox.showerror("Ошибка", "Введите текст для кодирования")
                self.result_text.insert("end", "Результат: Ошибка - текст для кодирования отсутствует.\n")
                step_end_time = time.time()
                self.result_text.insert("end",
                                        f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                return

            self.result_text.insert("end",
                                    f"Текст получен (первые 50 символов): '{input_text[:50]}{'...' if len(input_text) > 50 else ''}'\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 3: Преобразование текста в двоичный код ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 3: Преобразование текста в двоичный код
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Конвертация текста в последовательность битов.\n")

            binary_data = text_to_binary(input_text)
            self.result_text.insert("end",
                                    f"Бинарное представление (первые 100 бит): {binary_data[:100]}{'...' if len(binary_data) > 100 else ''}\n")

            # Показываем посимвольное кодирование для отладки
            self.result_text.insert("end", "\nПосимвольное бинарное представление (первые 5 символов):\n")
            for char in input_text[:5]:
                binary_char = format(ord(char), '08b')
                self.result_text.insert("end", f"{char} -> {binary_char}\n")
            if len(input_text) > 5:
                self.result_text.insert("end", f"... (еще {len(input_text) - 5} символов)\n")

            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 4: Разделение на блоки ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 4: Разделение на блоки
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Разделение бинарных данных на блоки по k бит.\n")

            # Делим двоичную последовательность на блоки по k бит
            if len(binary_data) % self.k != 0:
                padding = self.k - (len(binary_data) % self.k)
                binary_data += '0' * padding
                self.result_text.insert("end",
                                        f"Добавлено {padding} нулей для выравнивания до размера блока k={self.k}\n")

            num_blocks = len(binary_data) // self.k
            self.result_text.insert("end", f"Разделено на {num_blocks} блоков по {self.k} бит\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 5: Кодирование блоков ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 5: Кодирование блоков
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Кодирование каждого блока с использованием матрицы G.\n")
            self.result_text.insert("end", "Процесс кодирования по блокам (первые 5 блоков):\n")

            encoded_data = ""
            for i in range(0, len(binary_data), self.k):
                block = binary_data[i:i + self.k]

                # Преобразуем блок в массив бит
                block_bits = np.array([int(bit) for bit in block])

                # Умножаем на порождающую матрицу по модулю 2
                codeword = np.remainder(np.dot(block_bits, self.G_matrix), 2)

                # Преобразуем закодированный блок обратно в строку
                encoded_block = ''.join(map(str, codeword))
                encoded_data += encoded_block

                # Выводим процесс кодирования для первых 5 блоков
                if i // self.k < 5:
                    self.result_text.insert("end", f"Блок {i // self.k + 1}: {block} -> {encoded_block}\n")

            if num_blocks > 5:
                self.result_text.insert("end", f"... (еще {num_blocks - 5} блоков)\n")

            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")


            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 6: Сохранение и вывод результатов
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Сохранение закодированных данных и вывод итогов.\n")

            # Сохраняем закодированные данные
            self.parent.encoded_text = encoded_data

            # Выводим статистику
            input_bits = len(binary_data)
            output_bits = len(encoded_data)
            redundancy = (output_bits - input_bits) / input_bits * 100 if input_bits > 0 else 0

            self.result_text.insert("end", f"Статистика кодирования:\n")
            self.result_text.insert("end", f"- Исходных бит: {input_bits}\n")
            self.result_text.insert("end", f"- Закодированных бит: {output_bits}\n")
            self.result_text.insert("end", f"- Избыточность: {redundancy:.2f}%\n")
            self.result_text.insert("end", f"- Средняя длина блока: {self.n} бит\n")

            # Выводим фрагмент данных
            self.result_text.insert("end", "\nФрагмент закодированных данных:\n")
            if len(encoded_data) > 100:
                self.result_text.insert("end", f"Начало: {encoded_data[:50]}...\n")
                self.result_text.insert("end", f"Конец: ...{encoded_data[-50:]}\n")
            else:
                self.result_text.insert("end", encoded_data + "\n")

            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

        except Exception as e:
            self.result_text.insert("end", f"КРИТИЧЕСКАЯ ОШИБКА: {str(e)}\n")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

        finally:
            operation_end_time = time.time()
            self.result_text.insert("end", f"""============================================================
            OPERATION COMPLETED: Кодирование текста блочным кодом
            END TIME: {datetime.fromtimestamp(operation_end_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
            TOTAL DURATION: {operation_end_time - operation_start_time:.3f} seconds
            ============================================================\n""")

    def add_noise(self):
        operation_start_time = time.time()
        operation_start_dt = datetime.fromtimestamp(operation_start_time)

        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"""============================================================
OPERATION: Внесение ошибок в канале
START TIME: {operation_start_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
============================================================\n\n""")

        try:
            # --- Шаг 1: Проверка входных данных ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 1: Проверка входных данных
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            if not self.parent.encoded_text:
                messagebox.showerror("Ошибка", "Сначала закодируйте текст")
                self.result_text.insert("end", "Результат: Ошибка - отсутствуют закодированные данные.\n")
                step_end_time = time.time()
                self.result_text.insert("end",
                                        f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                return

            encoded_data = self.parent.encoded_text
            self.result_text.insert("end", f"Получены закодированные данные длиной {len(encoded_data)} бит\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 2: Процесс внесения ошибок ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 2: Внесение ошибок в блоки
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Добавление 2 ошибок в каждый блок длиной n бит.\n")

            noisy_data = ""
            total_errors = 0
            num_blocks = len(encoded_data) // self.n

            for i in range(0, len(encoded_data), self.n):
                block = encoded_data[i:i + self.n].ljust(self.n, '0')
                error_pos = random.sample(range(self.n), 2)

                # Инвертируем биты
                block_list = list(block)
                for pos in error_pos:
                    block_list[pos] = '1' if block_list[pos] == '0' else '0'

                noisy_block = ''.join(block_list)
                noisy_data += noisy_block
                total_errors += 2

                # Логируем первые 3 блока
                if i // self.n < 3:
                    self.result_text.insert("end", f"Блок {i // self.n + 1}:\n")
                    self.result_text.insert("end", f"Исходный: {block}\n")
                    self.result_text.insert("end", f"С ошибками: {noisy_block}\n")
                    self.result_text.insert("end", f"Позиции ошибок: {error_pos}\n\n")

            self.result_text.insert("end", f"Всего внесено ошибок: {total_errors} ({total_errors // 2} блоков)\n")
            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 3: Сохранение результатов ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 3: Сохранение результатов
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.parent.noisy_text = noisy_data

            self.result_text.insert("end", "Фрагмент данных с ошибками:\n")
            if len(noisy_data) > 100:
                self.result_text.insert("end", f"Начало: {noisy_data[:50]}...\n")
                self.result_text.insert("end", f"Конец: ...{noisy_data[-50:]}\n")
            else:
                self.result_text.insert("end", noisy_data + "\n")

            step_end_time = time.time()
            self.result_text.insert("end",
                                    f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

        except Exception as e:
            self.result_text.insert("end", f"КРИТИЧЕСКАЯ ОШИБКА: {str(e)}\n")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

        finally:
            operation_end_time = time.time()
            self.result_text.insert("end", f"""============================================================
OPERATION COMPLETED: Внесение ошибок в канале
END TIME: {datetime.fromtimestamp(operation_end_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
TOTAL DURATION: {operation_end_time - operation_start_time:.3f} seconds
============================================================\n""")
        return True

    def decode_text(self):
        if not self.parent.noisy_text:
            messagebox.showerror("Ошибка", "Сначала внесите ошибки в закодированный текст")
            return

        if self.H_matrix is None:
            messagebox.showerror("Ошибка", "Матрица кода не сгенерирована")
            return

        # ==================== ЗАГОЛОВОК ОПЕРАЦИИ ====================
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", "\n=== ДЕКОДИРОВАНИЕ ДАННЫХ ===")

        # === ШАГ 1: ПОДГОТОВКА ДАННЫХ ===
        self.result_text.insert("end", "\n\n[1/4] Подготовка данных:")
        self.result_text.insert("end", "\nПолучение закодированных данных с ошибками")
        noisy_data = self.parent.noisy_text

        # === ШАГ 2: ОБРАБОТКА БЛОКОВ ===
        self.result_text.insert("end", "\n\n[2/4] Обработка блоков:")
        decoded_data = ""
        error_blocks = 0
        total_blocks = len(noisy_data) // self.n

        self.result_text.insert("end", f"\nВсего блоков для обработки: {total_blocks}")
        self.result_text.insert("end", "\nНачало процесса декодирования...")

        for i in range(0, len(noisy_data), self.n):
            block = noisy_data[i:i+self.n]
            if len(block) < self.n:  # Если последний блок неполный, дополняем его нулями
                self.result_text.insert("end", f"Последний блок неполный, дополняем нулями: {block} -> ")
                block = block + '0' * (self.n - len(block))
                self.result_text.insert("end", f"{block}\n")

            # Преобразуем блок в массив бит
            received_vector = np.array([int(bit) for bit in block])

            # Вычисляем синдром ошибки
            syndrome = np.remainder(np.dot(received_vector, self.H_matrix.T), 2)

            # Информация о синдроме
            syndrome_str = ''.join(map(str, syndrome))

            # Если синдром не нулевой, пытаемся исправить ошибки
            if np.any(syndrome):
                self.result_text.insert("end", f"Блок {i//self.n + 1}: {block}, синдром: {syndrome_str} - Обнаружена ошибка, ")

                # Создаем словарь синдромов для всех возможных векторов ошибок
                error_syndromes = {}

                # Пытаемся исправить ошибки в зависимости от нашей корректирующей способности
                correctable = False
                error_pos = []

                # Проверяем все возможные векторы ошибок с 1 ошибкой
                for pos in range(self.n):
                    error_vector = np.zeros(self.n, dtype=int)
                    error_vector[pos] = 1
                    error_syndrome = np.remainder(np.dot(error_vector, self.H_matrix.T), 2)
                    error_syndromes[tuple(error_syndrome)] = (error_vector, [pos])

                # Если наш код может исправлять 2 ошибки, проверяем векторы с 2 ошибками
                if self.error_correction_capability >= 2:
                    for pos1 in range(self.n):
                        for pos2 in range(pos1 + 1, self.n):
                            error_vector = np.zeros(self.n, dtype=int)
                            error_vector[pos1] = 1
                            error_vector[pos2] = 1
                            error_syndrome = np.remainder(np.dot(error_vector, self.H_matrix.T), 2)
                            error_syndromes[tuple(error_syndrome)] = (error_vector, [pos1, pos2])

                # Если синдром соответствует одному из известных векторов ошибок
                if tuple(syndrome) in error_syndromes:
                    # Исправляем ошибку
                    error_vector, error_pos = error_syndromes[tuple(syndrome)]
                    corrected_vector = np.remainder(received_vector + error_vector, 2)
                    correctable = True

                    self.result_text.insert("end", f"исправлены ошибки в позициях {error_pos}\n")
                else:
                    # Если не можем исправить ошибки
                    error_blocks += 1
                    corrected_vector = received_vector  # Оставляем как есть

                    self.result_text.insert("end", f"невозможно исправить\n")

                # Для систематического кода первые k бит - это информационные биты
                if self.k <= len(corrected_vector):
                    info_bits = corrected_vector[:self.k]
                else:
                    info_bits = corrected_vector  # На случай, если k каким-то образом больше n
            else:
                # Если синдром нулевой, ошибок нет или они скомпенсировали друг друга
                self.result_text.insert("end", f"Блок {i//self.n + 1}: {block}, синдром: {syndrome_str} - Ошибок не обнаружено\n")

                # Для систематического кода первые k бит - это информационные биты
                if self.k <= len(received_vector):
                    info_bits = received_vector[:self.k]
                else:
                    info_bits = received_vector  # На случай, если k каким-то образом больше n

            # Преобразуем информационные биты обратно в строку
            decoded_block = ''.join(map(str, info_bits))
            decoded_data += decoded_block

            # Показываем извлеченные информационные биты
            info_bits_str = ''.join(map(str, info_bits))
            self.result_text.insert("end", f"Извлеченные информационные биты: {info_bits_str}\n")
        self.result_text.insert("end", "\n\n[3/4] Постобработка данных:")

        # === ШАГ 4: АНАЛИЗ РЕЗУЛЬТАТОВ ===
        self.result_text.insert("end", "\n\n[4/4] Анализ результатов:")
        # Проверяем, были ли блоки, которые не удалось декодировать
        if error_blocks > 0:
            if self.error_correction_capability < 2:
                messagebox.showwarning("Предупреждение",
                                     f"Не удалось декодировать {error_blocks} блоков. " +
                                     "Код не способен исправить 2 и более ошибок.")
                # Активируем кнопку адаптации
                self.adapt_button.configure(state="normal")
            else:
                messagebox.showwarning("Предупреждение",
                                     f"Не удалось декодировать {error_blocks} блоков. " +
                                     "Возможно, некоторые блоки содержат более 2 ошибок.")

        # Сохраняем декодированные данные
        self.parent.decoded_text = decoded_data

        # Выводим результат
        self.result_text.insert("end", "\nДекодированные данные (информационные биты):\n")
        self.result_text.insert("end", decoded_data)

        # Сохраняем оригинальный двоичный текст перед кодированием
        # для сравнения с декодированным результатом
        original_binary = None
        try:
            input_text = self.input_text.get("1.0", "end-1c")
            if input_text:
                original_binary = text_to_binary(input_text)
                self.result_text.insert("end", f"\n\nОригинальный бинарный текст ({len(original_binary)} бит):\n")
                self.result_text.insert("end", original_binary)
        except:
            pass

        # Преобразуем двоичные данные обратно в текст
        try:
            # Обрезаем возможные лишние биты в конце для корректного преобразования
            # Если известна оригинальная длина бинарных данных, используем её
            if original_binary and len(original_binary) <= len(decoded_data):
                self.result_text.insert("end", f"\n\nОбрезаем декодированные данные до исходной длины: {len(decoded_data)} -> {len(original_binary)} бит\n")
                decoded_data = decoded_data[:len(original_binary)]

            # Строка должна быть кратна 8 для преобразования в ASCII
            padding = 8 - (len(decoded_data) % 8) if len(decoded_data) % 8 != 0 else 0
            if padding > 0:
                self.result_text.insert("end", f"Добавляем {padding} нулей в конец для выравнивания до размера байта (8 бит)\n")
                decoded_data = decoded_data + '0' * padding

            self.result_text.insert("end", f"\nДекодированные данные после корректировки ({len(decoded_data)} бит):\n")
            self.result_text.insert("end", decoded_data)

            # Анализируем полученный результат
            if original_binary and len(original_binary) <= len(decoded_data):
                # Сравниваем оригинальные данные с декодированными
                errors = sum(1 for a, b in zip(original_binary, decoded_data) if a != b)
                error_rate = errors / len(original_binary)
                self.result_text.insert("end", f"\n\nСравнение с исходными данными: {errors} ошибок из {len(original_binary)} бит ({error_rate:.2%} ошибок)\n")

            decoded_text = binary_to_text(decoded_data)
            self.result_text.insert("end", "\n\nДекодированный текст:\n")
            self.result_text.insert("end", decoded_text)

            self.result_text.insert("end", "\n\n=== ДЕКОДИРОВАНИЕ ЗАВЕРШЕНО ===")
            return error_blocks == 0  # Возвращаем True, если все блоки декодированы успешно
        except Exception as e:
            self.result_text.insert("end", f"\n\nНе удалось преобразовать двоичные данные в текст: {str(e)}")
            return False

    def adapt_code(self):
        # Увеличиваем параметры кода для исправления большего числа ошибок
        old_n = self.n
        old_k = self.k

        # Необходимое количество проверочных бит для исправления 2 ошибок
        # По формуле 2^(n-k) >= n+1
        # Увеличиваем n при сохранении k (уменьшаем скорость кода R = k/n)
        while 2**(self.n - self.k) < self.n + 1:
            self.n += 1

        # Для надежности добавляем еще немного избыточности
        self.n += 1

        # Обновляем поля ввода
        self.n_entry.delete(0, "end")
        self.n_entry.insert(0, str(self.n))

        self.result_text.insert("end", f"\n\nАдаптация кода: параметры изменены с ({old_n}, {old_k}) на ({self.n}, {self.k})\n")

        # Получаем исходный текст из поля ввода для повторного кодирования
        input_text = self.input_text.get("1.0", "end-1c")
        if not input_text:
            messagebox.showerror("Ошибка", "Отсутствует исходный текст для адаптации")
            return

        # Пытаемся генерировать матрицу с требуемой корректирующей способностью
        max_attempts = 10
        success = False

        for attempt in range(max_attempts):
            # Генерируем порождающую матрицу G
            # Сначала создаем единичную матрицу k x k
            I_k = np.eye(self.k, dtype=int)

            # Затем создаем случайную матрицу k x (n-k)
            P = np.random.randint(0, 2, size=(self.k, self.n - self.k))

            # Объединяем их, чтобы получить G в систематической форме [I_k | P]
            self.G_matrix = np.hstack((I_k, P))

            # Генерируем проверочную матрицу H
            # Создаем матрицу P^T
            P_t = P.T

            # Создаем единичную матрицу (n-k) x (n-k)
            I_nk = np.eye(self.n - self.k, dtype=int)

            # Объединяем их, чтобы получить H в систематической форме [P^T | I_(n-k)]
            self.H_matrix = np.hstack((P_t, I_nk))

            # Определяем корректирующую способность кода
            min_d = self.calculate_min_distance()
            self.error_correction_capability = (min_d - 1) // 2

            # Проверяем, достигли ли мы требуемой корректирующей способности
            if self.error_correction_capability >= 2:
                success = True
                break

        if not success:
            # Если не удалось сгенерировать код с нужной корректирующей способностью,
            # увеличиваем n еще больше
            old_n = self.n
            self.n += 2
            self.n_entry.delete(0, "end")
            self.n_entry.insert(0, str(self.n))

            self.result_text.insert("end", f"Не удалось создать код с корректирующей способностью 2, увеличиваем n до {self.n}\n")

            # Повторно генерируем матрицу
            self.generate_matrix()

        # Обновляем информацию о корректирующей способности
        self.info_label.configure(text=f"Текущая корректирующая способность: {self.error_correction_capability} ошибок")

        # Выводим матрицы для отладки
        G_str = ""
        for row in self.G_matrix:
            G_str += ' '.join(map(str, row)) + '\n'

        H_str = ""
        for row in self.H_matrix:
            H_str += ' '.join(map(str, row)) + '\n'

        self.result_text.insert("end", "\nСгенерированные матрицы кода:\n")
        self.result_text.insert("end", "Порождающая матрица G:\n")
        self.result_text.insert("end", G_str + "\n")
        self.result_text.insert("end", "Проверочная матрица H:\n")
        self.result_text.insert("end", H_str + "\n")

        # Обновляем информацию
        messagebox.showinfo("Адаптация",
                           f"Код адаптирован для исправления 2 ошибок.\nПараметры изменены с ({old_n}, {old_k}) на ({self.n}, {self.k}).")

        # Автоматически перекодируем исходный текст
        self.encode_text()

        # Автоматически вносим ошибки
        self.add_noise()

        # Автоматически декодируем
        success = self.decode_text()

        # Повторяем адаптацию, если декодирование не удалось и n не слишком большое
        if not success and self.n < 20:  # Ограничиваем n, чтобы избежать бесконечного цикла
            self.result_text.insert("end", "\n\nДекодирование после адаптации не успешно. Повторяем адаптацию...\n")
            self.adapt_code()  # Рекурсивно пытаемся адаптировать код дальше
            return

        # Деактивируем кнопку адаптации
        self.adapt_button.configure(state="disabled")