

def count_economically_viable_ways(k: int, operations: str) -> int:
    n: int = len(operations)
    viable_ways: int = 0
    consecutive_matches: int = 0

    # Проходим по строке операций с конца к началу
    for i in range(n - k - 1, -1, -1):
        if operations[i] == operations[i + k]:
            consecutive_matches += 1
        else:
            consecutive_matches = 0

        viable_ways += consecutive_matches

    return viable_ways


def main() -> None:
    k: int = int(input())
    operations: str = input()

    result: int = count_economically_viable_ways(k, operations)
    print(result)


if __name__ == "__main__":
    main()
