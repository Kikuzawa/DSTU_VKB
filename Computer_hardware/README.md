
# Аппаратные средства вычислительной техники

Язык: C++ (Arduino), Assembly

Вариант: 9

## 4 семестр

2 блока
### Arduino
1. `Знакомство с Tinkercad`
2. `Мигание светодиодом.`
3. `Звуковые сигналы`
4. `Работа с кнопками`
5. `работа с ЖК дисплеем`
6. `изучение кода`
7. `самостоятельное кодирование платы`


### Assembly
1. Первая ознакомительная, ее пропустил
2. `Начальные сведения о языке Ассемблер`
3. `Циклические и разветвляющиеся программы`

## 5 семестр

2 блока
### Arduino (проект)

Отчёт по проекту - `Report_Project_Arduino.docx`.
Тема: `Менеджер паролей`

### Assembly
4. `Применение логических инструкций`
5. `Обработка символьной информации с помощью функций DOS`
6. `Подпрограммы`
7. `Обработка прерываний`


# Примечание

В папке `Задания_Tasks` содержатся файл с заданиями для лабораторных работ по Assembler, Arduino не нашел, смотрите отчет.
Есть отчет по Arduino `Report_Labs_Arduino_Computer_hardware.docx` и `Report_Project_Arduino.docx`. По Assebler отчета только за 5 семестр `Report_Labs_Asm_Computer_hardware_5_semestr.docx`. 
в папках `X lab` хранятся файлы-исходники от лабораторных работ именно по Assembler. Для Arduino исходников нет, только отчет.

Запускались на emu8086. В lab7 необходимо компелировать код в exe файл, который потом нужно запустить в DosBox

# Как работать с TurboDebugger

Переместите папку `TurboDebugger` в какое-либо место на вашем компьютере.

Например: C:\TurboDebugger

Затем создаем или копируем файлы *.asm в данную папку

Например: task.asm

Выполняем следующий алгоритм для компиляции в программе DOS-BOX:

1. Вводим команду: mount c c:\TurboDebugger
2. Набираем: c:
3. Набираем: tasm/zi task.asm
4. В нашей папке должен появиться файл TASK.OBG
5. Набираем: tlink/v TASK.OBJ
6. В нашей папке должен появиться файл TASK.exe
7. Набираем команду для запуска TurboDebugger: td.exe 
8. Появится окно, в котором выберем FILE -> file open
9. Выбираем TASK.exe
10. Если все сделано правильно, то получаем файл в режиме отладки, иначе - программа откроется в зеленом окне
11. ГОТОВО
