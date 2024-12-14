def verification_ABC(ABC):
    try:
        text = str(input('Введите текст: '))
    except ValueError:
        print('Ошибка: Введены недопустимые символы')
        return verification_ABC(ABC)
    for i in text:
        if i not in ABC:
            print('Ошибка: Введены недопустимые символы')
            return verification_ABC(ABC)
    return text

def verification_Mode():
    try:
        mode = str(input('Выберите режим: [E]ncrypt|[D]ecrypt: ').upper())
    except ValueError:
        print('Ошибка, неправильный ввод!')
        return verification_Mode()
    if mode not in ['E', 'D', 'e', 'd','Encrypt','encrypt','ENCRYPT','Decrypt','decrypt','DECRYPT','[D]','[d]','[E]','[e]']:
        print('Ошибка, неправильный ввод!');
        return verification_Mode()
    return mode

def verification_Main():
    try:
        num = int(input('Введите номер [0-2]: '))
    except ValueError:
        print('Ошибка: неправильный ввод!')
        return verification_Main()
    if num not in [0, 1, 2]:
        print('Ошибка: неправильный ввод!')
        return verification_Main()
    else:
        return num