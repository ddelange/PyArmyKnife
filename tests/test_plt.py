from pyarmyknife import plt


def test_set():
    plt.set_figureformat("jpg")
    assert plt._figureformat == "jpg"

    plt.set_figuredpi(300)
    assert plt._figuredpi == 300
