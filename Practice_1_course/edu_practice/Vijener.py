from itertools import cycle
from verification import *
import string

def Vijener():
    ABC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + string.ascii_letters + string.digits \
          + string.punctuation + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + ' '

    def encode(text, key):
        FV = lambda arg: ABC[(ABC.index(arg[0])+ABC.index(arg[1]) % len(ABC)) % len(ABC)]
        return ''.join(map(FV, zip(text, cycle(key))))

    def decode(encode_text, key):
        FV = lambda arg: ABC[ABC.index(arg[0])-ABC.index(arg[1]) % len(ABC)]
        return ''.join(map(FV, zip(encode_text, cycle(key))))

    Mode = verification_Mode()

    print('--Сообщение--')
    text = verification_ABC(ABC)

    print('--Ключ--')
    key = verification_ABC(ABC)

    if Mode in ['E','e']:
        print("Зашифрованный текст: {}".format(encode(text, key)))
    else:
        print("Расшифрованный текст: {}".format(decode(text, key)))