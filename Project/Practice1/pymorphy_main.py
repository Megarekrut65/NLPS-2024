from data import WORDS
import pymorphy3


def main():
    analyzer = pymorphy3.analyzer.MorphAnalyzer(lang="uk")
    for i, word in enumerate(WORDS):
        res = analyzer.parse(word)
        for item in res:
            forms = item.lexeme
            print(f"\n{i + 1})\nСлово: {item.word}\nЛема: {item.normal_form}\n"
                  f"Ознаки: {item.tag}\n\nФорми слова: ")
            for form in forms:
                print("\t", form.word)

if __name__ == "__main__":
    main()