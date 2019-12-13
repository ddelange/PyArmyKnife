"""pyarmyknife.misc module."""

import logging

logger = logging.getLogger(__name__)


def flatten(obj, ltypes=(list, tuple)):
    """Flatten a nested variable, by default only list/tuple combinations.

    Source: Mike C Fletcher's flatten http://www.bit.ly/2ULLMnm
    """
    ltype = type(obj)
    obj = list(obj)
    i = 0
    while i < len(obj):
        while isinstance(obj[i], ltypes) and not (
            isinstance(obj[i], str) and len(obj[i]) == 1
        ):
            if not obj[i]:
                obj.pop(i)
                i -= 1
                break
            else:
                obj[i : i + 1] = obj[i]
        i += 1
    return ltype(obj)


def split_batch(data, *, size=100):
    """Yield iterable generator object of splitted lists or dicts."""
    from itertools import islice

    it = iter(data)
    if isinstance(data, dict):
        yield from (
            {k: data[k] for k in islice(it, size)} for _ in range(0, len(data), size)
        )
    else:
        try:
            import boltons.iterutils

            yield from boltons.iterutils.chunked_iter(data, size)
        except ImportError:
            yield from (type(data)(islice(it, size)) for _ in range(0, len(data), size))


def get_current_function(depth=0):
    """Get the function object of the current function (depth=0).

    Or the function above that (depth=1) et cetera
    """
    from inspect import currentframe, getframeinfo

    caller = currentframe()
    for i in range(depth + 1):
        caller = caller.f_back
    func_name = getframeinfo(caller)[2]
    try:
        return caller.f_back.f_locals.get(
            func_name, caller.f_globals.get(func_name)
        )  # use get_current_function(1).__name__
    except Exception as e:
        return f"{e}: unknown function"


def local_vars(*, print_vars=True, depth=0, fillers=25):
    """Print -in order of declaration- all local variables.

    In the current function (depth=0) or the function above that (depth=1) et cetera

    Fill up to (fillers) characters with periods '.'
    """
    from inspect import currentframe, getouterframes

    fct = get_current_function(depth + 1)
    locs = getouterframes(currentframe())[depth + 1][0].f_locals
    variables = []
    for var in fct.__code__.co_varnames:
        var_string = "{0:.<{2}}{1}".format(
            var, locs[var], fillers if len(var) < fillers else len(var) + 4
        )
        if print_vars:
            print(var_string)  # noqa:T001
        variables.append((var, locs[var]))
    return variables


def pp(*, indent=1, width=80, depth=None, stream=None, compact=False):
    import pprint

    return pprint.PrettyPrinter(
        indent=indent, width=width, depth=depth, stream=stream, compact=compact
    ).pprint


def set_trace():
    import ipdb

    ipdb.set_trace()


def line_up(iteration=1):
    """Move cursor up and clear that line."""
    from sys import stdout

    stdout.write("\x1b[{}F".format(iteration))
    stdout.write("\x1b[2K")


def write_up(writeline, iteration=1):
    """Run liup, then fills that line, and put the cursor down to original position."""
    from sys import stdout

    line_up(iteration)
    stdout.write(writeline)
    stdout.write("\x1b[{}E".format(iteration))
    stdout.flush()


def bold(string):
    """Return an ANSI bold string."""
    from os import name

    return string if name == "nt" else "\033[1m{}\033[0;0m".format(string)


def integer_input(question=""):
    """User input of integer."""
    if question and not question.endswith(" "):
        question += " "
    while True:
        try:
            return int(input("{}Enter an integer: ".format(question)))
        except ValueError:
            print("Not an integer! Please try again...")  # noqa:T001


# Airflow datetime:


def myconverter(o):
    """Use json.dumps(data, default=myconverter)."""
    import datetime

    if isinstance(o, datetime.datetime):
        return o.__str__()


def parse_datetime(datetime_string, strf="%Y-%m-%d %H:%M:%S%z"):
    import datetime

    if "." in datetime_string:
        strf = "%Y-%m-%d %H:%M:%S.%f%z"
    return datetime.datetime.strptime(
        datetime_string.replace(":00", "00"), strf  # %z timezone in format +0000
    )


class cst(object):
    """SI constants."""

    Pi = 3.141592653589793238462643383279502884  # https://github.com/numpy/numpy/blob/464f79eb1d05bf938d16b49da1c39a4e02506fa3/numpy/core/include/numpy/npy_math.h#L79
    Grav = 6.67384e-11  # m^3 kg^-1 s^-2
    Planck = 6.626070040e-34  # m^2 kg s^-1         OR    J s
    Boltz = 1.38064852e-23  # m^2 kg s^-2 K^-1    OR    J K^-1
    Stef_Boltz = 5.670367e-8  # W m^-2 K^-4
    c = 2.99792458e8  # m s^-1
    # c = (1/(ep0*mu0))**0.5            # m s^-1
    mu0 = (
        4 * Pi * 1e-7
    )  # H m^-1   OR    T m A^-1    OR    Wb A^-1 m^-1 OR    V s A^-1 m^-1
    ep0 = 1 / (mu0 * c ** 2)  # F m^-1   OR    s^4 A^2 m^-2 kg^-1 m^-1
    e_mass = 9.10938215e-31  # kg
    n_mass = 1.674927471e-27  # kg
    p_mass = 1.672621777e-27  # kg
    eV = 1.602176565e-19  # J ev^-1  OR    C    OR    A s
    toarcsec = (60 ** 2 * 180) / Pi  # arcsec rad^-1
    torad = Pi / (60 ** 2 * 180)  # rad arcsec^-1

    # Distances
    AU = 1.495978707e11  # m
    pc = 3.08567758e16  # m
    ly = 9.4607304725808e15  # m

    # Celestial bodies
    mEarth = 5.972e24  # kg
    REarth = 6.371e6  # m
    mMoon = 7.346e22  # kg
    dEarth_Moon = 3.844e8  # m
    mSun = 1.989e30  # kg
    RSun = 6.958e8  # m
    mISS = 4.5e5  # kg
    LSun = 3.83e26  # W


cst = cst()


class formulae(object):
    # Newton's theory of gravitation, standard value for human on earth
    def f_newton(self, r=cst.REarth, m1=cst.mEarth, m2=80):
        return cst.Grav * m1 * m2 / r ** 2  # N

    # Escape velocity, standard value for earth
    def escape_velocity(self, Height=cst.REarth, Mass=cst.mEarth):
        return (2 * cst.Grav * float(Mass) / float(Height)) ** 0.5  # m s^-1

    # Solving energy conservation with two heights and two velocities, 1 unknown
    # V or H can be unknown by entering -1, H or V respectively will then be returned
    def energy_conservation(self, Velocity=0, Height=0, velocity=0, height=0, Mass=0):
        if 0 in [Velocity, Height, velocity, height, Mass] or (
            Velocity == -1 and Height == -1
        ):
            logger.info("Not physical.")
            return -1
        elif Velocity == -1:
            return (
                velocity ** 2
                + 2 * cst.Grav * Mass / Height
                - 2 * cst.Grav * Mass / height
            ) ** 0.5
        elif Height == -1:
            return (
                cst.Grav
                * Mass
                / ((velocity ** 2) / 2 - cst.Grav * Mass / height + (Velocity ** 2) / 2)
            )
        else:
            return -1


formulae = formulae()
