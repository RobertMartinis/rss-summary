#!/usr/bin/env python3
from constants import NUM_THREADS, URLS
from tools.ParseXML import ParseXML
from Summarize import Summarize
from multiprocessing.pool import ThreadPool

# User agent to use when fetching the RSS-feed.
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

def summarize_articles(urls):
    name = urls[0]
    rss_url = urls[1]
    summarizer = Summarize(rss_url, headers, name)
    summarizer.fetch()
    summaries = summarizer.summaries
    parser = ParseXML(summaries, f'./{name}_feed.xml')
    parser.write()

if __name__ == '__main__':
    thread_data = []
    for website in URLS:
        sublist = []
        sublist.append(website)
        sublist.append(URLS[website])
        thread_data.append(sublist)
    with ThreadPool(NUM_THREADS) as pool:
        pool.map(summarize_articles, thread_data)
