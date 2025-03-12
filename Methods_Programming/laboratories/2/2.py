from typing import List, Iterable


def can_form_branches(
        max_uncomfortable: int,
        discomforts: Iterable[int],
        r: int,
        c: int
) -> bool:
    count = 0
    members_in_current_branch = 0
    for discomfort in discomforts:
        members_in_current_branch -= 1
        if members_in_current_branch < 1 and discomfort <= max_uncomfortable:
            count += 1
            members_in_current_branch = c

    return count >= r

def find_minimum_max_uncomfortable(n: int, r: int, c: int, heights: Iterable[int]) -> int:
    heights: List[int] = sorted(heights)
    discomforts: List[int] = [heights[i + c - 1] - heights[i] for i in range(n - c + 1)]

    left = -1
    right = heights[-1] - heights[0]

    while left + 1 < right:
        mid = (left + right) // 2
        if can_form_branches(mid, discomforts, r, c):
            right = mid
        else:
            left = mid

    return right


def main() -> None:
    n, r, c = map(int, input().split())
    heights: List[int] = [int(input()) for _ in range(n)]
    result: int = find_minimum_max_uncomfortable(n, r, c, heights)
    print(result)


if __name__ == "__main__":
    main()
