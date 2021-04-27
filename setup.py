# -*- coding: utf-8 -*-

from os import path, system
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

if not path.exists(path.join(here, 'src/Qieyun/rhyme_book.csv')) \
        or not path.exists(path.join(here, 'src/Qieyun/rhyme_table.csv')):
    system('python3 prepare.py')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='qieyun',
    version='0.13.3',
    description='A Python library for the Qieyun phonological system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nk2028/qieyun-python',
    author='The nk2028 Project',
    author_email='support@nk2028.shn.hk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: Chinese (Traditional)',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='middle-chinese historical-linguistics qieyun',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'Qieyun': ['rhyme_book.csv', 'rhyme_table.csv'],
    },
    python_requires='>=3.6, <4',
    install_requires=['qieyun-encoder>=0.4,<0.5', 'networkx>=2.5,<2.6'],
    entry_points={},
    project_urls={
        'Bug Reports': 'https://github.com/nk2028/qieyun-python/issues',
        'Source': 'https://github.com/nk2028/qieyun-python',
    },
)
