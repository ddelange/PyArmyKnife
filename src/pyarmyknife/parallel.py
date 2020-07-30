from functools import partial
import psutil


def max_cores():
    """Avoid bottlenecks from hyperthreading (stackoverflow.com/a/49327206/5511061)."""
    return min(psutil.cpu_count(logical=False) + 1, psutil.cpu_count(logical=True))


def parallel_function(  # noqa:E302
    function, input_iterable, *, n_workers=-1, progressbar=True, args=(), **kwargs
):
    """Apply function to each element of input_iterable and ensure output order."""
    from pathos.multiprocessing import ProcessingPool

    total = len(input_iterable)
    if total == 1:
        # no sense running parallel
        return [function(input_iterable[0])]

    n_cores = max_cores()
    allow_more_workers = kwargs.pop("allow_more_workers", False)
    if n_workers < 1:
        n_workers = n_cores
    elif not allow_more_workers:
        # no sense having more workers than cores or chunks
        n_workers = min(n_workers, n_cores, total)

    pool = ProcessingPool(n_workers)

    stage = pool.imap(partial(function, *args, **kwargs), input_iterable)
    if progressbar:
        from tqdm import tqdm

        stage = tqdm(stage, total=total)

    return [x for x in stage]


def parallel_apply(
    df_or_series,
    function,
    *,
    chunk_size=1000,
    n_workers=-1,
    progressbar=True,
    axis=0,
    args=(),
    **kwargs
):
    """Run apply on n_workers. Split in chunks, gather results, and concat them."""
    from pandas import Series, concat
    from numpy import array_split

    # no sense running parallel if data is too small
    n_chunks = int(len(df_or_series) / chunk_size)

    n_cores = max_cores()
    max_chunks_per_core = kwargs.pop("max_chunks_per_core", 20)
    allow_more_workers = kwargs.pop("allow_more_workers", False)
    if max_chunks_per_core:
        # no sense making too many chunks
        n_chunks = min(n_chunks, max_chunks_per_core * n_cores)
    if n_chunks < 1 or n_workers == 1 or n_cores == 1:
        # no sense running parallel
        n_chunks = 1

    if axis == 1:
        df_or_series = df_or_series.T

    dfs = array_split(df_or_series, n_chunks, axis=axis)

    def run_apply(function, df, args=(), **kwargs):
        # axis argument is handled such that always axis=0 here
        return df.apply(function, args=args, **kwargs)

    results = parallel_function(
        partial(run_apply, function, args=args, **kwargs),
        dfs,
        n_workers=n_workers,
        progressbar=progressbar,
        allow_more_workers=allow_more_workers,
    )

    if (
        len(results) > 1
        and isinstance(results[0], Series)
        and results[0].index.equals(results[1].index)
    ):
        # one more aggregation needed for final df, e.g. df.parallel_apply(sum)
        return concat(results, axis=1).apply(function, axis=1, args=args, **kwargs)

    if axis == 1:
        results = (df.T for df in results)
    return concat(results)


def patch_pandas():
    """Run this function to add parallel_apply method to PandasObject."""
    from pandas.core.base import PandasObject

    setattr(PandasObject, "parallel_apply", parallel_apply)
