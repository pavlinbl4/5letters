"""
программа на PyQt6 для выбора файла на компьютере
"""

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget


class FileSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор файла")
        # self.setGeometry(100, 100, 400, 300) создает окно с указанными отступами
        self.setFixedSize(400, 200)  # создает окно в центре экрана
        self.selected_file_path = None

        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Создаем кнопку
        self.button = QPushButton("Выбрать файл", self)
        self.button.clicked.connect(self.select_file)
        layout.addWidget(self.button)

    def select_file(self):
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Все файлы (*.*)"
        )

        if file_path:
            self.selected_file_path = file_path
            self.close()

    def get_selected_file_path(self):
        return self.selected_file_path


def get_file_path():
    """
    Функция для получения пути к выбранному файлу.
    
    Returns:
        str: путь к выбранному файлу или None, если файл не был выбран
    """
    app = QApplication(sys.argv)
    selector = FileSelector()
    selector.show()
    app.exec()
    return selector.get_selected_file_path()


# Пример использования:
if __name__ == '__main__':
    file_path = get_file_path()
    if file_path:
        print(f"Выбранный файл: {file_path}")
    else:
        print("Файл не был выбран")
