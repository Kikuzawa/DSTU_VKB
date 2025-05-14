import customtkinter as ctk
import numpy as np
import random
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from coding_block_window import CodingBlock
from coding_convolutional_window import CodingConvolutional

# Настройка темы и стиля приложения
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class ChannelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройка основного окна
        self.title("Канал связи - Лабораторная работа")
        self.geometry("1500x1000")
        self.minsize(800, 600)  # Минимальный размер окна
        
        # Настройка масштабирования сетки
        self.grid_rowconfigure(0, weight=1)  # Основной контент растягивается
        self.grid_rowconfigure(1, weight=0)  # Нижнее меню фиксированной высоты
        self.grid_columnconfigure(0, weight=1)
        
        # Установка цветов
        self.bg_color = "#f0f0f0"
        self.sidebar_color = "#e0e0e0"
        self.accent_color = "#2d9a3e"
        self.text_color = "#1a1a1a"
        self.configure(fg_color=self.bg_color)
        
        # Создание переменных для хранения данных
        self.input_text = ""
        self.encoded_text = ""
        self.noisy_text = ""
        self.decoded_text = ""
        
        # Создание основного фрейма для контента
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
        
        # Создание основных фреймов
        self.create_main_frame()
        self.create_bottom_menu()
        
        # Создание модулей для работы с кодами
        self.block_code_module = CodingBlock(self)
        self.convolutional_code_module = CodingConvolutional(self)
        
        # Показать стартовую страницу
        self.show_module("block_code")
    
    def create_bottom_menu(self):
        # Создание нижней панели меню
        self.bottom_menu = ctk.CTkFrame(self, height=40, fg_color=self.sidebar_color)
        self.bottom_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Настройка масштабирования
        self.bottom_menu.grid_columnconfigure(0, weight=1)  # Для информации
        self.bottom_menu.grid_columnconfigure(1, weight=0)  # Для кнопок
        self.bottom_menu.grid_columnconfigure(2, weight=1)  # Для версии
        
        # Информация о работе (слева)
        self.info_label = ctk.CTkLabel(self.bottom_menu,
                                     text="Лабораторная работа 5 - Theory Information",
                                     font=ctk.CTkFont(size=12),
                                     text_color=self.text_color)
        self.info_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        # Кнопки переключения модулей (по центру)
        buttons_frame = ctk.CTkFrame(self.bottom_menu, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, padx=20, pady=5)
        
        self.block_code_button = ctk.CTkButton(buttons_frame,
                                             text="Блочные коды",
                                             command=lambda: self.show_module("block_code"),
                                             height=28,
                                             width=120,
                                             font=ctk.CTkFont(size=12),
                                             fg_color=self.accent_color,
                                             hover_color="#1f7a2f")
        self.block_code_button.pack(side="left", padx=5)
        
        self.conv_code_button = ctk.CTkButton(buttons_frame,
                                            text="Сверточные коды",
                                            command=lambda: self.show_module("convolutional_code"),
                                            height=28,
                                            width=120,
                                            font=ctk.CTkFont(size=12),
                                            fg_color=self.accent_color,
                                            hover_color="#1f7a2f")
        self.conv_code_button.pack(side="left", padx=5)
        
        # Версия программы (справа)
        version_label = ctk.CTkLabel(self.bottom_menu,
                                   text="kikuzawa",
                                   font=ctk.CTkFont(size=12),
                                   text_color="#666666")
        version_label.grid(row=0, column=2, padx=20, pady=5, sticky="e")
    
    def create_main_frame(self):
        # Основной фрейм для содержимого
        self.main_frame = ctk.CTkFrame(self.main_content, corner_radius=15, fg_color="#222222")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def show_module(self, module_name):
        # Очистка основного фрейма
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Подсветка активной кнопки
        self.block_code_button.configure(fg_color=self.accent_color if module_name == "block_code" else "#555555")
        self.conv_code_button.configure(fg_color=self.accent_color if module_name == "convolutional_code" else "#555555")
        
        # Отображение выбранного модуля
        if module_name == "block_code":
            self.block_code_module.create_widgets(self.main_frame)
        elif module_name == "convolutional_code":
            self.convolutional_code_module.create_widgets(self.main_frame)

    def load_text_from_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
        return None

if __name__ == "__main__":
    app = ChannelApp()
    app.mainloop() 