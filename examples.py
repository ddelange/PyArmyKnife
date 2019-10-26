import pyarmyknife as pak


def test_function(data, increase_by, sleep=False):
    """Do some massive stuff with one element from iterable."""
    if sleep:
        from time import sleep

        sleep(2)
    return data + increase_by


def various_examples():
    current_file = pak.fileio.current_file
    current_path = pak.fileio.current_path

    current_function = pak.misc.get_current_function()

    pp = pak.misc.pp()

    pp([current_file, current_path, current_function])

    pak.misc.local_vars(print_vars=True)

    pak.misc.set_trace()


if __name__ == "__main__":
    a = pak.parallel.parallel_function(
        test_function, range(50), increase_by=42, sleep=True
    )
    various_examples()
