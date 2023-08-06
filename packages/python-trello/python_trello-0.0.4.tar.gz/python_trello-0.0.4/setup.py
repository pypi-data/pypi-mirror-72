from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="python_trello",
    version="0.0.4",
    description="A simple library for easily creating and updating Trello cards.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/anubhavcodes/pytrello",
    author="Anubhav Y",
    author_email="contact+code@anubhav.codes",
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    setup_requires=['pytest-runner'],
    install_requires=[
        "requests",
        "bs4",
    ],
)
