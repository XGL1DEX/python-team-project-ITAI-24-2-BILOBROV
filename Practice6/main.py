import os
import re
from collections import Counter
from pathlib import Path

# Базовий список українських стоп-слів
DEFAULT_STOP_WORDS = {
    "і", "та", "а", "але", "чи", "або", "як", "що", "це", "в", "у", "на", "під", 
    "за", "до", "з", "із", "зі", "для", "про", "при", "від", "перед", "над", 
    "не", "ні", "так", "й", "він", "вона", "воно", "вони", "я", "ми", "ви", "ти"
}

def analyze_text(text, stop_words=None):
    if stop_words is None:
        stop_words = DEFAULT_STOP_WORDS

    total_chars = len(text)
    chars_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\r", ""))

    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])

    clean_text = text.lower()
    words = re.findall(r'\b[а-яієїґьa-z\-]+\b', clean_text)
    total_words = len(words)

    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    most_common_words = word_counts.most_common(5)

    return {
        "total_characters": total_chars,
        "characters_no_spaces": chars_no_spaces,
        "total_words": total_words,
        "total_sentences": sentence_count,
        "most_common_words": most_common_words
    }

def analyze_file(file_path):
    if not os.path.exists(file_path):
        print(f"Помилка: Файл за шляхом '{file_path}' не знайдено.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        
        results = analyze_text(text_content)

        print(f"=== РЕЗУЛЬТАТИ АНАЛІЗУ ФАЙЛУ: {os.path.basename(file_path)} ===")
        print(f"Кількість символів (з пробілами): {results['total_characters']}")
        print(f"Кількість символів (без пробілів): {results['characters_no_spaces']}")
        print(f"Загальна кількість слів: {results['total_words']}")
        print(f"Кількість речень: {results['total_sentences']}")
        print("\nТоп-5 найчастіших слів (без стоп-слів):")
        for word, count in results['most_common_words']:
            print(f"  - '{word}': {count} раз(и)")

    except Exception as e:
        print(f"Сталася помилка при читанні файлу: {e}")

if __name__ == "__main__":

    script_dir = Path(__file__).resolve().parent

    filename = "text_to_analyze.txt"
    full_path = script_dir / filename

    analyze_file(full_path)