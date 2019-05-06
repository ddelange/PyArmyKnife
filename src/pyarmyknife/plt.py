from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import int
from builtins import str
from future import standard_library

standard_library.install_aliases()

# String for np.savefig
_figureformat = 'pdf'
_figuredpi = 400


def set_figureformat(new_format):
    global _figureformat
    _figureformat = new_format


def set_figure_dpi(new_dpi):
    global _dpi
    _figuredpi = new_dpi


def hide_ticklines(ax=None, which='both', idx=[0, -1]):
    """Hide inside and outside ticks for indices corresponding to ticklabels."""
    from matplotlib.pyplot import gca
    from numpy import append
    ax = gca() if ax is None else ax
    if which is 'both':
        hide_ticklines(ax, 'x', idx)
        hide_ticklines(ax, 'y', idx)
    elif which is 'x':
        for i in append([i * 2 for i in idx], [i * 2 + 1 for i in idx]):
            ax.xaxis.get_ticklines()[i].set_visible(False)
    elif which is 'y':
        for i in append([i * 2 for i in idx], [i * 2 + 1 for i in idx]):
            ax.yaxis.get_ticklines()[i].set_visible(False)


def plt_setup(packages=[], preamble=[], tex=True, bold=None):
    """
    Set up LaTex rendering with custom preamble.

    Bold text/maths rendering
    Tick formatting, font sizes, gridlines
    """
    from matplotlib import rcParams
    if isinstance(packages, str):
        packages = [packages]
    if isinstance(preamble, str):
        preamble = [preamble]
    packages.extend(['amsmath,wasysym'])
    preamble.extend([r'\usepackage[detect-weight=true, detect-family=true, detect-inline-weight=math, detect-display-math]{siunitx}', r'\DeclareSIUnit\Msun{\ensuremath{\mathrm{M}_{\text{\footnotesize{\astrosun}}}}}'])
    from matplotlib import rc
    rc('font', family='serif')
    rc('text', usetex=tex)
    if bold is True:
        rcParams['axes.labelweight'] = 'bold'  # for math mode and siunitx detection only, use \bf{Flux\ (\si{})} for upright bold or without \bf for italic results
        if '\\boldmath' not in rcParams['text.latex.preamble']:
            rcParams['text.latex.preamble'].append('\\boldmath')  # \boldmath declaration switches to a bold math italic font; this causes letters, numbers, and most symbols used in math mode to be set in a bold type.
    elif bold is False:
        rcParams['axes.labelweight'] = 'normal'
        if '\\boldmath' in rcParams['text.latex.preamble']:
            rcParams['text.latex.preamble'].remove('\\boldmath')

    if len(packages) > 0:
        packages = [s for s in list(set(packages)) if not str(s).strip('-').isdigit()]  # filter out integers and duplicates
        rcParams['text.latex.preamble'].extend(['\\usepackage{%s}' % (i,) if '\\usepackage{%s}' % (i,) not in rcParams['text.latex.preamble'] else '' for i in packages])
    if len(preamble) > 0:
        preamble = [s for s in list(set(preamble)) if not str(s).strip('-').isdigit()]  # filter out integers and duplicates
        rcParams['text.latex.preamble'].extend([i if i not in rcParams['text.latex.preamble'] else '' for i in preamble])
    from matplotlib.pyplot import tick_params, grid, gca
    gca().ticklabel_format(style='sci', scilimits=(-3, 5), axis='both')
    gca().xaxis.label.set_size(17)
    gca().yaxis.label.set_size(17)
    gca().tick_params(axis='both', which='both', color='black', direction='out', length=2.5, width=0.5, zorder=1)
    hide_ticklines()
    rc('legend', **{'fontsize': 14})
    tick_params(labelsize=16)
    grid(b='on', which='major', axis='both')


def cbar_setup(img=None, fig=None, ax=None, label='', tick_length=2.5, tick_width=0.5):
    """Return a cbar with nice ticks and a label, based on colorbar of img."""
    from matplotlib.pyplot import gca, gcf
    from matplotlib.ticker import MaxNLocator
    fig1 = gcf() if fig is None else fig
    ax1 = gca() if ax is None else ax
    img = ax1.get_images() if img is None else img
    cbar = fig1.colorbar(img, ax=ax1)
    cbar.solids.set_edgecolor('face')  # smoother color gradient
    cbar.set_label(label)
    cbar.ax.tick_params(right='on', direction='out', color='black', length=tick_length, width=tick_width, zorder=1)
    hide_ticklines(cbar.ax, which='y')
    return cbar


def save_figure(figname, printformat=None, dpi=None, open=False, setup=True, clear=True, fig=None, bbox_inches='tight', pad_inches=0.1):
    """Save (and opens) a file with a name in the same directory as this python file."""
    import fileio.openfile
    from matplotlib.pyplot import savefig, clf, close, draw, figure, gcf
    printformat = _figureformat if printformat is None else printformat
    dpi = _figuredpi if dpi is None else dpi
    fig = gcf() if fig is None else fig
    try:
        str(figname), str(printformat), int(dpi) < 5000, bool(open)
        if figname.endswith(printformat):
            figname = figname[:-(len(printformat) + 1)]
    except Exception:
        print('Wrong input for savefigure function.')
        return -1
    if path.exists(path.dirname(figname + '.' + printformat)):
        finalname = figname + '.' + printformat
    else:
        finalname = curpath + 'img' + sep + figname + '.' + printformat
        if not path.exists(path.dirname(finalname)):
            makedirs(path.dirname(finalname))
    savefig(finalname, format=printformat, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches)
    if clear:
        clf()
        close()
    else:
        setup = False
    print('Saved to \'.../{}\'.'.format(sep.join((finalname).split(sep)[-3:])))
    if open:
        openfile(finalname)
    if setup:
        plt_setup()
    return finalname


def get_cmap(name):
    try:
        from matplotlib.pyplot import get_cmap
        return get_cmap(name)
    except Exception:
        if name in ['cividis', 'cividis_r']:
            from matplotlib.colors import ListedColormap
            _cividis_data = [[0.000000, 0.135112, 0.304751],
                             [0.000000, 0.138068, 0.311105],
                             [0.000000, 0.141013, 0.317579],
                             [0.000000, 0.143951, 0.323982],
                             [0.000000, 0.146877, 0.330479],
                             [0.000000, 0.149791, 0.337065],
                             [0.000000, 0.152673, 0.343704],
                             [0.000000, 0.155377, 0.350500],
                             [0.000000, 0.157932, 0.357521],
                             [0.000000, 0.160495, 0.364534],
                             [0.000000, 0.163058, 0.371608],
                             [0.000000, 0.165621, 0.378769],
                             [0.000000, 0.168204, 0.385902],
                             [0.000000, 0.170800, 0.393100],
                             [0.000000, 0.173420, 0.400353],
                             [0.000000, 0.176082, 0.407577],
                             [0.000000, 0.178802, 0.414764],
                             [0.000000, 0.181610, 0.421859],
                             [0.000000, 0.184550, 0.428802],
                             [0.000000, 0.186915, 0.435532],
                             [0.000000, 0.188769, 0.439563],
                             [0.000000, 0.190950, 0.441085],
                             [0.000000, 0.193366, 0.441561],
                             [0.003602, 0.195911, 0.441564],
                             [0.017852, 0.198528, 0.441248],
                             [0.032110, 0.201199, 0.440785],
                             [0.046205, 0.203903, 0.440196],
                             [0.058378, 0.206629, 0.439531],
                             [0.068968, 0.209372, 0.438863],
                             [0.078624, 0.212122, 0.438105],
                             [0.087465, 0.214879, 0.437342],
                             [0.095645, 0.217643, 0.436593],
                             [0.103401, 0.220406, 0.435790],
                             [0.110658, 0.223170, 0.435067],
                             [0.117612, 0.225935, 0.434308],
                             [0.124291, 0.228697, 0.433547],
                             [0.130669, 0.231458, 0.432840],
                             [0.136830, 0.234216, 0.432148],
                             [0.142852, 0.236972, 0.431404],
                             [0.148638, 0.239724, 0.430752],
                             [0.154261, 0.242475, 0.430120],
                             [0.159733, 0.245221, 0.429528],
                             [0.165113, 0.247965, 0.428908],
                             [0.170362, 0.250707, 0.428325],
                             [0.175490, 0.253444, 0.427790],
                             [0.180503, 0.256180, 0.427299],
                             [0.185453, 0.258914, 0.426788],
                             [0.190303, 0.261644, 0.426329],
                             [0.195057, 0.264372, 0.425924],
                             [0.199764, 0.267099, 0.425497],
                             [0.204385, 0.269823, 0.425126],
                             [0.208926, 0.272546, 0.424809],
                             [0.213431, 0.275266, 0.424480],
                             [0.217863, 0.277985, 0.424206],
                             [0.222264, 0.280702, 0.423914],
                             [0.226598, 0.283419, 0.423678],
                             [0.230871, 0.286134, 0.423498],
                             [0.235120, 0.288848, 0.423304],
                             [0.239312, 0.291562, 0.423167],
                             [0.243485, 0.294274, 0.423014],
                             [0.247605, 0.296986, 0.422917],
                             [0.251675, 0.299698, 0.422873],
                             [0.255731, 0.302409, 0.422814],
                             [0.259740, 0.305120, 0.422810],
                             [0.263738, 0.307831, 0.422789],
                             [0.267693, 0.310542, 0.422821],
                             [0.271639, 0.313253, 0.422837],
                             [0.275513, 0.315965, 0.422979],
                             [0.279411, 0.318677, 0.423031],
                             [0.283240, 0.321390, 0.423211],
                             [0.287065, 0.324103, 0.423373],
                             [0.290884, 0.326816, 0.423517],
                             [0.294669, 0.329531, 0.423716],
                             [0.298421, 0.332247, 0.423973],
                             [0.302169, 0.334963, 0.424213],
                             [0.305886, 0.337681, 0.424512],
                             [0.309601, 0.340399, 0.424790],
                             [0.313287, 0.343120, 0.425120],
                             [0.316941, 0.345842, 0.425512],
                             [0.320595, 0.348565, 0.425889],
                             [0.324250, 0.351289, 0.426250],
                             [0.327875, 0.354016, 0.426670],
                             [0.331474, 0.356744, 0.427144],
                             [0.335073, 0.359474, 0.427605],
                             [0.338673, 0.362206, 0.428053],
                             [0.342246, 0.364939, 0.428559],
                             [0.345793, 0.367676, 0.429127],
                             [0.349341, 0.370414, 0.429685],
                             [0.352892, 0.373153, 0.430226],
                             [0.356418, 0.375896, 0.430823],
                             [0.359916, 0.378641, 0.431501],
                             [0.363446, 0.381388, 0.432075],
                             [0.366923, 0.384139, 0.432796],
                             [0.370430, 0.386890, 0.433428],
                             [0.373884, 0.389646, 0.434209],
                             [0.377371, 0.392404, 0.434890],
                             [0.380830, 0.395164, 0.435653],
                             [0.384268, 0.397928, 0.436475],
                             [0.387705, 0.400694, 0.437305],
                             [0.391151, 0.403464, 0.438096],
                             [0.394568, 0.406236, 0.438986],
                             [0.397991, 0.409011, 0.439848],
                             [0.401418, 0.411790, 0.440708],
                             [0.404820, 0.414572, 0.441642],
                             [0.408226, 0.417357, 0.442570],
                             [0.411607, 0.420145, 0.443577],
                             [0.414992, 0.422937, 0.444578],
                             [0.418383, 0.425733, 0.445560],
                             [0.421748, 0.428531, 0.446640],
                             [0.425120, 0.431334, 0.447692],
                             [0.428462, 0.434140, 0.448864],
                             [0.431817, 0.436950, 0.449982],
                             [0.435168, 0.439763, 0.451134],
                             [0.438504, 0.442580, 0.452341],
                             [0.441810, 0.445402, 0.453659],
                             [0.445148, 0.448226, 0.454885],
                             [0.448447, 0.451053, 0.456264],
                             [0.451759, 0.453887, 0.457582],
                             [0.455072, 0.456718, 0.458976],
                             [0.458366, 0.459552, 0.460457],
                             [0.461616, 0.462405, 0.461969],
                             [0.464947, 0.465241, 0.463395],
                             [0.468254, 0.468083, 0.464908],
                             [0.471501, 0.470960, 0.466357],
                             [0.474812, 0.473832, 0.467681],
                             [0.478186, 0.476699, 0.468845],
                             [0.481622, 0.479573, 0.469767],
                             [0.485141, 0.482451, 0.470384],
                             [0.488697, 0.485318, 0.471008],
                             [0.492278, 0.488198, 0.471453],
                             [0.495913, 0.491076, 0.471751],
                             [0.499552, 0.493960, 0.472032],
                             [0.503185, 0.496851, 0.472305],
                             [0.506866, 0.499743, 0.472432],
                             [0.510540, 0.502643, 0.472550],
                             [0.514226, 0.505546, 0.472640],
                             [0.517920, 0.508454, 0.472707],
                             [0.521643, 0.511367, 0.472639],
                             [0.525348, 0.514285, 0.472660],
                             [0.529086, 0.517207, 0.472543],
                             [0.532829, 0.520135, 0.472401],
                             [0.536553, 0.523067, 0.472352],
                             [0.540307, 0.526005, 0.472163],
                             [0.544069, 0.528948, 0.471947],
                             [0.547840, 0.531895, 0.471704],
                             [0.551612, 0.534849, 0.471439],
                             [0.555393, 0.537807, 0.471147],
                             [0.559181, 0.540771, 0.470829],
                             [0.562972, 0.543741, 0.470488],
                             [0.566802, 0.546715, 0.469988],
                             [0.570607, 0.549695, 0.469593],
                             [0.574417, 0.552682, 0.469172],
                             [0.578236, 0.555673, 0.468724],
                             [0.582087, 0.558670, 0.468118],
                             [0.585916, 0.561674, 0.467618],
                             [0.589753, 0.564682, 0.467090],
                             [0.593622, 0.567697, 0.466401],
                             [0.597469, 0.570718, 0.465821],
                             [0.601354, 0.573743, 0.465074],
                             [0.605211, 0.576777, 0.464441],
                             [0.609105, 0.579816, 0.463638],
                             [0.612977, 0.582861, 0.462950],
                             [0.616852, 0.585913, 0.462237],
                             [0.620765, 0.588970, 0.461351],
                             [0.624654, 0.592034, 0.460583],
                             [0.628576, 0.595104, 0.459641],
                             [0.632506, 0.598180, 0.458668],
                             [0.636412, 0.601264, 0.457818],
                             [0.640352, 0.604354, 0.456791],
                             [0.644270, 0.607450, 0.455886],
                             [0.648222, 0.610553, 0.454801],
                             [0.652178, 0.613664, 0.453689],
                             [0.656114, 0.616780, 0.452702],
                             [0.660082, 0.619904, 0.451534],
                             [0.664055, 0.623034, 0.450338],
                             [0.668008, 0.626171, 0.449270],
                             [0.671991, 0.629316, 0.448018],
                             [0.675981, 0.632468, 0.446736],
                             [0.679979, 0.635626, 0.445424],
                             [0.683950, 0.638793, 0.444251],
                             [0.687957, 0.641966, 0.442886],
                             [0.691971, 0.645145, 0.441491],
                             [0.695985, 0.648334, 0.440072],
                             [0.700008, 0.651529, 0.438624],
                             [0.704037, 0.654731, 0.437147],
                             [0.708067, 0.657942, 0.435647],
                             [0.712105, 0.661160, 0.434117],
                             [0.716177, 0.664384, 0.432386],
                             [0.720222, 0.667618, 0.430805],
                             [0.724274, 0.670859, 0.429194],
                             [0.728334, 0.674107, 0.427554],
                             [0.732422, 0.677364, 0.425717],
                             [0.736488, 0.680629, 0.424028],
                             [0.740589, 0.683900, 0.422131],
                             [0.744664, 0.687181, 0.420393],
                             [0.748772, 0.690470, 0.418448],
                             [0.752886, 0.693766, 0.416472],
                             [0.756975, 0.697071, 0.414659],
                             [0.761096, 0.700384, 0.412638],
                             [0.765223, 0.703705, 0.410587],
                             [0.769353, 0.707035, 0.408516],
                             [0.773486, 0.710373, 0.406422],
                             [0.777651, 0.713719, 0.404112],
                             [0.781795, 0.717074, 0.401966],
                             [0.785965, 0.720438, 0.399613],
                             [0.790116, 0.723810, 0.397423],
                             [0.794298, 0.727190, 0.395016],
                             [0.798480, 0.730580, 0.392597],
                             [0.802667, 0.733978, 0.390153],
                             [0.806859, 0.737385, 0.387684],
                             [0.811054, 0.740801, 0.385198],
                             [0.815274, 0.744226, 0.382504],
                             [0.819499, 0.747659, 0.379785],
                             [0.823729, 0.751101, 0.377043],
                             [0.827959, 0.754553, 0.374292],
                             [0.832192, 0.758014, 0.371529],
                             [0.836429, 0.761483, 0.368747],
                             [0.840693, 0.764962, 0.365746],
                             [0.844957, 0.768450, 0.362741],
                             [0.849223, 0.771947, 0.359729],
                             [0.853515, 0.775454, 0.356500],
                             [0.857809, 0.778969, 0.353259],
                             [0.862105, 0.782494, 0.350011],
                             [0.866421, 0.786028, 0.346571],
                             [0.870717, 0.789572, 0.343333],
                             [0.875057, 0.793125, 0.339685],
                             [0.879378, 0.796687, 0.336241],
                             [0.883720, 0.800258, 0.332599],
                             [0.888081, 0.803839, 0.328770],
                             [0.892440, 0.807430, 0.324968],
                             [0.896818, 0.811030, 0.320982],
                             [0.901195, 0.814639, 0.317021],
                             [0.905589, 0.818257, 0.312889],
                             [0.910000, 0.821885, 0.308594],
                             [0.914407, 0.825522, 0.304348],
                             [0.918828, 0.829168, 0.299960],
                             [0.923279, 0.832822, 0.295244],
                             [0.927724, 0.836486, 0.290611],
                             [0.932180, 0.840159, 0.285880],
                             [0.936660, 0.843841, 0.280876],
                             [0.941147, 0.847530, 0.275815],
                             [0.945654, 0.851228, 0.270532],
                             [0.950178, 0.854933, 0.265085],
                             [0.954725, 0.858646, 0.259365],
                             [0.959284, 0.862365, 0.253563],
                             [0.963872, 0.866089, 0.247445],
                             [0.968469, 0.869819, 0.241310],
                             [0.973114, 0.873550, 0.234677],
                             [0.977780, 0.877281, 0.227954],
                             [0.982497, 0.881008, 0.220878],
                             [0.987293, 0.884718, 0.213336],
                             [0.992218, 0.888385, 0.205468],
                             [0.994847, 0.892954, 0.203445],
                             [0.995249, 0.898384, 0.207561],
                             [0.995503, 0.903866, 0.212370],
                             [0.995737, 0.909344, 0.217772]]
            cmaps = {}
            for (_name, _data) in (('cividis', _cividis_data), ('test', _cividis_data)):
                cmaps[_name] = ListedColormap(_data, name=_name)
                # generate reversed colormap
                _name = _name + '_r'
                cmaps[_name] = ListedColormap(list(reversed(_data)), name=_name)
            return cmaps[name]
