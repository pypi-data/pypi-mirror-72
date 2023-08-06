pyboin
======

[![](https://github.com/AjxLab/pyboin/workflows/build/badge.svg)](https://github.com/AjxLab/pyboin/actions)
[![PyPi](https://badge.fury.io/py/pyboin.svg)](https://pypi.python.org/pypi/pyboin/)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)


pyboin is Pure-Python Japanese character interconverter for Hiragana and Vowel.
```
「こんにちは」 -> 「おんいいあ」
```


## Requirement
* Python3


## Usage
```python
import pyboin

# Argument 'cv' may be omitted.
# Specify katakana or hiragana as the first argument.
pyboin.text2boin('こんにちは', cv='katakana')
# => 'オンイイア'

pyboin.text2boin('こんにちは', cv='hiragana')
# => 'おんいいあ'
```


## Installation
```sh
$ pip install pyboin
```


## Contributing
Bug reports and pull requests are welcome on GitHub at [https://github.com/AjxLab/pyboin](https://github.com/AjxLab/pyboin).


## Author
* Tatsuya Abe
* '''abe12<at>mccc.jp'''
