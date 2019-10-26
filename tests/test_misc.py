from pyarmyknife.misc import flatten


def test_flatten():
    assert flatten(["abc", ("d", "e"), ["f"]], ltypes=(list, tuple, str)) == [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
    ]
