import heapq
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Flight:
    src: int
    dep_time: int
    dest: int
    arr_time: int


class Graph:
    def __init__(self) -> None:
        # Словарь, где ключ - номер пункта, а значение - список кортежей, представляющих соседние пункты
        # с временем отправления и прибытия.
        self._adjacency_list: Dict[int, List[Tuple[int, int, int]]] = defaultdict(list)

    def add_flight(self, flight: Flight) -> None:
        self._adjacency_list[flight.src].append((flight.dest, flight.dep_time, flight.arr_time))

    def get_neighbors(self, node: int) -> List[Tuple[int, int, int]]:
        return self._adjacency_list.get(node, [])


def min_time_to_destination(n: int, a: int, b: int, graph: Graph) -> int:
    min_time = [float('inf')] * (n + 1)
    min_time[a] = 0
    heap = [(0, a)]

    while heap:
        time, node = heapq.heappop(heap)
        if time > min_time[node]:
            continue
        for dest, dep_time, arr_time in graph.get_neighbors(node):
            if dep_time >= time and min_time[dest] > arr_time:
                min_time[dest] = arr_time
                heapq.heappush(heap, (arr_time, dest))

    return round(min_time[b])


def main() -> None:
    n: int = int(input())
    a, b = map(int, input().split())
    k: int = int(input())

    flights: List[Flight] = [Flight(*map(int, input().split())) for _ in range(k)]

    graph = Graph()
    for flight in flights:
        graph.add_flight(flight)

    result: int = min_time_to_destination(n, a, b, graph)
    print(result)


if __name__ == "__main__":
    main()
