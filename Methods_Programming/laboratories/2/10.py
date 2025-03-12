
from array import array, ArrayType
from copy import copy
from typing import List, Tuple, Sequence


def find_most_stylish_outfit(
        hats: Sequence[int],
        shirts: Sequence[int],
        pants: Sequence[int],
        shoes: Sequence[int]
) -> Tuple[int, int, int, int]:
    indices: ArrayType[int] = array('i', [0, 0, 0, 0])
    min_diff: float = float('inf')
    best_indices: ArrayType[int] = array('i', [0, 0, 0, 0])

    while all(indices[i] < len(lst) for i, lst in enumerate((hats, shirts, pants, shoes))):
        current_colors = (hats[indices[0]], shirts[indices[1]], pants[indices[2]], shoes[indices[3]])
        min_color = min(current_colors)
        max_color = max(current_colors)
        current_diff = max_color - min_color

        # Обновляем минимальную разницу и сохраняем текущие индексы
        if current_diff < min_diff:
            min_diff = current_diff
            best_indices = copy(indices)

        # Если разница минимальна (0), выходим из цикла
        if current_diff == 0:
            break

        # Сдвигаем указатель у минимального элемента
        for i, color in enumerate(current_colors):
            if color == min_color:
                indices[i] += 1
                break

    return (
        hats[best_indices[0]],
        shirts[best_indices[1]],
        pants[best_indices[2]],
        shoes[best_indices[3]]
    )


def main() -> None:
    colors_for_clothes: List[List[int]] = []

    for _ in range(4):
        _ = int(input())
        colors = sorted(map(int, input().split()))
        colors_for_clothes.append(colors)

    stylish_outfit: Tuple[int, int, int, int] = find_most_stylish_outfit(*colors_for_clothes)
    print(*stylish_outfit)


if __name__ == "__main__":
    main()
