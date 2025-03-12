
import math
from itertools import combinations
from typing import List, Tuple, cast


def calculate_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    """Вычисляет евклидово расстояние между двумя точками."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def prim_algorithm(points: List[Tuple[int, int]], connections: List[Tuple[int, int]]) -> float:
    """Находит минимальную стоимость соединения всех точек с помощью алгоритма Прима."""
    num_points = len(points)
    adj_matrix = [[float('inf')] * num_points for _ in range(num_points)]

    # Заполнение матрицы расстояний
    for i, j in combinations(range(num_points), 2):
        adj_matrix[i][j] = adj_matrix[j][i] = calculate_distance(points[i], points[j])

    # Учитываем существующие соединения
    for start, end in connections:
        adj_matrix[start - 1][end - 1] = adj_matrix[end - 1][start - 1] = 0.0

    # Алгоритм Прима
    in_mst = [False] * num_points
    key_values = [float('inf')] * num_points
    key_values[0] = 0.0
    total_cost = 0.0

    for _ in range(num_points):
        # Находим минимальный ключ
        u = min((val, idx) for idx, val in enumerate(key_values) if not in_mst[idx])[1]
        in_mst[u] = True
        total_cost += key_values[u]

        # Обновляем ключи соседей
        for v in range(num_points):
            if adj_matrix[u][v] < key_values[v] and not in_mst[v]:
                key_values[v] = adj_matrix[u][v]

    return total_cost


def main() -> None:
    num_points = int(input())
    points = cast(List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(num_points)])
    num_connections = int(input())
    connections = cast(List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(num_connections)])

    min_cost = prim_algorithm(points, connections)
    print(f"{min_cost:.5f}")


if __name__ == "__main__":
    main()
