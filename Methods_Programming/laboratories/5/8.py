def is_valid_move(board, x, y):
    return 0 <= x < len(board) and 0 <= y < len(board) and board[x][y] == -1


def get_possible_moves(x, y):
    moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    valid_moves = []
    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        if is_valid_move(board, new_x, new_y):
            valid_moves.append((new_x, new_y))
    return valid_moves


def solve_knight_tour(n):
    # Проверка невозможных случаев
    if n <= 1 or n == 3 or n == 4:
        return None

    # Инициализация доски
    board = [[-1] * n for _ in range(n)]
    board[0][0] = 0  # Начальная позиция

    def solve_util(x, y, move_num):
        if move_num == n * n:
            return True

        # Получаем возможные ходы в определенном порядке
        moves = get_possible_moves(x, y)

        for next_x, next_y in moves:
            board[next_x][next_y] = move_num
            if solve_util(next_x, next_y, move_num + 1):
                return True
            board[next_x][next_y] = -1

        return False

    if solve_util(0, 0, 1):
        return board
    return None


def main():
    n = int(input())
    result = solve_knight_tour(n)

    if result is None:
        print(0)
    else:
        print(1)
        for row in result:
            print(' '.join(str(x + 1) for x in row))


if __name__ == "__main__":
    main()