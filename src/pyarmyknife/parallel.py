"""pyarmyknife.parallel module."""


def parallel_function(
    function, input_iterable, *, n_workers=-1, progressbar=True, **kwargs
):
    """Apply function to each element of input_iterable and ensure output order."""
    from functools import partial
    from multiprocessing import cpu_count
    from pypeln import process as pr
    from tqdm import tqdm

    n_cores = cpu_count()
    n_workers = n_cores if n_workers == -1 else max(min(n_workers, n_cores), 1)

    input_tuples = enumerate(input_iterable)

    def _wrap(input_tuple, function, **kwargs):
        return input_tuple[0], function(input_tuple[1], **kwargs)

    stage = pr.map(
        partial(_wrap, function=function, **kwargs), input_tuples, workers=n_workers
    )
    if progressbar:
        stage = tqdm(stage, total=len(input_iterable))
    return [t[1] for t in sorted((x for x in stage), key=lambda t: t[0])]
