from array import array
from collections import namedtuple
from typing import List, Sequence, TypeVar, Generic

Edge = namedtuple('Edge', ['weight', 'vertex1', 'vertex2'])

T = TypeVar('T')


class DisjointSetUnion(Generic[T]):
    def __init__(self, size: int):
        self.parent = array("i", range(size))
        self.rank = array("i", [0] * size)

    def find(self, node: T) -> int:
        if node != self.parent[node]:
            # Сжатие пути (оптимизация поиска)
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1: T, node2: T) -> None:
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            # Union by rank
            if self.rank[root1] < self.rank[root2]:
                root1, root2 = root2, root1
            self.parent[root2] = root1
            if self.rank[root1] == self.rank[root2]:
                self.rank[root1] += 1


def kruskal(num_vertices: int, edges: Sequence[Edge]) -> int:
    dsu: DisjointSetUnion[int] = DisjointSetUnion(num_vertices)
    minimum_spanning_tree_weight: int = 0

    # Сортируем рёбра по весу в порядке возрастания
    for edge in sorted(edges, key=lambda e: e.weight):
        # Если вершины ещё не соединены, то объединяем их и добавляем вес ребра в итоговый результат
        if dsu.find(edge.vertex1) != dsu.find(edge.vertex2):
            dsu.union(edge.vertex1, edge.vertex2)
            minimum_spanning_tree_weight += edge.weight

    return minimum_spanning_tree_weight


def main() -> None:
    num_vertices, num_edges = map(int, input().split())
    edges: List[Edge] = []

    for _ in range(num_edges):
        vertex1, vertex2, weight = map(int, input().split())
        edges.append(Edge(weight, vertex1 - 1, vertex2 - 1))

    print(kruskal(num_vertices, edges))


if __name__ == "__main__":
    main()
