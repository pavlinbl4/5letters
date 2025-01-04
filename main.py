# from complete_word_app import get_letter_settings
from nouns_from_csv import read_column

dictionary = read_column('nouns_5.csv')


def find_words_with_letters(letter_positions, unused_letters, used_letters_no_position):
    # список возможных слов
    possible_words = []

    # перебираю слова в словаре
    for word in dictionary:
        match = True

        # проверяю слово на буквы, которых не может быть в слове
        for letter in word:
            if letter in unused_letters:
                match = False
                break

        # проверяю слово на наличие в нем угаданных букв
        if match:
            count = 0
            for letter in used_letters_no_position:
                if letter in word:
                    count += 1
            if count < len(used_letters_no_position):
                match = False

        # проверю слово на наличие в нем угаданной буквы с известной позицией в слове
        if match:
            for position, letter in letter_positions.items():
                # if position < 0 or position >= word_length or word[position] != letter:
                if word[position] != letter:
                    match = False
                    break

        if match:
            possible_words.append(word)

    # возвращаю список возможный слов
    return possible_words


if __name__ == '__main__':

    check_new_word = get_letter_settings()

    # словарь угаданных с позицией букв
    letter_positions = {}

    # множество букв, которых не может быть в слове
    unused_letters = set()

    # множество букв, который есть в слове
    used_letters_no_position = set()


    # цикл для вызова графического интерфейса
    stop_kran = 1
    while stop_kran != ' ':
        new_letter_positions = check_new_word['result_dict']
        new_unused_letters = check_new_word['no_list']
        new_used_letters = check_new_word['yes_list']

        letter_positions.update(new_letter_positions)

        unused_letters.update(new_unused_letters)

        used_letters_no_position.update(new_used_letters)
        unused_letters = unused_letters.difference(used_letters_no_position)

        result = find_words_with_letters(letter_positions, unused_letters, used_letters_no_position)

        print(f'{unused_letters  = }')
        print(f'{used_letters_no_position = }')
        print(f'{letter_positions = }')
        print("ВОЗМОЖНЫЕ ВАРИАНТЫ СЛОВ")
        print([word for word in result])
        stop_kran = input('Чтоб продолжать нажмите любую клавишу\n'
                          'Для остановки - введите пробел\n ')

        check_new_word = get_letter_settings()
