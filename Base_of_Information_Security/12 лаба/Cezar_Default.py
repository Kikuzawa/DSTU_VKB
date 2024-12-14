def cezar_default_eng(text, shift, flag):  # shiht - encode, -shift - decode
    try:
        if flag == 0:
            shift = int(shift)
        else:
            shift = -1 * int(shift)
        new_text = ""
        for char in text:
            if char.isalpha():
                shifted = ord(char) + shift
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                new_text += chr(shifted)
            else:
                new_text += char
        return str(new_text)
    except:
        return ("Ошибка :(\n"
                "Введите целое число (шаг)")

def cezar_default_rus(text, shift, flag):  # shiht - encode, -shift - decode
    try:
        if flag == 0:
            shift = int(shift)
        else:
            shift = -1 * int(shift)
        new_text = ""
        for char in text:
            if char.isalpha():
                shifted = ord(char) + shift
                if char.isupper():
                    if shifted < ord('А'):
                        shifted += 32
                    elif shifted > ord('Я'):
                        shifted -= 32
                elif char.islower():
                    if shifted < ord('а'):
                        shifted += 32
                    elif shifted > ord('я'):
                        shifted -= 32
                new_text += chr(shifted)
            else:
                new_text += char
        return str(new_text)
    except:
        return ("Ошибка :(\n"
                "Введите целое число (шаг)")
