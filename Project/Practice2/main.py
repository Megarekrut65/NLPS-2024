import stanza
from data import text

stanza.download("uk")
def main():
    nlp = stanza.Pipeline(lang="uk", processors="tokenize,ner")

    doc = nlp(text)

    for sentence in doc.sentences:
        for ent in sentence.ents:
            print(f"Сутність: {ent.text}\tТип: {ent.type}")

if __name__ == "__main__":
    main()