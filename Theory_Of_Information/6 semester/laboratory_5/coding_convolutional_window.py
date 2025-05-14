import customtkinter as ctk
import numpy as np
import random
from tkinter import messagebox
from helpful_utils import text_to_binary, binary_to_text
import time
from datetime import datetime

class CodingConvolutional:
    def __init__(self, parent):
        self.parent = parent
        self.constraint_length = 3  # Длина ограничения
        self.rate = 1/2  # Скорость кода (1/2 означает, что из 1 бита получается 2)
        self.generator_polynomials = ["111", "101"]  # Полиномы генератора (начальные)
        self.num_polynomials = 2     # Количество полиномов
        self.registers = None  # Регистры сдвига
        self.error_probability = 0.05  # Вероятность ошибки
        self.erasure_probability = 0.03  # Вероятность стирания
        self.channel_type = "ДСК"  # Тип канала (ДСК, ДСКС, Z-канал)
        self.poly_entries = []  # Список полей ввода для полиномов
        
    def create_widgets(self, parent_frame):
        # Создание основного фрейма
        self.main_frame = ctk.CTkFrame(parent_frame)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок модуля
        self.title_label = ctk.CTkLabel(self.main_frame, text="Модели каналов связи со сверточным кодом",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(padx=10, pady=10)

        # Фрейм для ввода параметров
        self.params_frame = ctk.CTkFrame(self.main_frame)
        self.params_frame.pack(fill="x", padx=10, pady=10)

        # Параметры кода
        self.params_label = ctk.CTkLabel(self.params_frame, text="Параметры сверточного кода:",
                                        font=ctk.CTkFont(weight="bold"))
        self.params_label.grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=3)

        # Длина ограничения
        self.constraint_label = ctk.CTkLabel(self.params_frame, text="Длина ограничения:")
        self.constraint_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.constraint_entry = ctk.CTkEntry(self.params_frame, width=60)
        self.constraint_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.constraint_entry.insert(0, str(self.constraint_length))

        # Кнопка обновления длины ограничения
        self.update_constraint_button = ctk.CTkButton(self.params_frame, text="Обновить длину",
                                              command=self.update_constraint_length)
        self.update_constraint_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # Количество полиномов
        self.num_poly_label = ctk.CTkLabel(self.params_frame, text="Количество полиномов:")
        self.num_poly_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.num_poly_entry = ctk.CTkEntry(self.params_frame, width=60)
        self.num_poly_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.num_poly_entry.insert(0, str(self.num_polynomials))

        # Кнопка обновления количества полиномов
        self.update_poly_button = ctk.CTkButton(self.params_frame, text="Обновить количество",
                                              command=self.update_polynomials_count)
        self.update_poly_button.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Создаем контейнер для трех колонок
        columns_frame = ctk.CTkFrame(self.main_frame)
        columns_frame.pack(fill="x", padx=10, pady=10)
        columns_frame.grid_columnconfigure(0, weight=1)  # Полиномы
        columns_frame.grid_columnconfigure(1, weight=1)  # Параметры канала
        columns_frame.grid_columnconfigure(2, weight=1)  # Операции

        # === ЛЕВАЯ КОЛОНКА: ПОЛИНОМЫ ===
        poly_column = ctk.CTkFrame(columns_frame)
        poly_column.grid(row=0, column=0, sticky="nsew", padx=5)

        # Заголовок с информацией о полиномах
        self.poly_label = ctk.CTkLabel(poly_column, text=f"Полиномы генератора ({self.num_polynomials}):",
                                     font=ctk.CTkFont(weight="bold"))
        self.poly_label.pack(padx=10, pady=(10, 5))

        # Текстовое поле для редактирования полиномов
        self.poly_summary = ctk.CTkTextbox(poly_column, height=100)
        self.poly_summary.pack(fill="x", padx=10, pady=5)

        # Кнопка для применения изменений
        self.apply_poly_button = ctk.CTkButton(poly_column, text="Применить изменения",
                                           command=self._apply_polynomial_changes,
                                           height=28)
        self.apply_poly_button.pack(padx=10, pady=5)

        # === СРЕДНЯЯ КОЛОНКА: ПАРАМЕТРЫ КАНАЛА ===
        channel_column = ctk.CTkFrame(columns_frame)
        channel_column.grid(row=0, column=1, sticky="nsew", padx=5)

        self.channel_label = ctk.CTkLabel(channel_column, text="Параметры канала:",
                                        font=ctk.CTkFont(weight="bold"))
        self.channel_label.pack(padx=10, pady=(10, 5))

        # Тип канала
        channel_type_frame = ctk.CTkFrame(channel_column)
        channel_type_frame.pack(fill="x", padx=10, pady=2)

        self.channel_type_label = ctk.CTkLabel(channel_type_frame, text="Тип канала:")
        self.channel_type_label.pack(side="left", padx=5)

        self.channel_type_var = ctk.StringVar(value=self.channel_type)
        self.channel_type_combo = ctk.CTkComboBox(channel_type_frame,
                                                values=["ДСК", "ДСКС", "Z-канал"],
                                                variable=self.channel_type_var,
                                                command=self.on_channel_changed,
                                                height=28,
                                                width=120)
        self.channel_type_combo.pack(side="right", padx=5)

        # Вероятность ошибки
        error_frame = ctk.CTkFrame(channel_column)
        error_frame.pack(fill="x", padx=10, pady=2)

        self.error_label = ctk.CTkLabel(error_frame, text="Вероятность ошибки (p):")
        self.error_label.pack(side="left", padx=5)

        self.error_entry = ctk.CTkEntry(error_frame, width=60, height=28)
        self.error_entry.pack(side="right", padx=5)
        self.error_entry.insert(0, str(self.error_probability))

        # Вероятность стирания
        erasure_frame = ctk.CTkFrame(channel_column)
        erasure_frame.pack(fill="x", padx=10, pady=2)

        self.erasure_label = ctk.CTkLabel(erasure_frame, text="Вероятность стирания (q):")
        self.erasure_label.pack(side="left", padx=5)

        self.erasure_entry = ctk.CTkEntry(erasure_frame, width=60, height=28)
        self.erasure_entry.pack(side="right", padx=5)
        self.erasure_entry.insert(0, str(self.erasure_probability))

        # === ПРАВАЯ КОЛОНКА: ОПЕРАЦИИ ===
        operation_column = ctk.CTkFrame(columns_frame)
        operation_column.grid(row=0, column=2, sticky="nsew", padx=5)

        self.operation_label = ctk.CTkLabel(operation_column, text="Операции:",
                                          font=ctk.CTkFont(weight="bold"))
        self.operation_label.pack(padx=10, pady=(10, 5))

        # Кнопки операций в вертикальном расположении
        self.encode_button = ctk.CTkButton(operation_column, text="Кодировать",
                                         command=self.encode_text,
                                         height=28)
        self.encode_button.pack(padx=10, pady=2, fill="x")

        self.noise_button = ctk.CTkButton(operation_column, text="Внести ошибки/стирания",
                                        command=self.add_noise,
                                        height=28)
        self.noise_button.pack(padx=10, pady=2, fill="x")

        self.decode_button = ctk.CTkButton(operation_column, text="Декодировать",
                                         command=self.decode_text,
                                         height=28)
        self.decode_button.pack(padx=10, pady=2, fill="x")

        self.capacity_button = ctk.CTkButton(operation_column, text="Рассчитать пропускную способность",
                                           command=self.calculate_capacity,
                                           height=28)
        self.capacity_button.pack(padx=10, pady=2, fill="x")

        # Фрейм для ввода текста
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="x", padx=10, pady=10)

        # Заголовок для ввода текста
        self.input_label = ctk.CTkLabel(self.input_frame, text="Исходный текст:",
                                      font=ctk.CTkFont(weight="bold"))
        self.input_label.pack(padx=10, pady=5, anchor="w")

        # Текстовое поле для ввода
        self.input_text = ctk.CTkTextbox(self.input_frame, height=100)
        self.input_text.pack(fill="x", padx=10, pady=5)

        # Кнопки для загрузки текста из файла и очистки
        self.buttons_frame = ctk.CTkFrame(self.input_frame)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)

        self.load_button = ctk.CTkButton(self.buttons_frame, text="Загрузить из файла",
                                       command=self.load_text)
        self.load_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(self.buttons_frame, text="Очистить",
                                        command=lambda: self.input_text.delete("1.0", "end"))
        self.clear_button.pack(side="left", padx=5)

        # Фрейм для отображения результатов
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок для результатов
        self.result_label = ctk.CTkLabel(self.result_frame, text="Результаты:",
                                       font=ctk.CTkFont(weight="bold"))
        self.result_label.pack(padx=10, pady=5, anchor="w")

        # Текстовое поле для вывода результатов
        self.result_text = ctk.CTkTextbox(self.result_frame, height=250)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Настройка интерфейса в зависимости от типа канала
        self.on_channel_changed(self.channel_type)

        # Обновляем сводку полиномов
        self.update_polynomials_summary()

    def create_polynomial_entries(self):
        # Очищаем существующие поля ввода
        for entry in self.poly_entries:
            entry.destroy()
        self.poly_entries = []

        # Удаляем предыдущий контейнер, если он существует
        for widget in self.poly_frame.winfo_children():
            widget.destroy()

        # Если полиномов слишком много, используем компактный режим отображения
        compact_mode = self.num_polynomials > 8

        # Добавляем информационную строку
        info_text = f"Всего полиномов: {self.num_polynomials}, длина полинома: {self.constraint_length} бит"
        info_label = ctk.CTkLabel(self.poly_frame, text=info_text, font=ctk.CTkFont(size=10))
        info_label.pack(fill="x", padx=10, pady=(5, 0), anchor="w")

        # Создаем компактный контейнер с прокруткой и ограниченной высотой
        container_height = 90 if compact_mode else 100
        poly_container = ctk.CTkScrollableFrame(self.poly_frame, height=container_height)
        poly_container.pack(fill="x", padx=10, pady=2)

        # Определяем оптимальное количество полиномов в строке в зависимости от их количества
        if compact_mode:
            polynomials_per_row = 5  # Очень компактное отображение при большом количестве
        elif self.num_polynomials <= 3:
            polynomials_per_row = self.num_polynomials
        elif self.num_polynomials <= 6:
            polynomials_per_row = 3
        else:
            polynomials_per_row = 4

        # Создаем сетку для размещения полиномов
        row_frames = []

        # Создаем фреймы для каждой строки
        row_count = (self.num_polynomials + polynomials_per_row - 1) // polynomials_per_row
        for i in range(row_count):
            row_frame = ctk.CTkFrame(poly_container)
            row_frame.pack(fill="x", padx=2, pady=2)
            row_frames.append(row_frame)

        # Заполняем строки полиномами
        for i in range(self.num_polynomials):
            row_index = i // polynomials_per_row
            col_index = i % polynomials_per_row

            # Создаем компактный фрейм для каждого полинома
            poly_entry_frame = ctk.CTkFrame(row_frames[row_index])
            poly_entry_frame.grid(row=0, column=col_index, padx=2, pady=2, sticky="w")

            # Максимально компактная метка
            label_width = 20 if compact_mode else 25
            font_size = 9 if compact_mode else 10
            poly_label = ctk.CTkLabel(poly_entry_frame, text=f"П{i+1}:", width=label_width, font=ctk.CTkFont(size=font_size))
            poly_label.pack(side="left", padx=1)

            # Компактное поле ввода с шириной в зависимости от количества полиномов
            if compact_mode:
                entry_width = 70
            elif polynomials_per_row <= 3:
                entry_width = 120
            else:
                entry_width = 90

            poly_entry = ctk.CTkEntry(poly_entry_frame, width=entry_width, font=ctk.CTkFont(size=font_size+1))
            poly_entry.pack(side="left", padx=1)

            # Заполняем поле существующим значением из списка полиномов
            if i < len(self.generator_polynomials):
                poly_entry.insert(0, self.generator_polynomials[i])

            self.poly_entries.append(poly_entry)

        # Добавляем нижнюю панель управления с кнопками
        controls_frame = ctk.CTkFrame(self.poly_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)

        # Добавляем кнопку информации о полиномах
        info_button = ctk.CTkButton(controls_frame, text="?", width=25, height=25,
                                   command=self._show_polynomials_help)
        info_button.pack(side="left", padx=5)

        # Если есть рекомендуемые полиномы, добавляем кнопку их применения
        if self.constraint_length <= 5:
            suggestions = self.get_polynomial_suggestions(self.constraint_length)
            if suggestions and len(suggestions) > 0:
                apply_button = ctk.CTkButton(controls_frame, text="Применить рекомендуемые",
                                          width=160, height=25,
                                          command=lambda: self._apply_recommended_polynomials(suggestions))
                apply_button.pack(side="left", padx=5)

        # Добавляем кнопку применения для всех полиномов одинакового значения
        if self.num_polynomials > 2:
            same_poly_button = ctk.CTkButton(controls_frame, text="Одинаковые полиномы",
                                         width=140, height=25,
                                         command=self._apply_same_polynomial)
            same_poly_button.pack(side="left", padx=5)

    def _show_polynomials_help(self):
        """Показывает информацию о полиномах"""
        help_text = (
            "Полиномы генератора определяют правила кодирования информационных битов.\n\n"
            f"Длина полинома ({self.constraint_length} бит) должна соответствовать длине ограничения.\n"
            "Рекомендуется, чтобы первый и последний биты полинома были равны 1.\n\n"
            "Полиномы можно записать в двух форматах:\n"
            "1. Двоичный формат: строка из 0 и 1 длиной с длину ограничения\n"
            "   Пример: '111' - означает, что будут использованы все регистры\n"
            "2. Формат индексов: список индексов регистров через запятую\n"
            "   Пример: '0,1,2' - это эквивалент '111' (используются регистры с индексами 0, 1 и 2)\n\n"
            "Примеры эффективных полиномов:\n"
        )

        # Добавляем примеры для разных длин ограничения
        for length in range(2, min(6, self.constraint_length + 1)):
            suggestions = self.get_polynomial_suggestions(length)
            if suggestions:
                binary_examples = ', '.join(suggestions)
                index_examples = []
                for suggestion in suggestions:
                    indices = [i for i, bit in enumerate(suggestion) if bit == '1']
                    index_examples.append(str(indices).replace('[', '').replace(']', ''))

                help_text += f"Для длины {length}:\n"
                help_text += f"- Двоичный: {binary_examples}\n"
                help_text += f"- Индексы: {', '.join(index_examples)}\n"

        messagebox.showinfo("Информация о полиномах", help_text)

    def _apply_recommended_polynomials(self, suggestions):
        """Применяет рекомендуемые полиномы"""
        # Используем только необходимое количество полиномов
        recommended = suggestions[:self.num_polynomials]

        # Если рекомендаций меньше, чем нужно полиномов, дублируем их
        while len(recommended) < self.num_polynomials:
            recommended.append(suggestions[0])

        # Обновляем список полиномов
        self.generator_polynomials = recommended.copy()

        # Получаем числовое представление полиномов
        numeric_polys = self.binary_polys_to_numeric()

        # Выводим информацию
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Применены рекомендуемые полиномы:\n")
        for i, poly in enumerate(recommended):
            self.result_text.insert("end", f"Полином {i+1}: {poly} (двоичный) / {numeric_polys[i]} (индексы)\n")

        # Обновляем сводку полиномов
        self.update_polynomials_summary()

    def _apply_same_polynomial(self):
        """Применяет первый полином ко всем полиномам"""
        if not self.generator_polynomials or len(self.generator_polynomials) == 0:
            messagebox.showerror("Ошибка", "Нет доступных полиномов")
            return

        # Берем первый полином и применяем его ко всем остальным
        first_poly = self.generator_polynomials[0]
        self.generator_polynomials = [first_poly] * self.num_polynomials

        # Получаем числовое представление полиномов
        numeric_polys = self.binary_polys_to_numeric()

        # Выводим информацию
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Применен одинаковый полином ко всем позициям:\n")
        for i, poly in enumerate(self.generator_polynomials):
            self.result_text.insert("end", f"Полином {i+1}: {poly} (двоичный) / {numeric_polys[i]} (индексы)\n")

        # Обновляем сводку полиномов
        self.update_polynomials_summary()
    
    def get_polynomial_suggestions(self, constraint_length):
        """Возвращает список эффективных полиномов для заданной длины ограничения"""
        # Словарь эффективных полиномов для разных длин ограничения
        # Источник: учебные материалы по теории кодирования
        suggestions = {
            2: ["11"],
            3: ["111", "101"],
            4: ["1111", "1101", "1011"],
            5: ["11111", "10101", "11001", "10011"]
        }
        
        return suggestions.get(constraint_length, [])
    
    def update_polynomials_count(self):
        try:
            # Получаем новое количество полиномов
            new_count = int(self.num_poly_entry.get())
            if new_count < 1:
                messagebox.showerror("Ошибка", "Количество полиномов должно быть не менее 1")
                return
            
            # Ограничение на максимальное количество полиномов для удобства использования
            if new_count > 10:
                response = messagebox.askquestion("Предупреждение", 
                                               f"Вы выбрали {new_count} полиномов. Большое количество полиномов может снизить скорость кода и усложнить интерфейс. Продолжить?")
                if response != 'yes':
                    return
            
            # Обновляем количество полиномов
            self.num_polynomials = new_count
            
            # Получаем текущую длину ограничения
            try:
                constraint_length = int(self.constraint_entry.get())
                if constraint_length < 2:
                    constraint_length = 3  # Устанавливаем значение по умолчанию
                    self.constraint_entry.delete(0, "end")
                    self.constraint_entry.insert(0, str(constraint_length))
                    self.constraint_length = constraint_length
            except ValueError:
                constraint_length = 3  # Устанавливаем значение по умолчанию
                self.constraint_entry.delete(0, "end")
                self.constraint_entry.insert(0, str(constraint_length))
                self.constraint_length = constraint_length
            
            # Создаем новые полиномы по умолчанию, полностью удаляя предыдущие
            self.generator_polynomials = []
            for i in range(new_count):
                # Создаем полином по умолчанию с соответствующей длиной ограничения
                # Используем шаблон 1...1 (первый и последний бит = 1)
                default_poly = '1' + '0' * (constraint_length - 2) + '1'
                self.generator_polynomials.append(default_poly)
            
            # Обновляем скорость кода
            self.rate = 1 / self.num_polynomials
            
            # Обновляем заголовок с информацией о количестве полиномов
            self.poly_label.configure(text=f"Полиномы генератора ({self.num_polynomials}):")
            
            # Обновляем сводку о полиномах
            self.update_polynomials_summary()
            
            # Очищаем текстовое поле для результатов
            self.result_text.delete("1.0", "end")
            
            # Обновляем информацию
            self.result_text.insert("1.0", "=== Обновление параметров сверточного кода ===\n")
            self.result_text.insert("end", f"Количество полиномов обновлено: {self.num_polynomials}\n")
            self.result_text.insert("end", f"Длина ограничения: {self.constraint_length}\n")
            self.result_text.insert("end", f"Скорость кода: 1/{self.num_polynomials}\n")
            self.result_text.insert("end", f"Предыдущие полиномы удалены, созданы новые полиномы по умолчанию.\n")
            
            # Выводим информацию о полиномах
            self.result_text.insert("end", "\nНовые полиномы генератора:\n")
            for i, poly in enumerate(self.generator_polynomials):
                self.result_text.insert("end", f"Полином {i+1}: {poly}\n")
            
            # Информация о влиянии скорости кода на кодирование
            self.result_text.insert("end", f"\nВлияние скорости кода на кодирование:\n")
            self.result_text.insert("end", f"- Скорость 1/{self.num_polynomials} означает, что каждый исходный бит преобразуется в {self.num_polynomials} кодовых битов\n")
            self.result_text.insert("end", f"- Более низкая скорость (больше полиномов) повышает избыточность и помехоустойчивость кода\n")
            self.result_text.insert("end", f"- Более высокая скорость (меньше полиномов) снижает избыточность, но ухудшает помехоустойчивость\n")
            
            # Проверяем полиномы для безопасности
            self._validate_polynomials()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Количество полиномов должно быть целым числом")
    
    def on_channel_changed(self, channel_type):
        # Сохраняем новый тип канала
        self.channel_type = channel_type
        
        # Настраиваем интерфейс в зависимости от типа канала
        if channel_type == "ДСКС":
            # В канале со стираниями показываем значение из сохраненного параметра
            self.erasure_entry.delete(0, "end")
            self.erasure_entry.insert(0, str(self.erasure_probability))
        else:
            # В других каналах устанавливаем значение 0 для вероятности стирания
            self.erasure_entry.delete(0, "end")
            self.erasure_entry.insert(0, "0")
            self.erasure_probability = 0
        
        # Проверяем значение вероятности ошибки
        if not self.error_entry.get():
            # Устанавливаем значение по умолчанию, если поле пустое
            self.error_entry.delete(0, "end")
            self.error_entry.insert(0, str(self.error_probability))
        
        # Очищаем текстовое поле для результатов и добавляем информацию о выбранном канале
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"=== Выбран канал: {channel_type} ===\n\n")
        
        # Показываем описание и характеристики выбранного канала
        if channel_type == "ДСК":
            self.result_text.insert("end", "Двоичный симметричный канал (ДСК)\n\n")
            self.result_text.insert("end", "Характеристики:\n")
            self.result_text.insert("end", "- 0→1 и 1→0 происходят с одинаковой вероятностью p\n")
            self.result_text.insert("end", "- Симметричность ошибок (одинаковая вероятность для 0 и 1)\n")
            self.result_text.insert("end", "- Формула пропускной способности: C = 1 - H(p)\n")
            self.result_text.insert("end", "- Где H(p) = -p·log₂(p) - (1-p)·log₂(1-p) - двоичная энтропия\n\n")
            
            
            # Рекомендации для ДСК
            self.result_text.insert("end", "Рекомендации для кодирования:\n")
            self.result_text.insert("end", "- Оптимальны симметричные коды\n")
            self.result_text.insert("end", "- Эффективны коды с большим кодовым расстоянием\n")
            self.result_text.insert("end", "- Хороши сверточные коды с равномерным распределением единиц в полиномах\n")
            
        elif channel_type == "ДСКС":
            self.result_text.insert("end", "Двоичный симметричный канал со стираниями (ДСКС)\n\n")
            self.result_text.insert("end", "Характеристики:\n")
            self.result_text.insert("end", "- 0→1 и 1→0 происходят с одинаковой вероятностью p\n")
            self.result_text.insert("end", "- Стирание бита происходит с вероятностью q\n")
            self.result_text.insert("end", "- Корректная передача происходит с вероятностью 1-p-q\n")
            self.result_text.insert("end", "- Формула пропускной способности: C = (1-q)·(1-H(p/(1-q)))\n\n")
            
            
            
            # Рекомендации для ДСКС
            self.result_text.insert("end", "Рекомендации для кодирования:\n")
            self.result_text.insert("end", "- Стирания легче исправлять, чем ошибки (известна позиция стирания)\n")
            self.result_text.insert("end", "- Для стираний эффективны сверточные коды с большой избыточностью\n")
            self.result_text.insert("end", "- При высокой вероятности стираний рекомендуется увеличивать число полиномов\n")
            
        elif channel_type == "Z-канал":
            self.result_text.insert("end", "Z-канал (канал с асимметричными ошибками)\n\n")
            self.result_text.insert("end", "Характеристики:\n")
            self.result_text.insert("end", "- 0→1 никогда не происходит (вероятность 0)\n")
            self.result_text.insert("end", "- 1→0 происходит с вероятностью p\n")
            self.result_text.insert("end", "- Асимметричность ошибок (только в одном направлении)\n")
            self.result_text.insert("end", "- При оптимальном распределении входных символов пропускная способность выше, чем у ДСК\n\n")
            
            
            # Рекомендации для Z-канала
            self.result_text.insert("end", "Рекомендации для кодирования:\n")
            self.result_text.insert("end", "- Эффективны коды с большим весом (много единиц)\n")
            self.result_text.insert("end", "- Полиномы с большим числом единиц повышают вероятность обнаружения ошибок\n")
            self.result_text.insert("end", "- Асимметрия канала может быть использована для оптимизации кодов\n")
        
        # Общая информация о сверточных кодах
        self.result_text.insert("end", "\n=== Общая информация о сверточных кодах ===\n")
        self.result_text.insert("end", "- Сверточные коды эффективны при последовательной передаче данных\n")
        self.result_text.insert("end", "- Длина ограничения определяет память кода и сложность декодирования\n")
        self.result_text.insert("end", "- Количество полиномов влияет на скорость кода и его избыточность\n")
        self.result_text.insert("end", "- Скорость кода R = 1/n, где n - количество полиномов\n")
        self.result_text.insert("end", "- Для надежной передачи скорость кода должна быть меньше пропускной способности канала\n")
        
        # Рекомендуем пользователю следующие шаги
        self.result_text.insert("end", "\nДля начала работы:\n")
        self.result_text.insert("end", "1. Введите исходный текст или загрузите его из файла\n")
        self.result_text.insert("end", "2. Настройте параметры кода (длина ограничения, количество и значения полиномов)\n")
        self.result_text.insert("end", "3. Нажмите 'Кодировать' для получения сверточного кода\n")
    
    def load_text(self):
        text = self.parent.load_text_from_file()
        if text:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", text)
    
    def encode_text(self):
        operation_start_time = time.time()
        operation_start_dt = datetime.fromtimestamp(operation_start_time)

        # Получаем входной текст
        input_text = self.input_text.get("1.0", "end").strip()
        
        # Очищаем результаты
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"""============================================================
OPERATION: Сверточное кодирование
START TIME: {operation_start_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
============================================================\n\n""")

        # --- Шаг 1: Валидация входных данных ---
        step_start_time = time.time()
        self.result_text.insert("end", f"""------------------------------------------------------------
STEP 1: Валидация входных данных
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
        self.result_text.insert("end", "Пояснение: Проверка наличия текста для кодирования.\n")
        self.result_text.insert("end", f"Входные данные:\n  Текст: '{input_text[:50]}{'...' if len(input_text) > 50 else ''}'\n")

        if not input_text:
            messagebox.showerror("Ошибка", "Введите текст для кодирования")
            self.result_text.insert("end", "Результат: Ошибка - текст для кодирования отсутствует.\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
            return
        self.result_text.insert("end", "Результат: Входной текст присутствует.\n")
        step_end_time = time.time()
        self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

        try:
            # --- Шаг 2: Валидация параметров кодирования ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 2: Валидация параметров сверточного кода
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Проверка корректности полиномов генератора и длины ограничения.\n")
            self.result_text.insert("end", f"Текущие параметры:\n  Полиномы: {self.generator_polynomials}\n  Длина ограничения: {self.constraint_entry.get()}\n")

            if not self._validate_polynomials():
                messagebox.showerror("Ошибка", "Некорректные полиномы генератора")
                self.result_text.insert("end", "Результат: Ошибка - некорректные полиномы генератора.\n")
                step_end_time = time.time()
                self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                return
            
            try:
                current_constraint_length = int(self.constraint_entry.get())
                if current_constraint_length < 2:
                    messagebox.showerror("Ошибка", "Длина ограничения должна быть не менее 2")
                    self.result_text.insert("end", "Результат: Ошибка - длина ограничения < 2.\n")
                    step_end_time = time.time()
                    self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                    return
                self.constraint_length = current_constraint_length # Обновляем, если успешно
            except ValueError:
                messagebox.showerror("Ошибка", "Длина ограничения должна быть целым числом")
                self.result_text.insert("end", "Результат: Ошибка - длина ограничения не целое число.\n")
                step_end_time = time.time()
                self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                return
            
            for poly in self.generator_polynomials:
                if len(poly) != self.constraint_length:
                    messagebox.showerror("Ошибка", f"Длина полинома {poly} не соответствует длине ограничения ({self.constraint_length})")
                    self.result_text.insert("end", f"Результат: Ошибка - длина полинома {poly} не равна {self.constraint_length}.\n")
                    step_end_time = time.time()
                    self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                    return
                if not all(bit in '01' for bit in poly):
                    messagebox.showerror("Ошибка", f"Полином {poly} должен состоять только из 0 и 1")
                    self.result_text.insert("end", f"Результат: Ошибка - полином {poly} содержит не бинарные символы.\n")
                    step_end_time = time.time()
                    self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                    return
            self.result_text.insert("end", "Результат: Параметры кода валидны.\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 3: Преобразование текста в двоичный код ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 3: Преобразование текста в двоичный код
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Исходный текст конвертируется в последовательность битов (0 и 1) с использованием кодировки UTF-8.\n")
            self.result_text.insert("end", f"Входные данные:\n  Текст: '{input_text[:50]}{'...' if len(input_text) > 50 else ''}'\n")
            binary_data = text_to_binary(input_text)
            if not binary_data:
                messagebox.showerror("Ошибка", "Не удалось преобразовать текст в двоичный код")
                self.result_text.insert("end", "Результат: Ошибка - не удалось преобразовать текст в двоичный код.\n")
                step_end_time = time.time()
                self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n")
                return
            self.result_text.insert("end", f"Результат (первые 100 бит): {binary_data[:100]}{'...' if len(binary_data) > 100 else ''}\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 4: Вывод базовой информации о кодировании ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 4: Информация о параметрах кодирования
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Отображение основных параметров, используемых для кодирования.\n")
            self.result_text.insert("end", f"  Тип канала: {self.channel_type}\n")
            self.result_text.insert("end", f"  Длина ограничения: {self.constraint_length}\n")
            self.result_text.insert("end", f"  Количество полиномов: {len(self.generator_polynomials)}\n")
            code_rate = 1 / len(self.generator_polynomials)
            self.result_text.insert("end", f"  Скорость кода: R = 1/{len(self.generator_polynomials)} = {code_rate:.4f}\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 5: Анализ эффективности кода (Пропускная способность) ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 5: Анализ кода (пропускная способность канала)
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Расчет приблизительной пропускной способности выбранного канала и сравнение со скоростью кода.\n")
            try:
                p = float(self.error_entry.get())
                q = float(self.erasure_entry.get()) if self.channel_type == "ДСКС" else 0
                self.result_text.insert("end", f"Входные параметры для расчета:\n  Вероятность ошибки (p): {p}\n  Вероятность стирания (q): {q if self.channel_type == 'ДСКС' else 'N/A'}\n")
                
                channel_capacity_value, capacity_details = self._calculate_channel_capacity_internal(p, q, self.channel_type)
                self.result_text.insert("end", capacity_details)
                self.result_text.insert("end", f"Расчетная пропускная способность канала ({self.channel_type}): C ≈ {channel_capacity_value:.4f} бит/символ\n")

                if code_rate <= channel_capacity_value:
                    self.result_text.insert("end", f"Итог: ✅ Скорость кода ({code_rate:.4f}) не превышает пропускную способность ({channel_capacity_value:.4f}).\n")
                    self.result_text.insert("end", "       Теоретически, возможна надежная передача.\n")
                else:
                    self.result_text.insert("end", f"Итог: ⚠️ Скорость кода ({code_rate:.4f}) превышает пропускную способность ({channel_capacity_value:.4f}).\n")
                    self.result_text.insert("end", "       Надежная передача невозможна. Рекомендуется увеличить избыточность кода (например, увеличить число полиномов).\n")
                    required_polys = max(2, int(np.ceil(1 / channel_capacity_value))) if channel_capacity_value > 0 else len(self.generator_polynomials) + 1
                    if required_polys > len(self.generator_polynomials):
                         self.result_text.insert("end", f"       Рекомендуемое мин. кол-во полиномов: {required_polys}\n")

            except Exception as e:
                self.result_text.insert("end", f"Предупреждение: Не удалось вычислить пропускную способность канала: {str(e)}\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")
            
            # --- Шаг 6: Сверточное кодирование --- 
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 6: Процесс сверточного кодирования
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""") 
            self.result_text.insert("end", "Пояснение: Применение алгоритма сверточного кодирования к двоичным данным.\n")
            # convolutional_encode теперь будет возвращать (encoded_data, log_details)
            encoded_data, log_details_encode = self.convolutional_encode(binary_data, step_start_time)
            self.result_text.insert("end", log_details_encode) # Добавляем детали из convolutional_encode
            step_end_time = time.time() # Общее время шага кодирования
            self.result_text.insert("end", f"END (Общее время кодирования): {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION (Общее время кодирования): {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            self.parent.input_text = input_text
            self.parent.encoded_text = encoded_data
            
            # --- Шаг 7: Статистика кодирования ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 7: Статистика кодирования
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Отображение ключевых метрик процесса кодирования.\n")
            input_bits = len(binary_data)
            output_bits = len(encoded_data)
            redundancy_ratio = (output_bits - input_bits) / input_bits if input_bits > 0 else 0
            
            self.result_text.insert("end", f"  Длина исходных данных: {input_bits} бит\n")
            self.result_text.insert("end", f"  Длина закодированных данных: {output_bits} бит\n")
            self.result_text.insert("end", f"  Избыточность кода: {redundancy_ratio:.2f} ({redundancy_ratio*100:.0f}%)\n")

            error_correction_level = "Низкая"
            if len(self.generator_polynomials) >= 3 and self.constraint_length >= 4:
                error_correction_level = "Высокая"
            elif len(self.generator_polynomials) >= 2 and self.constraint_length >= 3:
                error_correction_level = "Средняя"
            self.result_text.insert("end", f"  Ориентировочная способность исправления ошибок: {error_correction_level}\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 8: Вывод части закодированных данных ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 8: Результат кодирования (фрагмент)
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", "Пояснение: Отображение начала и конца закодированной последовательности для предварительного просмотра.\n")
            if len(encoded_data) > 100:
                self.result_text.insert("end", f"  Первые 50 символов: {encoded_data[:50]}\n")
                self.result_text.insert("end", f"  Последние 50 символов: {encoded_data[-50:]}\n")
            else:
                self.result_text.insert("end", f"  Закодированные данные: {encoded_data}\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")

            # --- Шаг 9: Рекомендации и следующий шаг ---
            step_start_time = time.time()
            self.result_text.insert("end", f"""------------------------------------------------------------
STEP 9: Рекомендации и следующие шаги
START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}
------------------------------------------------------------
""")
            self.result_text.insert("end", f"Пояснение: Советы по использованию кода в зависимости от типа канала и указания для следующего этапа работы.\n")
            self.result_text.insert("end", f"Рекомендации для канала {self.channel_type}:\n")
            if self.channel_type == "ДСК":
                self.result_text.insert("end", "  - ДСК хорошо работает с симметричными кодами.\n")
                self.result_text.insert("end", "  - Увеличение количества полиномов улучшает корректирующую способность кода.\n")
            elif self.channel_type == "ДСКС":
                self.result_text.insert("end", "  - В ДСКС стирания лучше обрабатываются, чем ошибки, так как известны позиции стираний.\n")
                self.result_text.insert("end", "  - Рекомендуется использовать коды с большим расстоянием Хэмминга.\n")
            elif self.channel_type == "Z-канал":
                self.result_text.insert("end", "  - Z-канал имеет асимметричные ошибки (только 1→0), это можно использовать для оптимизации.\n")
                self.result_text.insert("end", "  - Полиномы с большим количеством единиц помогают лучше защититься от ошибок типа 1→0.\n")
            self.result_text.insert("end", "\nСледующий шаг: ✓ Кодирование успешно завершено. Теперь вы можете нажать 'Внести ошибки/стирания' для моделирования канала.\n")
            step_end_time = time.time()
            self.result_text.insert("end", f"END: {datetime.fromtimestamp(step_end_time).strftime('%H:%M:%S.%f')[:-3]}\nDURATION: {step_end_time - step_start_time:.3f} seconds\n------------------------------------------------------------\n\n")
            
        except Exception as e:
            self.result_text.insert("end", f"КРИТИЧЕСКАЯ ОШИБКА в процессе кодирования: {str(e)}\n")
            messagebox.showerror("Критическая ошибка кодирования", f"Произошла ошибка: {str(e)}")
        
        finally:
            operation_end_time = time.time()
            self.result_text.insert("end", f"""============================================================
OPERATION COMPLETED: Сверточное кодирование
END TIME: {datetime.fromtimestamp(operation_end_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
TOTAL DURATION: {operation_end_time - operation_start_time:.3f} seconds
============================================================\n""")

    def _calculate_channel_capacity_internal(self, p, q, channel_type):
        """Внутренний метод для расчета пропускной способности канала и формирования детального лога.
        Возвращает (значение_пропускной_способности, строка_лога_деталей).
        """
        log_details = ""
        channel_capacity_value = 0

        if channel_type == "ДСК":
            log_details += "  Расчет для ДСК: C = 1 - H(p), где H(p) = -p*log2(p) - (1-p)*log2(1-p)\n"
            if p == 0 or p == 1:
                channel_capacity_value = 1.0
                log_details += f"  H({p}) = 0 (канал без ошибок или полностью ошибочный)\n"
            else:
                h_binary = -p * np.log2(p) - (1-p) * np.log2(1-p)
                channel_capacity_value = 1 - h_binary
                log_details += f"  H({p}) = -{p}*log2({p}) - {1-p}*log2({1-p}) = {h_binary:.4f}\n"
            log_details += f"  C_ДСК = 1 - {h_binary if p !=0 and p !=1 else 0:.4f} = {channel_capacity_value:.4f}\n"

        elif channel_type == "ДСКС":
            log_details += "  Расчет для ДСКС: C = (1-q)*(1 - H(p_eff)), где p_eff = p/(1-q)\n"
            if q == 1:
                channel_capacity_value = 0.0
                log_details += "  q=1: Канал полностью стирает данные. C_ДСКС = 0\n"
            else:
                p_eff = p / (1-q)
                log_details += f"  p_eff = {p}/(1-{q}) = {p_eff:.4f}\n"
                if p_eff < 0 or p_eff > 1: # Добавим проверку p_eff, т.к. p+q > 1 не проверяется до этого шага
                     log_details += f"  Предупреждение: p_eff ({p_eff:.4f}) вне диапазона [0,1]. Сумма p+q ({p+q}) может быть > 1. C будет неверной.\n" 
                     # Можно установить capacity_value в 0 или оставить как есть, но с предупреждением
                     # Для безопасности, если p_eff выходит за рамки, это обычно означает p+q > 1, и такой канал невалиден
                     # Установим в 0, если p+q > 1 не было поймано ранее
                     if p + q > 1:
                         channel_capacity_value = 0.0
                         h_eff = float('nan') # Неопределенность
                     else: # Если p+q <=1, но p_eff некорректен из-за округления или граничных случаев
                         if p_eff <= 0 or p_eff >= 1: # Исправлено для включения граничных случаев
                            h_eff = 0.0
                         else:
                            h_eff = -p_eff * np.log2(p_eff) - (1-p_eff) * np.log2(1-p_eff)
                elif p_eff == 0 or p_eff == 1:
                    h_eff = 0.0
                    log_details += f"  H({p_eff:.4f}) = 0\n"
                else:
                    h_eff = -p_eff * np.log2(p_eff) - (1-p_eff) * np.log2(1-p_eff)
                    log_details += f"  H({p_eff:.4f}) = {h_eff:.4f}\n"
                
                if not (np.isnan(h_eff)) : # Только если h_eff корректно посчитан
                    channel_capacity_value = (1-q) * (1 - h_eff)
                    log_details += f"  C_ДСКС = (1-{q})*(1 - {h_eff:.4f}) = {channel_capacity_value:.4f}\n"
                else:
                    log_details += f"  C_ДСКС = Ошибка расчета (возможно p+q > 1)\n"
                    channel_capacity_value = 0.0 # На случай если не было поймано раньше

        elif channel_type == "Z-канал":
            log_details += "  Расчет для Z-канала (приближенная формула для оптимального входа):\n"
            log_details += "  C = log2(1 + (1-p) * (p^(p/(1-p)))) если 0 < p < 1\n"
            if p == 0:
                channel_capacity_value = 1.0
                log_details += "  p=0: Канал без ошибок (0->0, 1->1). C_Z = 1\n"
            elif p == 1:
                channel_capacity_value = 0.0
                log_details += "  p=1: Канал всегда передает 0 (0->0, 1->0). C_Z = 0\n"
            else:
                # Формула Бергера для Z-канала (более точная)
                # C = log2(1 + ( (1-p) / (p**(p/(1-p))) ) ) не совсем та.
                # Более распространена: H( (1-p) / (1+ (1-p)/p^(p/(1-p))) ) - H(p) / (1+ (1-p)/p^(p/(1-p))) - это для p(x=1) оптимизированного.
                # Самая простая и часто используемая: C = log2(1 + (1-p)*(p**(p/(1-p))))
                # Но она дает неверные результаты для p > 0.5. 
                # Используем формулу Галлагера для Z-канала: C = max_{0<=a<=1} [ H(a(1-p)) - a*H(p) ]
                # где a = p(x=1). Это сложно для аналитического решения здесь.
                # Для простоты, возьмем известную верхнюю границу или одну из аппроксимаций.
                # C_Z = log2(1 + (1-p)*(p**(p/(1-p)))) - эта формула корректна для p < 0.5. Для p > 0.5 она неверна.
                # Для Z-канала C = H( (1-p)/( (1-p) + p**(p/(1-p)) ) ) - (p(X=1)) H(p), где p(X=1) = 1 / (1 + sqrt( (1-p)/p ) ) 
                # Вместо сложной формулы, используем ту, что была в calculate_capacity, но с пояснениями.
                # Ранее было: capacity_z = np.log2(1 + (1-p) * (p ** (p/(1-p))))
                # Эта формула имеет ограничения по p. Проверим её.
                if p > 0 and p < 1:
                    try:
                        # Эта формула может быть нестабильной или неточной для некоторых p
                        # Добавляем более надежную аппроксимацию, если она существует
                        # Используем более простую оценку, как в функции calculate_capacity:
                        # C = H(y) - H(y|x) = H( (1-a) + a(1-p) ) - a*H(p)
                        # Оптимальное 'a' (p(X=1)) для Z-канала: a_opt = 1 / (1 + sqrt(p/(1-p))) если мы можем выбирать p(x)
                        # Если p(x) = 0.5 (равновероятный вход):
                        # C = 0.5 * log2(1/(1-p)) при p < 0.5, или C = 1 - H( (1+p)/2 ) - (1-p)/2 * log2(e)
                        # Используем аппроксимацию для равновероятного входа, если p(X=0)=p(X=1)=0.5
                        # C = (1-p) * (1 - H(0.5)) + p * (1 - H(0.5 / (1-p) )) - не то
                        # Для Z-канала, если вход равновероятен:  C = 1 - H( (1+p)/2 ) - (1-p)/2
                        # Это тоже не самая простая. Вернемся к аппроксимации, которая была:
                        # C = log2(1 + (1-p) * p**(p/(1-p))) - эта формула верна при p(x=0) = p**(1/(1-p))/(1+p**(1/(1-p))) 
                        # что не всегда так. 

                        # Самая простая верхняя оценка (upper bound) для Z-канала: C <= 1 - H(p)
                        # Используем формулу из старой calculate_capacity, так как она была там:
                        # capacity_z = np.log2(1 + (1-p) * (p ** (p/(1-p)))) - эта формула из Cover & Thomas для специфичного p(x)
                        # Проверим ее на область определения
                        if p == 0.5:
                             channel_capacity_value = np.log2(1.5) # ~0.585
                        elif (p/(1-p)) < 0 and p < 1: # p > 1, что не должно быть
                             channel_capacity_value = 0 # Невалидный p
                             log_details += f"  Предупреждение: p/(1-p) < 0, что странно для 0<p<1. p={p}.\n"
                        elif (1-p) == 0: # p=1
                             channel_capacity_value = 0
                        else:
                            # Предотвращаем RuntimeWarning для p близких к 1 в p**(p/(1-p))
                            if p > 0.99999: # очень близко к 1
                                term_val = 0 # p**(p/(1-p)) -> 0 for p->1
                            else:
                                term_val = p**(p/(1-p))
                            channel_capacity_value = np.log2(1 + (1-p) * term_val) if (1 + (1-p) * term_val) > 0 else 0
                        log_details += f"  Использована формула C_Z = log2(1 + (1-p)*p^(p/(1-p))): {channel_capacity_value:.4f}\n"
                        log_details += f"  Примечание: Эта формула предполагает оптимальное распределение входных символов, которое может отличаться от равновероятного.\n"
                    except (ValueError, RuntimeWarning) as e_cap:
                        log_details += f"  Ошибка при расчете C_Z по формуле: {str(e_cap)}. Используем оценку C <= 1 - H(p).\n"
                        if p == 0 or p == 1: h_p_val = 0
                        else: h_p_val = -p * np.log2(p) - (1-p) * np.log2(1-p)
                        channel_capacity_value = 1 - h_p_val
                        log_details += f"  Оценка C_Z ≈ 1 - H({p}) = {channel_capacity_value:.4f}\n"
                else: # p=0 или p=1 уже обработаны
                     channel_capacity_value = 1.0 if p == 0 else 0.0

        return channel_capacity_value, log_details

    def convolutional_encode(self, binary_data, operation_step_start_time):
        """Сверточное кодирование. Возвращает (encoded_data, log_details)."""
        step_start_time = time.time()
        log_details = ""
        log_details += f"  STEP 6.1: Подготовка к кодированию\n  START: {datetime.fromtimestamp(step_start_time).strftime('%H:%M:%S.%f')[:-3]}\n"
        log_details += "  Пояснение: Преобразование полиномов в числовой формат и добавление хвостовых битов к данным.\n"

        numeric_polynomials = self.binary_polys_to_numeric()
        padded_data = binary_data + '0' * (self.constraint_length - 1)

        log_details += f"  Входные данные для кодировщика:\n    Бинарные данные (первые 60): {binary_data[:60]}{'...' if len(binary_data) > 60 else ''}\n    Дополненные данные (первые 60): {padded_data[:60]}{'...' if len(padded_data) > 60 else ''}\n    Числовые полиномы: {numeric_polynomials}\n"
        log_details += f"  END: {datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')[:-3]}\n  DURATION: {time.time() - step_start_time:.3f} seconds\n  ----------------------------------------\n"

        # --- Подшаг: Инициализация регистров и переменных ---
        sub_step_start_time = time.time()
        log_details += f"  STEP 6.2: Инициализация регистров и процесса кодирования\n  START: {datetime.fromtimestamp(sub_step_start_time).strftime('%H:%M:%S.%f')[:-3]}\n"
        log_details += "  Пояснение: Установка начального состояния регистров сдвига.\n"

        encoded_data_list = [] # Собираем биты в список для эффективности
        max_register_idx = 0
        if numeric_polynomials and any(numeric_polynomials):
             max_register_idx = max(max(p) if p else -1 for p in numeric_polynomials)
        registers = [0] * (max_register_idx + 1) 

        log_details += f"  Начальное состояние регистров (длина {len(registers)}): {''.join(map(str, registers))}\n"
        log_details += f"  END: {datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')[:-3]}\n  DURATION: {time.time() - sub_step_start_time:.3f} seconds\n  ----------------------------------------\n"
        
        # --- Подшаг: Цикл кодирования ---
        sub_step_start_time = time.time()
        log_details += f"  STEP 6.3: Основной цикл кодирования\n  START: {datetime.fromtimestamp(sub_step_start_time).strftime('%H:%M:%S.%f')[:-3]}\n"
        log_details += "  Пояснение: Побитовая обработка входных данных, сдвиг регистров и вычисление выходных битов на основе полиномов.\n"
        log_details += "  Пример кодирования первых нескольких битов (до 5 итераций):\n"
        log_details += "  Итерация | Входной бит | Состояние регистров | Выходные биты (для полиномов)\n"
        log_details += "  ---------|-------------|---------------------|-------------------------------\n"
        
        for i, bit in enumerate(padded_data):
            registers.insert(0, int(bit))
            registers.pop()
            
            current_output_bits = []
            for poly_idx, poly in enumerate(numeric_polynomials):
                xor_sum = 0
                for reg_idx in poly:
                    if 0 <= reg_idx < len(registers):
                        xor_sum ^= registers[reg_idx]
                current_output_bits.append(str(xor_sum))
            encoded_data_list.extend(current_output_bits)
            
            if i < 5: # Логируем только первые 5 итераций для примера
                reg_str = ''.join(map(str, registers[:max_register_idx+1]))
                out_str = ''.join(current_output_bits)
                poly_outputs_str = " / ".join([f"P{idx+1}:{b}" for idx, b in enumerate(current_output_bits)])
                log_details += f"    {i+1:<6} |      {bit:<8} | {reg_str:<19} | {out_str} ({poly_outputs_str})\n"
        
        if len(padded_data) > 5:
            log_details += "  ... (остальные итерации не логируются подробно для краткости) ...\n"
        
        encoded_data_str = "".join(encoded_data_list)
        log_details += f"  Результат (закодированные данные, первые 100 бит): {encoded_data_str[:100]}{'...' if len(encoded_data_str) > 100 else ''}\n"
        log_details += f"  END: {datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')[:-3]}\n  DURATION: {time.time() - sub_step_start_time:.3f} seconds\n  ----------------------------------------\n"
        
        return encoded_data_str, log_details
    
    def binary_polys_to_numeric(self):
        """Преобразует полиномы из двоичного формата в числовой формат индексов"""
        numeric_polynomials = []
        for poly in self.generator_polynomials:
            indices = [i for i, bit in enumerate(poly) if bit == '1']
            numeric_polynomials.append(indices)
        return numeric_polynomials
    
    def numeric_poly_to_binary(self, numeric_poly, length):
        """Преобразует полином из числового формата индексов в двоичный формат"""
        binary_poly = ['0'] * length
        for idx in numeric_poly:
            if 0 <= idx < length:
                binary_poly[idx] = '1'
        return ''.join(binary_poly)
    
    def add_noise(self):
        if not self.parent.encoded_text:
            messagebox.showerror("Ошибка", "Сначала закодируйте текст")
            return
        
        try:
            # Получаем параметры канала
            try:
                self.error_probability = float(self.error_entry.get())
            except ValueError:
                # Устанавливаем значение по умолчанию
                self.error_probability = 0.05
                self.error_entry.delete(0, "end")
                self.error_entry.insert(0, str(self.error_probability))
            
                try:
                    self.erasure_probability = float(self.erasure_entry.get())
                except ValueError:
                    # Устанавливаем значение по умолчанию
                    self.erasure_probability = 0.03 if self.channel_type == "ДСКС" else 0
                    self.erasure_entry.delete(0, "end")
                    self.erasure_entry.insert(0, str(self.erasure_probability))
            
            # Проверка корректности вероятностей
            if self.error_probability < 0 or self.error_probability > 1:
                messagebox.showerror("Ошибка", "Вероятность ошибки должна быть в диапазоне [0, 1]")
                return
            
            if self.erasure_probability < 0 or self.erasure_probability > 1:
                messagebox.showerror("Ошибка", "Вероятность стирания должна быть в диапазоне [0, 1]")
                return
            
            if self.error_probability + self.erasure_probability > 1:
                messagebox.showerror("Ошибка", "Сумма вероятностей ошибки и стирания не может превышать 1")
                return
            
            # Получаем закодированные данные
            encoded_data = self.parent.encoded_text
            
            # Вносим ошибки и стирания в зависимости от типа канала
            noisy_data = ""
            error_count = 0
            erasure_count = 0
            bits_processed = 0
            
            # Для детальной статистики
            zero_to_one_count = 0  # 0->1
            one_to_zero_count = 0  # 1->0
            zeros_count = 0
            ones_count = 0
            
            # Детальная статистика для Z-канала
            z_channel_error_count = 0
            z_channel_ones_count = 0
            
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", "=== Моделирование канала связи ===\n")
            self.result_text.insert("end", f"Тип канала: {self.channel_type}\n")
            self.result_text.insert("end", f"Параметры канала:\n")
            self.result_text.insert("end", f"- Вероятность ошибки (p): {self.error_probability}\n")
            
            if self.channel_type == "ДСКС":
                self.result_text.insert("end", f"- Вероятность стирания (q): {self.erasure_probability}\n")
            
            
            
            for bit in encoded_data:
                bits_processed += 1
                r = random.random()
                
                # Учитываем исходные биты для статистики
                if bit == '0':
                    zeros_count += 1
                elif bit == '1':
                    ones_count += 1
                    if self.channel_type == "Z-канал":
                        z_channel_ones_count += 1
                
                if self.channel_type == "ДСК":
                    # Двоичный симметричный канал
                    if r < self.error_probability:
                        new_bit = '1' if bit == '0' else '0'
                        noisy_data += new_bit
                        error_count += 1
                        
                        # Подсчет типов ошибок
                        if bit == '0':
                            zero_to_one_count += 1
                        else:
                            one_to_zero_count += 1
                    else:
                        noisy_data += bit
                
                elif self.channel_type == "ДСКС":
                    # Двоичный симметричный канал со стираниями
                    if r < self.error_probability:
                        new_bit = '1' if bit == '0' else '0'
                        noisy_data += new_bit
                        error_count += 1
                        
                        # Подсчет типов ошибок
                        if bit == '0':
                            zero_to_one_count += 1
                        else:
                            one_to_zero_count += 1
                    elif r < self.error_probability + self.erasure_probability:
                        noisy_data += 'e'  # Обозначаем стирание символом 'e'
                        erasure_count += 1
                    else:
                        noisy_data += bit
                
                elif self.channel_type == "Z-канал":
                    # Z-канал: 0->0 всегда, 1->0 с вероятностью p
                    if bit == '1' and r < self.error_probability:
                        noisy_data += '0'
                        error_count += 1
                        one_to_zero_count += 1
                        z_channel_error_count += 1
                    else:
                        noisy_data += bit
            
            # Вычисляем вероятности ошибок и стираний
            total_bits = bits_processed
            error_prob = error_count / total_bits if total_bits > 0 else 0
            erasure_prob = erasure_count / total_bits if total_bits > 0 else 0
            
            # Для Z-канала отдельно считаем вероятность ошибок при передаче 1
            z_prob = 0
            if self.channel_type == "Z-канал" and z_channel_ones_count > 0:
                z_prob = z_channel_error_count / z_channel_ones_count
            
            # Сохраняем данные с ошибками
            self.parent.noisy_text = noisy_data
            
            # Выводим результат
            self.result_text.insert("end", "\n\n=== Статистика внесения ошибок ===\n")
            
            if total_bits > 100:
                self.result_text.insert("end", "Первые 50 бит закодированных данных:\n")
                self.result_text.insert("end", encoded_data[:50] + "\n")
                self.result_text.insert("end", "Первые 50 бит данных с ошибками:\n")
                self.result_text.insert("end", noisy_data[:50] + "\n")
            else:
                self.result_text.insert("end", "Закодированные данные:\n")
                self.result_text.insert("end", encoded_data + "\n")
                self.result_text.insert("end", "Данные с ошибками:\n")
                self.result_text.insert("end", noisy_data + "\n")
            
            self.result_text.insert("end", f"\nРаспределение исходных битов:\n")
            self.result_text.insert("end", f"- Нули: {zeros_count} ({zeros_count/total_bits:.4f})\n")
            self.result_text.insert("end", f"- Единицы: {ones_count} ({ones_count/total_bits:.4f})\n")
            
            self.result_text.insert("end", f"\nСтатистика канала:\n")
            self.result_text.insert("end", f"- Общее количество битов: {total_bits}\n")
            self.result_text.insert("end", f"- Количество ошибок: {error_count}\n")
            self.result_text.insert("end", f"- Фактическая вероятность ошибки: {error_prob:.6f}\n")
            
            # Детальная статистика по типам ошибок
            if error_count > 0:
                self.result_text.insert("end", f"\nТипы битовых ошибок:\n")
                zero_to_one_ratio = zero_to_one_count / error_count if error_count > 0 else 0
                one_to_zero_ratio = one_to_zero_count / error_count if error_count > 0 else 0
                
                self.result_text.insert("end", f"- 0→1: {zero_to_one_count} ({zero_to_one_ratio:.4f})\n")
                self.result_text.insert("end", f"- 1→0: {one_to_zero_count} ({one_to_zero_ratio:.4f})\n")
            
            if self.channel_type == "ДСКС":
                self.result_text.insert("end", f"- Количество стираний: {erasure_count}\n")
                self.result_text.insert("end", f"- Фактическая вероятность стирания: {erasure_prob:.6f}\n")
            
            if self.channel_type == "Z-канал":
                self.result_text.insert("end", f"- Количество единиц в исходных данных: {z_channel_ones_count}\n")
                self.result_text.insert("end", f"- Количество ошибок типа 1→0: {z_channel_error_count}\n")
                self.result_text.insert("end", f"- Вероятность ошибки при передаче '1': {z_prob:.6f}\n")
                
            # Добавляем инструкцию для следующего шага
            self.result_text.insert("end", "\n✓ Ошибки и стирания внесены. Теперь вы можете нажать 'Декодировать' для восстановления данных.\n")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при внесении ошибок: {str(e)}")
    
    def decode_text(self):
        if not self.parent.noisy_text:
            messagebox.showerror("Ошибка", "Сначала внесите ошибки в закодированный текст")
            return
        
        # Получаем данные с ошибками/стираниями
        noisy_data = self.parent.noisy_text
        
        # Если в канале были стирания, заменяем их на более вероятные биты
        if 'e' in noisy_data:
            # Для простоты заменяем стирания на '0'
            noisy_data = noisy_data.replace('e', '0')
        
        # Конвертируем полиномы в числовой формат
        numeric_polynomials = self.binary_polys_to_numeric()
        
        # Декодирование с использованием алгоритма Витерби из Laba.py
        try:
            decoded_data = self.viterbi_decode(noisy_data, numeric_polynomials)
            
            # Удаляем добавленные биты в конце (tail bits)
            if len(decoded_data) >= self.constraint_length - 1:
                decoded_data = decoded_data[:-self.constraint_length + 1]
            
            # Сохраняем декодированные данные
            self.parent.decoded_text = decoded_data
            
            # Выводим результат
            self.result_text.insert("end", "\n\nДекодированные данные:\n")
            self.result_text.insert("end", decoded_data)
            
            # Добавляем информацию о процессе декодирования
            self.result_text.insert("end", f"\n\nИнформация о декодировании:\n")
            self.result_text.insert("end", f"Количество полиномов: {len(numeric_polynomials)}\n")
            self.result_text.insert("end", f"Использован метод декодирования: алгоритм Витерби\n")
            
            # Преобразуем двоичные данные обратно в текст с явным указанием кодировки UTF-8
            try:
                decoded_text = binary_to_text(decoded_data)
                self.result_text.insert("end", "\n\nДекодированный текст:\n")
                self.result_text.insert("end", decoded_text)
            except Exception as e:
                self.result_text.insert("end", f"\n\nНе удалось преобразовать двоичные данные в текст: {str(e)}")
                
        except Exception as e:
            messagebox.showerror("Ошибка декодирования", f"Ошибка при декодировании: {str(e)}")
    
    def viterbi_decode(self, encoded_bits, polynomials):
        """Декодирует последовательность с помощью алгоритма Витерби."""
        if not encoded_bits:
            return ''
        
        n_outputs = len(polynomials)
        if len(encoded_bits) % n_outputs != 0:
            raise ValueError("Некорректная длина закодированной последовательности")
        
        max_register = max(max(p) for p in polynomials)
        n_states = 2 ** max_register
        states = [format(i, f'0{max_register}b') for i in range(n_states)]
        
        # Вывод в интерфейс информации о декодировании Витерби
        self.result_text.insert("end", "\n=== Декодирование алгоритмом Витерби ===\n")
        self.result_text.insert("end", f"Количество состояний: {n_states}\n")
        self.result_text.insert("end", f"Длина закодированной последовательности: {len(encoded_bits)} бит\n")
        self.result_text.insert("end", f"Количество шагов: {len(encoded_bits)//n_outputs}\n")
        
        path_metrics = {s: float('inf') for s in states}
        path_metrics['0' * max_register] = 0
        paths = {s: [] for s in states}
        
        for i in range(0, len(encoded_bits), n_outputs):
            current_bits = encoded_bits[i:i+n_outputs]
            new_metrics = {s: float('inf') for s in states}
            new_paths = {s: [] for s in states}
            
            for state in states:
                if path_metrics[state] == float('inf'):
                    continue
                
                for input_bit in ['0', '1']:
                    next_state = (input_bit + state)[:-1]
                    tmp_registers = list(map(int, (input_bit + state)))
                    expected = []
                    for poly in polynomials:
                        xor = 0
                        for idx in poly:
                            xor ^= tmp_registers[idx]
                        expected.append(str(xor))
                    expected_str = ''.join(expected)
                    
                    metric = sum(c1 != c2 for c1, c2 in zip(current_bits, expected_str))
                    total_metric = path_metrics[state] + metric
                    
                    if total_metric < new_metrics[next_state]:
                        new_metrics[next_state] = total_metric
                        new_paths[next_state] = paths[state] + [input_bit]
            
            path_metrics, paths = new_metrics, new_paths
        
        final_state = min(path_metrics, key=path_metrics.get)
        self.result_text.insert("end", f"\nФинальная метрика: {path_metrics[final_state]:.1f}\n")
        
        return ''.join(paths[final_state])
    
    def calculate_capacity(self):
        """
        Рассчитывает пропускную способность канала связи на основе моделирования передачи данных
        с внесением случайных ошибок. Использует текст из окна ввода и одну случайную вероятность
        для всех типов каналов.
        """
        try:
            # Получаем текст из окна ввода
            input_text = self.input_text.get("1.0", "end").strip()
            if not input_text:
                messagebox.showwarning("Предупреждение", "Введите текст для кодирования в поле ввода")
                return
                
            # Преобразуем текст в двоичную последовательность
            binary_sequence = text_to_binary(input_text)
            if not binary_sequence:
                messagebox.showerror("Ошибка", "Не удалось преобразовать текст в двоичную последовательность")
                return
                
            # Генерируем ОДНУ случайную вероятность ошибки для всех каналов
            random_p = random.uniform(0.01, 0.3)  # Ограничиваем сверху 0.3 для более реалистичных значений
            random_q = random.uniform(0.01, 0.2)  # Вероятность стирания для ДСКС
            
            # Кодируем последовательность
            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", f"Исходный текст: {input_text}\n")
            self.result_text.insert("end", f"Двоичная последовательность: {binary_sequence}\n")
            
            encoded_sequence, _ = self.convolutional_encode(binary_sequence, time.time())
            self.result_text.insert("end", f"Закодированная последовательность: {encoded_sequence}\n\n")
            
            # Функция для внесения ошибок в последовательность
            def add_errors(sequence, error_rate):
                result = []
                for bit in sequence:
                    if random.random() < error_rate:
                        # Инвертируем бит с вероятностью error_rate
                        result.append('1' if bit == '0' else '0')
                    else:
                        result.append(bit)
                return ''.join(result)
            
            # Функция для внесения стираний в последовательность
            def add_erasures(sequence, erasure_rate):
                result = []
                for bit in sequence:
                    if random.random() < erasure_rate:
                        # Заменяем бит на 'e' (стирание) с вероятностью erasure_rate
                        result.append('e')
                    else:
                        result.append(bit)
                return ''.join(result)
            
            # Функция для расчета пропускной способности на основе количества ошибок
            def calculate_empirical_capacity(original, received, rate):
                total_bits = len(original)
                error_bits = sum(1 for o, r in zip(original, received) if o != r and r != 'e')
                erasure_bits = received.count('e')
                
                # Эмпирические вероятности
                p_empirical = error_bits / total_bits if total_bits > 0 else 0
                q_empirical = erasure_bits / total_bits if total_bits > 0 else 0
                
                # Рассчитываем пропускную способность
                if p_empirical == 0 and q_empirical == 0:
                    return rate  # Если ошибок нет, пропускная способность равна скорости кодирования
                
                if q_empirical == 1:
                    return 0  # Если все стерто, пропускная способность 0
                    
                if p_empirical == 0:
                    # Только стирания
                    return rate * (1 - q_empirical)
                
                # Общий случай с ошибками и стираниями
                h = -p_empirical * np.log2(p_empirical) - (1-p_empirical) * np.log2(1-p_empirical) if 0 < p_empirical < 1 else 0
                return rate * (1 - q_empirical) * (1 - h)
            
            # Выводим заголовок
            self.result_text.insert("end", "\n\n=== Результаты моделирования передачи данных ===\n")
            
            # 1. Двоичный симметричный канал (ДСК)
            corrupted_dsk = add_errors(encoded_sequence, random_p)
            capacity_dsk = calculate_empirical_capacity(encoded_sequence, corrupted_dsk, self.rate)
            
            # 2. Двоичный симметричный канал со стираниями (ДСКС)
            corrupted_dsks = add_errors(encoded_sequence, random_p)
            corrupted_dsks = add_erasures(corrupted_dsks, random_q)
            capacity_dsks = calculate_empirical_capacity(encoded_sequence, corrupted_dsks, self.rate)
            
            # 3. Z-канал (только переход 1->0 с вероятностью p)
            def add_z_errors(sequence, error_rate):
                result = []
                for bit in sequence:
                    if bit == '1' and random.random() < error_rate:
                        result.append('0')  # Только 1->0 ошибки
                    else:
                        result.append(bit)
                return ''.join(result)
            
            corrupted_z = add_z_errors(encoded_sequence, random_p)
            capacity_z = calculate_empirical_capacity(encoded_sequence, corrupted_z, self.rate)
            
            # Выводим результаты
            self.result_text.insert("end", f"\nПараметры моделирования:\n")
            self.result_text.insert("end", f"- Длина закодированной последовательности: {len(encoded_sequence)} бит\n")
            self.result_text.insert("end", f"- Скорость кодирования: {self.rate:.2f}\n")
            self.result_text.insert("end", f"- Использованная вероятность ошибки (p): {random_p:.4f}\n")
            self.result_text.insert("end", f"- Использованная вероятность стирания (q): {random_q:.4f}\n")
            
            self.result_text.insert("end", "\nРезультаты моделирования для разных каналов:\n")
            
            # ДСК
            self.result_text.insert("end", f"\n1. Двоичный симметричный канал (ДСК):\n")
            self.result_text.insert("end", f"- Эмпирическая пропускная способность: {capacity_dsk:.4f} бит/символ\n")
            
            # ДСКС
            self.result_text.insert("end", f"\n2. ДСК со стираниями (ДСКС):\n")
            self.result_text.insert("end", f"- Эмпирическая пропускная способность: {capacity_dsks:.4f} бит/символ\n")
            
            # Z-канал
            self.result_text.insert("end", f"\n3. Z-канал:\n")
            self.result_text.insert("end", f"- Эмпирическая пропускная способность: {capacity_z:.4f} бит/символ\n")
            
            # Теоретические значения для сравнения
            self.result_text.insert("end", "\nТеоретические значения для сравнения:\n")
            
            # Теоретическая пропускная способность ДСК
            if random_p != 0 and random_p != 1:
                theo_dsk = 1 + random_p * np.log2(random_p) + (1-random_p) * np.log2(1-random_p)
            else:
                theo_dsk = 1 if random_p == 0 else 0
            
            # Теоретическая пропускная способность ДСКС
            if random_q != 1:
                if random_p != 0 and random_p != 1-random_q:
                    theo_dsks = 1 - random_q + (1-random_p-random_q) * np.log2((1-random_p-random_q)/(1-random_q)) + random_p * np.log2(random_p/(1-random_q))
                else:
                    theo_dsks = 1 - random_q
            else:
                theo_dsks = 0
            
            # Теоретическая пропускная способность Z-канала
            if random_p != 0 and random_p != 1:
                p_power = random_p ** (random_p/(1-random_p))
                theo_z = np.log2(1 + (1-random_p) * p_power)
            else:
                theo_z = 1 if random_p == 0 else 0
            
            self.result_text.insert("end", f"- Теоретическая ДСК: {theo_dsk:.4f} бит/символ\n")
            self.result_text.insert("end", f"- Теоретическая ДСКС: {theo_dsks:.4f} бит/символ\n")
            self.result_text.insert("end", f"- Теоретическая Z-канал: {theo_z:.4f} бит/символ\n")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете пропускной способности: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def update_constraint_length(self):
        try:
            # Получаем новое значение длины ограничения
            new_constraint_length = int(self.constraint_entry.get())
            
            if new_constraint_length < 2:
                messagebox.showerror("Ошибка", "Длина ограничения должна быть не менее 2")
                return
            
            # Обновляем длину ограничения
            self.constraint_length = new_constraint_length
            
            # Создаем новые полиномы по умолчанию, полностью удаляя предыдущие
            self.generator_polynomials = []
            for i in range(self.num_polynomials):
                # Создаем полином по умолчанию с соответствующей длиной ограничения
                # Используем шаблон 1...1 (первый и последний бит = 1)
                default_poly = '1' + '0' * (self.constraint_length - 2) + '1'
                self.generator_polynomials.append(default_poly)
            
            # Обновляем сводку о полиномах
            self.update_polynomials_summary()
            
            # Очищаем текстовое поле для результатов
            self.result_text.delete("1.0", "end")
            
            # Обновляем информацию
            self.result_text.insert("1.0", "=== Обновление параметров сверточного кода ===\n")
            self.result_text.insert("end", f"Длина ограничения обновлена: {self.constraint_length}\n")
            self.result_text.insert("end", f"Все полиномы пересозданы под новую длину ограничения.\n")
            
            # Предложение эффективных полиномов для новой длины
            suggestions = self.get_polynomial_suggestions(self.constraint_length)
            if suggestions:
                self.result_text.insert("end", f"\nРекомендуемые полиномы для длины ограничения {self.constraint_length}:\n")
                for i, poly in enumerate(suggestions):
                    self.result_text.insert("end", f"- {poly}\n")
                
            # Выводим информацию о полиномах
            self.result_text.insert("end", "\nНовые полиномы генератора:\n")
            for i, poly in enumerate(self.generator_polynomials):
                self.result_text.insert("end", f"Полином {i+1}: {poly}\n")
            
            # Информация о влиянии длины ограничения на кодирование
            self.result_text.insert("end", f"\nВлияние длины ограничения на кодирование:\n")
            self.result_text.insert("end", f"- Более длинное ограничение увеличивает избыточность и помехоустойчивость кода\n")
            self.result_text.insert("end", f"- Более короткое ограничение снижает избыточность, но ухудшает помехоустойчивость\n")
            
            # Проверяем полиномы для безопасности
            self._validate_polynomials()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Длина ограничения должна быть целым числом")
    
    def _validate_polynomials(self):
        """Проверяет и исправляет полиномы, если их длина не соответствует constraint_length"""
        valid_polynomials = []
        has_changes = False

        # Если список полиномов пуст или меньше, чем num_polynomials, добавим недостающие
        while len(self.generator_polynomials) < self.num_polynomials:
            default_poly = '1' + '0' * (self.constraint_length - 2) + '1'
            self.generator_polynomials.append(default_poly)
            has_changes = True
        
        # Обрезаем лишние полиномы, если их больше, чем num_polynomials
        if len(self.generator_polynomials) > self.num_polynomials:
            self.generator_polynomials = self.generator_polynomials[:self.num_polynomials]
            has_changes = True

        for i, poly in enumerate(self.generator_polynomials):
            # Проверяем, не является ли полином в числовом формате (список индексов)
            if isinstance(poly, list):
                # Преобразуем числовой формат в двоичный
                binary_poly = self.numeric_poly_to_binary(poly, self.constraint_length)
                valid_polynomials.append(binary_poly)
                has_changes = True
                continue
            
            # Проверяем длину полинома
            if len(poly) != self.constraint_length:
                # Создаем новый полином правильной длины
                new_poly = '1' + '0' * (self.constraint_length - 2) + '1'
                valid_polynomials.append(new_poly)
                has_changes = True
            # Проверяем состав полинома (только 0 и 1)
            elif not all(bit in '01' for bit in poly):
                # Заменяем недопустимые символы на 0
                new_poly = ''.join(['0' if bit not in '01' else bit for bit in poly])
                # Еще проверяем первый и последний бит
                if new_poly[0] != '1' or new_poly[-1] != '1':
                    new_poly = '1' + new_poly[1:-1] + '1'
                valid_polynomials.append(new_poly)
                has_changes = True
            # Проверяем, что первый и последний биты равны 1
            elif poly[0] != '1' or poly[-1] != '1':
                new_poly = '1' + poly[1:-1] + '1'
                valid_polynomials.append(new_poly)
                has_changes = True
            else:
                valid_polynomials.append(poly)
        
        # Обновляем список полиномов, если были изменения
        if has_changes:
            self.generator_polynomials = valid_polynomials
            self.update_polynomials_summary()
            return True
        
        return True  # Всегда возвращаем True, так как мы исправили все проблемы
    
    def toggle_poly_frame(self):
        """Сворачивает или разворачивает фрейм с полиномами"""
        if self.poly_expanded:
            self.poly_frame.pack_forget()
            self.toggle_poly_button.configure(text="Развернуть")
            self.poly_expanded = False
        else:
            self.poly_frame.pack(fill="x", padx=10, pady=(0, 10))
            self.toggle_poly_button.configure(text="Свернуть")
            self.poly_expanded = True
    
    def open_polynomials_window(self):
        """Открывает отдельное окно для редактирования полиномов"""
        # Создаем новое окно
        poly_window = ctk.CTkToplevel(self.parent)
        poly_window.title("Настройка полиномов генератора")
        poly_window.geometry("600x400")
        poly_window.grab_set()  # Делаем окно модальным
        
        # Заголовок
        header_frame = ctk.CTkFrame(poly_window)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        header_label = ctk.CTkLabel(header_frame, text=f"Полиномы генератора ({self.num_polynomials})", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(side="left", padx=10, pady=10)
        
        # Информационная строка
        info_text = f"Всего полиномов: {self.num_polynomials}, длина полинома: {self.constraint_length} бит"
        info_label = ctk.CTkLabel(poly_window, text=info_text, font=ctk.CTkFont(size=12))
        info_label.pack(fill="x", padx=10, pady=0, anchor="w")
        
        # Фрейм для полиномов с прокруткой
        poly_frame = ctk.CTkScrollableFrame(poly_window, height=250)
        poly_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Создаем поля ввода для полиномов
        poly_entries = []
        
        # Определяем оптимальное количество полиномов в строке
        polynomials_per_row = min(3, self.num_polynomials)
        
        # Создаем сетку для размещения полиномов
        row_frames = []
        
        # Создаем фреймы для каждой строки
        row_count = (self.num_polynomials + polynomials_per_row - 1) // polynomials_per_row
        for i in range(row_count):
            row_frame = ctk.CTkFrame(poly_frame)
            row_frame.pack(fill="x", padx=5, pady=5)
            row_frames.append(row_frame)
        
        # Заполняем строки полиномами
        for i in range(self.num_polynomials):
            row_index = i // polynomials_per_row
            col_index = i % polynomials_per_row
            
            # Создаем фрейм для полинома
            entry_frame = ctk.CTkFrame(row_frames[row_index])
            entry_frame.grid(row=0, column=col_index, padx=5, pady=5, sticky="w")
            
            # Метка
            label = ctk.CTkLabel(entry_frame, text=f"Полином {i+1}:", width=80)
            label.pack(side="left", padx=5)
            
            # Поле ввода
            entry = ctk.CTkEntry(entry_frame, width=150)
            entry.pack(side="left", padx=5)
            
            # Заполняем поле существующим значением
            if i < len(self.generator_polynomials):
                entry.insert(0, self.generator_polynomials[i])
            
            poly_entries.append(entry)
        
        # Фрейм для кнопок
        button_frame = ctk.CTkFrame(poly_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Кнопка для применения рекомендуемых полиномов
        if self.constraint_length <= 5:
            suggestions = self.get_polynomial_suggestions(self.constraint_length)
            if suggestions and len(suggestions) > 0:
                recommend_button = ctk.CTkButton(button_frame, text="Применить рекомендуемые",
                                              command=lambda: self._apply_recommended_to_entries(suggestions, poly_entries))
                recommend_button.pack(side="left", padx=10, pady=10)
        
        # Кнопка для применения одинаковых полиномов
        same_poly_button = ctk.CTkButton(button_frame, text="Одинаковые полиномы",
                                       command=lambda: self._apply_same_to_entries(poly_entries))
        same_poly_button.pack(side="left", padx=10, pady=10)
        
        # Кнопка информации
        info_button = ctk.CTkButton(button_frame, text="Информация о полиномах",
                                  command=self._show_polynomials_help)
        info_button.pack(side="left", padx=10, pady=10)
        
        # Кнопки OK и Отмена
        cancel_button = ctk.CTkButton(button_frame, text="Отмена",
                                    command=poly_window.destroy)
        cancel_button.pack(side="right", padx=10, pady=10)
        
        ok_button = ctk.CTkButton(button_frame, text="Применить",
                                command=lambda: self._apply_polynomials_from_window(poly_entries, poly_window))
        ok_button.pack(side="right", padx=10, pady=10)
        
    def _apply_recommended_to_entries(self, suggestions, entries):
        """Применяет рекомендуемые полиномы к полям ввода"""
        # Используем только необходимое количество полиномов
        recommended = suggestions[:self.num_polynomials]
        
        # Если рекомендаций меньше, чем нужно полиномов, дублируем их
        while len(recommended) < self.num_polynomials:
            recommended.append(suggestions[0])
        
        # Получаем числовое представление полиномов для отображения
        numeric_polys = []
        for poly in recommended:
            indices = [i for i, bit in enumerate(poly) if bit == '1']
            numeric_polys.append(indices)
        
        # Обновляем поля ввода
        for i, poly in enumerate(recommended):
            if i < len(entries):
                entries[i].delete(0, "end")
                # Показываем двоичный формат в полях ввода
                entries[i].insert(0, poly)

    def _apply_same_to_entries(self, entries):
        """Применяет одинаковый полином ко всем полям ввода"""
        if not entries or len(entries) == 0:
            return
            
        # Используем значение из первого поля ввода
        first_poly = entries[0].get()
        
        # Проверяем, в каком формате введен полином
        if ',' in first_poly:
            try:
                # Пробуем разобрать как список индексов
                indices = [int(idx.strip()) for idx in first_poly.split(',')]
                # Проверяем валидность индексов
                if any(idx < 0 or idx >= self.constraint_length for idx in indices):
                    messagebox.showerror("Ошибка", f"Индексы должны быть в диапазоне от 0 до {self.constraint_length-1}")
                    return
                
                # Создаем двоичный полином
                binary_poly = self.numeric_poly_to_binary(indices, self.constraint_length)
                
                # Применяем это значение ко всем полям
                for entry in entries:
                    entry.delete(0, "end")
                    entry.insert(0, binary_poly)
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат числовых индексов")
                return
        else:
            # Проверяем корректность двоичного полинома
            if len(first_poly) != self.constraint_length or not all(bit in '01' for bit in first_poly):
                messagebox.showerror("Ошибка", f"Полином должен состоять из {self.constraint_length} бит (0 или 1)")
                return
                
            # Применяем это значение ко всем полям
            for entry in entries:
                entry.delete(0, "end")
                entry.insert(0, first_poly)
    
    def _apply_polynomials_from_window(self, entries, window):
        """Применяет полиномы из отдельного окна"""
        # Собираем значения из полей ввода
        polynomials = []
        for entry in entries:
            poly_input = entry.get().strip()
            
            # Проверяем, является ли ввод числовым форматом (через запятую)
            if ',' in poly_input:
                try:
                    # Пробуем разобрать как список индексов
                    indices = [int(idx.strip()) for idx in poly_input.split(',')]
                    # Проверяем валидность индексов
                    if any(idx < 0 or idx >= self.constraint_length for idx in indices):
                        messagebox.showerror("Ошибка", f"Индексы должны быть в диапазоне от 0 до {self.constraint_length-1}")
                        return
                    
                    # Создаем двоичный полином из индексов
                    binary_poly = self.numeric_poly_to_binary(indices, self.constraint_length)
                    polynomials.append(binary_poly)
                except ValueError:
                    messagebox.showerror("Ошибка", "Некорректный формат числовых индексов")
                    return
            else:
                # Проверяем корректность двоичного полинома
                if len(poly_input) != self.constraint_length:
                    messagebox.showerror("Ошибка", f"Длина полиномов должна соответствовать длине ограничения ({self.constraint_length})")
                    return
                
                if not all(bit in '01' for bit in poly_input):
                    messagebox.showerror("Ошибка", "Полиномы должны быть записаны в двоичном виде (только 0 и 1)")
                    return
                
                polynomials.append(poly_input)
        
        # Обновляем список полиномов
        self.generator_polynomials = polynomials
        
        # Закрываем окно
        window.destroy()
        
        # Обновляем информацию в основном окне
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Полиномы генератора обновлены:\n")
        
        # Выводим полиномы в двух форматах (двоичном и числовом)
        numeric_polys = self.binary_polys_to_numeric()
        for i, poly in enumerate(self.generator_polynomials):
            self.result_text.insert("end", f"Полином {i+1}: {poly} (двоичный) / {numeric_polys[i]} (индексы)\n")
        
        # Обновляем метку с количеством полиномов и сводку полиномов
        self.poly_label.configure(text=f"Полиномы генератора ({self.num_polynomials}):")
        self.update_polynomials_summary()
    
    def update_polynomials_summary(self):
        """Обновляет текстовое поле с информацией о текущих полиномах"""
        self.poly_summary.delete("1.0", "end")
        
        # Получаем числовое представление полиномов
        numeric_polys = self.binary_polys_to_numeric()
        
        # Добавляем информацию о полиномах
        for i, poly in enumerate(self.generator_polynomials):
            self.poly_summary.insert("end", f"{poly}\n")
            
    def _apply_polynomial_changes(self):
        """Применяет изменения полиномов из текстового поля"""
        try:
            # Получаем текст из поля
            text = self.poly_summary.get("1.0", "end").strip()
            polynomials = [p.strip() for p in text.split('\n') if p.strip()]
            
            # Проверяем количество полиномов
            if len(polynomials) != self.num_polynomials:
                messagebox.showerror("Ошибка", f"Количество полиномов должно быть равно {self.num_polynomials}")
                self.update_polynomials_summary()
                return
            
            # Проверяем каждый полином
            for i, poly in enumerate(polynomials):
                # Проверяем длину
                if len(poly) != self.constraint_length:
                    messagebox.showerror("Ошибка", 
                                       f"Длина полинома {i+1} должна быть равна {self.constraint_length}")
                    self.update_polynomials_summary()
                    return
                
                # Проверяем, что полином состоит только из 0 и 1
                if not all(bit in '01' for bit in poly):
                    messagebox.showerror("Ошибка", 
                                       f"Полином {i+1} должен состоять только из 0 и 1")
                    self.update_polynomials_summary()
                    return
            
            # Если все проверки пройдены, обновляем полиномы
            self.generator_polynomials = polynomials
            
            # Выводим информацию об обновлении
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", "Полиномы генератора обновлены:\n")
            
            # Выводим полиномы в двух форматах (двоичном и числовом)
            numeric_polys = self.binary_polys_to_numeric()
            for i, poly in enumerate(self.generator_polynomials):
                self.result_text.insert("end", f"Полином {i+1}: {poly} (двоичный) / {numeric_polys[i]} (индексы)\n")
            
            messagebox.showinfo("Успех", "Полиномы успешно обновлены")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обновлении полиномов: {str(e)}")
            self.update_polynomials_summary()