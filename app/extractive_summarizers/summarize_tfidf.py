from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import tokenize
from app.text_generator import get_sample_text
import numpy as np

tfid_vec = TfidfVectorizer()
num_summary_sents = 3


def get_tfidf(text: str):
    sentences = tokenize_sentence(text)
    words_tfidf = tfid_vec.fit_transform(sentences)
    sent_sum = words_tfidf.sum(axis=1)
    significant_sent = np.argsort(sent_sum, axis=0)[::-1]
    return significant_sent


def tokenize_sentence(text: str):
    return tokenize.sent_tokenize(text)


for text in get_sample_text():
    significant_sent = get_tfidf(text)
    sentences = tokenize_sentence(text)
    for i in range(0, len(sentences)):
        if i in significant_sent[:num_summary_sents]:
            print(sentences[i])

