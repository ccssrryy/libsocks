#!/usr/bin/env python3

import os
import re

from setuptools import setup, find_packages

base_path = os.path.dirname(__file__)

requirements = []

with open("README.md") as f:
    long_description = f.read()

with open(os.path.join(base_path, "libsocks/__init__.py")) as f:
    VERSION = re.compile(r'.*__version__ = "(.*?)"', re.S).match(f.read()).group(1)

setup(
    name="libsocks",
    version=VERSION,
    description="a socks5/socks/http proxy client module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    license="BSD",
    author="ccssrryy",
    author_email="cs010@hotmail.com",
    keywords=["socks", "socks5", "socks4", "asyncio", "proxy"],
    include_package_data=True,
    packages=find_packages(include=[
        "libsocks", "libsocks.*"
        ]),
    install_requires=requirements,
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ),
)