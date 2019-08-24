from bs4 import BeautifulSoup
from send_to_kindle.downloader.article import Article


def test_to_html(get_soup):
    template = get_soup("html/article-template.html")
    content = get_soup("html/medium-article.html").find("article")
    result = get_soup("html/article-result.html")

    article = Article("t.co", "Templated article", template)
    article.content = content
    html = article.to_html()

    assert html.prettify() == result.prettify()
