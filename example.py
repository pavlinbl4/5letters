from complete_word_app import get_letter_settings

word = "привет"
results = get_letter_settings()

print("Результаты:")
print(f"Yes: {results['yes_set']}")
print(f"No: {results['no_set']}")
print(f"Positions: {results['result_dict']}")
