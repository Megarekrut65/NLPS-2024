from data import WORDS
import stanza


def main():
    stanza.download("uk")
    nlp = stanza.Pipeline("uk")
    res = nlp("грати")
    print(res)

if __name__ == "__main__":
    main()