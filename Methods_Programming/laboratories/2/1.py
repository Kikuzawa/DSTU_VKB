from collections import deque
from itertools import permutations
from typing import Set, AnyStr, Sequence


def generate_permutations(number: AnyStr) -> Sequence[AnyStr]:
    letters: AnyStr = number[0] + number[4] + number[5]
    digits: AnyStr = number[1] + number[2] + number[3]

    unique_letter_permutations: Set[AnyStr] = {''.join(p) for p in permutations(letters)}
    unique_digit_permutations: Set[AnyStr] = {''.join(p) for p in permutations(digits)}

    all_combinations: deque[AnyStr] = deque()
    for letter in unique_letter_permutations:
        for digit in unique_digit_permutations:
            combined_number = f"{letter[0]}{digit[0]}{digit[1]}{digit[2]}{letter[1]}{letter[2]}"
            all_combinations.append(combined_number)

    return all_combinations


def main() -> None:
    car_number: str = input()
    permutations_list: Sequence[AnyStr] = generate_permutations(car_number)

    print(len(permutations_list), *permutations_list, sep='\n')


if __name__ == "__main__":
    main()
