import requests
from bs4 import BeautifulSoup
from send_to_kindle.downloader.article import Article
from send_to_kindle.downloader.content_extractor import MediumExtractor

def extract_content(url, soup):
    content_extractor = MediumExtractor()
    return content_extractor.extract(soup)

def get_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    article = Article(url=url, title=soup.title.text.strip())
    article.content = extract_content(url, soup)
    return article
