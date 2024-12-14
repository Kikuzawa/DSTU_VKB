import sys
from PyQt6.QtWidgets import  QComboBox, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QApplication, QWidget, QDialog, QLabel
from PyQt6.QtCore import QFile
import Cezar_Default
import Cezar_affin_system
import Cezar_with_key
import Trisemus_crypt

class DocumentationDialog(QDialog):
    def __init__(self, file_path):
        super().__init__()

        self.setWindowTitle('Документация')
        self.setGeometry(100, 100, 950, 800)

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)

        # Read documentation from the provided file
        with open(file_path, 'r', encoding='utf-8') as file:
            documentation = file.read()
            text_edit.setPlainText(documentation)

        self.setLayout(layout)
class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cezar' Crypt")
        self.setGeometry(100, 100, 1200, 600)

        # Создание компонентов интерфейса
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Шифр Цезаря", "Аффинная система (Цезарь)", "Шифр Цезаря с ключом", "Система Трисемуса"])

        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Зашифровать", "Расшифровать"])

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "Английский"])

        self.input_text_edit = QTextEdit()
        self.input_key = QLineEdit()
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)

        self.encrypt_decrypt_button = QPushButton("Зашифровать/Расшифровать")
        self.encrypt_decrypt_button.clicked.connect(self.encrypt_decrypt)

        self.doc_button = QPushButton("Документация", self)
        self.doc_button.clicked.connect(self.show_documentation)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)

        # Создание и настройка компоновщика
        layout = QVBoxLayout()
        layout.addWidget(self.method_combo)
        layout.addWidget(self.operation_combo)
        layout.addWidget(self.lang_combo)
        layout.addWidget(self.input_text_edit)
        layout.addWidget(self.input_key)
        layout.addWidget(self.output_text_edit)
        layout.addWidget(self.encrypt_decrypt_button)

        layout.addWidget(self.doc_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)



    def show_documentation(self):
        documentation_dialog = DocumentationDialog('/home/kikuzawa/Documents/GitHubAndVSCode/DSTU_VKB/Base_of_Information_Security/12 лаба/documentation.txt')
        documentation_dialog.exec()


    def encrypt_decrypt(self):
        method = self.method_combo.currentText()
        operation = self.operation_combo.currentText()
        language = self.lang_combo.currentText()
        message = str(self.input_text_edit.toPlainText())
        key = str(self.input_key.text())
        match language:
            case "Русский":
                match operation:
                    case "Зашифровать":
                        match method:
                            case "Шифр Цезаря":
                                self.output_text_edit.setPlainText(Cezar_Default.cezar_default_rus(message, key, 0))
                            case "Аффинная система (Цезарь)":
                                self.output_text_edit.setPlainText(Cezar_affin_system.cezar_affine_system_rus(key, message, 0))
                            case "Шифр Цезаря с ключом":
                                try:
                                    key, shift = map(str, key.split())
                                    shift = int(shift)
                                    self.output_text_edit.setPlainText(Cezar_with_key.cezar_with_key_rus(message, key, shift))
                                except Exception as e:
                                    self.output_text_edit.setPlainText('Ошибка :(\n'
                                                                       f'{e}')
                            case "Система Трисемуса":
                                self.output_text_edit.setPlainText(Trisemus_crypt.Trisemus_rus(message, key, 0))
                    case "Расшифровать":
                        match method:
                            case "Шифр Цезаря":
                                self.output_text_edit.setPlainText(Cezar_Default.cezar_default_rus(message, key, 1))
                            case "Аффинная система (Цезарь)":
                                self.output_text_edit.setPlainText(Cezar_affin_system.cezar_affine_system_rus(key, message, 1))
                            case "Шифр Цезаря с ключом":
                                try:
                                    key, shift = map(str, key.split())
                                    shift = int(shift)
                                    self.output_text_edit.setPlainText(
                                        Cezar_with_key.cezar_with_key_rus(message, key, -shift))
                                except:
                                    self.output_text_edit.setPlainText('Ошибка :(\n'
                                                                       'Введите ключ слово и шаг через пробел')
                            case "Система Трисемуса":
                               self.output_text_edit.setPlainText(Trisemus_crypt.Trisemus_rus(message, key, 1))
            case "Английский":
                match operation:
                    case "Зашифровать":
                        match method:
                            case "Шифр Цезаря":
                                self.output_text_edit.setPlainText(Cezar_Default.cezar_default_eng(message, key, 0))
                            case "Аффинная система (Цезарь)":
                                self.output_text_edit.setPlainText(Cezar_affin_system.cezar_affine_system_eng(key, message, 0))
                            case "Шифр Цезаря с ключом":
                                try:
                                    key, shift = map(str, key.split())
                                    shift = int(shift)
                                    self.output_text_edit.setPlainText(
                                        Cezar_with_key.cezar_with_key_eng(message, key, shift))
                                except:
                                    self.output_text_edit.setPlainText('Ошибка :(\n'
                                                                       'Введите ключ слово и шаг через пробел')
                            case "Система Трисемуса":
                                self.output_text_edit.setPlainText(Trisemus_crypt.Trisemus_eng(message, key, 0))
                    case "Расшифровать":
                        match method:
                            case "Шифр Цезаря":
                                self.output_text_edit.setPlainText(Cezar_Default.cezar_default_eng(message, key, 1))
                            case "Аффинная система (Цезарь)":
                                self.output_text_edit.setPlainText(Cezar_affin_system.cezar_affine_system_eng(key, message, 1))
                            case "Шифр Цезаря с ключом":
                                try:
                                    key, shift = map(str, key.split())
                                    shift = int(shift)
                                    self.output_text_edit.setPlainText(
                                        Cezar_with_key.cezar_with_key_eng(message, key, -shift))
                                except:
                                    self.output_text_edit.setPlainText('Ошибка :(\n'
                                                                       'Введите ключ слово и шаг через пробел')
                            case "Система Трисемуса":
                                self.output_text_edit.setPlainText(Trisemus_crypt.Trisemus_eng(message, key, 1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec())