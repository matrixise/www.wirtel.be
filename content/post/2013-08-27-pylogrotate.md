---
tags:
- python
date: 2013-08-27
title: Sphinx, Pygments and the logrotate format.
slug: pylogrotate

---

# PyLogrotate

## Introduction

Yesterday, I noticed there was no logrotate lexer for Pygments, so I
developed one for you.

If you want to contribute, please submit a Pull Request on the project
page.

Here is the repository of the project:
<git://github.com/matrixise/pylogrotate.git>

You are invited to contribute to this project ;-)

## Installation

```bash
git clone git://github.com/matrixise/pylogrotate.git

virtualenv ~/.virtualenvs/pylogrotate
source ~/.virtualenvs/pylogrotate

cd pylogrotate
python setup develop
```

## Usage

### Pygmentize

If you want to use it with `pygmentize`, just download it and install it
in a VirtualEnv, see the "Installation" section.

```bash
pygmentize -l logrotate -O full -f /tmp/test.html logrotate.conf
```

### Sphinx

In order to use it with Sphinx, just install it and define in your
`conf.py` file a `setup` function as defined in the below example.

```python
def setup(app):
   from pylogrotate.lexer import LogrotateLexer
   app.add_lexer('logrotate', LogrotateLexer())
```