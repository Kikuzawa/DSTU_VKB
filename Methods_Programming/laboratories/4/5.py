from collections import defaultdict
from dataclasses import dataclass
from functools import total_ordering
from heapq import heappop, heappush
from typing import List, Tuple, Dict, Set, cast


@dataclass(frozen=True)
@total_ordering
class State:
    cost: int
    city: int
    tank: int
    canister: int

    def __lt__(self, other: 'State') -> bool:
        return self.cost < other.cost

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return (self.cost, self.city, self.tank, self.canister) == (other.cost, other.city, other.tank, other.canister)


class Graph:
    def __init__(self) -> None:
        self._adjacency_list: Dict[int, List[int]] = defaultdict(list)

    def add_edge(self, u: int, v: int) -> None:
        self._adjacency_list[u].append(v)
        self._adjacency_list[v].append(u)

    def get_neighbors(self, city: int) -> List[int]:
        return self._adjacency_list[city]


def min_fuel_cost(n: int, fuel_costs: List[int], graph: Graph) -> int:
    # Используем очередь с приоритетом
    pq: List[State] = [State(0, 1, 0, 0)]  # начинаем с города 1, пустой бак и канистра
    visited: Set[Tuple[int, int, int]] = set()

    while pq:
        state = heappop(pq)

        # Если добрались до города N, возвращаем стоимость
        if state.city == n:
            return state.cost

        # Проверка на повторное посещение состояния
        if (state.city, state.tank, state.canister) in visited:
            continue
        visited.add((state.city, state.tank, state.canister))

        # 1. Заправка только бака
        if state.tank == 0:
            heappush(pq, State(state.cost + fuel_costs[state.city - 1], state.city, 1, state.canister))

        # 2. Заправка бака и канистры
        if state.tank == 0 and state.canister == 0:
            heappush(pq, State(state.cost + 2 * fuel_costs[state.city - 1], state.city, 1, 1))

        # 3. Переливание бензина из канистры в бак
        if state.tank == 0 and state.canister > 0:
            heappush(pq, State(state.cost, state.city, 1, 0))

        # 4. Переход в соседний город (тратим 1 единицу топлива)
        if state.tank > 0:
            for neighbor in graph.get_neighbors(state.city):
                heappush(pq, State(state.cost, neighbor, state.tank - 1, state.canister))

    return -1  # Если не удалось добраться до города N


def main() -> None:
    n: int = int(input())
    fuel_costs: List[int] = list(map(int, input().split()))
    m: int = int(input())
    roads: List[Tuple[int, int]] = cast(List[Tuple[int, int]], [tuple(map(int, input().split())) for _ in range(m)])

    graph = Graph()
    for u, v in roads:
        graph.add_edge(u, v)

    print(min_fuel_cost(n, fuel_costs, graph))


if __name__ == '__main__':
    main()
