from send_to_kindle.downloader import get_article
from send_to_kindle.downloader.article_downloader import extract_content
import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from unittest.mock import patch
import requests_mock


@pytest.fixture
def medium_url():
    return "https://medium.com/@antonio.feregrino/lorem-ipsum-cb19745555ea"



@pytest.mark.parametrize(['input', 'expected'], [
    ("html/medium.html", "html/medium-article.html"),
    ("html/medium_subtitled.html", "html/medium_subtitled-article.html")
])
def test_extract_content(get_file_content, input, expected):
    content = get_file_content(input)
    original_soup = BeautifulSoup(content)

    content_article = get_file_content(expected)
    article_soup = BeautifulSoup(content_article, 'lxml')

    result = extract_content(original_soup)
    assert result == article_soup.find('article').prettify().strip()


def test_get_article(get_file_content, medium_url):
    content = get_file_content("html/medium.html")
    with requests_mock.mock() as mocked_requests:
        mocked_requests.get(medium_url, text=content)
        with patch(
            "send_to_kindle.downloader.article_downloader.extract_content",
            return_value="the_content",
        ):
            article = get_article(medium_url)

            assert article.title == "Lorem Ipsum - Antonio Feregrino - Medium"
            assert article.content == "the_content"
