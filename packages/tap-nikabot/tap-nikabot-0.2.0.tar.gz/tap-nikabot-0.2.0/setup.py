#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="tap-nikabot",
    version="0.2.0",
    description="Singer.io tap for extracting data from Nikabot",
    author="Paul Heasley",
    author_email="paul@phdesign.com.au",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_nikabot"],
    install_requires=["singer-python==5.9.0", "requests==2.23.0", "backoff==1.8.0"],
    entry_points="""
    [console_scripts]
    tap-nikabot=tap_nikabot:main
    """,
    packages=find_packages(exclude=("tests",)),
    package_data={"schemas": ["tap_nikabot/schemas/*.json"]},
    include_package_data=True,
)
