from nouns_from_csv import read_column
from spacy_tool import lemmatize_words_list


def find_words_with_letters(dictionary, word_length, letter_positions):
    """
    Находит слова в словаре заданной длины, содержащие указанные буквы на заданных позициях.

    :param dictionary: список слов
    :param word_length: длина искомых слов
    :param letter_positions: словарь {позиция: буква}, где позиция - индекс (начиная с 0)
    :return: список слов, подходящих под условия
    """
    result = []

    for word in dictionary:
        # Проверяем длину слова
        if len(word) != word_length:
            continue
        # Проверяем буквы на заданных позициях
        match = True
        for position, letter in letter_positions.items():

            # if position < 0 or position >= word_length or word[position] != letter:
            if word[position] != letter:
                match = False
                break

        if match:
            result.append(word)

    return result


if __name__ == '__main__':
    # Пример использования:
    # Загружаем словарь из текстового файла
    # with open("/Users/evgeniy/Documents/russian.txt", encoding="utf-8") as f:
    #     dictionary = [line.strip() for line in f]

    dictionary = read_column('nouns.csv')

    word_length = 5
    letter_positions = {4: 'р', 1: 'у', 3: 'о', }

    result = find_words_with_letters(dictionary, word_length, letter_positions)
    print([word for word in lemmatize_words_list(result) if len(word) == 5])
    # print("Найденные слова:", result)
