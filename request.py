#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

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

    @property
    def urls(self):
        return self.urls

    @urls.setter
    def urls(self, value):
        self.urls = value

    @property
    def titles(self):
        return self.titles

    @titles.setter
    def titles(self, value):
        self.titles = value

    @property
    def descriptions(self):
        return self.descriptions

    @descriptions.setter
    def descriptions(self, value):
        self.descriptions = value

    @property
    def pub_dates(self):
        return self.pub_dates

    @pub_dates.setter
    def pub_dates(self, value):
        self.pub_dates = value

class FetchArticles:
    def __init__(self):
        self.feed = ReadRss('https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/', headers)
if __name__ == '__main__':

    feed = ReadRss('https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/', headers)
    print(feed.descriptions)
