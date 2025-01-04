import os

input_file = "/Users/evgeniy/Documents/russian.txt"
temp_file = "temp_utf8.txt"

# Читаем и конвертируем
with open(input_file, "r", encoding="windows-1251") as infile, \
     open(temp_file, "w", encoding="utf-8") as outfile:
    outfile.write(infile.read())

# Заменяем оригинальный файл новым
os.replace(temp_file, input_file)

print(f"Файл {input_file} успешно перекодирован в UTF-8")