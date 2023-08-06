# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="hdql",
    version="0.0.1",
    description="Short description",
    license="MIT",
    author="andriy_yatskovets",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
)
