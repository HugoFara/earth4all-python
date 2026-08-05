"""Equations of the Finance sector.

Transcribed from `src/finance/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, smooth
from ..symbolics import D, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def finance(name="fin", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Finance sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    FSRT = sys.parameter("FSRT", params["FSRT"], "Financial Sector Response Time y")
    GRCR = sys.parameter("GRCR", params["GRCR"], "sGReoCR<0: Growth Rate effect on Credit Risk")
    IEFT = sys.parameter("IEFT", params["IEFT"], "Inflation Expectation Formation Time y")
    INSR = sys.parameter("INSR", params["INSR"], "sINeoSR>0: INflation effect on Signal Rate")
    IPTCB = sys.parameter("IPTCB", params["IPTCB"], "Inflation Perception Time CB y")
    IT = sys.parameter("IT", params["IT"], "Inflation Target 1/y")
    NBOM = sys.parameter("NBOM", params["NBOM"], "Normal Bank Operating Margin 1/y")
    NBBM = sys.parameter("NBBM", params["NBBM"], "Normal Basic Bank Margin 1/y")
    NSR = sys.parameter("NSR", params["NSR"], "Normal Signal Rate 1/y")
    SRAT = sys.parameter("SRAT", params["SRAT"], "Signal Rate Adjustment Time y")
    UPTCB = sys.parameter("UPTCB", params["UPTCB"], "Unemployment Perception Time CB y")
    UNSR = sys.parameter("UNSR", params["UNSR"], "sUNeoSR<0: UNemployment effect on Signal Rate")
    UT = sys.parameter("UT", params["UT"], "Unemployment Target")
    CBC = sys.variable("CBC", description="Corporate Borrowing Cost 1/y")
    CBSR = sys.variable("CBSR", inits["CBSR"], "Central Bank Signal Rate 1/y")
    CCSD = sys.variable("CCSD", inits["CCSD"], "Cost of Capital for Secured Debt 1/y")
    CSR = sys.variable("CSR", description="Change in Signal Rate 1/yy")
    GBC = sys.variable("GBC", description="Govmnt Borrowing Cost 1/y")
    CBC1980 = sys.variable("CBC1980", description="Corporate Borrowing Cost in 1980 1/y")
    ELTI = sys.variable("ELTI", inits["ELTI"], "Expected Long Term Inflation 1/y")
    ISR = sys.variable("ISR", description="Indicated Signal Rate 1/y")
    NCCR = sys.variable("NCCR", description="Normal Corporate Credit Risk 1/y")
    PI = sys.variable("PI", inits["PI"], "Perceived Inflation CB 1/y")
    PU = sys.variable("PU", inits["PU"], "Perceived Unemployment CB (1)")
    TGIR = sys.variable("TGIR", description="10-yr Govmnt Interest Rate 1/y")
    TIR = sys.variable("TIR", description="3m Interest Rate 1/y")
    WBC = sys.variable("WBC", description="Worker Borrowing Cost 1/y")
    IR = sys.variable("IR")
    OGR = sys.variable("OGR")
    UR = sys.variable("UR")
    add_equation(eqs, CBC, CCSD + NCCR)
    add_equation(eqs, CBC1980, NSR + NBBM + NBOM + NCCR)
    smooth(eqs, CCSD, TIR + NBOM, FSRT)
    add_equation(eqs, D(CBSR), CSR)
    add_equation(eqs, CSR, (ISR - CBSR) / SRAT)
    smooth(eqs, ELTI, PI, IEFT)
    add_equation(eqs, GBC, TIR)
    add_equation(eqs, ISR, NSR * (1 + INSR * (PI / IT - 1) + UNSR * (PU / UT - 1)))
    add_equation(eqs, NCCR, 0.02 * (1 + GRCR * (OGR / 0.03 - 1)))
    smooth(eqs, PI, IR, IPTCB)
    smooth(eqs, PU, UR, UPTCB)
    add_equation(eqs, TGIR, GBC + ELTI)
    add_equation(eqs, TIR, CBSR + NBBM)
    add_equation(eqs, WBC, CCSD)
    return sys


def finance_full_support(name="fin", params=None, inits=None, tables=None, ranges=None):
    """The Finance sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    IR = sys.variable("IR", description="Inventory.Inflation Rate 1/y")
    OGR = sys.variable("OGR", description="Output.Output Growth Rate 1/y")
    UR = sys.variable("UR", description="Labour market.Unemployment Rate (1)")
    add_equation(eqs, IR, interpolate(t, tables["IR"], ranges["IR"]))
    add_equation(eqs, OGR, interpolate(t, tables["OGR"], ranges["OGR"]))
    add_equation(eqs, UR, interpolate(t, tables["UR"], ranges["UR"]))
    return sys


def finance_partial_support(name="fin", params=None, inits=None, tables=None, ranges=None):
    """The Finance sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    IR = sys.variable("IR", description="Inventory.Inflation Rate 1/y")
    OGR = sys.variable("OGR", description="Output.Output Growth Rate 1/y")
    UR = sys.variable("UR", description="Labour market.Unemployment Rate (1)")
    add_equation(eqs, IR, interpolate(t, tables["IR"], ranges["IR"]))
    add_equation(eqs, OGR, interpolate(t, tables["OGR"], ranges["OGR"]))
    add_equation(eqs, UR, interpolate(t, tables["UR"], ranges["UR"]))
    return sys
