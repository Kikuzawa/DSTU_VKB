def min_path(mask, pos, n, dist):
    # Базовый случай: если все точки посещены, возвращаемся в точку 11
    if mask == ((1 << n) - 1):
        return dist[pos][11]

    ans = float('inf')

    # Проверяем все непосещенные точки
    for i in range(n):
        if (mask & (1 << i)) == 0:  # Если точка не посещена
            # Вычисляем расстояние через текущую точку
            ans = min(ans, dist[pos][i] + min_path(mask | (1 << i), i, n, dist))

    return ans


# Чтение входных данных
N = int(input())
dist = []
for _ in range(N):
    dist.append(list(map(int, input().split())))

Q = int(input())
results = []

# Обработка каждого варианта удаления точек
for _ in range(Q):
    # Читаем количество удаляемых точек и сами точки
    C = list(map(int, input().split()))
    count = C[0]  # Количество точек для удаления
    points = C[1:]  # Список точек для удаления

    # Создаём маску активных точек
    active_mask = (1 << N) - 1
    for point in points:
        active_mask &= ~(1 << (point - 1))  # Приводим к нулевому индексу

    # Если точка 11 не удалена и есть хотя бы одна активная точка
    if active_mask & (1 << 11):
        result = min_path(active_mask, 11, N, dist)
        results.append(str(result))

print('\n'.join(results))