def test_imports():
    import pyarmyknife as pak
    from pyarmyknife import fileio, misc, parallel, plt, www
    from pyarmyknife.fileio import dump  # noqa:F401
    from pyarmyknife.misc import flatten  # noqa:F401
    from pyarmyknife.parallel import parallel_function  # noqa:F401
    from pyarmyknife.plt import plt_setup  # noqa:F401
    from pyarmyknife.www import extract_domain  # noqa:F401
    assert pak.fileio.current_file == fileio.current_file
    assert pak.misc.cst.Pi == misc.cst.Pi
    assert pak.parallel.parallel_function == parallel.parallel_function
    assert pak.plt._figureformat == plt._figureformat
    assert pak.www.extract_domain('') == www.extract_domain(None)
