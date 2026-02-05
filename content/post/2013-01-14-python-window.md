---
tags:
- python
date: 2013-01-14
slug: python-window-iterator
lang: fr
title: Astuce Windows Iterator

---

Voici le lien original:
<http://sametmax.com/implementer-une-fenetre-glissante-en-python-avec-un-deque/>

# Window Iterator

Une astuce que j'ai pû voir sur le site de
[sam&max](http://sametmax.com).

```python
#!/usr/bin/env python
from collections import deque
from itertools import count
from itertools import islice
from itertools import izip

DEFAULT_SIZE=3

def window(iterable, size=DEFAULT_SIZE):
    iterable = iter(iterable)
    d = deque(islice(iterable, size), size)

    yield d
    for iterm in iterable:
        d.append(item)
        yield d

def main():
    for x in izip(count(), window(xrange(1, 13))):
        print x

if __name__ == '__main__':
    main()
```