# PyArmyKnife

A collection of Python3 utilities for personal and professional use.

## Installation
```bash
pip install git+https://github.com/ddelange/PyArmyKnife.git@master
```

## Usage
```python
import pyarmyknife as pak


def test():
    current_file = pak.fileio.current_file
    current_path = pak.fileio.current_path

    current_function = pak.misc.get_current_function()

    pp = pak.misc.pp()

    pp([current_file, current_path, current_function])

    pak.misc.local_vars(print_vars=True)

    pak.misc.set_trace()


if __name__ == '__main__':
    test()
```
