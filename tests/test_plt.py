from pyarmyknife.plt import _figuredpi, _figureformat, set_figuredpi, set_figureformat


def test_string_compress():
    set_figureformat("jpg")
    assert _figureformat == "jpg"

    set_figuredpi(300)
    assert _figuredpi == 300
