import os

import stanza
from string import punctuation

class Word:
    def __init__(self, word, count):
        self.word = word
        self.count = count

    def __str__(self):
        return f"{self.word}\t{self.count}"

    def __lt__(self, other):
        return self.count < other.count

def read_all(folder):
    if not os.path.exists(folder):
        return ""

    files = os.listdir(folder)
    text = ""
    for filename in files:
        file = open(folder + "/"+ filename, errors="ignore", encoding="utf-8")
        text += file.read().strip()
        file.close()

    return text

def read_words(filename):
    if not os.path.exists(filename):
        return []

    file = open(filename, errors="ignore", encoding="utf-8")
    words = file.readlines()
    words = [word.strip() for word in words]

    file.close()

    return words

def save_tsv(filename, words):
    file = open(filename, "w", errors="ignore", encoding="utf-8")
    for word in words:
        file.write(f"{word}\n")
    file.close()

def remove_stop_words(words):
    stop_words = read_words("stopwords_ua.txt")

    result = {}
    punctuation_ = punctuation + "“»«”—–"
    for word in words:
        if not(word in stop_words or word in punctuation_ or word.isdigit()):
            result[word] = words[word]
    return result

def get_lemmas(text):
    stanza.download("uk")
    nlp = stanza.Pipeline(lang="uk")
    doc = nlp(text)

    words = {}
    for sentence in doc.sentences:
        for word in sentence.words:
            key = word.lemma
            if words.get(key):
                words[key].count += 1
            else:
                words[key] = Word(key, 1)
    return words

def sort_by_count(words):
    return sorted(list(words.values()), reverse=True)

def create_words_from_texts():
    folder = input("Enter folder with texts: ")
    text = read_all(folder)
    words = get_lemmas(text)
    save_tsv("result/raw_words.tsv", sort_by_count(words))

    words = remove_stop_words(words)
    sorted_words = sort_by_count(words)
    save_tsv("result/words.tsv", sorted_words)
    save_tsv("result/frequent_words.tsv", [word.word for word in sorted_words[:100]])

    print("Result saved in result folder")

def mark_words():
    filename = input("Enter filename with words: ")
    words = read_words(filename)
    result = []
    print("Enter mark from -2 to 2:")
    for word in words:
        try:
            mark = int(input(f"{word}: "))
            result.append(f"{word}\t{mark}")
        except:
            pass
    save_tsv("result/result.tsv", result)
    print("Result saved in result/result.tsv")

def main():
    answer = input("generate - to create file of most frequent words in text\n"
                   "mark - to mark words from file\n").strip().lower()
    if answer == "generate":
        create_words_from_texts()
    elif answer == "mark":
        mark_words()

if __name__ == "__main__":
    main()