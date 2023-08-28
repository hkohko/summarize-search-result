import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from app.locations import Directories

stopword = list(STOP_WORDS)

with open(Directories.SAMPLE_TEXT.joinpath("text_1.txt"), encoding="utf-8") as file:
    sample_text = file.read()

nlp = spacy.load("en_core_web_sm")
docx = nlp(sample_text)
mytoken = [token.text for token in docx]

word_frequency = {}
filter_stopword = []

for word in docx:
    text_token = word.text
    if text_token not in stopword:
        filter_stopword.append(word)

for word in filter_stopword:
    text_token = word.text
    if text_token not in word_frequency.keys():
        word_frequency[text_token] = 1
    else:
        word_frequency[text_token] += 1
        
print(word_frequency)
