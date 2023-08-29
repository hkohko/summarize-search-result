import spacy
from heapq import nlargest
from spacy.language import Language
from spacy.tokens.doc import Doc
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from app.locations import Directories

stopword = list(STOP_WORDS)

with open(Directories.SAMPLE_TEXT.joinpath("text_1.txt"), encoding="utf-8") as file:
    sample_text = file.read()

nlp: Language = spacy.load("en_core_web_sm")
docx: Doc = nlp(sample_text)


def tokenize_word(docx):
    # token.text = tokenize, and convert to string.
    # allows for string methods to be applied to it
    mytoken = [token.text.lower() for token in docx]
    return mytoken


def tokenize_sents(docx: Doc):
    list_of_sentence = [sent.text.lower() for sent in docx.sents]
    return list_of_sentence


def remove_stopwords(docx: Doc):
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


def rank_score_sents(docx: Doc, weighted_words: dict[str]):
    score = {}
    sents_list = tokenize_sents(docx)
    words_list = tokenize_word(docx)
    for sent in sents_list:
        for word in words_list:
            if word in weighted_words.keys() and len(sent.split(" ")) < 30:
                if sent not in score.keys():
                    score[sent] = weighted_words[word]
                else:
                    score[sent] += weighted_words[word]
    return score


def nlargest_summary(score: dict):
    nlargest_summary = nlargest(7, score, key=score.get)
    return nlargest_summary


def main(docx: Doc):
    filtered_stopwords = remove_stopwords(docx)
    word_freq = get_word_frequency(filtered_stopwords)
    weighted_words = word_weights(word_freq)
    score = rank_score_sents(docx, weighted_words)
    prelim_summary = nlargest_summary(score)
    print(prelim_summary)


if __name__ == "__main__":
    main(docx)
