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

# удален блок main
