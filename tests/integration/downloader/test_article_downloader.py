from send_to_kindle.downloader import get_article
from send_to_kindle.downloader.article_downloader import extract_content
import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from unittest.mock import patch
import requests_mock


def test_get_article(get_file_content):
    content = get_file_content("html/integration-medium.html")
    expected_content = BeautifulSoup(content, "lxml").find("article").prettify().strip()
    expected_title = "In a World of Smart Gadgets, Why Are Toilets Still so Dumb?"

    article = get_article(
        "https://onezero.medium.com/in-a-world-of-smart-gadgets-why-are-toilets-still-so-dumb-722e734aa1b7"
    )

    assert article.title == expected_title
    assert article.content.prettify().strip() == expected_content
