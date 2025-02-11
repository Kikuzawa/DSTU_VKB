from collections import deque
from typing import List, Deque, Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    operation: str  # Операция: "+" для погрузки, "-" для разгрузки
    cell_index: int  # Номер отсека (1-based индекс)
    fuel_type: str  # Тип топлива в бочке


def process_docks(cells: int, max_len: int, actions: Iterable[Action]):
    max_tanks: int = 0  # Максимальное количество бочек на барже
    current_tanks: int = 0  # Текущее количество бочек на барже
    error: bool = False  # Флаг ошибки

    # Инициализация отсеков: каждый отсек представлен деком (очередью)
    cell: List[Deque[str]] = [deque() for _ in range(cells)]

    # Обработка каждого действия
    for action in actions:
        if action.operation == "+":  # Погрузка бочки
            cell_index: int = action.cell_index - 1  # Преобразуем в 0-based индекс
            cell[cell_index].append(action.fuel_type)  # Добавляем бочку в отсек
            current_tanks += 1  # Увеличиваем счетчик бочек

            # Проверка на превышение максимального количества бочек
            if current_tanks > max_len:
                error = True
                break
            # Обновляем максимальное количество бочек
            max_tanks = max(max_tanks, current_tanks)
        else:  # Разгрузка бочки
            cell_index: int = action.cell_index - 1  # Преобразуем в 0-based индекс

            # Проверка на пустой отсек или несоответствие типа топлива
            if not cell[cell_index] or cell[cell_index].pop() != action.fuel_type:
                error = True
                break
            current_tanks -= 1  # Уменьшаем счетчик бочек

    # Возвращаем -1, если баржа не пуста или произошла ошибка, иначе возвращаем максимальное количество бочек
    return -1 if current_tanks > 0 or error else max_tanks


def main():
    # Чтение входных данных
    request: List[str] = input().split()
    docks: int = int(request[0])  # Количество доков
    cells: int = int(request[1])  # Количество отсеков
    max_len: int = int(request[2])  # Максимальное количество бочек на барже

    # Создание списка действий
    actions: List[Action] = []
    for _ in range(docks):
        action_data: List[str] = input().split()
        action = Action(operation=action_data[0], cell_index=int(action_data[1]), fuel_type=action_data[2])
        actions.append(action)

    # Обработка действий и получение результата
    result: int = process_docks(cells, max_len, actions)

    # Вывод результата
    print("Error" if result == -1 else result)


main()