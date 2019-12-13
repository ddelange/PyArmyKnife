"""pyarmyknife.fileio module."""

import inspect
import logging
import os

logger = logging.getLogger(__name__)

try:
    stack = inspect.stack()
    # print([entry for entry in stack])
    # current_file = [entry[1] for entry in stack if entry[-2][0].strip(' ').startswith('import %s' % inspect.getmodule(stack[1][0]).__name__)][0]
    current_file = stack[-1][1]
    current_path = os.path.dirname(current_file) + os.sep
except Exception as e:
    current_file, current_path = None, os.getcwdu()
    logger.info(
        f"{e}: Can't get current filename, probably running as main or using interactive mode. Skipping current_file and current_path."
    )


def dump(value, filename, *, compress=9, protocol=2):
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
        logger.error("Unexpected error in dump: " + e)


def load(filename):
    """Load a Python object from disk."""
    try:
        from sklearn.externals.joblib import load as jobload
    except Exception:
        from joblib import load as jobload
    return jobload(filename)


def string_compress(data, compression_level=4, **kwargs):
    """Serialize and compress a variable into a Py3 str."""
    import base64
    import msgpack
    import brotli

    compressed = brotli.compress(
        msgpack.packb(
            data,
            use_bin_type=kwargs.pop("use_bin_type", True),
            strict_types=kwargs.pop("strict_types", True),
            **kwargs,
        ),
        quality=compression_level,
    )
    return base64.b64encode(compressed).decode("ascii")


def string_decompress(compressed, **kwargs):
    """Decompress and unpack a Py3 string from string_compress into a variable."""
    import base64
    import msgpack
    import brotli

    decompressed = brotli.decompress(base64.b64decode(compressed.encode("ascii")))
    return msgpack.unpackb(decompressed, raw=kwargs.pop("raw", False), **kwargs)


def list_files(directory, hidden=False):
    """Return a list of files in a directory."""
    files = []
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)) and (
            hidden or not item.startswith(".")
        ):
            files.append(item)
    return files


def open_with_default(filepath):
    """Open a file with default application depending on operating system."""
    from subprocess import call as subcall
    from os import system, name
    from sys import platform

    if platform.startswith("darwin"):  # Mac
        if filepath.endswith("pdf"):
            # preferably open with Skim, because of its auto refresh (Terminal: defaults write -app Skim SKAutoReloadFileUpdate -boolean true)
            system('open -a Skim "{}"'.format(filepath))
        else:
            subcall(("open", filepath))
    elif name == "posix":  # Unix
        # subcall(('xdg-open', filepath))
        system('xdg-open "{}" > /dev/null 2>&1 &'.format(filepath))
    elif name == "nt":  # Windows
        system('start "" /b "{}"'.format(filepath))


def write_fits(images, name):
    from astropy.io import fits

    if not os.path.exists(current_path + "img"):
        os.makedirs(current_path + "img")
    nwhdulist = fits.HDUList()
    nwhdulist.append(
        fits.PrimaryHDU()
    )  # header=fits.open(fitslocation+source_list[0])[0].header))
    for image in images:
        nwhdulist.append(fits.ImageHDU(data=image))
    nwhdulist.writeto(os.path.join(current_path, "img", name + ".fits", clobber=True))
    nwhdulist.close()


def append_to_txt(plaintext, name="output.txt"):
    with open(os.path.join(current_path, name), "a") as fp:
        fp.write(str(plaintext) + "\n")


def write_dict_to_json(data_dict, filename="output", openfile=False):
    import json

    if not filename.endswith(".json"):
        filename = os.path.join(current_path, filename + ".json")
    with open(filename, "w") as output_file:
        json.dump(data_dict, output_file, indent=2)
    if openfile:
        open_with_default(filename)
    return f"{filename}"


def load_json(filename):
    import json

    if os.path.isfile(filename):
        with open(filename, "r") as fp:
            return json.load(fp)
