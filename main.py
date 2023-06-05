#!/usr/bin/env python3
import os
import importlib
from constants import URLS
from tools.ParseXML import ParseXML

# User agent to use when fetching the RSS-feed.
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}

'''
    This function returns a list of all the websites in the websites folder.
'''
def get_websites():
    folder_path = './websites'
    websites = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Check if the item is a file and ends with .py extension
        if os.path.isfile(item_path) and item.endswith(".py"):
            # Extract the module name by removing the .py extension
            website_name = item[:-3]
            websites.append(website_name)
    return websites

"""
    This is the main file of the project. It fetches the RSS-feeds, summarizes the
    articles, and writes the summaries to the XML-file.
"""
if __name__ == '__main__':
    websites = get_websites()
    urls = URLS
    for website in websites:
        module = importlib.import_module('websites.' + website)
        website_class = getattr(module, website.capitalize())
        website_class = website_class(urls[website], headers)
        website_class.fetch()
        summaries = website_class.summaries
        parser = ParseXML(summaries, f'./{website}_feed.xml')
        parser.write()
