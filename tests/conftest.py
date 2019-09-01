import pytest
from pathlib import Path
from bs4 import BeautifulSoup


@pytest.fixture
def from_email():
    return "from@mail.com"


@pytest.fixture
def to_email():
    return "to@mail.com"


@pytest.fixture
def subject():
    return "subject"


@pytest.fixture
def password():
    return "password"


@pytest.fixture
def host():
    return "localhost"


@pytest.fixture
def port():
    return 1234


@pytest.fixture
def attachment_path():
    return Path("/fakepath")


@pytest.fixture(scope="session")
def get_file_content(pytestconfig):
    def inner(file, mode="r"):
        file_path = Path(pytestconfig.rootdir, "tests", file)
        with open(file_path, mode) as readable:
            return readable.read()

    return inner


@pytest.fixture(scope="session")
def get_soup(get_file_content):
    def inner(file):
        content = get_file_content(file)
        return BeautifulSoup(content, "lxml")

    return inner
