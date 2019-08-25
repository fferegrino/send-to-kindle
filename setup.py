from setuptools import setup, find_packages
from pathlib import Path

root_dir = Path(__file__).parent
requirements = Path(root_dir, "requirements.txt")
requirements_dev = Path(root_dir, "requirements-dev.txt")
packages = find_packages(where=root_dir, exclude=["tests*"])

VERSION = "0.0.0"


def list_requirements(file_name):
    return [line.strip() for line in open(file_name)]


with open("README.md", "r") as readable:
    long_description = readable.read()

setup(
    name="send_to_kindle",
    author="Antonio Feregrino",
    author_email="antonio.feregrino@gmail.com",
    version=VERSION,
    packages=packages,
    description="Send web articles to your kindle!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fferegrino/send-to-kindle",
    install_requires=list_requirements(requirements),
    tests_require=list_requirements(requirements_dev),
    entry_points="""
        [console_scripts]
        send_to_kindle=send_to_kindle.cli:download
    """,
    include_package_data=True,
)
