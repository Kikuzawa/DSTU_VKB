def solve(S, N, positions):
    # Создаем матрицу театра
    theater = [[None] * S for _ in range(S)]

    # Заполняем позиции студентов
    student_positions = []
    for i, (ai, bi) in enumerate(positions):
        theater[ai - 1][bi - 1] = i

    # Проверяем возможность решения
    def check_solution():
        # Проверяем строки
        for row in theater:
            males = females = 0
            for cell in row:
                if cell is not None:
                    if solution[cell] == 'M':
                        males += 1
                    else:
                        females += 1
            if abs(males - females) > 1:
                return False

        # Проверяем столбцы
        for col in range(S):
            males = females = 0
            for row in range(S):
                if theater[row][col] is not None:
                    if solution[theater[row][col]] == 'M':
                        males += 1
                    else:
                        females += 1
            if abs(males - females) > 1:
                return False
        return True

    # Ищем решение методом перебора
    def dfs(pos=0):
        if pos >= len(positions):
            return check_solution()

        ai, bi = positions[pos]
        ai -= 1
        bi -= 1

        for gender in ['M', 'W']:
            solution[pos] = gender
            if dfs(pos + 1):
                return True
            solution[pos] = None

        return False

    global solution
    solution = [None] * N

    if dfs():
        return ''.join(solution)
    return "Impossible"


# Пример использования
S, N = map(int, input().split())
positions = []
for _ in range(N):
    ai, bi = map(int, input().split())
    positions.append((ai, bi))

result = solve(S, N, positions)
print(result)