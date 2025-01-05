import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример кнопки PyQt6")

        # Создаем кнопку
        self.button = QPushButton("Нажми меня", self)
        self.button.setGeometry(50, 50, 200, 100)  # Устанавливаем размер и положение кнопки

        # Подключаем сигнал нажатия кнопки к функции
        self.button.clicked.connect(self.on_button_click)

    @staticmethod
    def on_button_click():
        print("Кнопка нажата!")

# Запуск приложения
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
