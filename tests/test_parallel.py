from pyarmyknife.parallel import parallel_function


def foo(x, power):
    return pow(x, power)


def test_parallel_function(size=100, power=1.1):
    multicore_list = parallel_function(foo, range(size), power=power)
    multicore_list = parallel_function(foo, range(size), power=power, progressbar=False)
    assert multicore_list == [foo(x, power=power) for x in range(size)]
