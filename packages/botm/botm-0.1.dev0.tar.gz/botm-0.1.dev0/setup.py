#!/usr/bin/env python3
# botm - Automatize your bots.
# Copyright (C) 2020  Hearot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <https: //www.gnu.org/licenses/>.


import re

from setuptools import find_packages
from setuptools import setup

GITHUB_REPOSITORY = "https://github.com/hearot/botm/blob/v%s/"


with open("botm/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read().replace("./", GITHUB_REPOSITORY % version)

with open("requirements.txt", encoding="utf-8") as r:
    requirements = [p.strip() for p in r]

setup(
    author="Hearot",
    author_email="gabriel@hearot.it",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Typing :: Typed",
    ],
    description="Automatize your bots",
    install_requires=requirements,
    keywords="bot bots botmanager bot-manager chatbot chatbots managing",
    license="LGPLv3+",
    long_description=long_description,
    name="botm",
    packages=find_packages(),
    project_urls={
        "Tracker": "https://github.com/hearot/botm/issues",
        "Source": "https://github.com/hearot/botm",
    },
    python_requires=">=3.6.*",
    url="https://github.com/hearot/botm",
    version=version,
)
