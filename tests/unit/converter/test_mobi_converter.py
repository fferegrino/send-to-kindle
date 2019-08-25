from unittest.mock import patch, MagicMock
from send_to_kindle.converter.mobi_converter import html_to_mobi
from pathlib import Path
import pytest


@patch("send_to_kindle.converter.mobi_converter.run")
def test_html_to_mobi(run_mock):
    book_name = "my-book"
    expected_book_name_call = f"{book_name}.mobi"
    kindle_get_path = Path("/kindlegen")
    input_path = Path("/input/abook.html")
    kindle_get_path_ = Path("/kindlegen")
    expected_env_call = {"PATH": str(kindle_get_path_.resolve())}
    expected_return_path = Path("/input", expected_book_name_call)

    run_return = MagicMock()
    run_return.returncode = 0
    run_mock.return_value = run_return

    actual = html_to_mobi(kindle_get_path, input_path, book_name)

    assert actual == expected_return_path
    run_mock.assert_called_once_with(
        ["kindlegen", "-o", expected_book_name_call, str(input_path.resolve())],
        env=expected_env_call,
    )
