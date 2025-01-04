import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
from functools import partial




class WordInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Введите слово")
        self.setFixedSize(500, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        self.label = QLabel("Введите слово (ровно 5 букв):")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.label)

        # Поле ввода
        self.word_input = QLineEdit(self)
        self.word_input.setAlignment(Qt.AlignCenter)
        self.word_input.setStyleSheet("font-size: 26px; min-height: 50px;")
        layout.addWidget(self.word_input)

        # Кнопки
        self.submit_button = QPushButton("Подтвердить", self)
        self.submit_button.setStyleSheet("font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_word)
        layout.addWidget(self.submit_button)

        self.reset_button = QPushButton("Сброс", self)
        self.reset_button.setStyleSheet("font-size: 16px;")
        self.reset_button.clicked.connect(self.reset_input)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)
#
    def submit_word(self):
        word = self.word_input.text().strip()
        if len(word) != 5:
            QMessageBox.critical(self, "Ошибка", "Слово должно состоять ровно из 5 букв!")
        else:
            dialog = LetterSelectionWindow(word)
            if dialog.exec_():  # Ждем завершения окна
                result = dialog.result
                QMessageBox.information(
                    self,
                    "Результат",
                    f"Yes List: {result['yes_list']}\n"
                    f"No List: {result['no_list']}\n"
                    f"Result Dict: {result['result_dict']}"
                )

            else:
                QMessageBox.information(self, "Информация", "Настройка букв отменена.")



    def reset_input(self):
        if QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите сбросить?") == QMessageBox.Yes:
            self.word_input.clear()




class LetterSelectionWindow(QDialog):
    def __init__(self, word):
        super().__init__()
        self.setWindowTitle("Настройка букв")
        self.setFixedSize(600, 500)

        self.word = word
        self.yes_set = set()
        self.no_list = []
        self.result_dict = {}
        self.result = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget(len(self.word), 3, self)
        self.table.setHorizontalHeaderLabels(["Буква", "Выбор (Yes/No)", "Цифра (1-5)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 16px;")
        for row, letter in enumerate(self.word):
            self.table.setItem(row, 0, QTableWidgetItem(letter))

            yes_no_combobox = QComboBox()
            yes_no_combobox.addItems(["No", "Yes"])
            yes_no_combobox.setStyleSheet("font-size: 16px;")
            yes_no_combobox.currentTextChanged.connect(partial(self.update_yes_no, row, letter))
            self.table.setCellWidget(row, 1, yes_no_combobox)

            number_combobox = QComboBox()
            number_combobox.addItems([str(i) for i in range(6)])
            number_combobox.setStyleSheet("font-size: 16px;")
            number_combobox.currentTextChanged.connect(partial(self.update_number, row, letter))
            self.table.setCellWidget(row, 2, number_combobox)

        layout.addWidget(self.table)

        # Кнопки
        self.submit_button = QPushButton("Подтвердить", self)
        self.submit_button.setStyleSheet("font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_results)
        layout.addWidget(self.submit_button)

        self.reset_button = QPushButton("Сброс", self)
        self.reset_button.setStyleSheet("font-size: 16px;")
        self.reset_button.clicked.connect(self.reset_choices)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def update_yes_no(self, row, letter, choice):
        if choice == "Yes":
            self.yes_set.add(letter)
            self.no_list = [(i, ch) for i, ch in self.no_list if ch != letter]
        else:
            self.yes_set.discard(letter)
            if (row, letter) not in self.no_list:
                self.no_list.append((row, letter))

    def update_number(self, row, letter, number):
        number = int(number)
        if number > 0:
            self.result_dict[number - 1] = letter

    def submit_results(self):
        self.result = {
            "yes_list": list(self.yes_set),
            "no_list": self.no_list,
            "result_dict": self.result_dict,
        }
        self.accept()


    def reset_choices(self):
        if QMessageBox.question(self, "Подтверждение", "Сбросить все настройки?") == QMessageBox.Yes:
            self.yes_set.clear()
            self.no_list.clear()
            self.result_dict.clear()
            for row in range(self.table.rowCount()):
                yes_no_box = self.table.cellWidget(row, 1)
                number_box = self.table.cellWidget(row, 2)
                yes_no_box.setCurrentText("No")
                number_box.setCurrentText("0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WordInputWindow()
    main_window.show()
    # print(main_window)
    sys.exit(app.exec_())