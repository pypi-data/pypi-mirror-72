from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyboin',
    packages=['pyboin'],
    install_requires=["jaconv"],

    version='0.1.1',
    license='MIT',

    author='Tatsuya Abe',
    author_email='abe12@mccc.jp',

    url='https://github.com/AjxLab/pyboin',

    desription='Pure-Python Japanese character interconverter for Hiragana and Vowel.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='crawling crawler scraping',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
