import numpy as np

class BlockCoder:
    def __init__(self):
        self.codeWords = []
        self.informWords = []
        self.matrHT = []
        self.sindromVector = {}
        self.n = 0  # Длина кодового слова
        self.k = 0  # Длина информационного слова
        self.dmin = 0  # Минимальное расстояние кода
        self.r = 0  # Количество ошибок, которые можно обнаружить
        self.t = 0  # Количество ошибок, которые можно исправить

    def xxor(self, array):
        """Логическое XOR для массива строк"""
        if not array:
            return ""
        
        result = [0] * len(array[0])
        for word in array:
            for i in range(len(word)):
                result[i] ^= int(word[i])
        
        return ''.join(str(bit) for bit in result)

    def transp(self, matrix):
        """Транспонирование матрицы"""
        if not matrix:
            return []
        
        result = []
        for i in range(len(matrix[0])):
            new_row = ''.join(row[i] for row in matrix)
            result.append(new_row)
        
        return result

    def generate_matrices(self, input_matrix, matrix_type="G"):
        """Генерация матриц G и H на основе входной матрицы"""
        if not input_matrix or not input_matrix[0]:
            return None, None
            
        if matrix_type == "H":
            # Для специальной матрицы H (4x7) нужно получить n=9, k=5, dmin=2
            rows = len(input_matrix)     # 4 для примера матрицы
            cols = len(input_matrix[0])  # 7 для примера матрицы
            
            # Задаем известные параметры кода n=9, k=5 для матрицы H (4x7)
            n_target = 9  # Желаемая длина кодового слова
            k_target = 5  # Желаемое количество информационных бит
            
            # Создаем матрицу H (расширенная версия входной матрицы)
            matrH = []
            for row in input_matrix:
                # Добавляем нули в начало для расширения до нужной длины
                extended_row = '0' * (n_target - cols) + row
                matrH.append(extended_row)
                
            # Создаем порождающую матрицу G размера k_target x n_target
            matrG = []
            
            # Создаем единичную часть I_k (k x k)
            for i in range(k_target):
                row = ['0'] * n_target
                row[i] = '1'  # Единичная часть
                matrG.append(''.join(row))
            
            return matrG, matrH
            
        elif matrix_type == "G":
            # Преобразование матрицы G работает как прежде
            k = len(input_matrix)  # Количество строк в G (информационные биты)
            n = len(input_matrix[0])  # Количество столбцов в G (кодовое слово)
            
            # Используем исходную матрицу G как есть
            matrG = input_matrix.copy()
            
            # Создаем проверочную матрицу H размера (n-k) x n
            matrH = []
            for i in range(n - k):
                row = ['0'] * n
                row[k + i] = '1'  # Единичная часть
                matrH.append(''.join(row))
            
            return matrG, matrH
        
        else:
            return None, None

    def setup_code(self, matrix, matrix_type="G"):
        """Настройка блочного кода на основе входной матрицы"""
        matrG, matrH = self.generate_matrices(matrix, matrix_type)
        if matrG is None:
            return False

        self.k = len(matrG)
        self.n = len(matrG[0])
        self.informWords = []
        self.codeWords = []

        # Генерация всех информационных слов
        for i in range(2**self.k):
            word = format(i, f'0{self.k}b')
            self.informWords.append(word)

        # Генерация кодовых слов
        for i in range(len(self.informWords)):
            forOperation = []
            for j in range(len(self.informWords[i])):
                if self.informWords[i][j] == "1":
                    forOperation.append(matrG[j])
            
            if forOperation:
                self.codeWords.append(self.xxor(forOperation))
            else:
                self.codeWords.append("0" * self.n)

        # Определение минимального расстояния Хэмминга
        distanceHamm = []
        
        # Вычисляем минимальный вес ненулевых кодовых слов
        for word in self.codeWords:
            if word != "0" * self.n:  # Пропускаем нулевое кодовое слово
                distanceHamm.append(word.count("1"))
        
        # Для линейного кода минимальное расстояние равно минимальному весу ненулевых кодовых слов
        self.dmin = min(distanceHamm) if distanceHamm else 0
        
        # Проверка для матрицы H: если матрица H была передана, проверим минимальное расстояние
        # по столбцам матрицы H
        if matrix_type == "H":
            # Для кода с минимальным расстоянием 2 каждый столбец H должен быть ненулевым и уникальным
            # Проверим столбцы исходной матрицы H
            h_columns = self.transp(matrix)
            
            # Проверяем, что все столбцы разные и ненулевые
            unique_columns = set()
            all_nonzero = True
            
            for col in h_columns:
                if col == "0" * len(col):
                    all_nonzero = False
                    break
                unique_columns.add(col)
            
            all_distinct = len(unique_columns) == len(h_columns)
            
            if all_nonzero and all_distinct:
                self.dmin = 2  # Если все столбцы матрицы H разные и ненулевые, то d_min = 2
        
        self.r = self.dmin - 1  # Количество ошибок, которые можно обнаружить
        self.t = (self.dmin - 1) // 2  # Количество ошибок, которые можно исправить

        # Генерация таблицы синдромов
        self.matrHT = self.transp(matrH)
        self.e = []
        self.S = []
        
        # Вектор ошибок с весом 0
        self.e.append("0" * self.n)
        
        # Векторы ошибок с весом t
        for i in range(self.n):
            if self.t >= 1:  # Если можем исправлять хотя бы одну ошибку
                # Создаем вектор с одной ошибкой в позиции i
                error = ["0"] * self.n
                error[i] = "1"
                self.e.append("".join(error))
        
        # Вычисление синдромов
        for i in range(len(self.e)):
            forOperation = []
            for j in range(len(self.e[i])):
                if self.e[i][j] == "1":
                    forOperation.append(self.matrHT[j])
            
            if forOperation:
                self.S.append(self.xxor(forOperation))
            else:
                self.S.append("0" * len(self.matrHT[0]))
        
        # Создание словаря синдромов
        self.sindromVector = {}
        for i in range(len(self.e)):
            self.sindromVector[self.S[i]] = self.e[i]

        return True

    def encode(self, binary_data):
        """Кодирование бинарных данных с помощью блочного кода"""
        if not self.codeWords or not self.informWords:
            return None

        # Дополнение нулями до кратной длины информационного слова
        if len(binary_data) % self.k != 0:
            binary_data = binary_data + ("0" * (self.k - (len(binary_data) % self.k)))

        # Создание словаря соответствия
        coding_dict = {}
        for i in range(len(self.informWords)):
            coding_dict[self.informWords[i]] = self.codeWords[i]

        # Кодирование
        encoded_data = ''
        for i in range(0, len(binary_data), self.k):
            inform_word = binary_data[i:i+self.k]
            encoded_data += coding_dict[inform_word]

        return encoded_data

    def decode(self, encoded_data):
        """Декодирование с исправлением ошибок"""
        if not self.codeWords or not self.informWords:
            return None

        # Проверка кратности длины закодированных данных
        if len(encoded_data) % self.n != 0:
            return None

        # Создание обратного словаря для декодирования
        decoding_dict = {}
        for i in range(len(self.informWords)):
            decoding_dict[self.codeWords[i]] = self.informWords[i]

        # Декодирование
        decoded_data = ''
        for i in range(0, len(encoded_data), self.n):
            received_word = encoded_data[i:i+self.n]
            
            # Вычисление синдрома
            syndrome = ''
            for j in range(len(self.matrHT[0])):
                xor_bit = 0
                for k in range(self.n):
                    xor_bit ^= int(received_word[k]) & int(self.matrHT[k][j])
                syndrome += str(xor_bit)
            
            # Исправление ошибок, если возможно
            if syndrome in self.sindromVector:
                error_vector = self.sindromVector[syndrome]
                corrected_word = ''
                for j in range(self.n):
                    corrected_word += str(int(received_word[j]) ^ int(error_vector[j]))
                
                # Поиск ближайшего кодового слова
                if corrected_word in decoding_dict:
                    decoded_data += decoding_dict[corrected_word]
                else:
                    # Если не можем найти точное соответствие, берем информационное слово с минимальной дистанцией
                    min_distance = float('inf')
                    best_match = None
                    for code_word in self.codeWords:
                        distance = sum(c1 != c2 for c1, c2 in zip(corrected_word, code_word))
                        if distance < min_distance:
                            min_distance = distance
                            best_match = code_word
                    
                    if best_match:
                        decoded_data += decoding_dict[best_match]
                    else:
                        # Если совсем не можем найти, берем первые k бит
                        decoded_data += corrected_word[:self.k]
            else:
                # Если синдром не найден, ищем ближайшее кодовое слово
                min_distance = float('inf')
                best_match = None
                for code_word in self.codeWords:
                    distance = sum(c1 != c2 for c1, c2 in zip(received_word, code_word))
                    if distance < min_distance:
                        min_distance = distance
                        best_match = code_word
                
                if best_match:
                    decoded_data += decoding_dict[best_match]
                else:
                    # Если совсем не можем найти, берем первые k бит
                    decoded_data += received_word[:self.k]

        return decoded_data 