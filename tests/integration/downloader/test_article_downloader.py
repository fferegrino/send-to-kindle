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
    images = {
        "7ca0b474f6141a9bf5ba20b07ab5651e.jpg": "https://miro.medium.com/max/4800/1*Wt9RHB_ifSkbnHmPiiKtLw.jpeg",
        "68892b2cb660e9965894076dded2dd30.jpg": "https://miro.medium.com/max/1408/0*YfMmOhy01RTl5K0u",
        "3a699d7429177a7527ebe87fcd02ccbd.jpg": "https://miro.medium.com/max/2474/0*hZF4uuaYanSxmANz",
        "0672e5fb666089c1f3a93ae2ebb418d9.jpg": "https://miro.medium.com/max/3200/0*0rNhFlTZp6Ra-uRR",
    }
    assert article.content.prettify().strip() == expected_content
    assert article.title == expected_title
    assert article.image_map == images
