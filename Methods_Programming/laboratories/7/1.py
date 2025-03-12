

def find_max_repetition_count(s: str) -> int:
    length = len(s)
    for period_length in range(1, length // 2 + 1):
        if length % period_length == 0 and s[:period_length] * (length // period_length) == s:
            return length // period_length
    return 1

def main() -> None:
    input_string = input().strip()

    print(find_max_repetition_count(input_string))

if __name__ == '__main__':
    main()
