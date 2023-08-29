import spacy
from spacy import language
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from app.locations import Directories

stopword = list(STOP_WORDS)

with open(Directories.SAMPLE_TEXT.joinpath("text_1.txt"), encoding="utf-8") as file:
    sample_text = file.read()

nlp: language.Language = spacy.load("en_core_web_sm")
docx = nlp(sample_text)


def tokenize_word(docx):
    # token.text = tokenize, and convert to string.
    # allows for string methods to be applied to it
    mytoken = [token.text.lower() for token in docx]
    return mytoken


def tokenize_sents(docx):
    list_of_sentence = [sent for sent in docx.sents]
    return list_of_sentence


def remove_stopwords(docx):
    filter_stopword = []
    for word in docx:
        text_token = word.text
        if text_token not in stopword:
            filter_stopword.append(word)
    return filter_stopword


def get_word_frequency(filter_stopword: list):
    word_frequency = {}
    for word in filter_stopword:
        text_token = word.text
        if text_token not in word_frequency.keys():
            word_frequency[text_token] = 1
        else:
            word_frequency[text_token] += 1
    return word_frequency


def word_weights(word_frequency: dict[str]):
    word_max_freq = max(word_frequency.values())
    weighted_words = {}
    for word in word_frequency.keys():
        weighted_words[word] = (
            word_frequency.get(word) / word_max_freq
        )  # division elapsed time is pretty awful
    return weighted_words


def main():
    filtered_stopwords = remove_stopwords(docx)
    word_freq = get_word_frequency(filtered_stopwords)
    weighted_words = word_weights(word_freq)


if __name__ == "__main__":
    print(tokenize_word(docx))
