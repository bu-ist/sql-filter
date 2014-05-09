#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='bu-sql-filter',
    version='0.1.0',
    author='Boston University',
    author_email='webteam@bu.edu',
    url='https://github.com/bu-ist/sql-filter/',
    description='Utility for filtering SQL queries.',
    long_description=open('README.md').read(),
    packages=['sqlfilter'],
    scripts=['scripts/sql-filter.py'],
    license='LICENSE',
    install_requires=['sqlparse>=0.1, <0.2']
)