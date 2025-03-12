
from typing import List, Sequence


def max_distance_between_cows(stalls: Sequence[int], num_cows: int) -> int:

    left: int = 0
    right: int = stalls[-1] - stalls[0] + 1

    while left < right:
        mid: int = (left + right) // 2
        cows_placed: int = 1
        last_placed_stall: int = stalls[0]  # Последнее стойло, в которое была поставлена корова

        for current_stall in stalls[1:]:
            if current_stall - last_placed_stall >= mid:
                cows_placed += 1
                last_placed_stall = current_stall

        if cows_placed >= num_cows:
            left = mid + 1
        else:
            right = mid

    return left - 1


def main() -> None:
    n, k = map(int, input().split())
    stalls: List[int] = list(map(int, input().split()))

    result: int = max_distance_between_cows(stalls, k)
    print(result)


if __name__ == "__main__":
    main()
