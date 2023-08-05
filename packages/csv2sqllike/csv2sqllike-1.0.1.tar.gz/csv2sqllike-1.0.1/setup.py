#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='csv2sqllike',
    author='Junsang Park',
    author_email='publichey@gmail.com',
    url='https://github.com/hoosiki/csv2sqlLike',
    version='1.0.1',
    long_description=readme,
    long_description_content_type="text/markdown",
    description='Python functions for data analysis using python native container. Load data from csv files and deal with data like sql.',
    packages=find_packages(),
    licnese='BSD',
    include_package_date=False,
    install_requirement=[
        'csv',
        'pymysql'
    ],
    download_url='https://github.com/hoosiki/csv2sqlLike/blob/master/dist/csv2sqllike-1.0.1.tar.gz'
)
