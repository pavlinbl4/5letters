import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
)


class WordInputWindow(QWidget):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.setWindowTitle("Введите слово")
        self.setFixedSize(500, 300)
        self.word = None  # Для сохранения введённого слова

        self.label = None  # Определение атрибута
        self.word_input = None
        self.submit_button = None
        self.reset_button = None

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
        self.word_input.setStyleSheet("font-size: 16px;")
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

    def submit_word(self):
        word = self.word_input.text().strip()
        if len(word) != 5:
            QMessageBox.critical(self, "Ошибка", "Слово должно состоять ровно из 5 букв!")
        else:
            self.word = word
            self.close()

    def reset_input(self):
        self.word_input.clear()


class LetterSelectionWindow(QWidget):
    def __init__(self, word, callback=None):
        super().__init__()

        self.callback = callback
        self.setWindowTitle("Настройка букв")
        self.setFixedSize(600, 500)

        self.word = word
        self.yes_set = set()
        self.no_list = []
        self.result_dict = {}

        self.table = None
        self.submit_button = None
        self.reset_button = None

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
            yes_no_combobox.setCurrentText("No")
            yes_no_combobox.currentTextChanged.connect(lambda value, r=row: self.update_yes_no(r, value))
            self.table.setCellWidget(row, 1, yes_no_combobox)

            self.no_list.append(letter)

            number_combobox = QComboBox()
            number_combobox.addItems([str(i) for i in range(6)])
            number_combobox.setStyleSheet("font-size: 16px;")
            number_combobox.currentTextChanged.connect(lambda value, r=row: self.update_number(r, value))
            self.table.setCellWidget(row, 2, number_combobox)

        layout.addWidget(self.table)

        self.submit_button = QPushButton("Подтвердить", self)
        self.submit_button.setStyleSheet("font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_results)
        layout.addWidget(self.submit_button)

        self.reset_button = QPushButton("Сброс", self)
        self.reset_button.setStyleSheet("font-size: 16px;")
        self.reset_button.clicked.connect(self.reset_choices)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def update_yes_no(self, row, choice):
        letter = self.word[row]
        if choice == "Yes":
            self.yes_set.add(letter)
            if letter in self.no_list:
                self.no_list.remove(letter)
        elif choice == "No":
            self.yes_set.discard(letter)
            if letter not in self.no_list:
                self.no_list.append(letter)

    def update_number(self, row, value):
        letter = self.word[row]
        number = int(value)
        if number > 0:
            self.result_dict[number - 1] = letter
            yes_no_box = self.table.cellWidget(row, 1)
            yes_no_box.setCurrentText("Yes")
            self.yes_set.add(letter)
            if letter in self.no_list:
                self.no_list.remove(letter)
        else:
            for key, val in list(self.result_dict.items()):
                if val == letter:
                    del self.result_dict[key]

    def get_results(self):
        return {
            'yes_list': list(self.yes_set),
            'no_list': self.no_list,
            'result_dict': self.result_dict
        }

    def submit_results(self):
        results = self.get_results()
        if self.callback:
            self.callback(results)
        self.close()
        return results

    def reset_choices(self):
        self.yes_set.clear()
        self.no_list.clear()
        self.result_dict.clear()
        for row in range(self.table.rowCount()):
            yes_no_box = self.table.cellWidget(row, 1)
            number_box = self.table.cellWidget(row, 2)
            yes_no_box.setCurrentText("No")
            number_box.setCurrentText("0")
            self.no_list.append(self.word[row])


def get_letter_settings():
    """Функция для вызова GUI и получения результатов."""
    app = QApplication.instance() or QApplication(sys.argv)
    word_window = WordInputWindow()
    word_window.show()
    app.exec_()

    word = word_window.word
    if not word:
        return None

    results = {}

    def callback(data):
        nonlocal results
        results = data

    selection_window = LetterSelectionWindow(word, callback=callback)
    selection_window.show()
    app.exec_()
    return results

# Удален блок if __name__ == "__main__"
