import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def create_gui(existing_yes_set, existing_no_list):
    # Результаты для возврата
    yes_set = set(existing_yes_set)
    no_list = existing_no_list.copy()
    result_dict = {}

    word = ""  # Переменная для хранения слова

    def center_window(window, width, height):
        """Размещает окно по центру экрана."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_confirm_word():
        nonlocal word
        word = word_entry.get()
        if len(word) == 5:  # Проверка длины слова
            root.destroy()
            create_second_window(word)
        else:
            messagebox.showerror("Ошибка", "Слово должно состоять ровно из 5 букв.")

    def create_second_window(word):
        def on_confirm_results():
            for i, letter in enumerate(word):
                choice = choice_vars[letter, i].get()
                number = int(num_vars[letter, i].get())
                if choice == "Yes":
                    yes_set.add(letter)
                elif choice == "No" and letter not in yes_set:
                    no_list.append(letter)
                if number > 0:
                    result_dict[number - 1] = letter  # Значением ключа будет на 1 меньше
            second_window.destroy()

        def update_yes_set_and_dict(letter, index):
            number = int(num_vars[letter, index].get())
            if number > 0:
                for i, l in enumerate(word):
                    if l == letter:
                        choice_vars[l, i].set("Yes")
                result_dict[number - 1] = letter  # Значением ключа будет на 1 меньше

        second_window = tk.Tk()
        second_window.title("Настройка букв")
        center_window(second_window, 600, 500)
        second_window.resizable(False, False)

        # Создаем заголовки столбцов
        font = ("Arial", 16)
        tk.Label(second_window, text="Буква", font=font).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(second_window, text="Выбор (Yes/No)", font=font).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(second_window, text="Цифра (1-5)", font=font).grid(row=0, column=2, padx=10, pady=10)

        choice_vars = {}
        num_vars = {}

        for i, letter in enumerate(word):
            tk.Label(second_window, text=letter, font=font).grid(row=i + 1, column=0, padx=10, pady=5)

            choice_var = tk.StringVar(value="No")
            choice_menu = ttk.Combobox(second_window, textvariable=choice_var, values=["Yes", "No"], state="readonly", font=font)
            choice_menu.grid(row=i + 1, column=1, padx=10, pady=5)
            choice_vars[letter, i] = choice_var

            num_var = tk.StringVar(value="0")
            num_menu = ttk.Combobox(second_window, textvariable=num_var, values=[str(x) for x in range(6)], state="readonly", font=font)
            num_menu.grid(row=i + 1, column=2, padx=10, pady=5)
            num_vars[letter, i] = num_var

            num_menu.bind("<<ComboboxSelected>>", lambda e, l=letter, idx=i: update_yes_set_and_dict(l, idx))

        confirm_button = tk.Button(second_window, text="Подтвердить", command=on_confirm_results, font=font)
        confirm_button.grid(row=len(word) + 1, column=1, columnspan=2, pady=20)

        reset_button = tk.Button(second_window, text="Сброс", command=lambda: reset_choices(), font=font)
        reset_button.grid(row=len(word) + 2, column=1, columnspan=2, pady=10)

        def reset_choices():
            for var in choice_vars.values():
                var.set("No")
            for var in num_vars.values():
                var.set("0")
            yes_set.clear()
            result_dict.clear()

        second_window.mainloop()

    # Первое окно
    root = tk.Tk()
    root.title("Введите слово")
    center_window(root, 500, 300)
    root.resizable(False, False)

    font = ("Arial", 18)
    tk.Label(root, text="Введите слово (ровно 5 букв):", font=font).pack(pady=20)
    word_entry = tk.Entry(root, font=font, width=20)
    word_entry.pack(pady=10)

    confirm_button = tk.Button(root, text="Подтвердить", command=on_confirm_word, font=font)
    confirm_button.pack(pady=10)

    reset_button = tk.Button(root, text="Сброс", command=lambda: word_entry.delete(0, tk.END), font=font)
    reset_button.pack(pady=10)

    root.mainloop()

    return list(yes_set), no_list, result_dict

# Запуск функции
existing_yes = []
existing_no = []
results = create_gui(existing_yes, existing_no)
print("Yes List:", results[0])  # Теперь это уникальные буквы
print("No List:", results[1])
print("Result Dict:", results[2])