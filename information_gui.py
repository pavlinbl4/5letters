from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QMainWindow
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 300)
        self.setWindowTitle("Пример кнопки PyQt6")



def show_info():
    """Функция для вызова GUI и получения результатов."""
    app = QApplication.instance()
    word_window = MainWindow()
    word_window.show()
    app.exec_()


if __name__ == '__main__':
    show_info()
