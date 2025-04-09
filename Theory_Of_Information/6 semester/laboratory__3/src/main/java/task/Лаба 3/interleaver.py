import numpy as np

class BlockInterleaver:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        
    def set_dimensions(self, rows, cols):
        """Установка размеров перемежителя"""
        self.rows = rows
        self.cols = cols
        
    def interleave(self, binary_data):
        """Перемежение двоичных данных"""
        # Проверяем, что длина данных не превышает размер перемежителя
        if len(binary_data) > self.rows * self.cols:
            raise ValueError(f"Длина данных ({len(binary_data)}) превышает размер перемежителя ({self.rows * self.cols})")
            
        # Дополняем данные нулями, если нужно
        padded_data = binary_data
        padding_needed = self.rows * self.cols - len(binary_data)
        if padding_needed > 0:
            padded_data = binary_data + '0' * padding_needed
            
        # Заполняем матрицу перемежителя по строкам
        matrix = []
        for i in range(self.rows):
            row = padded_data[i * self.cols: (i + 1) * self.cols]
            matrix.append(row)
            
        # Считываем по столбцам
        interleaved_data = ''
        for j in range(self.cols):
            for i in range(self.rows):
                if j < len(matrix[i]):
                    interleaved_data += matrix[i][j]
                    
        return interleaved_data
        
    def deinterleave(self, interleaved_data):
        """Деперемежение двоичных данных"""
        # Проверяем, что длина данных соответствует размеру перемежителя
        expected_length = self.rows * self.cols
        if len(interleaved_data) != expected_length:
            raise ValueError(f"Длина данных ({len(interleaved_data)}) не соответствует размеру перемежителя ({expected_length})")
            
        # Заполняем матрицу перемежителя по столбцам
        matrix = [['0' for _ in range(self.cols)] for _ in range(self.rows)]
        idx = 0
        for j in range(self.cols):
            for i in range(self.rows):
                if idx < len(interleaved_data):
                    matrix[i][j] = interleaved_data[idx]
                    idx += 1
                    
        # Считываем по строкам
        deinterleaved_data = ''
        for i in range(self.rows):
            for j in range(self.cols):
                deinterleaved_data += matrix[i][j]
                
        return deinterleaved_data
        
    def calculate_dimensions(self, data_length):
        """Расчет оптимальных размеров перемежителя для заданной длины данных"""
        # Находим ближайший квадрат
        square_size = int(np.ceil(np.sqrt(data_length)))
        
        # Варианты размеров
        dims = []
        for rows in range(1, square_size * 2):
            cols = int(np.ceil(data_length / rows))
            dims.append((rows, cols, rows * cols - data_length))
            
        # Выбираем вариант с минимальным необходимым дополнением
        dims.sort(key=lambda x: x[2])
        best_rows, best_cols, _ = dims[0]
        
        return best_rows, best_cols 