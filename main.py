#!/usr/bin/env python3
from constants import URLS
from tools.ParseXML import ParseXML
from Summarize import Summarize

# User agent to use when fetching the RSS-feed.
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

if __name__ == '__main__':
    # TODO: Multithread this loop.
    for website in URLS:
        summarizer = Summarize(URLS[website], headers, website)
        summarizer.fetch()
        summaries = summarizer.summaries
        parser = ParseXML(summaries, f'./{website}_feed.xml')
        parser.write()
