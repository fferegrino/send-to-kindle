from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from send_to_kindle.cli import download, get_config_path
from pathlib import Path
import pytest


@pytest.fixture
def config(from_email, password, to_email, host, port):

    config_dict = {
        "mail_account": {"from": from_email, "password": password, "to": to_email},
        "mail_server": {"host": host, "port": port},
        "kindlegen": {"path": "kindlegen_path"},
    }
    config = MagicMock()
    config.get.side_effect = lambda one, two: config_dict[one][two]
    return config


@patch("send_to_kindle.cli.get_article")
@patch("send_to_kindle.cli.html_to_mobi")
@patch("send_to_kindle.cli.write_temp_html")
@patch("send_to_kindle.cli.download_images")
@patch("send_to_kindle.cli.EmailSender.send_mail")
def test_download(
    send_mail_mock,
    download_images_mock,
    write_temp_html_mock,
    html_to_mobi_mock,
    get_article_mock,
    config,
    to_email,
    attachment_path,
):
    article_title = "A title"
    url = "http://article.com"
    runner = CliRunner()
    html_to_mobi_mock.return_value = attachment_path
    article = MagicMock()
    article.title = article_title
    get_article_mock.return_value = article

    with patch("send_to_kindle.cli.get_config", return_value=config):
        result = runner.invoke(download, [url])
        send_mail_mock.assert_called_once_with(article_title, to_email, attachment_path)
        get_article_mock.assert_called_once_with(url)
        html_to_mobi_mock.assert_called_once()
        download_images_mock.assert_called_once()


def test_get_config_path_file_exists(tmp_path):
    config_ini = Path(tmp_path, "send_to_kindle.ini")
    config_ini.touch()
    actual = get_config_path(config_ini)
    expected = Path(tmp_path, "send_to_kindle.ini")
    actual = get_config_path(config_ini)

    assert expected == actual


def test_get_config_path_file_uses_home(tmp_path):
    config_ini = Path(tmp_path, "send_to_kindle.ini")
    config_ini.touch()
    expected = Path(tmp_path, "send_to_kindle.ini")

    with patch("send_to_kindle.cli.Path.home", return_value=tmp_path):
        actual = get_config_path(None)
    assert expected == actual


def test_get_config_path_file_fails(tmp_path):
    with pytest.raises(ValueError):
        with patch("send_to_kindle.cli.Path.home", return_value=tmp_path):
            value = get_config_path(None)
