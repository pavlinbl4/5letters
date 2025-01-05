import spacy

# Загрузка русской языковой модели
nlp = spacy.load('ru_core_news_md')

def lemmatize_words_list(words_list: list):
    # Используем множество для хранения уникальных лемм
    lemma_collection = {token.lemma_ for word in words_list for token in nlp(word) if token.pos_ == 'NOUN' and len(token) == 5}
    return lemma_collection


if __name__ == '__main__':

# Пример списка слов
    words = ["бегут", "собаки", "цифры", "играть", "веток", "играть", 'гости']

    # Обработка списка слов
    result = lemmatize_words_list(words)
    print(result)
    # assert result == ['бежать', 'собака', 'красивый', 'играть', 'веселый']

