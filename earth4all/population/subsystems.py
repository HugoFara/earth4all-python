"""Equations of the Population sector.

Transcribed from `src/population/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, delay_n, interpolate, ramp
from ..symbolics import D, exp, ifelse, max, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def population(name="pop", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Population sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    CMFR = sys.parameter("CMFR", params["CMFR"], "Cost of Max Fertility Reduction (share of GDP)")
    DNC80 = sys.parameter("DNC80", params["DNC80"], "DNC in 1980")
    DNCA = sys.parameter("DNCA", params["DNCA"], "DNCalfa<0")
    DNCG = sys.parameter("DNCG", params["DNCG"], "DNCgamma")
    DNCM = sys.parameter("DNCM", params["DNCM"], "DNCmin")
    EIP = sys.parameter("EIP", params["EIP"], "Exogenous Introduction Period y")
    EIPF = sys.parameter("EIPF", params["EIPF"], "Exogenous Introduction Period Flag")
    FADFS = sys.parameter("FADFS", params["FADFS"], "Fraction Achieving Desired Family Size")
    FP = sys.parameter("FP", params["FP"], "Fertile Period")
    FW = sys.parameter("FW", params["FW"], "Fraction Women")
    GEFR = sys.parameter("GEFR", params["GEFR"], "Goal for Extra Fertility Reduction")
    GEPA = sys.parameter("GEPA", params["GEPA"], "Goal for Extra Pension Age y")
    LEA = sys.parameter("LEA", params["LEA"], "LEalfa")
    LEEPA = sys.parameter("LEEPA", params["LEEPA"], "sLEeoPa>0: Life Expectancy Effect on Pension Age")
    LEG = sys.parameter("LEG", params["LEG"], "LEgamma")
    LEMAX = sys.parameter("LEMAX", params["LEMAX"], "LEmax")
    MFM = sys.parameter("MFM", params["MFM"], "Max Fertility Multiplier")
    MLEM = sys.parameter("MLEM", params["MLEM"], "Max Life Expectancy Multiplier")
    OW2022 = sys.parameter("OW2022", params["OW2022"], "Observed Warming in 2022 deg C")
    OWELE = sys.parameter("OWELE", params["OWELE"], "sOWeoLE<0: Observed Warming Effect on Life Expectancy")
    SSP2FA2022F = sys.parameter("SSP2FA2022F", params["SSP2FA2022F"], "SSP2 Family Action from 2022 Flag")
    TAHI = sys.parameter("TAHI", params["TAHI"], "Time to adapt to higher income y")
    ORDER = int(params["ORDER"])
    A0020 = sys.variable("A0020", inits["A0020"], "Aged 0-20 years Mp")
    A2040 = sys.variable("A2040", inits["A2040"], "Aged 20-40 years Mp")
    A20PA = sys.variable("A20PA", description="Aged 20-Pension Age Mp")
    A4060 = sys.variable("A4060", inits["A4060"], "Aged 40-60 Mp")
    A60PL = sys.variable("A60PL", inits["A60PL"], "Aged 60 + Mp")
    BIRTHR = sys.variable("BIRTHR", description="Birth Rate 1/y")
    BIRTHS = sys.variable("BIRTHS", description="Births Mp/y")
    CEFR = sys.variable("CEFR", description="Cost of Extra Fertility Reduction (share of GDP)")
    DEATHR = sys.variable("DEATHR", description="Death Rate 1/y")
    DEATHS = sys.variable("DEATHS", description="Deaths Mp/y")
    DNC = sys.variable("DNC", description="Desired No of Children 1")
    DR = sys.variable("DR", description="Dependency Ratio p/p")
    EFR = sys.variable("EFR", description="Extra Fertility Reduction (1)")
    EGDPP = sys.variable("EGDPP", inits["EGDPP"], "Effective GDP per Person kDollar/p/y")
    EPA = sys.variable("EPA", inits["EPA"], "Extra Pension Age y")
    FM = sys.variable("FM", description="Fertility Multiplier (1)")
    GDPP = sys.variable("GDPP", description="GDP per Person kDollar/p/y")
    LE = sys.variable("LE", inits["LE"], "Life Expectancy y")
    LE60 = sys.variable("LE60", description="LE at 60 y")
    LEM = sys.variable("LEM", description="Life Expectancy Multipler (1)")
    LV_DEATHS = sys.variable_array("LV_DEATHS", ORDER, inits["DEATHS"] * (inits["LE"] - 60) / ORDER, "LV functions for deaths Mp/y")
    LV_PASS20 = sys.variable_array("LV_PASS20", ORDER, inits["PASS20"] * 20 / ORDER, "LV functions for passing 20 Mp/y")
    LV_PASS40 = sys.variable_array("LV_PASS40", ORDER, inits["PASS40"] * 20 / ORDER, "LV functions for passing 40 Mp/y")
    LV_PASS60 = sys.variable_array("LV_PASS60", ORDER, inits["PASS60"] * 20 / ORDER, "LV functions for passing 60 Mp/y")
    OF = sys.variable("OF", description="Observed Fertility 1")
    OP = sys.variable("OP", description="On Pension Mp")
    PA = sys.variable("PA", inits["PA"], "Pension Age y")
    PASS20 = sys.variable("PASS20", description="Passing 20 Mp/y")
    PASS40 = sys.variable("PASS40", inits["PASS40"], "Passing 40 Mp/y")
    PASS60 = sys.variable("PASS60", inits["PASS60"], "Passing 60 Mp/y")
    PGR = sys.variable("PGR", description="Population Growth Rate 1/y")
    POP = sys.variable("POP", description="Population Mp")
    PW = sys.variable("PW", description="Pensioners per Worker p/p")
    RT_DEATHS = sys.variable_array("RT_DEATHS", ORDER, inits["DEATHS"] * (inits["LE"] - 60) / ORDER, "RT functions for deaths Mp/y")
    RT_PASS20 = sys.variable_array("RT_PASS20", ORDER, inits["PASS20"] * 20 / ORDER, "RT functions for passing 20 Mp/y")
    RT_PASS40 = sys.variable_array("RT_PASS40", ORDER, inits["PASS40"] * 20 / ORDER, "RT functions for passing 40 Mp/y")
    RT_PASS60 = sys.variable_array("RT_PASS60", ORDER, inits["PASS60"] * 20 / ORDER, "RT functions for passing 60 Mp/y")
    WELE = sys.variable("WELE", description="Warming Effect on Life Expectancy (1)")
    GDP = sys.variable("GDP")
    IPP = sys.variable("IPP")
    OW = sys.variable("OW")
    add_equation(eqs, D(A0020), BIRTHS - PASS20)
    add_equation(eqs, D(A2040), PASS20 - PASS40)
    add_equation(eqs, A20PA, A2040 + A4060 + A60PL - OP)
    add_equation(eqs, D(A4060), PASS40 - PASS60)
    add_equation(eqs, D(A60PL), PASS60 - DEATHS)
    add_equation(eqs, BIRTHR, BIRTHS / POP)
    add_equation(eqs, BIRTHS, A2040 * FW * (OF / FP))
    add_equation(eqs, CEFR, CMFR * EFR)
    add_equation(eqs, DEATHR, DEATHS / POP)
    delay_n(eqs, PASS60, RT_DEATHS, LV_DEATHS, LE60, ORDER)
    add_equation(eqs, DEATHS, RT_DEATHS[ORDER - 1])
    add_equation(eqs, DNC, ((DNCM + (DNC80 - DNCM) * exp(-DNCG * (EGDPP - inits["EGDPP"]))) * (1 + DNCA * (EGDPP - inits["EGDPP"]))) * (1 - EFR) * FM)
    add_equation(eqs, DR, (A0020 + A60PL) / (A2040 + A4060))
    add_equation(eqs, EFR, ramp(t, GEFR / IPP, 2022, 2022 + IPP))
    add_equation(eqs, EPA, ramp(t, (GEPA - inits["EPA"]) / IPP, 2022, 22022 + IPP))
    add_equation(eqs, D(EGDPP), (GDPP - EGDPP) / TAHI)
    add_equation(eqs, FM, ifelse(SSP2FA2022F > 0, ifelse(t > 2022, 1 + ramp(t, (MFM - 1) / 78, 2022, 2100), 1), 1))
    add_equation(eqs, GDPP, GDP / POP)
    add_equation(eqs, LE, ((LEMAX - (LEMAX - inits["LE"]) * exp(-LEG * (EGDPP - inits["EGDPP"]))) * (1 + LEA * (EGDPP - inits["EGDPP"]))) * WELE * LEM)
    add_equation(eqs, LE60, LE - 60)
    add_equation(eqs, LEM, ifelse(SSP2FA2022F > 0, ifelse(t > 2022, 1 + ramp(t, (MLEM - 1) / 78, 2022, 2100), 1), 1))
    add_equation(eqs, OF, DNC * FADFS)
    add_equation(eqs, OP, A60PL * (LE - PA) / (LE - 60))
    add_equation(eqs, PA, ifelse(LE < inits["LE"], inits["PA"], inits["PA"] + LEEPA * (LE + EPA - inits["LE"])))
    delay_n(eqs, BIRTHS, RT_PASS20, LV_PASS20, 20, ORDER)
    add_equation(eqs, PASS20, RT_PASS20[ORDER - 1])
    delay_n(eqs, PASS20, RT_PASS40, LV_PASS40, 20, ORDER)
    add_equation(eqs, PASS40, RT_PASS40[ORDER - 1])
    delay_n(eqs, PASS40, RT_PASS60, LV_PASS60, 20, ORDER)
    add_equation(eqs, PASS60, RT_PASS60[ORDER - 1])
    add_equation(eqs, PGR, BIRTHR - DEATHR)
    add_equation(eqs, POP, A0020 + A2040 + A4060 + A60PL)
    add_equation(eqs, PW, OP / A20PA)
    add_equation(eqs, WELE, ifelse(t > 2022, max(0, 1 + OWELE * (OW / OW2022 - 1)), 1))
    return sys


def population_full_support(name="pop", params=None, inits=None, tables=None, ranges=None):
    """The Population sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    GDP = sys.variable("GDP", description="Inventory.GDP GDollar/y")
    IPP = sys.variable("IPP", description="Wellbeing.Introduction period for policy y")
    OW = sys.variable("OW", description="Climate.Observed warming deg C")
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, IPP, interpolate(t, tables["IPP"], ranges["IPP"]))
    add_equation(eqs, OW, interpolate(t, tables["OW"], ranges["OW"]))
    return sys


def population_partial_support(name="pop", params=None, inits=None, tables=None, ranges=None):
    """The Population sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    GDP = sys.variable("GDP", description="Inventory.GDP GDollar/y")
    IPP = sys.variable("IPP", description="Wellbeing.Introduction period for policy y")
    OW = sys.variable("OW", description="Climate.Observed warming deg C")
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, IPP, interpolate(t, tables["IPP"], ranges["IPP"]))
    add_equation(eqs, OW, interpolate(t, tables["OW"], ranges["OW"]))
    return sys
