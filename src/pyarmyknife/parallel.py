from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


# https://towardsdatascience.com/pandaral-lel-a-simple-and-efficient-tool-to-parallelize-your-pandas-operations-on-all-your-cpus-bb5ff2a409ae
def parallel_function(
    function,
    input_iterable,
    n_workers=-1,
    progressbar=True,
    **kwargs,
):
    """Apply function to each element of input_iterable."""
    from functools import partial
    from multiprocessing import cpu_count
    from pypeln import process as pr
    from tqdm import tqdm
    n_cores = cpu_count()
    n_workers = n_cores if n_workers == -1 else max(min(n_workers, n_cores), 1)
    stage = pr.map(
        partial(
            function,
            **kwargs,
        ),
        input_iterable,
        workers=n_workers,
    )
    if progressbar:
        return [x for x in tqdm(stage, total=len(input_iterable))]
    else:
        return [x for x in stage]
