from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ArrayElement:
    value: int
    index: int


def build_sparse_table(array: List[int]) -> Tuple[List[List[ArrayElement]], List[int]]:
    n: int = len(array)
    log_values: List[int] = [0] * (n + 1)

    # Предварительное вычисление логарифмов
    for i in range(2, n + 1):
        log_values[i] = log_values[i // 2] + 1

    max_power_of_two: int = log_values[n] + 1
    sparse_table: List[List[ArrayElement]] = [[ArrayElement(0, 0)] * max_power_of_two for _ in range(n)]

    # Инициализация разреженной таблицы
    for i in range(n):
        sparse_table[i][0] = ArrayElement(array[i], i)

    # Строим таблицу для отрезков длиной 2^j
    for j in range(1, max_power_of_two):
        for i in range(n - (1 << j) + 1): # (1 << j) = 2^j
            if sparse_table[i][j - 1].value >= sparse_table[i + (1 << (j - 1))][j - 1].value:
                sparse_table[i][j] = sparse_table[i][j - 1]
            else:
                sparse_table[i][j] = sparse_table[i + (1 << (j - 1))][j - 1]

    return sparse_table, log_values


def query_max(sparse_table: List[List[ArrayElement]], log_values: List[int], left: int, right: int) -> int:

    # Определяем наибольшую степень двойки, которая укладывается в отрезок
    max_power_of_two_in_range: int = log_values[right - left + 1]

    # Определяем максимальные элементы для двух подотрезков
    left_max: ArrayElement = sparse_table[left][max_power_of_two_in_range]
    right_max: ArrayElement = sparse_table[right - (1 << max_power_of_two_in_range) + 1][max_power_of_two_in_range]

    # Возвращаем индекс максимального элемента
    max_element: ArrayElement = left_max if left_max.value >= right_max.value else right_max

    return max_element.index + 1


def main() -> None:
    _: int = int(input())
    array: List[int] = list(map(int, input().split()))
    query_count: int = int(input())

    sparse_table, log_values = build_sparse_table(array)

    results: List[int] = []
    for _ in range(query_count):
        left, right = map(lambda x: int(x) - 1, input().split())
        max_index = query_max(sparse_table, log_values, left, right)
        results.append(max_index)

    print(' '.join(map(str, results)))


if __name__ == "__main__":
    main()
