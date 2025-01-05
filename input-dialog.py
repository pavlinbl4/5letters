import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit,
                            QVBoxLayout, QHBoxLayout, QWidget)
from PyQt6.QtCore import pyqtSlot, QSize

class InputDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ввод данных")
        self.setGeometry(100, 100, 400, 300)
        self.input_text = None

        # Создаем центральный виджет и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Создаем поле ввода
        self.input_field = QTextEdit(self)
        self.input_field.setPlaceholderText("Введите текст...")
        self.input_field.setMinimumHeight(150)
        main_layout.addWidget(self.input_field)

        # Создаем горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Создаем кнопки и настраиваем их размер
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setMinimumSize(QSize(100, 40))  # Ширина 100, высота 40
        self.submit_button.clicked.connect(lambda: self.on_submit())
        button_layout.addWidget(self.submit_button)

        # Добавляем небольшой отступ между кнопками
        button_layout.addSpacing(10)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setMinimumSize(QSize(100, 40))  # Ширина 100, высота 40
        self.reset_button.clicked.connect(lambda: self.on_reset())
        button_layout.addWidget(self.reset_button)

        # Добавляем растягивающееся пространство по краям от кнопок
        button_layout.addStretch()
        button_layout.insertStretch(0)

    @pyqtSlot()
    def on_submit(self):
        self.input_text = self.input_field.toPlainText()
        self.close()

    @pyqtSlot()
    def on_reset(self):
        self.input_field.clear()

    def get_input_text(self):
        return self.input_text

def get_input():
    """
    Функция для получения введенного текста.
    
    Returns:
        str: введенный текст или None, если окно было закрыто без ввода
    """
    app = QApplication(sys.argv)
    dialog = InputDialog()
    dialog.show()
    app.exec()
    return dialog.get_input_text()

# Пример использования
if __name__ == '__main__':
    result = get_input()
    if result:
        print(f"Введенный текст: {result}")
    else:
        print("Ввод отменен")
