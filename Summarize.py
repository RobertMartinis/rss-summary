from bs4 import BeautifulSoup
import requests
import sys
sys.path.append('../tools')
from constants import NUM_THREADS
from tools.ArticleSummarizer import ArticleSummarizer
import concurrent

"""
This class fetches articles from an RSS feed, and summarizes them.
"""

class Summarize:
    """
    Initializes the class with a RSS feed URL, and a list of headers.

    Args:
        rss_url (str): The URL to the RSS feed.
        headers (list): A list of headers.
    """
    def __init__(self, rss_url, headers, name):
        self.url = rss_url
        self.headers = headers
        self.summaries = []
        self.article_contents = []
        self.name = name
        self.urls = []
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            with open(f'./{name}_feed.xml', 'wb') as f:
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
                new_description = self.soup.new_tag('description')
                new_description.string = ("No summary available.")
                a.append(new_description)
            str = a.find('link').text
            str.strip('<link>')
            self.urls.append(str)
        self.articles_dicts = [{'title':a.find('title').text,'link':a.link, 'description':a.find('description').text,'pubdate':a.find('pubDate').text} for a in self.feed]
        self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
        self.descriptions = [d['description'] for d in self.articles_dicts if 'description' in d]
        self.pub_dates = [d['puDdate'] for d in self.articles_dicts if 'pubDate' in d]

    """
    Fetches the articles contents from the URLs, and appends them to the list of articles.
    """
    def __fetch_articles(self, url):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, features='html.parser')
        article = soup.find('article')
        if article == None:
            return
        paragraphs = article.find_all('p')
        paragraphs = [p.text for p in paragraphs]
        paragraphs = paragraphs[2:]
        self.article_contents.append(paragraphs)

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
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            executor.map(self.__fetch_articles, self.urls)
        self.__summarize_articles()
        return self.summaries
