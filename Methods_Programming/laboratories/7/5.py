
from collections import defaultdict
from typing import List, Sequence
from itertools import product


def find_minimum_groups(k: int, n: int, m: int, hieroglyphs: Sequence[str]) -> int:
    lamp_groups: defaultdict[str, int] = defaultdict(int)

    for row, col in product(range(n), range(m)):
        # Формируем ключ для группы лампочек на основе текущего столбца и всех иероглифов
        lamp_key = ''.join(hieroglyphs[glyph * n + row][col] for glyph in range(k))
        lamp_groups[lamp_key] += 1

    # Количество уникальных групп лампочек
    return len(lamp_groups)


def main() -> None:
    k, n, m = map(int, input().split())
    hieroglyphs: List[str] = [input() for _ in range(k * n)]

    print(find_minimum_groups(k, n, m, hieroglyphs))


if __name__ == '__main__':
    main()
