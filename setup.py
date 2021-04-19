# -*- coding: utf-8 -*-

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

assert path.exists(path.join(here, 'src/Qieyun/rhyme_book.csv')) \
and path.exists(path.join(here, 'src/Qieyun/rhyme_table.csv')), \
    'Please run prepare.py first.'

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'src/Qieyun/_version.py'), encoding='utf-8') as f:
    exec(f.read())

setup(
    name='qieyun',
    version=__version__,
    description='A Python library for the Qieyun phonological system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nk2028/qieyun-python',
    author='nk2028',
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
    install_requires=['networkx>=2.5,<2.6'],
    entry_points={},
    project_urls={
        'Bug Reports': 'https://github.com/nk2028/qieyun-python/issues',
        'Source': 'https://github.com/nk2028/qieyun-python',
    },
)
