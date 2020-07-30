# PyArmyKnife

A collection of Python3 utilities for personal and professional use.

[![python](https://img.shields.io/static/v1?label=python&message=3.3%2B&color=informational&logo=python&logoColor=white)](https://github.com/ddelange/pyarmyknife/releases/latest)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![codecov](https://codecov.io/gh/ddelange/pyarmyknife/branch/master/graph/badge.svg?token=<add_token_here>)](https://codecov.io/gh/ddelange/pyarmyknife)
[![Actions Status](https://github.com/ddelange/pyarmyknife/workflows/GH/badge.svg)](https://github.com/ddelange/pyarmyknife/actions)  <!-- use badge.svg?branch=develop to deviate from default branch -->


## Installation
```bash
pip install git+https://github.com/ddelange/PyArmyKnife.git@master
```

## Usage
```python
import numpy as np
import pandas as pd
import pyarmyknife as pak

# parralel_apply method
pak.parallel.patch_pandas()
help(pd.DataFrame.parallel_apply)

df = pd.DataFrame(np.random.randint(0, 300, size=(int(100000), 3)), columns=list("ABC"))

df["totals"] = df.parallel_apply(sum, axis=1, progressbar=False)

df.parallel_apply(sum)

# All sorts of other fun stuff
pp = pak.misc.pp()  # pretty printer: pp(list(range(100)))
t = pak.misc.set_trace  # ipdb: t()
```
