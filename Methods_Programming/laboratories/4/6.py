import sys
from dataclasses import dataclass
from typing import List, Tuple

INF = sys.maxsize // 2


@dataclass(frozen=True)
class Flight:
    start: int
    end: int
    weight_change: int
    index: int


def find_path_between_concerts(
        n: int,
        c: int,
        flights: List[Flight],
        concerts: List[int]
) -> Tuple[int, List[int]]:
    matrix = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    parents = [[0 for _ in range(n)] for _ in range(n)]

    for flight in flights:
        matrix[flight.start][flight.end] = -flight.weight_change
        parents[flight.start][flight.end] = flight.index

    # Алгоритм Флойда-Уоршелла для нахождения кратчайших путей
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    parents[i][j] = parents[i][k]

    # Проверка на отрицательные циклы
    for i in range(c):
        if matrix[concerts[i]][concerts[i]] < 0:
            return -1, []

    # Строим маршрут между концертами
    path = []
    for i in range(c - 1):
        v = concerts[i]
        while v != concerts[i + 1]:
            path.append(parents[v][concerts[i + 1]])
            v = flights[parents[v][concerts[i + 1]]].end
            if len(path) > 10000000:
                return -1, []

    return len(path), [p + 1 for p in path]


def main() -> None:
    n, m, c = map(int, input().split())
    flights: List[Flight] = []

    for i in range(m):
        vertex1, vertex2, w = map(int, input().split())
        vertex1 -= 1  # Приводим города к индексации с нуля
        vertex2 -= 1
        flights.append(Flight(vertex1, vertex2, w, i))

    concerts = [i - 1 for i in map(int, input().split())]

    # Получаем путь между концертами
    result, path = find_path_between_concerts(n, c, flights, concerts)

    if result == -1:
        print("infinitely kind")
    else:
        print(result)
        print(" ".join(map(str, path)))


if __name__ == "__main__":
    main()
