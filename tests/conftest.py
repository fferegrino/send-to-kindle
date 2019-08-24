import pytest
from pathlib import Path
from bs4 import BeautifulSoup


@pytest.fixture(scope="session")
def get_file_content(pytestconfig):
    def inner(file):
        file_path = Path(pytestconfig.rootdir, "tests", file)
        with open(file_path, "r") as readable:
            return readable.read()

    return inner


@pytest.fixture(scope="session")
def get_soup(get_file_content):
    def inner(file):
        content = get_file_content(file)
        return BeautifulSoup(content, "lxml")

    return inner
