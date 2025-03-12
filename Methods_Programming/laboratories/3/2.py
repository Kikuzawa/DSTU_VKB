from typing import List, AnyStr
from itertools import product


def levenshtein_distance(source: AnyStr, target: AnyStr) -> int:
    len_source: int = len(source)
    len_target: int = len(target)

    # Создаем таблицу для хранения расстояний
    distance_table: List[List[int]] = [[0] * (len_target + 1) for _ in range(len_source + 1)]

    # Инициализация первой строки и первого столбца
    for i, j in zip(range(len_source + 1), range(len_target + 1)):
        distance_table[i][0] = i  # Расстояние от source до пустой строки
        distance_table[0][j] = j  # Расстояние от пустой строки до target

    # Заполняем таблицу
    for i, j in product(range(1, len_source + 1), range(1, len_target + 1)):
        if source[i - 1] == target[j - 1]:
            distance_table[i][j] = distance_table[i - 1][j - 1]  # Символы совпадают
        else:
            distance_table[i][j] = 1 + min(distance_table[i - 1][j],
                                           distance_table[i][j - 1],
                                           distance_table[i - 1][j - 1])  # Удаление, вставка, замена

    return distance_table[len_source][len_target]


def main() -> None:
    a: str = input()
    b: str = input()

    distance = levenshtein_distance(a, b)
    print(distance)


if __name__ == "__main__":
    main()
