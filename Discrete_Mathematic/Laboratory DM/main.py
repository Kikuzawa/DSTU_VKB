import sys
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QApplication, QWidget, QDialog, QLabel
import math


class DocumentationDialog(QDialog):
    def __init__(self, file_path):
        super().__init__()

        self.setWindowTitle('Документация')
        self.setGeometry(100, 100, 750, 800)

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)

        with open(file_path, 'r', encoding='utf-8') as file:
            documentation = file.read()
            text_edit.setPlainText(documentation)

        self.setLayout(layout)


class Cube_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cube Rubik - CRYPT")
        self.setGeometry(50, 50, 1400, 600)

        self.name_msg = QLabel('Введите сообщение для шифрования / расшифрования:')
        self.input_message = QTextEdit()
        self.input_message.setFixedHeight(150)
        self.scr_msg = QLabel('Введите алгоритм шифрования [ Пример: U R L B* F D U* ]:')
        self.input_scramble = QLineEdit()
        self.res_msg = QLabel('Зашифрованное / расшифрованное сообщение: ')
        self.result_text = QTextEdit()
        self.result_text.setFixedHeight(150)

        self.encrypt_button = QPushButton("Зашифровать/Расшифровать")
        self.encrypt_button.clicked.connect(self.encrypt)

        self.decrypt_button = QPushButton("Получить ключ Дешифровки")
        self.decrypt_button.clicked.connect(self.decrypt)

        self.doc_button = QPushButton("Документация", self)
        self.doc_button.clicked.connect(self.show_documentation)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)

        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(350)
        self.input_text.setFixedWidth(700)
        self.in_txt = QLabel('Изначальный вид кубика:')
        self.output_text = QTextEdit()
        self.output_text.setFixedHeight(350)
        self.output_text.setFixedWidth(700)
        self.out_txt = QLabel('Конечный вид кубика:')

        layout = QVBoxLayout()
        layout.addWidget(self.name_msg)
        layout.addWidget(self.input_message)
        layout.addWidget(self.scr_msg)
        layout.addWidget(self.input_scramble)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.encrypt_button)
        layout1.addWidget(self.decrypt_button)

        layout2_1 = QHBoxLayout()
        layout2_1.addWidget(self.in_txt)
        layout2_1.addWidget(self.out_txt)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.input_text)
        layout2.addWidget(self.output_text)
        self.input_text.setReadOnly(True)
        self.output_text.setReadOnly(True)

        layout3 = QVBoxLayout()
        layout3.addWidget(self.res_msg)
        layout3.addWidget(self.result_text)
        layout3.addWidget(self.doc_button)
        layout3.addWidget(self.exit_button)
        self.result_text.setReadOnly(True)

        layout.addLayout(layout1)
        layout.addLayout(layout2_1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        self.setLayout(layout)

    def encrypt(self): #функция шифрования
        try:
            # задание стором класс
            white = Side()
            orange = Side()
            green = Side()
            red = Side()
            yellow = Side()
            blue = Side()

            white.SetAdjacents([blue.Up, red.Up, green.Up, orange.Up])
            orange.SetAdjacents([white.Up, green.Left, yellow.Down, blue.Right])
            green.SetAdjacents([white.Left, red.Left, yellow.Left, orange.Right])
            red.SetAdjacents([white.Down, blue.Left, yellow.Up, green.Right])
            yellow.SetAdjacents([green.Down, red.Down, blue.Down, orange.Down])
            blue.SetAdjacents([yellow.Right, red.Right, white.Right, orange.Left])

            Sides = {'U': white, 'F': green, 'R': red, 'B': blue, 'L': orange, 'D': yellow}

            output = ''

            msg = str(self.input_message.toPlainText())
            scramble = str(self.input_scramble.text())

            msg += ((math.ceil(len(msg) / 54) * 54) - len(msg)) * ' '
            msg = [msg[x:x + 54] for x in range(0, len(msg), 54)]
            msg = [[coiso[x:x + 9] for x in range(0, len(coiso), 9)] for coiso in msg]

            scramble += ' '
            scramble = scramble.split(' ')
            scramble = scramble[:len(scramble) - 1]

            matrix = []
            row_pattern = "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜"

            for _ in range(9):
                row = [char for char in row_pattern]
                matrix.append(row)

            flag = 0

            for x in msg:
                for y in range(len(x)):
                    list(Sides.values())[y].SetText(x[y])

                if flag == 0:
                    string_w = str(white).split('\n')
                    string_g = str(green).split('\n')
                    string_r = str(red).split('\n')
                    string_b = str(blue).split('\n')
                    string_o = str(orange).split('\n')
                    string_y = str(yellow).split('\n')

                    for i in range(5):
                        for j in range(3):
                            matrix[j][i + 4] = string_w[j][i] + ' '
                            matrix[j + 3][i] = string_g[j][i]
                            matrix[j + 3][i + 6] = string_r[j][i] + ' '
                            matrix[j + 3][i + 12] = string_b[j][i]
                            matrix[j + 3][i + 18] = string_o[j][i]
                            matrix[j + 6][i + 4] = string_y[j][i] + ' '

                    formatted_matrix = ""
                    for row in matrix:
                        formatted_row = "   ".join([str(element) for element in row])
                        formatted_matrix += formatted_row + "\n\n"

                    self.input_text.setPlainText(formatted_matrix)

                    flag = 1

                for y in scramble:
                    if len(y) == 1:
                        Sides[y].Turn(True)
                    elif y[1] == '*':
                        Sides[y[0]].Turn(False)
                    else:
                        for z in range(2):
                            Sides[y[0]].Turn(True)

                if flag == 1:
                    string_w = str(white).split('\n')
                    string_g = str(green).split('\n')
                    string_r = str(red).split('\n')
                    string_b = str(blue).split('\n')
                    string_o = str(orange).split('\n')
                    string_y = str(yellow).split('\n')

                    for i in range(5):
                        for j in range(3):
                            matrix[j][i + 4] = string_w[j][i] + ' '
                            matrix[j + 3][i] = string_g[j][i]
                            matrix[j + 3][i + 6] = string_r[j][i] + ' '
                            matrix[j + 3][i + 12] = string_b[j][i]
                            matrix[j + 3][i + 18] = string_o[j][i]
                            matrix[j + 6][i + 4] = string_y[j][i] + ' '

                    formatted_matrix = ""
                    for row in matrix:
                        formatted_row = "   ".join([str(element) for element in row])
                        formatted_matrix += formatted_row + "\n\n"

                    self.output_text.setPlainText(formatted_matrix)

                    flag = 2

                for a in Sides.values():
                    for b in a.Face:
                        for c in b:
                            output += c.value

            self.result_text.setPlainText(output)
        except:
            self.result_text.setPlainText('Неправильный ввод')

    def decrypt(self):
        try:
            key = str(self.input_scramble.text())
            decoded_key = []

            for symbol in reversed(key.split()):
                if "*" in symbol:
                    symbol = symbol.replace("*", "")
                else:
                    symbol = symbol + '*'
                decoded_key.append(symbol)
            decoded_key = " ".join(decoded_key)

            self.result_text.setPlainText(decoded_key)
        except:
            self.result_text.setPlainText('Неправильный ввод')

    def show_documentation(self):
        documentation_dialog = DocumentationDialog('/home/kikuzawa/Documents/GitHubAndVSCode/DSTU_VKB/Discrete_Mathematic/Laboratory DM/documentation.txt')
        documentation_dialog.exec()


class char():
    def __str__(self):
        return self.value


class Side():  # класс. задающий стороны кубика рубика

    def __init__(self):  # задание 9 маленьких кубиков каждой стороны
        self.UpLeftCorner = char()
        self.UpEdge = char()
        self.UpRightCorner = char()
        self.LeftEdge = char()
        self.Center = char()
        self.RightEdge = char()
        self.DownLeftCorner = char()
        self.DownEdge = char()
        self.DownRightCorner = char()
        # соединение кусочков в три горизонтальные линии кубика
        self.Face = [[self.UpLeftCorner, self.UpEdge, self.UpRightCorner], [self.LeftEdge, self.Center, self.RightEdge],
                     [self.DownLeftCorner, self.DownEdge, self.DownRightCorner]]
        # задание мини-команд для изменения положений квадратиков
        self.Up = [self.UpLeftCorner, self.UpEdge, self.UpRightCorner]
        self.Right = [self.UpRightCorner, self.RightEdge, self.DownRightCorner]
        self.Down = [self.DownRightCorner, self.DownEdge, self.DownLeftCorner]
        self.Left = [self.DownLeftCorner, self.LeftEdge, self.UpLeftCorner]

    def SetAdjacents(self, adjacents):  # задание смежностей
        self.Adjacents = adjacents

    def SetText(self, text):  # задание каждому квадратику одной стороны значений символов из сообщения
        self.UpLeftCorner.value = text[0]
        self.UpEdge.value = text[1]
        self.UpRightCorner.value = text[2]
        self.LeftEdge.value = text[3]
        self.Center.value = text[4]
        self.RightEdge.value = text[5]
        self.DownLeftCorner.value = text[6]
        self.DownEdge.value = text[7]
        self.DownRightCorner.value = text[8]

    def Turn(self, clockwise):  # задание поворотов - по часовой стрелки, в случае * - против часовой
        buffer = [] #запоминающий значения список
        opo = [[0 for x in range(3)] for x in range(3)] #opo - определение позиции на стороне
        for x in range(3):
            for y in range(3):
                opo[y][x] = self.Face[x][y].value

        if clockwise:  # по часовой
            for x in range(3):
                aux = opo[x][0]
                opo[x][0] = opo[x][2]
                opo[x][2] = aux

            buffer.append([x.value for x in self.Adjacents[len(self.Adjacents) - 1]])
            for x in self.Adjacents[:len(self.Adjacents) - 1]:
                buffer.append([y.value for y in x])
        else:#против часовой
            for x in range(3):
                aux = opo[0][x]
                opo[0][x] = opo[2][x]
                opo[2][x] = aux

            for x in self.Adjacents[1:]:
                buffer.append([y.value for y in x])
            buffer.append([x.value for x in self.Adjacents[0]])

        for x in range(3):
            for y in range(3):
                self.Face[x][y].value = opo[x][y]
        for x in range(4):
            for y in range(3):
                self.Adjacents[x][y].value = buffer[x][y]

    def __str__(self):
        return f'{self.UpLeftCorner} {self.UpEdge} {self.UpRightCorner}\n{self.LeftEdge} {self.Center} {self.RightEdge}\n{self.DownLeftCorner} {self.DownEdge} {self.DownRightCorner}'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Cube_GUI()
    window.show()
    sys.exit(app.exec())
