from pyarmyknife.fileio import string_compress, string_decompress


def test_string_compress():
    data = [1, 2, [3, 4], {"a": 1453.13245, "b": "c" * 800}]
    assert string_decompress(string_compress(data, strict_types=True)) == data
    data = (1, 2, 3)
    assert string_decompress(string_compress(data, strict_types=False)) == list(data)
