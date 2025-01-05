import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)

from word_processor_for_5letters import find_words_with_letters


class WordInputWindow(QWidget):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.setWindowTitle("Введите слово")
        self.setFixedSize(500, 300)

        # Глобальные коллекции для всех слов
        self.used_letters_no_position = set()  # Используемые буквы без указания позиции
        self.unused_letters = set()  # Неиспользуемые буквы
        self.letter_positions = {}  # Словарь позиций букв

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
            return

        # Создаем окно настройки букв
        dialog = LetterSelectionWindow(
            word,
            self.used_letters_no_position,
            self.unused_letters,
            self.letter_positions
        )

        if dialog.exec_():  # Ждем завершения окна
            result = dialog.get_results()
            self.used_letters_no_position.update(result['yes_set'])
            self.unused_letters.update(result['no_set'])
            self.letter_positions.update(result['result_dict'])

            # Убираем из unused_letters буквы из used_letters_no_position
            self.unused_letters -= self.used_letters_no_position

            possible_words = find_words_with_letters(
                self.letter_positions,
                self.unused_letters,
                self.used_letters_no_position,
            )

            QMessageBox.information(
                self,
                "Результат",
                f"Yes set: {list(self.used_letters_no_position)}\n"
                f"No set: {list(self.unused_letters)}\n"
                f"Result Dict: {self.letter_positions}\n"
                f"Possible words: {', '.join(possible_words)}"
            )
        else:
            QMessageBox.information(self, "Информация", "Настройка букв отменена.")

    def reset_input(self):
        self.word_input.clear()


class LetterSelectionWindow(QDialog):
    def __init__(self, word, used_letters_no_position, unused_letters, letter_positions):
        super().__init__()
        self.setWindowTitle("Настройка букв")
        self.setFixedSize(600, 500)

        self.word = word

        # Создаем локальные копии глобальных коллекций
        self.local_yes_set = set(used_letters_no_position)
        self.local_no_set = set(unused_letters)
        self.local_result_dict = dict(letter_positions)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget(len(self.word), 3, self)
        self.table.setHorizontalHeaderLabels(["Буква", "Выбор (Yes/No)", "Цифра (1-5)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 16px;")

        # Проход по каждой букве слова
        for row, letter in enumerate(self.word):
            # Буква
            self.table.setItem(row, 0, QTableWidgetItem(letter))

            # Выпадающее меню Yes/No
            yes_no_combobox = QComboBox()
            yes_no_combobox.addItems(["No", "Yes"])
            yes_no_combobox.setStyleSheet("font-size: 16px;")
            yes_no_combobox.setCurrentText("No")  # Устанавливаем "No" по умолчанию
            yes_no_combobox.currentTextChanged.connect(lambda value, r=row: self.update_yes_no(r, value))
            self.table.setCellWidget(row, 1, yes_no_combobox)

            # Добавляем букву в no_set сразу
            self.local_no_set.add(letter)

            # Выпадающее меню с цифрами
            number_combobox = QComboBox()
            number_combobox.addItems([str(i) for i in range(6)])
            number_combobox.setStyleSheet("font-size: 16px;")
            number_combobox.currentTextChanged.connect(lambda value, r=row: self.update_number(r, value))
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

    def update_yes_no(self, row, choice):
        """Обновляет локальные списки Yes/No на основе выбора."""
        letter = self.word[row]
        if choice == "Yes":
            self.local_yes_set.add(letter)
            self.local_no_set.discard(letter)
        elif choice == "No":
            self.local_yes_set.discard(letter)
            self.local_no_set.add(letter)

    def update_number(self, row, value):
        """Обновляет локальный словарь позиций букв."""
        letter = self.word[row]
        number = int(value)
        if number > 0:
            self.local_result_dict[number - 1] = letter
            self.local_yes_set.add(letter)
            self.local_no_set.discard(letter)
        else:
            # Удаляем букву из result_dict, если она там есть
            self.local_result_dict.pop(number - 1, None)

    def get_results(self):
        """Возвращает локальные изменения."""
        return {
            'yes_set': self.local_yes_set,
            'no_set': self.local_no_set,
            'result_dict': self.local_result_dict,
        }

    def submit_results(self):
        """Применяет локальные изменения и закрывает окно."""
        self.accept()  # Завершение окна подтверждением изменений

    def reset_choices(self):
        """Сбрасывает выбор пользователя."""
        self.local_yes_set.clear()
        self.local_no_set.clear()
        self.local_result_dict.clear()
        for row in range(self.table.rowCount()):
            yes_no_box = self.table.cellWidget(row, 1)
            number_box = self.table.cellWidget(row, 2)
            yes_no_box.setCurrentText("No")
            number_box.setCurrentText("0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WordInputWindow()
    main_window.show()
    sys.exit(app.exec_())
