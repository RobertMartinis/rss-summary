#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
from googletrans import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
import nltk

#nltk.download('punkt')

SENTENCES = 5
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

numThreads = 6
class ReadRss:

    def __init__(self, rss_url, headers):

        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        try:
            self.soup = BeautifulSoup(self.r.text, features='xml')
        except Exception as e:
            print('Could not parse xml: ', self.url)
            print(e)
        self.articles = self.soup.findAll('item')
        for a in self.articles:
            str = a.find('link').text
            str.strip('<link>')
            a.link = str
        self.articles_dicts = [{'title':a.find('title').text,'link':a.link, 'description':a.find('description').text,'pubdate':a.find('pubDate').text} for a in self.articles]
        self.urls = [d['link'] for d in self.articles_dicts if 'link' in d]
        self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
        self.descriptions = [d['description'] for d in self.articles_dicts if 'description' in d]
        self.pub_dates = [d['puDdate'] for d in self.articles_dicts if 'pubDate' in d]

    # @property
    # def urls(self):
    #     return self.urls

    # @urls.setter
    # def urls(self, value):
    #     self.urls = value

    # @property
    # def titles(self):
    #     return self.titles

    # @titles.setter
    # def titles(self, value):
    #     self.titles = value

    # @property
    # def descriptions(self):
    #     return self.descriptions

    # @descriptions.setter
    # def descriptions(self, value):
    #     self.descriptions = value

    # @property
    # def pub_dates(self):
    #     return self.pub_dates

    # @pub_dates.setter
    # def pub_dates(self, value):
    #     self.pub_dates = value

class FetchArticles:
    def __init__(self, urls, headers):
        self.headers = headers
        self.urls = urls
        self.articles = []
        self.feed = ReadRss('https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/', headers)
        try:
            with ThreadPoolExecutor(max_workers=numThreads) as executor:
                self.res = executor.map(requests.get, self.urls)
            for r in self.res:
                soup = BeautifulSoup(r.text, features='html.parser')
                article = soup.find('article')
                paragraphs = article.find_all('p')
                paragraphs = [p.text for p in paragraphs]
                paragraphs = paragraphs[2:]
                self.articles.append(paragraphs)
        except Exception as e:
            print(e)


class TranslateArticles:
    def __init__(self, articles):
        self.articles = articles
        self.translated_articles = []
        try:
            with ThreadPoolExecutor(max_workers=numThreads) as executor:
                self.res = executor.map(Translator().translate, self.articles)
            for r in self.res:
                self.translated_articles.append(r.text)
        except Exception as e:
            print(e)

class GenerateSummary:
    def __init__(self, articles):
        self.articles = articles
        self.summaries = [[0]*SENTENCES]*len(articles)
        stemmer = Stemmer('swedish')
        summarizer = Summarizer(stemmer)
        for i in range(len(self.articles)):
            parser = PlaintextParser.from_string(self.articles[i], Tokenizer('swedish'))
            j = 0
            for sentence in (summarizer(parser.document, SENTENCES)):
                self.summaries[i][j] = sentence
                j += 1


if __name__ == '__main__':
    feed = ReadRss('https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/', headers)
    fetch = FetchArticles(feed.urls, headers)
    articles = fetch.articles;
    translate = TranslateArticles(articles)
    summary = GenerateSummary(articles)
