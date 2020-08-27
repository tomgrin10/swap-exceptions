# swap-exceptions

[![PyPI](https://img.shields.io/pypi/v/swap-exceptions)](https://pypi.org/project/swap-exceptions/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swap-exceptions)](https://pypi.org/project/swap-exceptions/)
[![PyPI License](https://img.shields.io/pypi/l/swap-exceptions)](https://pypi.org/project/swap-exceptions/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)

Python utility decorator and context manager for swapping exceptions.

### Basic Usage

As a decorator:
```python
from swap_exceptions import swap_exceptions

@swap_exceptions({KeyError: ValueError("Incorrect value")})
def get_value(key: str):
    d = {'a': 1, 'b': 2}
    return d[key]

get_value('c')  # ValueError: Incorrect value
```

Or as a context manager:
```python
from swap_exceptions import swap_exceptions

def get_value(key: str):
    d = {'a': 1, 'b': 2}
    with swap_exceptions({KeyError: ValueError("Incorrect value")}):
        return d[key]

get_value('c')  # ValueError: Incorrect value
```

### Advanced Usage

Mapping key can also be a tuple:
```python
from swap_exceptions import swap_exceptions

@swap_exceptions({(KeyError, TypeError): ValueError("Incorrect value")})
def get_value(key: str):
    d = {'a': 1, 'b': 2, 'c': 'not a number'}
    return d[key] + 10

get_value('c')  # ValueError: Incorrect value
```

Mapping value can also be a factory that generates the exception:
```python
from swap_exceptions import swap_exceptions

@swap_exceptions({KeyError: lambda e: ValueError(f"Incorrect value {e.args[0]}")})
def get_value(key: str):
    d = {'a': 1, 'b': 2}
    return d[key]

get_value('c')  # ValueError: Incorrect value c
```
