import numpy as np
from PIL import Image
import random
import os

def load_image(file_path):
    """Загрузка изображения и преобразование в массив numpy"""
    try:
        img = Image.open(file_path).convert('RGB')
        return np.array(img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {str(e)}")
        return None

def save_image(img_array, file_path):
    """Сохранение массива numpy как изображения"""
    try:
        img = Image.fromarray(img_array.astype(np.uint8))
        img.save(file_path)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {str(e)}")
        return False

def int_to_binary(n, bits=8):
    """Преобразование целого числа в двоичную строку заданной длины"""
    return format(n, f'0{bits}b')

def binary_to_int(binary_str):
    """Преобразование двоичной строки в целое число"""
    return int(binary_str, 2)

def pixel_to_binary(pixel):
    """Преобразование одного пикселя (RGB) в двоичную строку"""
    return ''.join(int_to_binary(channel) for channel in pixel)

def binary_to_pixel(binary_str):
    """Преобразование двоичной строки в пиксель (RGB)"""
    if len(binary_str) != 24:  # RGB = 3 канала по 8 бит
        raise ValueError("Длина двоичной строки должна быть 24 бита для RGB пикселя")
    
    r = binary_to_int(binary_str[0:8])
    g = binary_to_int(binary_str[8:16])
    b = binary_to_int(binary_str[16:24])
    
    return np.array([r, g, b], dtype=np.uint8)

def introduce_errors(binary_str, error_rate):
    """Внесение случайных ошибок в двоичную строку с заданной вероятностью"""
    result = list(binary_str)
    for i in range(len(result)):
        if random.random() < error_rate:
            result[i] = '1' if result[i] == '0' else '0'
    return ''.join(result)

def image_to_binary(img_array):
    """Преобразование массива изображения в двоичную строку"""
    binary_rows = []
    for row in img_array:
        binary_row = ''
        for pixel in row:
            binary_row += pixel_to_binary(pixel)
        binary_rows.append(binary_row)
    return binary_rows

def binary_to_image(binary_rows, height, width):
    """Преобразование списка двоичных строк обратно в массив изображения"""
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    for i, binary_row in enumerate(binary_rows):
        if i >= height:
            break
        pixels_in_row = len(binary_row) // 24
        
        for j in range(min(pixels_in_row, width)):
            pixel_binary = binary_row[j*24:(j+1)*24]
            img_array[i, j] = binary_to_pixel(pixel_binary)
    
    return img_array

def save_intermediate_data(data, filename):
    """Сохранение промежуточных данных в текстовый файл"""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(str(data) + '\n')
        return True
    except Exception as e:
        print(f"Ошибка при сохранении данных: {str(e)}")
        return False

def clear_intermediate_data(filename):
    """Очистка файла с промежуточными данными"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("")
        return True
    except Exception as e:
        print(f"Ошибка при очистке файла: {str(e)}")
        return False

def introduce_errors_per_pixel(binary_str, error_rate, bits_per_pixel=24):
    """Внесение случайных ошибок в двоичную строку на уровне пикселей
    
    Обрабатывает каждый пиксель (группу из bits_per_pixel бит) отдельно,
    гарантируя, что в каждом пикселе будут внесены ошибки с заданной вероятностью.
    
    Args:
        binary_str: Двоичная строка
        error_rate: Вероятность ошибки для каждого пикселя (0.0 - 1.0)
        bits_per_pixel: Количество бит на пиксель (по умолчанию 24 для RGB)
        
    Returns:
        Двоичная строка с внесенными ошибками
    """
    result = list(binary_str)
    pixel_count = len(binary_str) // bits_per_pixel
    
    for i in range(pixel_count):
        # Для каждого пикселя решаем, вносить ли ошибку
        if random.random() < error_rate:
            # Выбираем случайный бит в пределах пикселя
            bit_pos = i * bits_per_pixel + random.randint(0, bits_per_pixel - 1)
            # Инвертируем бит
            if bit_pos < len(result):
                result[bit_pos] = '1' if result[bit_pos] == '0' else '0'
    
    return ''.join(result) 