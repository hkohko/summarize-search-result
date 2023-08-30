import nltk
from app.text_generator import get_sample_text
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.text_rank import TextRankSummarizer

nltk.download("punkt")
LANGUAGE = "english"


def textrank_summarizer():
    stemmer = Stemmer(LANGUAGE)
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    num_summary_sentence = 3
    for text in get_sample_text():
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        for sentence in summarizer(parser.document, num_summary_sentence):
            print(f"\n{str(sentence)}\n")


