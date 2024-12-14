import string
from verification import *

def wheatstone():
    ABC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + string.ascii_letters + string.digits \
          + string.punctuation + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + ' '

    def create_square(key):
        key = key.lower().replace(' ', '')
        square = []
        for letter in key:
            if letter not in square and letter in ABC:
                square.append(letter)
        for letter in ABC:
            if letter not in square:
                square.append(letter)
        return square

    def encode(plaintext, key1, key2):
        square1 = create_square(key1)
        square2 = create_square(key2)
        ciphertext = ''
        plaintext = plaintext.lower().replace(' ', '').replace('\n', '')
        if len(plaintext) % 2 == 1:
            plaintext += ' '
        for i in range(0, len(plaintext), 2):
            pair = plaintext[i:i+2]
            row1, col1 = divmod(square1.index(pair[0]), 8)
            row2, col2 = divmod(square2.index(pair[1]), 8)
            try:
                ciphertext += square1[row2*8+col1] + square2[row1*8+col2]
            except IndexError:
                pass
        return ciphertext

    def decode(ciphertext, key1, key2):
        square1 = create_square(key1)
        square2 = create_square(key2)
        plaintext = ''
        for i in range(0, len(ciphertext), 2):
            pair = ciphertext[i:i+2]
            row1, col1 = divmod(square1.index(pair[0]),8)
            row2, col2 = divmod(square2.index(pair[1]), 8)
            plaintext += square1[row2*8+col1] + square2[row1*8+col2]
        return plaintext

    print('--Первый ключ--')
    key1 = verification_ABC(ABC)

    print('--Второй ключ--')
    key2 = verification_ABC(ABC)

    print('--Сообщение--')
    plaintext = verification_ABC(ABC) + '.'

    ciphertext = encode(plaintext, key1, key2)
    decoded_plaintext = decode(ciphertext, key1, key2)

    print("Исходный текст:   ", plaintext)
    print("Зашифрованный текст:", ciphertext)
    print("Расшифрованный текст:  ", decoded_plaintext)

