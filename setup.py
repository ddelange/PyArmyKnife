from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import filter
from future import standard_library
from pathlib import Path
import re

from setuptools import find_packages, setup
standard_library.install_aliases()

here = Path(__file__).parent

init = here / 'src' / 'pyarmyknife' / '__init__.py'

with init.open(mode='rt', encoding='utf-8') as fp:
    txt = fp.read()

try:
    pattern = r"^__version__ = '([^']+)'\r?$"
    version = re.findall(pattern, txt, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


def read_requirements(path):
    try:
        with path.open(mode='rt', encoding='utf-8') as fp:
            _install_requires = (line.split('#')[0].strip() for line in fp)
            return list(filter(None, _install_requires))
    except (IOError, IndexError):
        raise RuntimeError(f'{path} is broken')


requirements = here / 'requirements' / 'prod.txt'
install_requires = read_requirements(requirements)
extras_require = {
    'sklearn': ['scikit-learn']
}

setup(
    name='pyarmyknife',
    version=version,
    author='D. de Lange',
    author_email='14880945+ddelange@users.noreply.github.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        '': ['*.csv', '*.xml', '*.yaml'],
    },
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.3.0',
)

