def text_to_binary(text):
    """
    Преобразует текст в двоичную строку с поддержкой UTF-8
    """
    if not text:
        return ""
    
    try:
        # Преобразуем текст в байты UTF-8
        binary = ''
        # Кодируем текст в UTF-8 и получаем байты
        for byte in text.encode('utf-8'):
            # Форматируем каждый байт в 8-битное двоичное представление
            binary_byte = format(byte, '08b')
            binary += binary_byte
        return binary
    except Exception as e:
        print(f"Ошибка при преобразовании текста в бинарный код: {e}")
        return ""

def binary_to_text(binary):
    """
    Преобразует двоичную строку в текст с поддержкой UTF-8
    """
    if not binary:
        return ""
    
    # Удаляем пробелы и другие невидимые символы
    binary = ''.join(binary.split())
    
    # Проверяем, что строка содержит только 0 и 1
    if not all(bit in '01' for bit in binary):
        binary = ''.join(bit for bit in binary if bit in '01')
    
    # Проверяем, что длина бинарной строки кратна 8
    if len(binary) % 8 != 0:
        # Дополняем нулями до кратности 8
        padding = 8 - (len(binary) % 8)
        binary += '0' * padding
    
    try:
        # Преобразуем бинарную строку в байты
        bytes_array = bytearray()
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            byte_value = int(byte, 2)
            bytes_array.append(byte_value)
        
        # Декодируем байты как UTF-8
        text = bytes_array.decode('utf-8', errors='replace')
        return text
    except Exception as e:
        print(f"Ошибка при преобразовании бинарного кода в текст: {e}")
        return "" 