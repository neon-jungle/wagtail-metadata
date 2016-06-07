#!/usr/bin/env python
"""
Install wagtail-metadata using setuptools
"""

with open('README.rst', 'r') as f:
    readme = f.read()

from setuptools import find_packages, setup

setup(
    name='wagtail-metadata',
    version='0.1.3',
    description="A tool to assist with metadata for social media.",
    long_description=readme,
    author='Liam Brenner',
    author_email='liam@takeflight.com.au',
    url='https://github.com/takeflight/wagtail-metadata',

    install_requires=[
        'wagtail>=1.0',
    ],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
