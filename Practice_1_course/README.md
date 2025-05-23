
# Практика 1 курс

Язык: Python (3.11)

## 2 семестр

### Тема

`Программная реализация систем шифрования Виженера и шифра «двойной квадрат» Уитстона`

### О работе
Шифр Виженера и Уитстона будут реализованы на языке Python (3.11). Проект будет состоять из 4 файлов:
    1. «Main.py» – главный исполняемый файл, в котором будет реализован выбор между шифром Виженера и Уистона;
    2. «Vijener.py» – шифр Виженера;
    3. «Wheatstone.py» – шифр Уитстона;
    4. «Verification.py» – файл, в котором реализованы функции для проверки на правильность ввода.


1. Основной файл main.py управляет основным потоком программы:
- Предоставляет пользовательский интерфейс для выбора между тремя действиями.
- Вызывает соответствующие функции Vijener() и wheatstone().
2. Файл Vijener.py реализует шифр Виженера:
- Использует алфавит ABC для работы с русскими и английскими символами.
- Реализует функции encode() и decode() для шифрования и расшифровки.
- Использует замуровку для создания зашифрованного текста.
3. Файл wheatstone.py реализует шифр "Двойного квадрата" Уитстона:
- Создает две квадратные таблицы на основе ключей.
- Использует функции encode() и decode() для обработки текста.
- Применяет принцип замены позиций символов в тексте.
4. Файл verification.py содержит вспомогательные функции:
- verification_ABC() проверяет корректность ввода текста.
- verification_Mode() получает режим работы (зашифровка/расшифровка).
- verification_Main() управляет основным циклом выбора пользователя.

## Примечание

Есть отчет по практике, связанный с этой программной реализацией `Report_Practice_1_cource.docx`
	
⬇️ интерфейс программы в консоли ⬇️

![image](https://github.com/Kikuzawa/DSTU_VKB/blob/main/Practice_1_course/screenshot/screenshot_14122024_092218.png)


