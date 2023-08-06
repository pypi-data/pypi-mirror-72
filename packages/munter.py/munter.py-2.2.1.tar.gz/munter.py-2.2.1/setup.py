#!/usr/bin/env python
"""munter.py distutils configuration."""
import os
import re
from setuptools import setup

CUR_DIR = os.path.dirname(__file__)
VERSION = re.search(
    "^__version__\\s*=\\s*'(.*)'",
    open(os.path.join(CUR_DIR, 'munter/__init__.py')).read(),
    re.M
    ).group(1)
README = ""

with open(os.path.join(CUR_DIR, 'README.md'), encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name='munter.py',
    version=VERSION,
    description=(
        'An easy-to-use implementation of the Munter time calculation'
    ),
    long_description=README,
    long_description_content_type='text/markdown',
    author='Alexander Vasarab',
    author_email='alexander@wylark.com',
    url='https://wylark.com/munter',
    project_urls={
        'Source Code': 'https://wylark.com/git/munter.git'
    },
    packages=['munter'],
    package_dir={'munter': 'munter'},
    entry_points={'console_scripts': ['munter = munter.munter:main']},
    include_package_data=True,
    python_requires='>=3.6',
    license='ISC',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "munter",
        "tour planning",
        "trip planning",
        "time estimate",
    ],
)
