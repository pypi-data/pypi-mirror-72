# NAME

**data_printer** - data printer and dumper

# VERSION

0.0.2

# SYNOPSIS

```python
from data_printer import p, np

import sys
from colored import fore, back, style

class A:
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

data = A(abc="acc", a=A(x=dict(p=10, r=[20, (2, 0.01)])), s='Строка\n', b=b'binary\n', r=r'\n')

# add ref to themselwes:
data.a.x['r'].append(data)  

# print colored structure to sys.stdout
p(data)

# print colored structure to file stream
p(data, file=sys.stderr)

# print uncolored structure to file stream
p(data, file=sys.stderr, color=False)

# serialize structure to string
s = np(data)

# serialize structure to colored string (colors as escape sequences)
s = np(data, color=True)

# default color scheme
p(data, color=dict(
    bool = fore.LIGHT_BLUE,
    none = fore.LIGHT_BLUE,
    int = fore.LIGHT_YELLOW,
    float = fore.LIGHT_YELLOW,
    str = fore.LIGHT_GREEN,
    bytes = fore.LIGHT_MAGENTA,
    object = fore.LIGHT_RED,
    key = fore.LIGHT_CYAN,
    ref = fore.RED,
    punct = fore.WHITE,
))

# replace two colors
s = np(data, color=dict(
    bool = fore.LIGHT_RED,
    none = fore.LIGHT_YELLOW,
))

```

# DESCRIPTION

Data recursive printer. Serialize any python3 data to string or print in console or file.

Is colorised output.

Data printer check many references to one structure.

# INSTALL

```sh
$ pip install data-printer
```

# REQUIREMENTS

* colored

# AUTHOR

Kosmina O. Yaroslav <dart@cpan.org>

# LICENSE

MIT License

Copyright (c) 2020 Kosmina O. Yaroslav

