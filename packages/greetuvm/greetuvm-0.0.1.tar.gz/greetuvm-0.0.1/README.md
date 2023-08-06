# greetuvm
> Greet You Very Much

An example project to help say hello to people or things.

This is actually a code-along for the talk [Publishing (Perfect) Python Packages on PyPi](https://youtu.be/GIF3LaRqgXo).

## Installation
Run the following to install:

```bash
$ pip install greetuvm
```

## Usage
```python
from hello import say_hello

# Say the generic "Hello"
say_hello()

# Say "Hello, Abel"
say_hello('Abel')
```

# Developing Greeter
To install greetuvm, along with the tools you need to develop and run tests,
run the following in your virtualenv:
```bash
$ pip install -e .[dev]
```
