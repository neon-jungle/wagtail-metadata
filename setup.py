#!/usr/bin/env python
"""
Install wagtail-metadata using setuptools
"""

from setuptools import find_packages, setup

with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name="wagtail-metadata",
    version="5.0.0",
    description="A tool to assist with metadata for social media.",
    long_description=readme,
    author="Neon Jungle",
    author_email="developers@neonjungle.studio",
    url="https://github.com/neon-jungle/wagtail-metadata",
    install_requires=[
        "wagtail>=5.0",
    ],
    zip_safe=False,
    license="BSD License",
    python_requires=">=3",
    packages=find_packages(exclude=["tests", "tests*"]),
    include_package_data=True,
    package_data={},
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 5",
        "License :: OSI Approved :: BSD License",
    ],
)
