from send_to_kindle.downloader import get_article
from send_to_kindle.downloader.article_downloader import extract_content, load_template
import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from unittest.mock import patch
import requests_mock
from send_to_kindle.downloader.content_extractor import ContentExtractor


@pytest.fixture
def medium_url():
    return "https://medium.com/@antonio.feregrino/lorem-ipsum-cb19745555ea"


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        ("html/medium.html", "html/medium-article.html"),
        ("html/medium_subtitled.html", "html/medium_subtitled-article.html"),
    ],
)
def test_extract_content(get_soup, input, expected):
    original_soup = get_soup(input)
    article_soup = get_soup(expected)

    result = extract_content(original_soup)
    stringified_result = result.prettify().strip()
    assert stringified_result == article_soup.find("article").prettify().strip()


@pytest.mark.parametrize(
    ["input", "expected"],
    [("html/article-images.html", "html/article-images-replaced.html")],
)
def test_get_replace_images(get_soup, input, expected):
    original_soup = get_soup(input)
    article_soup = get_soup(expected)

    epxected_replacements = {
        "4aa727af33567fe99b76b5a299d23df5": "https://miro.medium.com/max/1400/1*cff9OedFe861WaCwUiD76g.jpeg",
        "17b890c5e7ca026ac45f7edb37a7783e": "https://i.imgur.com/a8BTZ25.png",
    }

    extractor = ContentExtractor()
    soup, replacements = extractor.replace_images(original_soup)
    assert replacements == epxected_replacements
    assert soup.prettify().strip() == article_soup.find("article").prettify().strip()
    assert soup.prettify().strip() != original_soup.find("article").prettify().strip()


def test_get_article(get_file_content, medium_url):
    content = get_file_content("html/medium.html")
    with requests_mock.mock() as mocked_requests:
        mocked_requests.get(medium_url, text=content)
        with patch(
            "send_to_kindle.downloader.article_downloader.extract_content",
            return_value="the_content",
        ), patch(
            "send_to_kindle.downloader.article_downloader.extract_images",
            return_value=("the_content", {"k": "v"}),
        ) as extract_images_mock:
            article = get_article(medium_url)

            extract_images_mock.assert_called_once_with("the_content")
            assert article.title == "Lorem Ipsum - Antonio Feregrino - Medium"
            assert article.content == "the_content"
            assert article.image_map == {"k": "v"}
