# RSS-summary
Reads an RSS-feed, captures all the articles in the link-tags, and summarizes them in a few sentences. The summaries are then written to the respective articles description tag. This allows you to read
summaries of articles directly in your RSS reader, instead of having to open the article in your browser.

![showcase](https://github.com/RobertMartinis/rss-summary/assets/57859068/4bf694ca-d81d-4e13-8fea-619fcea5a23e)

# Adding RSS-Feeds
To add an RSS-feed, append the name of the RSS-feed together with it's url in the URL-dictionary contained in `constants.py`.
For example: `URLS =  {'BBC': 'http://feeds.bbci.co.uk/news/world/rss.xml'}`.

# Change number of summarized sentences
By default, the summary consists of 5 sentences. This can be changed in `constants.py` by changing the `SENTENCES` variable to the desired number of sentences.
