from collections import deque
from typing import List, cast, Tuple


class Graph:
    def __init__(self, n: int) -> None:
        """Инициализируем граф с n вершинами."""
        self._n = n
        self._adj_list: List[List[int]] = [[] for _ in range(n)]  # Список смежности для графа
        self._color: List[int] = []

    def add_edge(self, u: int, v: int) -> None:
        """Добавляем ребро между вершинами u и v."""
        self._adj_list[u - 1].append(v - 1)
        self._adj_list[v - 1].append(u - 1)

    def is_bipartite(self) -> bool:
        self._color = [-1] * self._n  # -1: не окрашена, 0: первая доля, 1: вторая доля

        def bfs(start_inner: int) -> bool:
            queue: deque[int] = deque([start_inner])
            self._color[start_inner] = 0
            while queue:
                v = queue.popleft()
                for u in self._adj_list[v]:
                    if self._color[u] == -1:
                        self._color[u] = 1 - self._color[v]
                        queue.append(u)
                    elif self._color[u] == self._color[v]:
                        return False
            return True

        for start in range(self._n):
            if self._color[start] == -1 and not bfs(start):  # Если вершина не посещена
                return False
        return True

    @property
    def bipartite_partition(self) -> List[int]:
        if self.is_bipartite():
            return [i + 1 for i in range(self._n) if self._color[i] == 0]
        return []


def main() -> None:
    n, m = map(int, input().split())
    pairs = cast(List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(m)])

    # Создаем граф и добавляем ребра
    graph = Graph(n)
    for u, v in pairs:
        graph.add_edge(u, v)

    # Проверяем, возможно ли рассадить
    result = graph.bipartite_partition

    if result:
        print("YES")
        print(*result)
    else:
        print("NO")


if __name__ == "__main__":
    main()
