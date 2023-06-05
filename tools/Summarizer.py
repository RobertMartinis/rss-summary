#!/usr/bin/env python3
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from constants import SENTENCES


"""
This class summarizes articles using LSA (Latent Semantic Analysis).
"""
class ArticleSummarizer:
    """
    Initializes the class with a list of articles, and a empty list of summaries.
    The summaries are each for each article in the list of articles.
    """
    def __init__(self, articles):
        self.articles = articles
        self.summaries = [[len(self.articles)]]*(len(self.articles))

    """
    Summarizes each article in the list of articles, and returns the summaries.

    Returns:
        summaries (list): A list of summaries, each summary is a list of sentences.
    """
    def summarize(self):
        for i in range(len(self.articles)):
            stemmer = Stemmer('swedish')
            summarizer = Summarizer(stemmer)
            parser = PlaintextParser.from_string(self.articles[i], Tokenizer('swedish'))
            sentence = (summarizer(parser.document, SENTENCES))
            self.summaries[i] = sentence
        return self.summaries
