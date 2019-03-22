import pkg_resources

__version__ = '0.0.1'

try:
    pkg_version = pkg_resources.get_distribution('pyarmyknife').version
except pkg_resources.DistributionNotFound:
    raise RuntimeError('Install pyarmyknife, eg "pip install -e ."')

if pkg_version != __version__:
    raise RuntimeError('Reinstall pyarmyknife, eg "pip install -e ."')
