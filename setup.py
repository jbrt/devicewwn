#!/usr/bin/env python3
# coding: utf-8

"""
Package installation
"""

from setuptools import setup, find_packages


def readme():
    with open('README.rst') as fh:
        return fh.read()


setup(
    name="devicewwn",
    version="0.6.4",
    packages=find_packages(),
    author="Julien B.",
    author_email="julien@toshokan.fr",
    description="Manipulating Fibre Channel WWN easily with decoding capabilities",
    long_description=readme(),
    license="GPLv3",
    keywords="WWN SAN storage EMC Symmetrix VMAX NetApp Fibre Channel",
    url="http://github.com/jbrt/devicewwn",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
)
