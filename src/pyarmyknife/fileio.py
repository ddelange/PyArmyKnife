import inspect
import os
from sys import platform


try:
    stack = inspect.stack()
    # print([entry for entry in stack])
    # current_file = [entry[1] for entry in stack if entry[-2][0].strip(' ').startswith('import %s' % inspect.getmodule(stack[1][0]).__name__)][0]
    current_file = stack[-1][1]
    current_path = os.path.dirname(current_file) + os.sep
except Exception as e:
    current_file, current_path = None, os.getcwd()
    print(f'{e}: Can\'t get current filename, probably running as main or using interactive mode. Skipping current_file and current_path.')


def dump(value, filename, compress=9, protocol=2):
    """Dump a Python object to disk."""
    try:
        try:  # sometimes the latter won't work where the externals does despite same __version__
            from sklearn.externals.joblib import dump as jobdump
        except Exception:
            from joblib import dump as jobdump
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        jobdump(value, filename, compress=compress, protocol=protocol)
    except Exception as e:
        print('Unexpected error in dump: ' + e)


def load(filename):
    """Load a Python object from disk."""
    try:
        from sklearn.externals.joblib import load as jobload
    except Exception:
        from joblib import load as jobload
    return jobload(filename)


def list_files(directory, hidden=False):
    """
    returns a list of files in a directory
    """
    files = []
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)) and (hidden or not item.startswith('.')):
            files.append(item)
    return files


def open_with_default(filepath):
    """
    opens a file (full path) with default application, on different operating systems
    """
    from subprocess import call as subcall
    from os import system
    if platform.startswith('darwin'):  # Mac
        if filepath.endswith('pdf'):
            # preferably open with Skim, because of its auto refresh (Terminal: defaults write -app Skim SKAutoReloadFileUpdate -boolean true)
            system('open -a Skim \"{}\"'.format(filepath))
        else:
            subcall(('open', filepath))
    elif os.name is 'posix':  # Unix
        # subcall(('xdg-open', filepath))
        system('xdg-open \"{}\" > /dev/null 2>&1 &'.format(filepath))
    elif os.name is 'nt':  # Windows
        system('start \"\" /b \"{}\"'.format(filepath))


def write_fits(images, name):
    from astropy.io import fits
    if not os.path.exists(curpath + 'img'):
        os.makedirs(curpath + 'img')
    nwhdulist = fits.HDUList()
    nwhdulist.append(fits.PrimaryHDU())  # header=fits.open(fitslocation+source_list[0])[0].header))
    for image in images:
        nwhdulist.append(fits.ImageHDU(data=image))
    nwhdulist.writeto(os.path.join(curpath, 'img', name + '.fits', clobber=True))
    nwhdulist.close()
