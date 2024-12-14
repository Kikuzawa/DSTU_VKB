def Trisemus_rus(text, key, flag):
    try:
        def generate_trisemus_matrix(keyword):
            # Удаление повторяющихся символов из ключевого слова
            keyword = list(''.join(sorted(set(keyword), key=keyword.index)))

            alphabet = [chr(ord('А') + i) for i in range(32) if chr(ord('А') + i) not in keyword]

            # Формирование матрицы
            first_row = keyword + alphabet[:8 - len(keyword)]
            k = len(alphabet[:8 - len(keyword)])
            alphabet = alphabet[k:]
            matrix = [first_row]
            for i in range(0, 3):
                matrix.append(alphabet[i * 8: (i + 1) * 8])

            return matrix

        def trisemus_encrypt(message, matrix):
            # Шифрование сообщения с использованием шифра Трисемуса
            result = ""
            for char in message:
                for row in matrix:
                    if char in row:
                        index_char = row.index(char)
                        index_row = matrix.index(row)
                        result += matrix[(index_row + 1) % 4][index_char]
                        break
                else:
                    # Если символ не найден в матрице, добавляем его как есть
                    result += char

            return result

        def trisemus_decrypt(message, matrix):
            # Дешифрование сообщения с использованием шифра Трисемуса
            result = ""
            for char in message:
                for row in matrix:
                    if char in row:
                        index_char = row.index(char)
                        index_row = matrix.index(row)
                        result += matrix[(index_row - 1) % 4][index_char]
                        break
                else:
                    # Если символ не найден в матрице, добавляем его как есть
                    result += char

            return result

        # Пример использования
        keyword = key.upper()
        message = text.upper()
        matrix = generate_trisemus_matrix(keyword)

        encrypted_message = trisemus_encrypt(message, matrix)
        decrypted_message = trisemus_decrypt(message, matrix)

        match flag:
            case 0:
                return str(encrypted_message)
            case 1:
                return str(decrypted_message)
    except:
        return "Ошибка :("

def Trisemus_eng(text, key, flag):
    try:
        def generate_trisemus_matrix(keyword):
            # Удаление повторяющихся символов из ключевого слова
            keyword = list(''.join(sorted(set(keyword), key=keyword.index)))

            alphabet = [chr(ord('A') + i) for i in range(26) if chr(ord('A') + i) not in keyword]
            alphabet.append('-')
            # Формирование матрицы
            first_row = keyword + alphabet[:9 - len(keyword)]
            k = len(alphabet[:9 - len(keyword)])
            alphabet = alphabet[k:]
            matrix = [first_row]
            for i in range(0, 2):
                matrix.append(alphabet[i * 9: (i + 1) * 9])

            return matrix

        def trisemus_encrypt(message, matrix):
            # Шифрование сообщения с использованием шифра Трисемуса
            result = ""
            for char in message:
                for row in matrix:
                    if char in row:
                        index_char = row.index(char)
                        index_row = matrix.index(row)
                        result += matrix[(index_row + 1) % 3][index_char]
                        break
                else:
                    # Если символ не найден в матрице, добавляем его как есть
                    result += char

            return result

        def trisemus_decrypt(message, matrix):
            # Дешифрование сообщения с использованием шифра Трисемуса
            result = ""
            for char in message:
                for row in matrix:
                    if char in row:
                        index_char = row.index(char)
                        index_row = matrix.index(row)
                        result += matrix[(index_row - 1) % 3][index_char]
                        break
                else:
                    # Если символ не найден в матрице, добавляем его как есть
                    result += char

            return result

        # Пример использования
        keyword = key.upper()
        message = text.upper()
        matrix = generate_trisemus_matrix(keyword)

        encrypted_message = trisemus_encrypt(message, matrix)
        decrypted_message = trisemus_decrypt(message, matrix)

        match flag:
            case 0:
                return str(encrypted_message)
            case 1:
                return str(decrypted_message)
    except:
        return "Ошибка :("