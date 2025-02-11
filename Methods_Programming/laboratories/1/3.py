from itertools import combinations, product
from typing import List, Set, Iterable, Tuple


def find_best_broadcast(n: int, k: int, customer_counts: List[int]) -> int:
    """
    Находит максимальное количество покупателей, которые увидят два рекламных ролика,
    транслируемых с учетом ограничений на время между показами.

    :param n: Количество моментов времени.
    :param k: Минимальное время между окончанием первого ролика и началом второго.
    :param customer_counts: Список количества покупателей в каждый момент времени.
    :return: Максимальное количество покупателей, которые увидят оба ролика.
    """
    # Находим максимальное количество покупателей в любой момент времени
    max_customers: int = max(customer_counts)
    # Находим все моменты времени, когда количество покупателей максимально
    max_customers_times: Set[int] = {index for index, value in enumerate(customer_counts)
                                     if value == max_customers}

    # Проверяем, есть ли два момента с максимальным количеством покупателей,
    # между которыми прошло достаточно времени
    for time1, time2 in combinations(max_customers_times, 2):
        if abs(time1 - time2) > k - 1:
            return max_customers * 2  # Если да, возвращаем удвоенное максимальное значение

    # Если таких моментов нет, ищем пару (максимальный момент + другой момент),
    # где между ними прошло достаточно времени
    all_possible_pairs: Iterable[Tuple[int, int]] = product(
        max_customers_times,
        range(len(customer_counts))
    )

    # Находим второе по величине количество покупателей, которое можно использовать
    # в паре с максимальным, соблюдая ограничение по времени
    second_max_customers: int = max(
        map(
            lambda pair: customer_counts[pair[1]],
            filter(
                lambda pair: pair[0] != pair[1] and abs(pair[0] - pair[1]) > k - 1,
                all_possible_pairs
            )
        ),
        default=0
    )

    # Если нашли подходящую пару, возвращаем сумму максимального и второго по величине
    if second_max_customers > 0:
        return max_customers + second_max_customers

    # Если не нашли подходящих пар, перебираем все возможные пары моментов времени
    # с учетом ограничения на минимальное время между показами
    max_viewers_sum: int = 0
    for first_ad_time in range(n - k):
        second_ad_time: int = first_ad_time + k
        if second_ad_time < n:
            viewers_sum: int = customer_counts[first_ad_time] + max(customer_counts[second_ad_time:n])
            max_viewers_sum = max(max_viewers_sum, viewers_sum)

    return max_viewers_sum


def main():
    """
    Основная функция для ввода данных и вывода результата.
    """
    # Ввод данных
    n, k = map(int, input().split())
    customer_counts: List[int] = list(map(int, input().split()))
    
    # Вычисление результата
    result: int = find_best_broadcast(n, k, customer_counts)
    
    # Вывод результата
    print(result)


if __name__ == "__main__":
    main()