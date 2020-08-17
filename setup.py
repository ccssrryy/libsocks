#!/usr/bin/env python3

import os
import re

from setuptools import setup, find_packages

base_path = os.path.dirname(__file__)

requirements = []

with open(os.path.join(base_path, "libsocks/__init__.py")) as f:
    VERSION = re.compile(r'.*__version__ = "(.*?)"', re.S).match(f.read()).group(1)

setup(
    name="libsocks",
    version=VERSION,
    description="A socks5/socks/http proxy client module",
    long_description="https://github.com/ccssrryy/libsocks/blob/master/README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/ccssrryy/libsocks",
    license="MIT",
    author="ccssrryy",
    author_email="cs010@hotmail.com",
    keywords=["socks", "socks5", "socks4", "asyncio", "proxy"],
    include_package_data=True,
    packages=find_packages(include=[
        "libsocks", "libsocks.*"
        ]),
    install_requires=requirements,
    python_requires=">=3.5",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ),
)
