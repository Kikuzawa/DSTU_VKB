from typing import List, AnyStr

def decrypt_message(encrypted_message):
    """
    Расшифровывает сообщение, которое было зашифровано методом Шпиона Коли.
    Метод шифрования: сначала идут символы с чётными индексами,
    затем символы с нечётными индексами.
    
    Например: "Привет!" -> "Пиветр!"
    
    Args:
        encrypted_message (AnyStr): Зашифрованное сообщение
        
    Returns:
        str: Расшифрованное исходное сообщение
    """
    # Преобразуем строку в список символов для возможности изменения элементов
    symbols: List[AnyStr] = list(encrypted_message)
    
    # Находим середину строки - это длина первой части зашифрованного сообщения
    n: int = len(encrypted_message) // 2
    
    # Переставляем символы на свои места
    # Для каждой пары символов:
    #   - первый символ пары берём из второй половины (encrypted_message[i + n])
    #   - второй символ пары берём из первой половины (encrypted_message[i])
    for i in range(n):
        symbols[2 * i: 2 * i + 2] = encrypted_message[i + n], encrypted_message[i]
    
    # Объединяем список символов обратно в строку
    return ''.join(symbols)

def main():
    """
    Главная функция программы.
    Читает зашифрованное сообщение и выводит его расшифрованную версию.
    """
    # Получаем зашифрованное сообщение от пользователя
    encrypted_message = input()
    
    # Расшифровываем сообщение
    decrypted_message: str = decrypt_message(encrypted_message)
    
    # Выводим результат
    print(decrypted_message)

# Запуск программы
main()