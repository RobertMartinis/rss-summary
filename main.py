#!/usr/bin/env python3
from websites.aftonbladet import Aftonbladet
from constants import URLS
from tools.ParseXML import ParseXML

# User agent to use when fetching the RSS-feed.
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

"""
    This is the main file of the project. It fetches the RSS-feed, summarizes the
    articles, and writes the summaries to the XML-file.
"""
if __name__ == '__main__':
    urls = URLS
    aftonbladet = Aftonbladet(urls['aftonbladet'], headers)
    aftonbladet.fetch()
    summaries = aftonbladet.summaries
    parser = ParseXML(summaries, './feed.xml')
    parser.write()
