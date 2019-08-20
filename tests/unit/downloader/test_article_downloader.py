from send_to_kindle.downloader import get_article
import pytest
from pathlib import Path
from unittest.mock import patch
import requests_mock


@pytest.fixture
def medium_url():
    return "https://medium.com/@antonio.feregrino/lorem-ipsum-cb19745555ea"


@pytest.fixture(scope="session")
def get_file_content(pytestconfig):
    def inner(file):
        file_path = Path(pytestconfig.rootdir, "tests", file)
        with open(file_path, "r") as readable:
            return readable.read()

    return inner


def test_get_article(get_file_content, medium_url):
    content = get_file_content("html/medium.html")
    with requests_mock.mock() as m:
        m.get(medium_url, text=content)
        with patch(
            "send_to_kindle.downloader.article_downloader.extract_content",
            return_value="the_content",
        ):
            article = get_article(medium_url)

            assert article.title == "Lorem Ipsum - Antonio Feregrino - Medium"
            assert article.content == "the_content"
