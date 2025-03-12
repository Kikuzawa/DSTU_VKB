
from array import array, ArrayType


def find_palindromes(s: str) -> int:
    # Преобразуем строку для работы с палиндромами
    transformed_string: str = "@#" + "#".join(s) + "#$"
    palindrome_lengths: ArrayType[int] = array("i", [0] * len(transformed_string))
    center: int = 0
    right_boundary: int = 0

    for i in range(1, len(transformed_string) - 1):
        if i < right_boundary:
            palindrome_lengths[i] = min(right_boundary - i, palindrome_lengths[2 * center - i])

        # Расширяем палиндром вокруг центра i
        while transformed_string[i + palindrome_lengths[i] + 1] == transformed_string[i - palindrome_lengths[i] - 1]:
            palindrome_lengths[i] += 1

        # Обновляем центр и правую границу, если нашли более длинный палиндром
        if i + palindrome_lengths[i] > right_boundary:
            center, right_boundary = i, i + palindrome_lengths[i]

    # Считаем количество палиндромных подстрок
    return sum((length + 1) // 2 for length in palindrome_lengths)


def main() -> None:
    input_string: str = input()
    print(find_palindromes(input_string))


if __name__ == "__main__":
    main()
