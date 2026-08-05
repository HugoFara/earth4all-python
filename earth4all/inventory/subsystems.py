"""Equations of the Inventory sector.

Transcribed from `src/inventory/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, pulse, smooth
from ..symbolics import D, ifelse, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def inventory(name="inv", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Inventory sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    DAT = sys.parameter("DAT", params["DAT"], "Demand Adjustment Time y")
    DDI1980 = sys.parameter("DDI1980", params["DDI1980"], "DDI in 1980 y")
    DIC = sys.parameter("DIC", params["DIC"], "Desired Inventory Coverage y")
    DRI = sys.parameter("DRI", params["DRI"], "Desired Relative Inventory")
    ICPT = sys.parameter("ICPT", params["ICPT"], "Inventory Coverage Perception Time y")
    MRIWI = sys.parameter("MRIWI", params["MRIWI"], "Minimum Relative Inventory Without Inflation")
    OO = sys.parameter("OO", params["OO"], "Optimal Output in 1980 Gu/y")
    PH = sys.parameter("PH", params["PH"], "Pulse Height")
    PPU = sys.parameter("PPU", params["PPU"], "Price Per Unit /u")
    SAT = sys.parameter("SAT", params["SAT"], "Sales Averaging Time y")
    INVEODDI = sys.parameter("INVEODDI", params["INVEODDI"], "sINVeoDDI < 0: INVentory Effect On Delivery Delay Index")
    INVEOIN = sys.parameter("INVEOIN", params["INVEOIN"], "sINVeoIN < 0: INVentory Effect On INflation")
    INVEOSWI = sys.parameter("INVEOSWI", params["INVEOSWI"], "sINVeoSWI < 0: INVentory Effect On Shifts Worked Index")
    SRI = sys.parameter("SRI", params["SRI"], "Sufficient Relative Inventory")
    SWI1980 = sys.parameter("SWI1980", params["SWI1980"], "SWI in 1980")
    TAS = sys.parameter("TAS", params["TAS"], "Time to Adjust Shifts y")
    DELDI = sys.variable("DELDI", inits["DELDI"], "DELivery Delay - Index (1)")
    EPP = sys.variable("EPP", inits["EPP"], "Effective Purchasing Power Gdollar/y")
    INV = sys.variable("INV", inits["INV"], "INVentory Gu")
    PRIN = sys.variable("PRIN", inits["PRIN"], "PRice INdex (1980=1)")
    PRI = sys.variable("PRI", inits["PRI"], "Perceived Relative Inventory (1)")
    RS = sys.variable("RS", inits["RS"], "Recent Sales Gu/y")
    SSWI = sys.variable("SSWI", inits["SSWI"], "ShiftS Worked - Index (1)")
    CDDI = sys.variable("CDDI", description="Change in DDI 1/y")
    CPI = sys.variable("CPI", description="Change in Price Index 1/y")
    DEL = sys.variable("DEL", description="DELiveries Gu/y")
    DEPU = sys.variable("DEPU", description="DEmand PUlse 2020-25 (1)")
    DSWI = sys.variable("DSWI", description="Desired Shifts Worked - Index (1)")
    GDP = sys.variable("GDP", description="GDP Gdollar/y")
    IC = sys.variable("IC", description="Inventory Coverage y")
    IR = sys.variable("IR", description="Inflation Rate 1/y")
    NI = sys.variable("NI", description="National Income Gdollar/y")
    OUTP = sys.variable("OUTP", description="OUTPut Gu/y")
    PNIS = sys.variable("PNIS", description="Pink Noise In Sales (1)")
    ROCDDI = sys.variable("ROCDDI", description="ROC in DDI 1/y")
    SA = sys.variable("SA", description="SAles Gdollar/y")
    ORO = sys.variable("ORO")
    TPP = sys.variable("TPP")
    add_equation(eqs, CDDI, ROCDDI * DELDI)
    add_equation(eqs, CPI, PRIN * IR)
    add_equation(eqs, DEL, ((EPP / PPU) / (DELDI / DDI1980)) * ifelse(t > 1984, PNIS, 1))
    add_equation(eqs, D(DELDI), CDDI)
    add_equation(eqs, DEPU, 0 + PH * pulse(t, 2020, 5))
    add_equation(eqs, DSWI, 1 + INVEOSWI * (PRI / DRI - 1))
    smooth(eqs, EPP, TPP, DAT)
    add_equation(eqs, GDP, OUTP * PPU)
    add_equation(eqs, IC, INV / RS)
    add_equation(eqs, D(INV), OUTP - DEL)
    add_equation(eqs, IR, INVEOIN * (PRI / MRIWI - 1))
    add_equation(eqs, NI, SA)
    add_equation(eqs, OUTP, ORO * SSWI / SWI1980)
    add_equation(eqs, D(PRIN), CPI)
    add_equation(eqs, PNIS, 1)
    smooth(eqs, PRI, (IC / DIC), ICPT)
    add_equation(eqs, ROCDDI, 0 + INVEODDI * (PRI / SRI - 1))
    smooth(eqs, RS, DEL, SAT)
    add_equation(eqs, SA, DEL * PPU)
    smooth(eqs, SSWI, DSWI, TAS)
    return sys


def inventory_full_support(name="inv", params=None, inits=None, tables=None, ranges=None):
    """The Inventory sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    ORO = sys.variable("ORO", description="Output.Optimal Real Output Gu/y")
    TPP = sys.variable("TPP", description="Demand.Total Purchasing Power G/y")
    add_equation(eqs, ORO, interpolate(t, tables["ORO"], ranges["ORO"]))
    add_equation(eqs, TPP, interpolate(t, tables["TPP"], ranges["TPP"]))
    return sys


def inventory_partial_support(name="inv", params=None, inits=None, tables=None, ranges=None):
    """The Inventory sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    ORO = sys.variable("ORO", description="Output.Optimal Real Output Gu/y")
    TPP = sys.variable("TPP", description="Demand.Total Purchasing Power G/y")
    add_equation(eqs, ORO, interpolate(t, tables["ORO"], ranges["ORO"]))
    add_equation(eqs, TPP, interpolate(t, tables["TPP"], ranges["TPP"]))
    return sys
