from bisect import bisect_left
from typing import List, Sequence, Iterable
from collections import deque


def longest_increasing_subsequence(sequence: Sequence[int]) -> Iterable[int]:
    largest_increasing_subsequence: List[int] = []
    prev_index: List[int] = [-1] * len(sequence)
    indices: List[int] = []

    for i, value in enumerate(sequence):
        pos = bisect_left(largest_increasing_subsequence, value)

        # Если значение больше всех элементов в lis, добавляем его
        if pos == len(largest_increasing_subsequence):
            largest_increasing_subsequence.append(value)
            indices.append(i)
        else:
            largest_increasing_subsequence[pos] = value
            indices[pos] = i

        # Восстанавливаем индексы
        if pos > 0:
            prev_index[i] = indices[pos - 1]

    # Восстанавливаем саму последовательность
    result: deque[int] = deque()
    k = indices[-1]
    while k != -1:
        result.append(sequence[k])
        k = prev_index[k]

    result.reverse()

    return result


def main() -> None:
    n, a1, k, b, m = map(int, input().split())

    # Генерируем последовательность по формуле, которая дана в условии
    sequence = [0] * n
    sequence[0] = a1
    for i in range(1, n):
        sequence[i] = (k * sequence[i - 1] + b) % m

    lis = longest_increasing_subsequence(sequence)

    print(" ".join(map(str, lis)))


if __name__ == "__main__":
    main()
