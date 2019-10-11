import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import theano_shim as shim
import pymc3 as pm
import arviz as az
import sampling_tutorial.SigFigRounding as sfr
from decimal import Decimal
from collections import Iterable

mpl.rcParams['figure.figsize'] = [10, 4]

shim.load_theano()

class cDist(pm.Continuous):
    def __init__(self, n, s=(0.,0.), domain_center=(0.,0.), domain_radius=10., **kwargs):
        self.domain_center = shim.asarray(domain_center)
        self.domain_radius = shim.cast_floatX(domain_radius)
        self.s = shim.cast_floatX(s, same_kind=False)
        self.n = n
        kwargs['testval'] = self.domain_center
        super().__init__(shape=(2,), **kwargs)
    def logp(self, c):
        def f(x):
            return shim.stack((x[...,0]**2 - x[...,1]**2, 2*x[...,0]*x[...,1]), axis=-1) + c
        x = self.s
        for i in range(self.n):
            x = f(x)
        def norm(_x):
            return shim.sum(abs(_x), axis=-1)
        bound = SmoothClip(4.)
        flatten_at_zero = FlatLowerBound(0., 0.001)
        return ((bound.high - bound(flatten_at_zero(norm(x))))
                - (shim.sum((c-self.domain_center)**2)/(2*self.domain_radius)))
    def _repr_latex_(self, name=None, dist=None):
        if dist is None:
            dist = self
        name = r'\text{%s}' % name
        s = getattr(self.s, 'name', round(self.s, 3))  # Use name for symbolics, number for plain vars
        if isinstance(s, np.ndarray):
            s = r'\begin{bmatrix}' + r'\\'.join(str(_s) for _s in s) + r'\end{bmatrix}'
        return r'${} \sim \mathcal{{D}}_{{{}}}\left({}\right)$'.format(name, self.n, s)

class SmoothClip:
    """
    Smooth, symmetric clippin function using the hyperbolic tangent.
    Takes a single parameter, Δ, which sets both the expected domain
    and the value of the bounds.

    Parameters:
    Δ: Positive number.
       The smoother is approximately the identity on [-Δ, Δ].
       Function will be bounded by (-2Δ, 2Δ).
    """
    def __init__(self, Δ):
        self.Δ = Δ
    def __call__(self, x):
        Δ = self.Δ
        return (2*Δ) * shim.tanh(x/(2*Δ))
    @property
    def low(self):
        return -2*self.Δ
    @property
    def high(self):
        return 2*self.Δ

class FlatBound:
    """
    Make a boundary flat (i.e. its derivative zero). Function is only valid on one side
    of the bound.

    **Important**: This does not enforce the bound. If you
    can't guarantee that x remains on the correct side of
    the bound, combine it with clipping:

    >>> smooth = SmoothLowerBound(0)
    >>> result = smooth(clip(x, 0, None))
    """

    def __init__(self, bound, β, side):
        """
        :param bound: Bound at which we want a flat derivative.
        :param β: Scale over which the input is distorted to achieve flat derivative.
        :param side: Either 'upper' or 'lower'.
        """
        self.bound = shim.cast_floatX(bound, same_kind=False)
        assert side in ('upper', 'lower')
        self.β = shim.cast_floatX(β, same_kind=False)
        self.a = {'upper': 1, 'lower': -1}[side]

    def __call__(self, x):
        β = self.β
        a = self.a
        return shim.ifelse(shim.eq(x,self.bound).all(),
                           shim.broadcast_to(self.bound + β, x.shape),
                           shim.cast_floatX(x + β*shim.exp(a*x/β)))

class FlatLowerBound(FlatBound):
    def __init__(self, bound, β):
        super().__init__(bound, β, 'lower')
class FlatUpperBound(FlatBound):
    def __init__(self, bound, β):
        super().__init__(bound, β, 'upper')

def effective_n(trace, sigdigits=3):
    ess = az.stats.diagnostics.ess(trace)
    data = round(ess['c'].data, sigdigits)
    if np.all(data == data.astype(int)):
        data = data.astype(int)
    ess['c'].data = data
    df = ess.to_dataframe()
    df.index = pd.Index(['$c_0$', '$c_1$'])
    df.columns = pd.Index(['effective sample size'])
    dftotal = pd.DataFrame(np.ones(2, dtype=int)*len(trace)*trace.nchains,
                           index = pd.Index(['$c_0$', '$c_1$']),
                           columns = pd.Index(['total samples']))
    return pd.concat((df, dftotal), axis='columns')

def round(x, sigfigs):
    if isinstance(x, np.ndarray):
        return int_if_no_decimal(np.array([sfr.RoundToSigFigs_decim(Decimal(_x), sigfigs) for _x in x]).astype(x.dtype))
    elif isinstance(x, Iterable):
        return int_if_no_decimal(type(x)(sfr.RoundToSigFigs_decim(Decimal(_x), sigfigs) for _x in x))
    else:
        return int_if_no_decimal(type(x)(sfr.RoundToSigFigs_decim(Decimal(x), sigfigs)))

import builtins
def int_if_no_decimal(x, int_dtype=np.int32):
    # TODO: Check that int_dtype is big enough for x
    if isinstance(x, np.ndarray):
        x_round = np.round(x)
        if np.all(x_round == x):
            return x_round.astype(int_dtype)
        else:
            return x
    elif isinstance(x, Iterable):
        def _r(y):
            for _y in y:
                y_round = builtins.round(_y)
                if y_round == _y:
                    yield int_dtype(y_round)
                else:
                    yield _y
        return type(x)(_r(x))
    else:
        x_round = builtins.round(x)
        if x_round == x:
            return int_dtype(x_round)
        else:
            return x
        
def format_traceplot(axes):
    for ax in axes[:,0]:
        ax.set_title("$c_0$")
    for ax in axes[:,1]:
        ax.set_title("$c_1$")
    fig = plt.gcf()
    fig.set_figwidth(8)
    fig.set_figheight(3)
    return axes
        
def format_joint_plot(axes, radius=None):
    axjoin, axhistx, axhisty = axes
    axjoin.set_xlabel('$c_0$')
    axjoin.set_ylabel('$c_1$')
    if radius is not None:
        axjoin.set_xlim(-radius, radius)
        axjoin.set_ylim(-radius, radius)
        
##################
# Archive

def cDist_pure_numpy():
    """Easier to play around with than the PyMC3 model."""
    n = 2
    def f(x, c):
        return np.stack((x[...,0]**2 - x[...,1]**2, 2*x[...,0]*x[...,1]), axis=-1) + c
    bound = SmoothClip(4.)
    flatten_at_zero = FlatLowerBound(0, .001)
    def p(c):
        c = np.array(c); x = np.zeros(2)
        for i in range(n):
            x = f(x, c)
        def norm(x):
            # return np.linalg.norm(x, axis=-1)
            return np.sum(abs(x), axis=-1)
        return np.exp((bound.high - bound(flatten_at_zero(norm(x))))**1.5)
        #return np.log(np.linalg.norm(x, axis=-1))
    
    return pd.DataFrame(p(XY),
                  index=np.round(XX[0,:], 3), columns=np.round(YY[:,0], 3))
