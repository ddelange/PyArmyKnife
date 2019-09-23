# PyArmyKnife

A collection of Python3 utilities for personal and professional use.

## Installation
```bash
pip install git+https://github.com/ddelange/PyArmyKnife.git@master
```

## Usage
```python
import pyarmyknife as pak


def foo(x, power):
    return x ** power


multicore_list = pak.parallel.parallel_function(foo, range(100000), power=1.1)
print(multicore_list[-10:])


def test():
    # for use in python files
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
