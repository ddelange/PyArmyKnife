from pyarmyknife.plt import _figureformat, _figuredpi, set_figureformat, set_figuredpi


def test_string_compress():
    set_figureformat('jpg')
    assert _figureformat == 'jpg'

    set_figuredpi(300)
    assert _figuredpi == 300
