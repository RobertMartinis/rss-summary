#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from googletrans import Translator
from constants import NUM_THREADS
"""
    This class translates the articles to English. If we use English, we can import
    stopwords to get a better summary. However, the summaries are good enough,
    as of now.
"""
class Translate:
    def __init__(self, articles):
        self.articles = articles
        self.translated_articles = []

        def __translate_articles(self):
            try:
                with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                    self.res = executor.map(Translator().translate, self.articles)
                for r in self.res:
                    self.translated_articles.append(r.text)
            except Exception as e:
                print(e)

        def translate(self):
            self.__translate_articles()
            return self.translated_articles
