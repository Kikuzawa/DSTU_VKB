

import math
from itertools import combinations
from typing import List, Tuple, Iterable, Sequence, cast, Dict
from collections import deque


def reconstruct_path(memoization_table, bits: int, parent: int, n: int) -> Iterable[int]:

    path: deque[int] = deque()

    for _ in range(n - 1):
        path.appendleft(parent)
        new_bits: int = bits & ~(1 << parent)
        _, parent = memoization_table[(bits, parent)]
        bits: int = new_bits

    return path


def tsp_dynamic_programming(points: Sequence[Tuple[float, float]]) -> Tuple[float, Iterable[int]]:
    n: int = len(points)
    dist_matrix: List[List[float]] = [[math.dist(points[i], points[j]) for j in range(n)] for i in range(n)]

    # Таблица мемоизации, где ключами являются пары (набор посещенных вершин, текущая вершина)
    # Устанавливаем начальные значения, когда первая вершина уже посещена
    memoization_table: Dict[Tuple[int, int], Tuple[float, int]] = {(1 << k, k): (dist_matrix[0][k], 0) for k in
                                                                   range(1, n)}

    # Проходимся по вершинам
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            # Устанавливаем биты для всех вершин в подмножестве
            bits: int = sum(1 << bit for bit in subset)

            # Находим кратчайший путь к этому подмножеству, заканчивающийся в вершине k
            for k in subset:
                prev: int = bits & ~(1 << k)
                memoization_table[(bits, k)] = min(
                    (memoization_table[(prev, m)][0] + dist_matrix[m][k], m)
                    for m in subset if m != 0 and m != k
                )

    # Мы возвращаемся к первой вершине, завершаем тур
    bits: int = (2 ** n - 1) - 1
    opt, parent = min((memoization_table[(bits, k)][0] + dist_matrix[k][0], k) for k in range(1, n))

    path = reconstruct_path(memoization_table, bits, parent, n)

    return opt, path


def main() -> None:
    n: int = int(input())
    points: List[Tuple[int, int]] = cast(List[Tuple[int, int]], [tuple(map(float, input().split())) for _ in range(n)])
    min_length, min_path = tsp_dynamic_programming(points)
    print('{:.15E}'.format(min_length))
    print(' '.join(map(lambda x: str(x + 1), min_path)))


if __name__ == '__main__':
    main()
