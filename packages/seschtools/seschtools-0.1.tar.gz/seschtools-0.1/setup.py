import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="seschtools",
    version="0.1",
    description=" Reads Survey Data file and Returns it as Pandas DataFrame",
    long_description=README,
    long_description_content_type="text/markdown",
    #url="https://github.com/",
    author="Nitin Singh",
    author_email="acc4nitin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["seschtools"],
    include_package_data=True,
    install_requires=["pandas", "tqdm"],
)