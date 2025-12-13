#!/usr/bin/env python3

# Number of sentences to summarize to.
NUM_SENTENCES = 5
# The URLS to the RSS-feeds.
WEBSITES = [
    {
        "name": "Aftonbladet",
        "url": "https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/",
        "language": "swedish",
    },
]
# The Path to where the summarized RSS-feed should be written.
PATH = "./"

# User agent to use when fetching the RSS-feed.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
}
