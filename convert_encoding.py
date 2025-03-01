import os

from PyQt5.QtWidgets import QApplication


class FileTextEncoding:
    def __init__(self):
        self.encoding_utf = "utf-8"
        self.encoding_win = "windows-1251"

    def encode(self, input_file):
        # Читаем и конвертируем
        with (open(input_file, "r", encoding=self.encoding_win) as infile,
              open('temp_file.txt', "w", encoding=self.encoding_utf) as outfile):
            outfile.write(infile.read())

        # Заменяем оригинальный файл новым
        os.replace('temp_file.txt', input_file)
        # os.remove('temp_file.txt')
        print(f"Файл {input_file} успешно перекодирован в UTF-8")


if __name__ == '__main__':
    FileTextEncoding().encode('/Users/evgeniy/Desktop/windows_encoding.txt')

