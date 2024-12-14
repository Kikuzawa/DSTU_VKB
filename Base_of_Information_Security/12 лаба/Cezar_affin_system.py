def cezar_affine_system_rus(key, plaintext, flag):
    try:
        def encrypt_affine(text, key_a, key_b):
            encrypted_text = ''
            alphabet_up = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            alphabet_low = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            for char in text:
                if char in alphabet_up:
                    char_index = alphabet_up.index(char)
                    encrypted_index = (char_index * key_a + key_b) % len(alphabet_up)
                    encrypted_text += alphabet_up[encrypted_index]
                elif char in alphabet_low:
                    char_index = alphabet_low.index(char)
                    encrypted_index = (char_index * key_a + key_b) % len(alphabet_low)
                    encrypted_text += alphabet_low[encrypted_index]
                else:
                    encrypted_text += char
            return encrypted_text

        # Функция для дешифрования текста аффинной системой подстановок Цезаря
        def decrypt_affine(text, key_a, key_b):
            decrypted_text = ''
            alphabet_up = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            alphabet_low = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            # Находим мультипликативное обратное для ключа key_a
            for i in range(len(alphabet_up)):
                if (key_a * i) % len(alphabet_up) == 1:
                    multiplicative_inverse = i
                    break
            else:
                return "Невозможно расшифровать. Некорректный ключ."

            for char in text:
                if char in alphabet_up:
                    char_index = alphabet_up.index(char)
                    decrypted_index = (multiplicative_inverse * (char_index - key_b)) % len(alphabet_up)
                    decrypted_text += alphabet_up[decrypted_index]
                elif char in alphabet_low:
                    char_index = alphabet_low.index(char)
                    decrypted_index = (multiplicative_inverse * (char_index - key_b)) % len(alphabet_low)
                    decrypted_text += alphabet_low[decrypted_index]
                else:
                    decrypted_text += char
            return decrypted_text

        key_a, key_b = map(int, key.split())

        match flag:
            case 0:
                return encrypt_affine(plaintext, key_a, key_b)
            case 1:
                return decrypt_affine(plaintext, key_a, key_b)
    except:
        return ("Ошибка :(\n"
                "Введите два числа (ключа) через пробел")
def cezar_affine_system_eng(key, plaintext, flag):
    try:
        def encrypt_affine(text, key_a, key_b):
            encrypted_text = ''
            alphabet_up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            alphabet_low = 'abcdefghijklmnopqrstuvwxyz'
            for char in text:
                if char in alphabet_up:
                    char_index = alphabet_up.index(char)
                    encrypted_index = (char_index * key_a + key_b) % len(alphabet_up)
                    encrypted_text += alphabet_up[encrypted_index]
                elif char in alphabet_low:
                    char_index = alphabet_low.index(char)
                    encrypted_index = (char_index * key_a + key_b) % len(alphabet_low)
                    encrypted_text += alphabet_low[encrypted_index]
                else:
                    encrypted_text += char
            return encrypted_text

        # Функция для дешифрования текста аффинной системой подстановок Цезаря
        def decrypt_affine(text, key_a, key_b):
            decrypted_text = ''
            alphabet_up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            alphabet_low = 'abcdefghijklmnopqrstuvwxyz'
            # Находим мультипликативное обратное для ключа key_a
            for i in range(len(alphabet_up)):
                if (key_a * i) % len(alphabet_up) == 1:
                    multiplicative_inverse = i
                    break
            else:
                return "Невозможно расшифровать. Некорректный ключ."

            for char in text:
                if char in alphabet_up:
                    char_index = alphabet_up.index(char)
                    decrypted_index = (multiplicative_inverse * (char_index - key_b)) % len(alphabet_up)
                    decrypted_text += alphabet_up[decrypted_index]
                elif char in alphabet_low:
                    char_index = alphabet_low.index(char)
                    decrypted_index = (multiplicative_inverse * (char_index - key_b)) % len(alphabet_low)
                    decrypted_text += alphabet_low[decrypted_index]
                else:
                    decrypted_text += char
            return decrypted_text

        key_a, key_b = map(int, key.split())

        match flag:
            case 0:
                return encrypt_affine(plaintext, key_a, key_b)
            case 1:
                return decrypt_affine(plaintext, key_a, key_b)
    except:
        return ("Ошибка :(\n"
                "Введите два числа (ключа) через пробел")
