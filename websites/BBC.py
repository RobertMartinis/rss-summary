#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys
sys.path.append('../tools')
from concurrent.futures import ThreadPoolExecutor
from constants import NUM_THREADS
from tools.Summarizer import ArticleSummarizer

"""
This class fetches articles from Aftonbladet's RSS feed, and summarizes them.
"""

class Bbc:
    """
    Initializes the class with a RSS feed URL, and a list of headers.

    Args:
        rss_url (str): The URL to the RSS feed.
        headers (list): A list of headers.
    """
    def __init__(self, rss_url, headers):
        self.url = rss_url
        self.headers = headers
        self.summaries = []
        self.article_contents = []
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            with open('./BBC_feed.xml', 'wb') as f:
                f.write(self.r.content)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        try:
            self.soup = BeautifulSoup(self.r.text, features='xml')
        except Exception as e:
            print('Could not parse xml: ', self.url)
            print(e)
        self.feed = self.soup.findAll('item')
        for a in self.feed:
            if a.description is None:
                self.feed.remove(a)
                continue
            str = a.find('link').text
            str.strip('<link>')
            a.link = str
        self.articles_dicts = [{'title':a.find('title').text,'link':a.link, 'description':a.find('description').text,'pubdate':a.find('pubDate').text} for a in self.feed]
        self.urls = [d['link'] for d in self.articles_dicts if 'link' in d]
        self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
        self.descriptions = [d['description'] for d in self.articles_dicts if 'description' in d]
        self.pub_dates = [d['puDdate'] for d in self.articles_dicts if 'pubDate' in d]

    """
    Fetches the articles contents from the URLs, and appends them to the list of articles.
    """
    def __fetch_articles(self):
        try:
            with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                self.res = executor.map(requests.get, self.urls)
            for r in self.res:
                soup = BeautifulSoup(r.text, features='html.parser')
                article = soup.find('article')
                if article == None:
                    continue
                paragraphs = article.find_all('p')
                paragraphs = [p.text for p in paragraphs]
                paragraphs = paragraphs[2:]
                self.article_contents.append(paragraphs)
        except Exception as e:
            print(e)

    """
    Summarizes the articles.
    """
    def __summarize_articles(self):
        summarizer = ArticleSummarizer(self.article_contents)
        self.summaries = summarizer.summarize()

    """
    Fetches the articles, and summarizes them.
    """
    def fetch(self):
        self.__fetch_articles()
        self.__summarize_articles()
        return self.summaries
