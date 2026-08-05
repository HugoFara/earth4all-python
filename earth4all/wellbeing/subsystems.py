"""Equations of the Wellbeing sector.

Transcribed from `src/wellbeing/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, smooth
from ..symbolics import exp, ifelse, log, max, min, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def wellbeing(name="wel", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Wellbeing sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    AI = sys.parameter("AI", params["AI"], "Acceptable Inequality")
    AP = sys.parameter("AP", params["AP"], "Acceptable Progress 1/y")
    AWBPD = sys.parameter("AWBPD", params["AWBPD"], "Average WellBeing Perception Delay y")
    DRDI = sys.parameter("DRDI", params["DRDI"], "Diminishing Return Disposable Income")
    DRPS = sys.parameter("DRPS", params["DRPS"], "Diminishing Return Public Spending")
    EIP = sys.parameter("EIP", params["EIP"], "Exogenous Introduction Period y")
    EIPF = sys.parameter("EIPF", params["EIPF"], "Exogenous Introduction Period Flag")
    GWEAWBGWF = sys.parameter("GWEAWBGWF", params["GWEAWBGWF"], "sGWeoAW<0: Global Warming Effect on Average WellBeing from Global Warming Flag")
    IEAWBIF = sys.parameter("IEAWBIF", params["IEAWBIF"], "sIIeoAW<0: Inequality Effect on Average WellBeing from Inequality Flag")
    MWBGW = sys.parameter("MWBGW", params["MWBGW"], "Min WellBeing from Global Warming")
    NRD = sys.parameter("NRD", params["NRD"], "Normal Reform Delay y")
    PAEAWBF = sys.parameter("PAEAWBF", params["PAEAWBF"], "sLPeoAWP>0: PArtecipation Effect on Average WellBeing Flag")
    PREAWBF = sys.parameter("PREAWBF", params["PREAWBF"], "sROPeoAW>0: PRogress Effect on Average WellBeing Flag")
    PESTF = sys.parameter("PESTF", params["PESTF"], "sPPReoSTE<0: Progress Effect on Social Tension Flag")
    SPS = sys.parameter("SPS", params["SPS"], "Satisfactory Public Spending")
    STEERDF = sys.parameter("STEERDF", params["STEERDF"], "sSTEeoRD>0: Social Tension Effect on Reform Delay Flag")
    STRERDF = sys.parameter("STRERDF", params["STRERDF"], "sSTReoRD<0: Social Trust Effect on Reform Delay Flag")
    TCRD = sys.parameter("TCRD", params["TCRD"], "Time to Change Reform Delay y")
    TDI = sys.parameter("TDI", params["TDI"], "Threshold Disposable Income kdollar/p/y")
    TEST = sys.parameter("TEST", params["TEST"], "Time to Establish Social Trust y")
    TI = sys.parameter("TI", params["TI"], "Threshold Inequality")
    TP = sys.parameter("TP", params["TP"], "Threshold Participation")
    TPR = sys.parameter("TPR", params["TPR"], "Threshold Progress Rate 1/y")
    TPS = sys.parameter("TPS", params["TPS"], "Threshold Public Spending kdollar/p/y")
    TW = sys.parameter("TW", params["TW"], "Threshold Warming deg C")
    AWBDI = sys.variable("AWBDI", description="Average WellBeing from Disposable Income (1)")
    AWBGW = sys.variable("AWBGW", description="Average WellBeing from Global Warming (1)")
    AWBI = sys.variable("AWBI", description="Average WellBeing Index (1)")
    AWBIN = sys.variable("AWBIN", description="Average WellBeing from INequality (1)")
    AWBPS = sys.variable("AWBPS", description="Average WellBeing from Public Spending (1)")
    AWBP = sys.variable("AWBP", description="Average WellBeing from Progress (1)")
    IEST = sys.variable("IEST", description="Inequity Effect on Social Trust (1)")
    IPP = sys.variable("IPP", description="Introduction Period for Policy y")
    IRD = sys.variable("IRD", description="Indicated Reform Delay y")
    IST = sys.variable("IST", description="Indicated Social Trust (1)")
    ORP = sys.variable("ORP", inits["ORP"], "Observed Rate of Progress 1/y")
    PAWBI = sys.variable("PAWBI", inits["PAWBI"], "Past AWI (1)")
    PSESTR = sys.variable("PSESTR", description="Public Spending Effect on Social TRust (1)")
    PSSGDP = sys.variable("PSSGDP", description="Public Spending as Share of GDP")
    RD = sys.variable("RD", inits["RD"], "Reform Delay y")
    STR = sys.variable("STR", inits["STR"], "Social Trust (1)")
    STE = sys.variable("STE", inits["STE"], "Social TEnsion (1)")
    STEERD = sys.variable("STEERD", description="Social TEnsion Effect on Reform Delay (1)")
    STRERD = sys.variable("STRERD", description="Social TRust Effect on Reform Delay (1)")
    WBEP = sys.variable("WBEP", description="WellBeing Effect of Participation (1)")
    GDPP = sys.variable("GDPP")
    INEQ = sys.variable("INEQ")
    LPR = sys.variable("LPR")
    PSP = sys.variable("PSP")
    PWA = sys.variable("PWA")
    WDI = sys.variable("WDI")
    add_equation(eqs, AWBDI, exp(DRDI + log(WDI / TDI)))
    add_equation(eqs, AWBIN, 1 + IEAWBIF * (INEQ / TI - 1))
    add_equation(eqs, AWBGW, max(MWBGW, min(1, 1 + GWEAWBGWF * (PWA / TW - 1))))
    add_equation(eqs, AWBI, (0.5 * AWBDI + 0.5 * AWBPS) * AWBIN * AWBGW * AWBP)
    add_equation(eqs, AWBP, (1 + PREAWBF * (ORP - TPR)) * WBEP)
    add_equation(eqs, AWBPS, exp(DRPS + log(PSP / TPS)))
    add_equation(eqs, IEST, interpolate(INEQ / AI, tables["IEST"], ranges["IEST"]))
    add_equation(eqs, IPP, ifelse(EIPF > 0, EIP, RD))
    add_equation(eqs, IRD, NRD * STRERD * STEERD)
    add_equation(eqs, IST, PSESTR * IEST)
    smooth(eqs, ORP, ((AWBI - PAWBI) / AWBI) / AWBPD, AWBPD)
    smooth(eqs, PAWBI, AWBI, AWBPD)
    add_equation(eqs, PSSGDP, PSP / GDPP)
    add_equation(eqs, PSESTR, interpolate(PSSGDP / SPS, tables["PSESTR"], ranges["PSESTR"]))
    smooth(eqs, RD, IRD, TCRD)
    add_equation(eqs, STE, 1 + PESTF * (ORP - AP))
    add_equation(eqs, STEERD, 1 + STEERDF * (STE / inits["STE"] - 1))
    add_equation(eqs, STRERD, 1 + STRERDF * (STR / inits["STR"] - 1))
    smooth(eqs, STR, IST, TEST)
    add_equation(eqs, WBEP, 1 + PAEAWBF * (LPR / TP - 1))
    return sys


def wellbeing_full_support(name="wel", params=None, inits=None, tables=None, ranges=None):
    """The Wellbeing sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    GDPP = sys.variable("GDPP", description="Population.GDP per Person kdollar/p/y")
    INEQ = sys.variable("INEQ", description="Demand.INEQuality")
    LPR = sys.variable("LPR", description="Labour and market.Labour Participation Rate (1)")
    PSP = sys.variable("PSP", description="Public.Public Spending per Person kDollar/p/y")
    PWA = sys.variable("PWA", description="Climate.Perceived warming deg C")
    WDI = sys.variable("WDI", description="Demand.Worker disposable income kDollar/p/y")
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, INEQ, interpolate(t, tables["INEQ"], ranges["INEQ"]))
    add_equation(eqs, LPR, interpolate(t, tables["LPR"], ranges["LPR"]))
    add_equation(eqs, PSP, interpolate(t, tables["PSP"], ranges["PSP"]))
    add_equation(eqs, PWA, interpolate(t, tables["PWA"], ranges["PWA"]))
    add_equation(eqs, WDI, interpolate(t, tables["WDI"], ranges["WDI"]))
    return sys


def wellbeing_partial_support(name="wel", params=None, inits=None, tables=None, ranges=None):
    """The Wellbeing sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    GDPP = sys.variable("GDPP", description="Population.GDP per Person kdollar/p/y")
    INEQ = sys.variable("INEQ", description="Demand.INEQuality")
    LPR = sys.variable("LPR", description="Labour and market.Labour Participation Rate (1)")
    PSP = sys.variable("PSP", description="Public.Public Spending per Person kDollar/p/y")
    PWA = sys.variable("PWA", description="Climate.Perceived warming deg C")
    WDI = sys.variable("WDI", description="Demand.Worker disposable income kDollar/p/y")
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, INEQ, interpolate(t, tables["INEQ"], ranges["INEQ"]))
    add_equation(eqs, LPR, interpolate(t, tables["LPR"], ranges["LPR"]))
    add_equation(eqs, PSP, interpolate(t, tables["PSP"], ranges["PSP"]))
    add_equation(eqs, PWA, interpolate(t, tables["PWA"], ranges["PWA"]))
    add_equation(eqs, WDI, interpolate(t, tables["WDI"], ranges["WDI"]))
    return sys
