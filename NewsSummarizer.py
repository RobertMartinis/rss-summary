from bs4 import BeautifulSoup
from config import HEADERS, WEBSITES, NUM_SENTENCES, PATH
import requests
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
import xml.etree.ElementTree as ET

def __add_summaries_to_feed( summaries, xml):
        tree = ET.parse(xml)
        description = tree.findall("channel/item/description")

        for i in range(len(summaries)):
            sentences = summaries[i]
            summary = ""
            for j, sentence in enumerate(sentences):
                string = str(sentence)
                string = f" {j+1}) " + string
                string = string + " \n"
                string = "<br>" + string + "<\\br>"
                summary += string
            description[i].text = summary


            tree.write(xml)
    
def write_summary():
    for website in WEBSITES:
        try:
            response = requests.get(website['url'], headers=HEADERS)
            response.raise_for_status()
            with open(f"./{website['name']}_feed.xml", "wb") as f:
                f.write(response.content)
            soup = BeautifulSoup(response.text, features="xml")
            
            
            feed_items = soup.find_all('item') 

            # Get the links to the articles from the RSS-feed
            links = []
            for item in feed_items:
                link = item.find('link').text 
                links.append(link)
            
            articles = []
            
            # Fetch the content for each article
            for link in links:
                response = requests.get(link, headers=HEADERS)
                article_soup = BeautifulSoup(response.text, features='html5lib')
                article = article_soup.find('article')
                paragraphs = article.find_all('p', recursive=False)

                # Get text from each <p>
                article_text = "\n\n".join(
                    p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
                )

                articles.append(article_text)
                
            # Summarize the contents using sumy

            summarized_articles = []
            
            for article in articles:
                
                article_language = website['language']
                stemmer = Stemmer(article_language)
                summarizer = Summarizer(stemmer)
                parser = PlaintextParser.from_string(article, Tokenizer(article_language))
                summarized_article = summarizer(parser.document, NUM_SENTENCES)
                summarized_articles.append(summarized_article)
            
            
            __add_summaries_to_feed(summarized_articles, f"{PATH}{website['name']}_feed.xml")
            
        except requests.RequestException as e:
            print(e)

