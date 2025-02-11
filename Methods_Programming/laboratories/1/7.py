from typing import List, Tuple, cast, Iterable
from collections import deque


def calculate_exit_times(arrival_times):
    # Время окончания работы каждого мастера (в минутах с начала суток)
    workers_time: List[int] = [0, 0, 0]
    # Очередь для хранения времени выхода клиентов (часы, минуты)
    exit_times: deque[Tuple[int, int]] = deque()

    # Обрабатываем каждого клиента
    for hours, minutes in arrival_times:
        # Переводим время прихода клиента в минуты с начала суток
        arrival_minutes = hours * 60 + minutes

        # Находим мастера, который освободится раньше всех
        next_worker_index = workers_time.index(min(workers_time))

        # Если мастер свободен к моменту прихода клиента, обслуживание начинается сразу
        if workers_time[next_worker_index] <= arrival_minutes:
            workers_time[next_worker_index] = arrival_minutes + 30
        else:
            # Если мастер занят, клиент ждет, пока мастер освободится
            workers_time[next_worker_index] += 30

        # Вычисляем время выхода клиента и добавляем его в очередь
        exit_time = workers_time[next_worker_index]
        exit_times.append((exit_time // 60, exit_time % 60))  # Переводим минуты обратно в часы и минуты

    return exit_times


def main():
    # Вводим количество клиентов
    n: int = int(input())
    # Вводим времена прихода клиентов (часы, минуты)
    arrival_times: List[Tuple[int, int]] = cast(
        List[Tuple[int, int]],
        [tuple(map(int, input().split())) for _ in range(n)]
    )

    # Вычисляем времена выхода клиентов
    exit_times: Iterable[Tuple[int, int]] = calculate_exit_times(arrival_times)

    # Выводим времена выхода для каждого клиента
    for hours, minutes in exit_times:
        print(hours, minutes)


main()