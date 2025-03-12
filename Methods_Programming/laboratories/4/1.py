from collections import deque
from itertools import product
from typing import Tuple, Generator, Any, Set


def get_moves(x: int, y: int) -> Generator[Tuple[int, int], Any, None]:
    moves: Tuple[Tuple[int, int], ...] = (
        (x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2),
        (x - 1, y - 2), (x - 2, y - 1), (x - 2, y + 1), (x - 1, y + 2)
    )
    yield from ((mx, my) for mx, my in moves if 0 <= mx <= 7 and 0 <= my <= 7)


def knights_meet(knight1: Tuple[int, int], knight2: Tuple[int, int]) -> int:
    visited: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
    queue: deque[Tuple[Tuple[int, int], Tuple[int, int], int]] = deque([(knight1, knight2, 0)])

    while queue:
        k1, k2, moves = queue.popleft()

        if k1 == k2:
            return moves

        visited.add((k1, k2))

        for move1, move2 in product(get_moves(k1[0], k1[1]), get_moves(k2[0], k2[1])):
            if (move1, move2) not in visited:
                visited.add((move1, move2))  # Добавляем в visited сразу
                queue.append((move1, move2, moves + 1))

    return -1


def main() -> None:
    knight1, knight2 = map(lambda k: (ord(k[0]) - ord('a'), int(k[1]) - 1), input().split())

    result: int = knights_meet(knight1, knight2)
    print(result)


if __name__ == "__main__":
    main()
