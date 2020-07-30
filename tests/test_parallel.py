from pyarmyknife.parallel import parallel_function, patch_pandas
import pandas as pd
import numpy as np


def foo(x, power):
    return pow(x, power)


def test_parallel_function(size=100, power=1.1):
    multicore_list = parallel_function(foo, range(size), power=power, progressbar=False)
    assert multicore_list == [foo(x, power=power) for x in range(size)]


def test_parallel_apply():
    patch_pandas()
    np.random.seed(1)
    df = pd.DataFrame(
        pd.np.random.randint(0, 300, size=(int(2000), 4)), columns=list("ABCD")
    )
    df["totals"] = df.parallel_apply(lambda x: x.A + x.B, axis=1, progressbar=False)
    df.parallel_apply(lambda x: x ** 2, progressbar=False)
    pd.testing.assert_series_equal(
        df.parallel_apply(sum, progressbar=False, max_chunks_per_core=10),
        df.parallel_apply(np.sum, raw=True, progressbar=False, allow_more_workers=True),
    )

    fn = lambda x: [x.A, x.B]  # noqa:E731
    pd.testing.assert_frame_equal(
        df.parallel_apply(fn, axis=1, result_type="expand", progressbar=False),
        df.apply(fn, axis=1, result_type="expand"),
    )
