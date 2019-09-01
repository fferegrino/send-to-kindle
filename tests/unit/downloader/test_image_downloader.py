import requests_mock
from pathlib import Path
from send_to_kindle.downloader.image_downloader import download_images


def test_download_images(tmpdir, get_file_content):
    tmp_dir = Path(tmpdir)
    image_map = {
        "ABC.jpg": "http://image/ABC",
        "DEF.jpg": "http://image/DEF",
        "GHI.jpg": "http://image/GHI",
    }

    expected_images = ["ABC", "DEF"]

    with requests_mock.mock() as m:
        m.get("http://image/ABC", content=get_file_content("images/solid.jpg", "rb"))
        m.get(
            "http://image/DEF", content=get_file_content("images/transparent.png", "rb")
        )
        m.get("http://image/GHI", content=get_file_content("images/animated.gif", "rb"))

        download_images(tmp_dir, image_map)

    existing_files = set(
        [available_file.name for available_file in tmp_dir.glob("**/*")]
    )

    assert set(image_map.keys()) == existing_files
