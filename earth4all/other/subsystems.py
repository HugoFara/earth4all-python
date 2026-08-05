"""Equations of the Other sector.

Transcribed from `src/other/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, smooth
from ..symbolics import exp, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def other(name="oth", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Other sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    INELOK = sys.parameter("INELOK", params["INELOK"], "sINEeoLOK<0: INequity Effect on LOgistic K")
    NK = sys.parameter("NK", params["NK"], "Normal K")
    TEGR = sys.parameter("TEGR", params["TEGR"], "Time to Establish Growth Rate y")
    CFETA = sys.variable("CFETA", description="Cost of Food and Energy TAs GDollar/y")
    CTA = sys.variable("CTA", description="Cost of TAs GDollar/y")
    FB15 = sys.variable("FB15", description="Fraction Below 15 kDollar/p/y (1)")
    IEL = sys.variable("IEL", description="Inequity Effect on Logistic k (1)")
    LK = sys.variable("LK", description="Logistic K (1)")
    PB15 = sys.variable("PB15", description="Population Below 15 kDollar/p/y Mp")
    PGDPP = sys.variable("PGDPP", inits["PGDPP"], "Past GDP per Person kDollar/y")
    RGGDPP = sys.variable("RGGDPP", description="Rate of Growth in GDP per Person 1/y")
    CE = sys.variable("CE")
    COFO = sys.variable("COFO")
    GDPP = sys.variable("GDPP")
    INEQ = sys.variable("INEQ")
    POP = sys.variable("POP")
    add_equation(eqs, CFETA, COFO + CE)
    add_equation(eqs, CTA, CFETA)
    add_equation(eqs, FB15, 1 - (1 / (1 + exp(-LK * (GDPP - 14)))))
    add_equation(eqs, IEL, 1 + INELOK * (INEQ / 0.5 - 1))
    add_equation(eqs, LK, NK * IEL)
    add_equation(eqs, PB15, POP * FB15)
    add_equation(eqs, RGGDPP, ((GDPP - PGDPP) / PGDPP) / TEGR)
    smooth(eqs, PGDPP, GDPP, TEGR)
    return sys


def other_full_support(name="oth", params=None, inits=None, tables=None, ranges=None):
    """The Other sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    CE = sys.variable("CE", description="Energy.Cost of Energy GDollar/y")
    COFO = sys.variable("COFO", description="Food and land.Cost of Food GDollar/y")
    GDPP = sys.variable("GDPP", description="Population.GDP per Person kDollar/p/y")
    INEQ = sys.variable("INEQ", description="Demand.Inequality")
    POP = sys.variable("POP", description="Population.Population Mp")
    add_equation(eqs, CE, interpolate(t, tables["CE"], ranges["CE"]))
    add_equation(eqs, COFO, interpolate(t, tables["COFO"], ranges["COFO"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, INEQ, interpolate(t, tables["INEQ"], ranges["INEQ"]))
    add_equation(eqs, POP, interpolate(t, tables["POP"], ranges["POP"]))
    return sys


def other_partial_support(name="oth", params=None, inits=None, tables=None, ranges=None):
    """The Other sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    CE = sys.variable("CE", description="Energy.Cost of Energy GDollar/y")
    COFO = sys.variable("COFO", description="Food and land.Cost of Food GDollar/y")
    GDPP = sys.variable("GDPP", description="Population.GDP per Person kDollar/p/y")
    INEQ = sys.variable("INEQ", description="Demand.Inequality")
    POP = sys.variable("POP", description="Population.Population Mp")
    add_equation(eqs, CE, interpolate(t, tables["CE"], ranges["CE"]))
    add_equation(eqs, COFO, interpolate(t, tables["COFO"], ranges["COFO"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, INEQ, interpolate(t, tables["INEQ"], ranges["INEQ"]))
    add_equation(eqs, POP, interpolate(t, tables["POP"], ranges["POP"]))
    return sys
