from typing import Tuple, List
from collections import deque


def fill_table(n: int, s: str, distance_table: List[List[int]]) -> None:
    for length in range(2, n + 1):  # Длина подстроки
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                distance_table[i][j] = distance_table[i + 1][j - 1] + 2
            else:
                distance_table[i][j] = max(distance_table[i + 1][j], distance_table[i][j - 1])


def longest_palindromic_subsequence(s: str) -> Tuple[int, str]:
    n = len(s)
    # Таблица для хранения длины максимального подпалиндрома
    # Все одиночные символы являются палиндромами длины 1
    distance_table: List[List[int]] = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    fill_table(n, s, distance_table)

    # Длина максимального подпалиндрома
    max_length: int = distance_table[0][n - 1]

    # Восстановление самого подпалиндрома
    left_index: int = 0
    right_index: int = n - 1

    subsequence: deque[str] = deque()

    while left_index <= right_index:
        if s[left_index] == s[right_index]:
            subsequence.append(s[left_index])
            left_index += 1
            right_index -= 1
        elif distance_table[left_index + 1][right_index] >= distance_table[left_index][right_index - 1]:
            left_index += 1
        else:
            right_index -= 1

    # Если длина подпалиндрома четная, то мы добавляем его в обратном порядке
    # Если нечетная, то добавляем последний символ
    palindromic_subsequence = ''.join(subsequence)
    if len(palindromic_subsequence) * 2 == max_length:
        result = palindromic_subsequence + palindromic_subsequence[::-1]
    else:
        result = palindromic_subsequence + palindromic_subsequence[-2::-1]

    return max_length, result


def main() -> None:
    s = input()
    max_length, palindromic_subsequence = longest_palindromic_subsequence(s)

    print(max_length)
    print(palindromic_subsequence)


if __name__ == "__main__":
    main()
