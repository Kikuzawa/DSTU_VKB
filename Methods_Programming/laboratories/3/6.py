from typing import Final, Dict, List, Sequence, AnyStr

BRACKET_PAIRS: Final[Dict[str, str]] = {
    '(': ')',
    '[': ']',
    '{': '}'
}


def reconstruct(
        s: AnyStr,
        distance_table: Sequence[Sequence[int]],
        table_for_restoring_sequence: Sequence[Sequence[int]],
        l: int,
        r: int
) -> AnyStr:
    if distance_table[l][r] == r - l + 1:  # Все символы уже в правильной последовательности
        return ""
    if distance_table[l][r] == 0:  # Неправильная последовательность
        return s[l:r + 1]
    if table_for_restoring_sequence[l][r] == -1:  # Если нет разделения
        return s[l] + reconstruct(s, distance_table, table_for_restoring_sequence, l + 1, r - 1) + s[r]

    return (reconstruct(s, distance_table, table_for_restoring_sequence, l, table_for_restoring_sequence[l][r]) +
            reconstruct(s, distance_table, table_for_restoring_sequence, table_for_restoring_sequence[l][r] + 1, r))


def fill_tables(
        s: AnyStr,
        n: int,
        distance_table: List[List[int]],
        table_for_restoring_sequence: List[List[int]]
) -> None:
    for right in range(n):
        for left in range(right, -1, -1):
            if left == right:
                distance_table[left][right] = 1
            else:
                min_removals = float('inf')
                split_index = -1

                # Проверка на соответствие скобок
                if s[left] in BRACKET_PAIRS and s[right] == BRACKET_PAIRS[s[left]]:
                    min_removals = distance_table[left + 1][right - 1]

                # Разделение на подзадачи
                for k in range(left, right):
                    current_removals = distance_table[left][k] + distance_table[k + 1][right]
                    if min_removals > current_removals:
                        min_removals = current_removals
                        split_index = k

                distance_table[left][right] = min_removals
                table_for_restoring_sequence[left][right] = split_index


def min_removals_to_valid_parentheses(s: AnyStr) -> AnyStr:

    n: int = len(s)
    # Таблица для хранения минимального количества удалений
    # Один символ всегда является правильной последовательностью
    distance_table: List[List[int]] = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    # Таблица для восстановления последовательности
    table_for_restoring_sequence: List[List[int]] = [[0] * n for _ in range(n)]

    fill_tables(s, n, distance_table, table_for_restoring_sequence)

    return reconstruct(s, distance_table, table_for_restoring_sequence, 0, n - 1)


def main() -> None:
    s: str = input()
    result = min_removals_to_valid_parentheses(s)
    print(result)


if __name__ == "__main__":
    main()
