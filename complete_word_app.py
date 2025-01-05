import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)

from main import find_words_with_letters


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
            # Передаём ссылки на коллекции и словарь в окно настройки букв
            dialog = LetterSelectionWindow(
                word,
                self.used_letters_no_position,
                self.unused_letters,
                self.letter_positions
            )
            if dialog.exec_():  # Ждем завершения окна
                result = dialog.get_results()  # Получаем результаты через метод

                letter_positions = result['result_dict']
                used_letters_no_position = result['yes_set']
                unused_letters = result['no_set']
                # исключаю попадения угаданный букв в коллекцию неиспользуемых букв
                unused_letters = unused_letters.difference(used_letters_no_position)
                possible_words = find_words_with_letters(letter_positions,
                                                         unused_letters,
                                                         used_letters_no_position,
                                                         )
                # print(f'{type(used_letters_no_position) = }')
                # print(f'{type(unused_letters) = }')
                # print([word for word in possible_words])

                QMessageBox.information(
                    self,
                    "Результат",
                    f"Yes set: {list(self.used_letters_no_position)}\n"
                    f"No List: {list(self.unused_letters)}\n"
                    f"Result Dict: {self.letter_positions}"
                    f"Possible words \n {[word for word in possible_words]}"
                )

            else:
                QMessageBox.information(self, "Информация", "Настройка букв отменена.")

    def reset_input(self):
        self.word_input.clear()


class LetterSelectionWindow(QDialog):
    def __init__(self, word, used_letters_no_position, unused_letters, letter_positions):
        super().__init__()
        # self.callback = callback
        self.setWindowTitle("Настройка букв")
        self.setFixedSize(600, 500)

        self.word = word

        self.used_letters_no_position = used_letters_no_position
        self.unused_letters = unused_letters
        self.letter_positions = letter_positions

        self.yes_set = set()
        self.no_set = set()  # Инициализируем пустую коллекцию
        self.result_dict = {}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица
        self.table = QTableWidget(len(self.word), 3, self)
        self.table.setHorizontalHeaderLabels(["Буква", "Выбор (Yes/No)", "Цифра (1-5)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 16px;")
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

            # Добавляем буквы в no_list сразу
            self.no_set.add(letter)

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
        """Обновляет список YES и NO на основе выбора."""
        letter = self.word[row]
        print(f"update_yes_no: row={row}, choice={choice}, letter={letter}")  # Лог

        if choice == "Yes":
            self.yes_set.add(letter)  # Добавляем в yes_set
            if letter in self.no_set:  # Убираем из no_list
                self.no_set.remove(letter)
        elif choice == "No":
            self.yes_set.discard(letter)  # Убираем из yes_set
            if letter not in self.no_set:  # Добавляем в no_list
                self.no_set.add(letter)

        # print(f"yes_set={self.yes_set}, no_list={self.no_list}")  # Лог

    def update_number(self, row, value):
        """Обновляет словарь при выборе числового значения."""
        letter = self.word[row]
        number = int(value)

        if number > 0:
            self.result_dict[number - 1] = letter  # Ключ меньше на 1
            yes_no_box = self.table.cellWidget(row, 1)
            yes_no_box.setCurrentText("Yes")
            self.yes_set.add(letter)
            if letter in self.no_set:
                self.no_set.remove(letter)
        else:
            # Удаляем букву из result_dict, если она там есть
            for key, val in list(self.result_dict.items()):
                if val == letter:
                    del self.result_dict[key]

    def get_results(self):
        """Возвращает результаты выбора."""
        return {
            'yes_set': self.yes_set,
            'no_set': self.no_set,
            'result_dict': self.result_dict
        }

    def submit_results(self):
        """Возвращает результаты и обновляет глобальные коллекции."""
        results = self.get_results()

        # Обновляем глобальные коллекции и словарь
        self.used_letters_no_position.update(results['yes_set'])
        self.unused_letters.update(results['no_set'])
        self.letter_positions.update(results['result_dict'])

        # Удаляем буквы из no_list, если они находятся в yes_list
        self.unused_letters -= self.used_letters_no_position

        self.accept()  # Возвращает QDialog.Accepted

    def reset_choices(self):
        """Сбрасывает выбор пользователя."""
        self.yes_set.clear()
        self.no_set.clear()
        self.result_dict.clear()
        for row in range(self.table.rowCount()):
            yes_no_box = self.table.cellWidget(row, 1)
            number_box = self.table.cellWidget(row, 2)
            yes_no_box.setCurrentText("No")
            number_box.setCurrentText("0")
            self.no_set.append(self.word[row])  # Добавляем букву обратно в no_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WordInputWindow()
    main_window.show()
    sys.exit(app.exec_())
