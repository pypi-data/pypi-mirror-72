#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='nnkortex',
    version='0.0.0',
    description='Core for Neural Networks',
    author='Edgar Y. Walker',
    author_email='edgar.y.walker@mnf.uni-tuebingen.de',
    packages=find_packages(exclude=[]),
    install_requires=[],
)
