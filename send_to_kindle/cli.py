import configparser
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

import click
import requests
from PIL import Image

from send_to_kindle.converter import html_to_mobi
from send_to_kindle.downloader import get_article
from send_to_kindle.sender.email_sender import EmailSender


def get_config_path(config_file):
    if config_file is None:
        config_file = Path(Path.home(), "send_to_kindle.ini").resolve()
    else:
        config_file = Path(config_file)
    if not config_file.exists():
        raise ValueError("The configuration file does not exist")
    return config_file


def get_config(config_file):
    config_file = get_config_path(config_file)
    parser = configparser.ConfigParser()
    parser.read(str(config_file))
    return parser


def download_images(folder, image_map):
    for image_id, img_url in image_map.items():
        image_path = Path(folder, image_id)
        with open(image_path, "wb") as output_file, requests.get(
            img_url, stream=True
        ) as response:
            shutil.copyfileobj(response.raw, output_file)
        image = Image.open(str(image_path.resolve()))
        rgb_im = image.convert("RGB")
        rgb_im.save(str(image_path.resolve()))


@contextmanager
def write_temp_html(html):
    try:
        temp_html = tempfile.NamedTemporaryFile(suffix=".html", mode="w")
        temp_html.write(html)
        temp_html.flush()
        yield Path(temp_html.name)
    finally:
        temp_html.close()


@click.command()
@click.argument("url")
@click.option("--config", type=click.Path(exists=True, dir_okay=False), default=None)
def download(url, config):
    configuration = get_config(config)
    from_email = configuration.get("mail_account", "from")
    password = configuration.get("mail_account", "password")
    to_email = configuration.get("mail_account", "to")
    host = configuration.get("mail_server", "host")
    port = configuration.getint("mail_server", "port")
    kindlegen_path = Path(configuration.get("kindlegen", "path"))

    article = get_article(url)
    with write_temp_html(article.to_html().prettify()) as html:
        download_images(html.parent, article.image_map)
        mobi_file = html_to_mobi(kindlegen_path, html, article.title)

    sender = EmailSender(from_email, password, host, port)
    sender.send_mail(article.title, to_email, mobi_file)


if __name__ == "__main__":
    download()  # pylint: disable=no-value-for-parameter
