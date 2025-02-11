from collections import deque
from typing import Sequence, List, Iterable


def process_queue(actions):
    queue_1 = deque()
    queue_2 = deque()
    results: List[str] = []

    for action in actions:
        if action[0] == '+':
            queue_2.append(action[1])
        elif action[0] == '*':
            queue_2.appendleft(action[1])
        else:
            results.append(queue_1.popleft())

        if len(queue_1) < len(queue_2):
            queue_1.append(queue_2.popleft())

    return results


def main():
    n: int = int(input())
    actions: List[List[str]] = []

    for _ in range(n):
        action: List[str] = input().split()
        actions.append(action)

    results: Iterable[str] = process_queue(actions)

    for result in results:
        print(result)



main()
