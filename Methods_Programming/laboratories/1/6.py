from collections import deque
from typing import List, Iterable

def can_sort_train(n, wagons):
    # Используем deque для стека тупика и стека пути 2
    dead_end_stack: deque[int] = deque()  # Стек для тупика
    output_track_stack: deque[int] = deque()  # Стек для пути 2

    for wagon in wagons:
        # Перемещаем вагоны из тупика на путь 2, если следующий вагон в порядке
        while dead_end_stack and dead_end_stack[-1] == len(output_track_stack) + 1:
            output_track_stack.append(dead_end_stack.pop())

        # Проверяем, можно ли сразу отправить вагон на путь 2
        if wagon == len(output_track_stack) + 1:
            output_track_stack.append(wagon)
        else:
            # Если нельзя, отправляем вагон в тупик
            dead_end_stack.append(wagon)

    # Проверяем оставшиеся вагоны в тупике
    while dead_end_stack and dead_end_stack[-1] == len(output_track_stack) + 1:
        output_track_stack.append(dead_end_stack.pop())

    # Если все вагоны успешно перемещены на путь 2, возвращаем True
    return len(output_track_stack) == n

def main():
    # Вводим количество вагонов
    n: int = int(input())
    # Вводим порядок вагонов на пути 1
    wagons: List[int] = list(map(int, input().split()))
    # Проверяем, можно ли отсортировать вагоны и выводим результат
    print("YES" if can_sort_train(n, wagons) else "NO")

main()