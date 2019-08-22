import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def get_file_content(pytestconfig):
    def inner(file):
        file_path = Path(pytestconfig.rootdir, "tests", file)
        with open(file_path, "r") as readable:
            return readable.read()

    return inner
