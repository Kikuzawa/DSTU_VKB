
from typing import List, Sequence


def max_segment_length(segments: Sequence[int], required_segments: int) -> int:
    left: int = 1
    right: int = 10_000_001

    while left < right:
        mid: int = (left + right) // 2
        total_segments: int = sum(length // mid for length in segments)

        if total_segments >= required_segments:
            left = mid + 1
        else:
            right = mid

    return left - 1


def main() -> None:
    n, k = map(int, input().split())
    segments: List[int] = [int(input()) for _ in range(n)]

    result: int = max_segment_length(segments, k)
    print(result)


if __name__ == "__main__":
    main()
