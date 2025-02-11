from typing import Dict, List, Iterable


def process_students(students):
    # Словарь для хранения учеников по классам
    classes: Dict[int, List[str]] = {9: [], 10: [], 11: []}

    # Обрабатываем каждого ученика
    for student in students:
        # Разделяем строку на номер класса и фамилию
        class_number, surname = student.split()
        class_number = int(class_number)  # Преобразуем номер класса в целое число
        # Добавляем ученика в соответствующий класс
        classes[class_number].append(f"{class_number} {surname}")

    # Формируем итоговую строку для вывода
    result = ""
    # Проходим по классам в порядке 9, 10, 11
    for class_number in classes:
        # Добавляем учеников текущего класса в результат
        result += "\n".join(student for student in classes[class_number]) + "\n"

    return result


def main():
    # Пути к входному и выходному файлам
    input_file_path = "/home/kikuzawa/Documents/GitHub/DSTU_VKB/Methods_Programming/laboratories/1/input.txt"
    output_file_path = "/home/kikuzawa/Documents/GitHub/DSTU_VKB/Methods_Programming/laboratories/1/output.txt"

    # Чтение данных из входного файла
    with open(input_file_path, 'r', encoding='KOI8-r') as file:
        # Обрабатываем учеников и сортируем их по классам
        students_by_class = process_students(map(str.strip, file.readlines()))

    # Запись результата в выходной файл
    with open(output_file_path, 'w', encoding='KOI8-r') as file:
        file.write(students_by_class)


main()