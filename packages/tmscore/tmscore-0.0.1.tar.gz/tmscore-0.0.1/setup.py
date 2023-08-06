# -*- coding: utf-8 -*-
"""
Created on 2020/6/29

@author: yang.zhou
"""
import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmscore",
    version="0.0.1",
    author="zhou yang",
    author_email="yang.zhou@howbuy.com",
    description="A small tms core package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://dev-gitlab.intelnal.howbuy.com/tms-pypi/tmscore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)