from itertools import permutations
from typing import List, Tuple, Union, cast


def solve(k: int, rates: List[Tuple[int, int, int, int]]) -> Union[List[int], int]:

    cockroaches = list(range(1, k + 1))  # Все возможные тараканы

    for perm in permutations(cockroaches):
        valid = True
        for rate in rates:
            a, b, c, d = rate

            # Находим индексы тараканов в текущей перестановке
            idx_a = perm.index(a)
            idx_b = perm.index(b)
            idx_c = perm.index(c)
            idx_d = perm.index(d)

            # Проверка, что ровно одна из ставок выполняется
            condition1 = idx_a < idx_b  # A до B
            condition2 = idx_c < idx_d  # C до D

            # Условие: ровно одно из утверждений должно быть истинным
            if condition1 == condition2:
                valid = False
                break

        if valid:
            return list(perm)

    return 0


def main() -> None:
    k, n = map(int, input().split())
    rates: List[Tuple[int, int, int, int]] = cast(List[Tuple[int, int, int, int]],
                                                  [tuple(map(int, input().split())) for _ in range(n)])

    result = solve(k, rates)

    if result == 0:
        print(0)
    else:
        print(" ".join(map(str, result[::-1])))


if __name__ == "__main__":
    main()
