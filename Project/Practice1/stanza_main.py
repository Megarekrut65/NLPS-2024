from data import WORDS
import stanza


def main():
    #stanza.download("uk")
    nlp = stanza.Pipeline("uk")
    for i, word in enumerate(WORDS):
        res = nlp(word)

        for sen in res.sentences:
            for word_ in sen.words:
                print(f"{i+1})\nСлово: {word_.text}\nЛема: {word_.lemma}\nЧастина мови: {word_.pos}\n"
                      f"Ознаки: {word_.feats}\n")

if __name__ == "__main__":
    main()