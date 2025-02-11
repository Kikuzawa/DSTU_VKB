from typing import List


def fill_matrix(n: int, m: int) -> List[List[int]]:
    """
    Создает и заполняет двумерный массив (матрицу) размером n x m по диагоналям.

    :param n: Количество строк в матрице.
    :param m: Количество столбцов в матрице.
    :return: Заполненная матрица.
    """
    # Создаем пустую матрицу размером n x m, заполненную нулями
    matrix: List[List[int]] = [[0 for _ in range(m)] for _ in range(n)]
    # Счетчик для заполнения матрицы значениями
    count: int = 0

    # Перебираем все диагонали матрицы
    for index_of_diagonal in range(n + m - 1):
        # Определяем начальную точку для заполнения текущей диагонали
        start_col: int
        start_row: int

        if index_of_diagonal < m:
            # Если диагональ начинается в верхней строке
            start_col = index_of_diagonal
            start_row = 0
        else:
            # Если диагональ начинается в последнем столбце
            start_col = m - 1
            start_row = index_of_diagonal - m + 1

        # Заполняем текущую диагональ
        while start_col >= 0 and start_row < n:
            matrix[start_row][start_col] = count
            count += 1
            start_col -= 1  # Двигаемся влево по столбцам
            start_row += 1  # Двигаемся вниз по строкам

    return matrix


def main():
    """
    Основная функция для ввода данных и вывода результата.
    """
    # Ввод данных: количество строк (n) и столбцов (m)
    n, m = map(int, input().strip().split())
    
    # Заполнение матрицы
    matrix = fill_matrix(n, m)
    
    # Вывод матрицы
    for row in matrix:
        # Форматированный вывод каждой строки матрицы
        print(' '.join(f'{num:3d}' for num in row))


if __name__ == "__main__":
    main()