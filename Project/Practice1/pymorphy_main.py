from data import WORDS
import pymorphy3


def main():
    res = pymorphy3.analyzer.MorphAnalyzer(lang="uk").parse("грати")
    print(res)

if __name__ == "__main__":
    main()