from pyarmyknife.fileio import string_compress, string_decompress


def test_string_compress():
    assert string_decompress(string_compress(range(10))) == range(10)
