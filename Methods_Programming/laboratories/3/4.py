from collections import deque
from typing import List, Iterable, Sequence


def longest_increasing_subsequence(sequence: Sequence[int]) -> Iterable[int]:
    n = len(sequence)
    distance_table: List[int] = [1] * n  # Массив для хранения длины LIS до каждого элемента
    prev_index: List[int] = [-1] * n  # Массив для восстановления последовательности

    # Заполняем массив dp
    for i in range(n):
        for j in range(i):
            if sequence[j] < sequence[i] and distance_table[j] + 1 > distance_table[i]:
                distance_table[i] = distance_table[j] + 1
                prev_index[i] = j

    # Находим максимальную длину и индекс последнего элемента LCS
    max_length: int = max(distance_table)
    max_index: int = distance_table.index(max_length)

    # Восстанавливаем саму последовательность
    result = deque()
    while max_index != -1:
        result.append(sequence[max_index])
        max_index = prev_index[max_index]

    result.reverse()

    return result


def main() -> None:
    _ = int(input())
    sequence = list(map(int, input().split()))

    lis = longest_increasing_subsequence(sequence)

    # Выводим результат
    print(' '.join(map(str, lis)))


if __name__ == "__main__":
    main()
