#!/usr/bin/env python
# -*- coding: utf-8 -*-

# flake8: noqa

import codecs
import os

from setuptools import find_packages, setup

HERE = os.path.dirname(os.path.abspath(__file__))

# Read title, version etc from _version.py and put them into local scope
exec(open("boto3_fixtures/_version.py").read())


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


def list_requirements(filename):
    return [line.strip() for line in open(filename) if line.strip() and line[0] != "-"]


setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    maintainer=__author__,
    maintainer_email=__author_email__,
    license="APACHE",
    url=__uri__,
    project_urls={
        "Bug Tracker": "https://github.com/alphachai/boto3-fixtures/issues",
        "Source Code": "https://github.com/alphachai/boto3-fixtures",
    },
    packages=find_packages(
        where=HERE, exclude=["dummy_lambda", "tests", "tests.*", "docs"]
    ),
    description=__summary__,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    setup_requires=["pytest-runner"],
    tests_require=list_requirements("requirements-dev.txt"),
    install_requires=list_requirements("requirements.txt"),
    python_requires=">=3.6",
    extras_require={"pytest": ["pytest"]},
    entry_points={"pytest11": ["name_of_plugin = boto3_fixtures.contrib.pytest"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Pytest",
    ],
)
