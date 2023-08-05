import io
import pathlib
import re

from setuptools import setup

with io.open("pypi_desc.md", "rt", encoding="utf8") as f:
    long_desc = f.read()

VERSION = "2.1.0"

# This call to setup() does all the work
setup(
    name="starcli",
    version=VERSION,
    description="Browse popular repos on github by star trends from your command line!",
    long_description=long_desc,
    python_requires=">=3.7",
    long_description_content_type="text/markdown",
    url="https://github.com/hedythedev/starcli",
    author="Hedy Li",
    author_email="hedyhyry@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["starcli"],
    include_package_data=True,
    install_requires=["requests>=2.22.0", "rich>=2.1.0",],
    entry_points={"console_scripts": ["starcli=starcli.__main__:cli",]},
)
