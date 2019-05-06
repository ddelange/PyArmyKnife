from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

import pkg_resources
import pyarmyknife.fileio
import pyarmyknife.misc
import pyarmyknife.parallel
import pyarmyknife.plt
import pyarmyknife.www

standard_library.install_aliases()


# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = '1.0.0'

try:
    pkg_version = pkg_resources.get_distribution('pyarmyknife').version
except pkg_resources.DistributionNotFound:
    raise RuntimeError('Install pyarmyknife, eg "pip install -e ."')

if pkg_version != __version__:
    raise RuntimeError(f'Reinstall pyarmyknife, eg "pip install -e ."')
