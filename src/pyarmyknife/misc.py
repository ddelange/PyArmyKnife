from itertools import islice


# Mike C Fletcher's flatten http://www.bit.ly/2ULLMnm
def flatten(obj, ltypes=(list, tuple)):
    """
    Flatten a nested variable, by default only list/tuple combinations.
    """
    ltype = type(obj)
    obj = list(obj)
    i = 0
    while i < len(obj):
        while isinstance(obj[i], ltypes):
            if not obj[i]:
                obj.pop(i)
                i -= 1
                break
            else:
                obj[i:i + 1] = obj[i]
        i += 1
    return ltype(l)


def split_batch(data, size=100):
    """
    Yield iterable generator object of splitted lists or dicts.
    """
    it = iter(data)
    for i in range(0, len(data), size):
        if isinstance(data, dict):
            yield {k: data[k] for k in islice(it, size)}
        elif isinstance(data, list):
            yield list(islice(it, size))


def get_current_function(depth=0):
    """
    Gets the function object of the current function (depth=0)
    or the function above that (depth=1) et cetera
    """
    from inspect import currentframe, getframeinfo
    caller = currentframe()
    for i in range(depth + 1):
        caller = caller.f_back
    func_name = getframeinfo(caller)[2]
    try:
        return caller.f_back.f_locals.get(func_name, caller.f_globals.get(func_name))  # use get_current_function(1).__name__
    except Exception as e:
        return f'{e}: unknown function'


def printvars(depth=0, sig=5, fillers=25):
    """
    Prints -in order of declaration- all local variables {with (sig) significant figures}
    in the current function (depth=0) or the function above that (depth=1) et cetera
    fills up to (fillers) characters with periods '.'
    """
    from inspect import currentframe, getouterframes
    fct = get_current_function(depth+1)
    locs = getouterframes(currentframe())[depth+1][0].f_locals
    for var in fct.__code__.co_varnames:
        try:
            print('{0:.<{3}}{1:.{2}g}'.format(var, locs[var], sig, fillers if len(var) < fillers else len(var)+4))
        except:
            pass


def liup(iteration=1):
    """
    puts cursor `iteration` lines higher at the beginning of the line, then clears that line
    """
    stdout.write('\x1b[{}F'.format(iteration))
    stdout.write('\x1b[2K')


def wriup(writeline='test3', iteration=1):
    """
    liup, then fills that line, and put the cursor down to original position
    """
    liup(iteration)
    stdout.write(writeline)
    stdout.write('\x1b[{}E'.format(iteration))
    stdout.flush()


def bold(string):
    """
    returns a ANSI bold string
    """
    if name is 'nt':
        return string
    else:
        return '\033[1m{}\033[0;0m'.format(string)


def integer_input(question=''):
    """
    User input of integer
    """
    if not question is '' and not question.endswith(' '):
        question += ' '

    while True:
        try:
            return int(input('{}Enter an integer: '.format(question)))
        except ValueError:
            print('Not an integer! Please try again...')


class cst:
    """
    Constants
    """
    Grav = 6.67384e-11                  # m^3 kg^-1 s^-2
    Planck = 6.626070040e-34            # m^2 kg s^-1         OR    J s
    Boltz = 1.38064852e-23              # m^2 kg s^-2 K^-1    OR    J K^-1
    Stef_Boltz = 5.670367e-8            # W m^-2 K^-4
    c = 2.99792458e8                    # m s^-1
    # c = sqrt(1/(ep0*mu0))             # m s^-1
    mu0 = 4 * pi * 1e-7                 # H m^-1   OR    T m A^-1    OR    Wb A^-1 m^-1 OR    V s A^-1 m^-1
    ep0 = 1 / (mu0 * c**2)              # F m^-1   OR    s^4 A^2 m^-2 kg^-1 m^-1
    e_mass = 9.10938215e-31             # kg
    n_mass = 1.674927471e-27            # kg
    p_mass = 1.672621777e-27            # kg
    eV = 1.602176565e-19                # J ev^-1  OR    C    OR    A s
    toarcsec = (60**2 * 180) / pi       # arcsec rad^-1
    torad = pi / (60**2 * 180)          # rad arcsec^-1

    # Distances
    AU = 1.495978707e11                 # m
    pc = 3.08567758e16                  # m
    ly = 9.4607304725808e15             # m

    # Celestial bodies
    mEarth = 5.972e24                   # kg
    REarth = 6.371e6                    # m
    mMoon = 7.346e22                    # kg
    dEarth_Moon = 3.844e8               # m
    mSun = 1.989e30                     # kg
    RSun = 6.958e8                      # m
    mISS = 4.5e5                        # kg
    LSun = 3.83e26                      # W


cst = cst()


class formulae:
    # Newton's theory of gravitation, standard value for human on earth
    def f_newton(self, r=cst.REarth, m1=cst.mEarth, m2=80):
        return cst.Grav * m1 * m2 / r**2       # N

    # Escape velocity, standard value for earth
    def escape_velocity(self, Height=cst.REarth, Mass=cst.mEarth):
        return sqrt(2 * cst.Grav * float(Mass) / float(Height))      # m s^-1

    # Solving energy conservation with two heights and two velocities, 1 unknown
    # V or H can be unknown by entering -1, H or V respectively will then be returned
    def energy_conservation(self, Velocity=0, Height=0, velocity=0, height=0, Mass=0):
        if 0 in [Velocity, Height, velocity, height, Mass] or (Velocity is -1 and Height is -1):
            print('Not physical.')
            return -1
        elif Velocity is -1:
            return sqrt(velocity**2 + 2 * cst.Grav * Mass / Height - 2 * cst.Grav * Mass / height)
        elif Height is -1:
            return cst.Grav * Mass / ((velocity**2) / 2 - cst.Grav * Mass / height + (Velocity**2) / 2)
        else:
            return -1


formulae = formulae()
