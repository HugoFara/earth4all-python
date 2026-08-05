"""Equations of the LabourMarket sector.

Transcribed from `src/labourmarket/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, ramp, smooth, withlookup
from ..symbolics import D, max, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def labour_market(name="lab", params=None, inits=None, tables=None, ranges=None):
    """The equations of the LabourMarket sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    AUR = sys.parameter("AUR", params["AUR"], "Acceptable Unemployment Rate (1)")
    FIC = sys.parameter("FIC", params["FIC"], "Fraction of Inflation Compensated (1)")
    GDPP1980 = sys.parameter("GDPP1980", params["GDPP1980"], "GDP per Person in 1980")
    GDPPEROCCLRM = sys.parameter("GDPPEROCCLRM", params["GDPPEROCCLRM"], "sGDPppeoROCCLR<0: GDPP Effect on Rate Of Change in Capital Labour Ratio")
    GENLPR = sys.parameter("GENLPR", params["GENLPR"], "Goal for Extra Normal LPR (1)")
    NLPR80 = sys.parameter("NLPR80", params["NLPR80"], "Normal LPR in 1980 (1)")
    PFTJ = sys.parameter("PFTJ", params["PFTJ"], "Persons per Full-Time Job p/ftj")
    PFTJ80 = sys.parameter("PFTJ80", params["PFTJ80"], "Persons per Full-Time Job in 1980 p/ftj")
    PRUN = sys.parameter("PRUN", params["PRUN"], "PRice per UNit dollar/u")
    PUELPR = sys.parameter("PUELPR", params["PUELPR"], "sPUNeoLPR>0: Perceived Unemployment Effect on Labour Participation Rate")
    ROCECLR80 = sys.parameter("ROCECLR80", params["ROCECLR80"], "ROC in ECLR in 1980 1/y")
    RWER = sys.parameter("RWER", params["RWER"], "Real Wage Erosion Rate 1/y")
    TAHW = sys.parameter("TAHW", params["TAHW"], "Time to Adjust Hours Worked y")
    TELLM = sys.parameter("TELLM", params["TELLM"], "Time to Enter/Leave Labor Market y")
    TENHW = sys.parameter("TENHW", params["TENHW"], "sTIeoNHW<0: Time Effect on Number Hours Worked")
    TYLD = sys.parameter("TYLD", params["TYLD"], "10-Yr Loop Delay y")
    WSOECLR = sys.parameter("WSOECLR", params["WSOECLR"], "sWSOeoCLR>0: Worker Share of Output Effect on Capital Labour Ratio ")
    WSOELPR = sys.parameter("WSOELPR", params["WSOELPR"], "sWSOeoLPR>0: Worker Share of Output Effect on Labour Participation Rate")
    AGIW = sys.variable("AGIW", description="Average Gross Income per Worker kdollar/p/y")
    AHW = sys.variable("AHW", description="Average Hours Worked kh/y")
    AHW1980 = sys.variable("AHW1980", description="Average Hours Worked in 1980 kh/y")
    AVWO = sys.variable("AVWO", description="AVailable WOrkforce Mp")
    CECLR = sys.variable("CECLR", description="Change in Embedded CLR kcu/ftj/y")
    CHWO = sys.variable("CHWO", description="CHange in WOrkforce Mp/y")
    CWRA = sys.variable("CWRA", description="Change in Wage RAte dollar/ph/y")
    CWSO = sys.variable("CWSO", description="Change in WSO 1/y")
    ECLR = sys.variable("ECLR", inits["ECLR"], "Embedded CLR kcu/ftj")
    ENLPR2022 = sys.variable("ENLPR2022", description="Extra Normal LPR from 2022 (1)")
    GDPPEROCCLR = sys.variable("GDPPEROCCLR", description="GDPppeoROCCLR")
    HFD = sys.variable("HFD", description="Hiring/Firing Delay y")
    HWMGDPP = sys.variable("HWMGDPP", description="Hours Worked Mult from GDPpP (1)")
    IWEOCLR = sys.variable("IWEOCLR", description="Indicated Wage Effect on Optimal CLR (1)")
    ILPR = sys.variable("ILPR", description="Indicated Labour Participation Rate (1)")
    LAPR = sys.variable("LAPR", description="LAbour PRoductivity dollar/ph")
    LAUS = sys.variable("LAUS", inits["LAUS"], "LAbour USe Gph/y")
    LAUS80 = sys.variable("LAUS80", description="LAbour USe in 1980 Gph/y")
    LPR = sys.variable("LPR", inits["ILPR"], "Labour Participation Rate (1)")
    LTEWSO = sys.variable("LTEWSO", description="Long-Term Erosion of WSO 1/y")
    NHW = sys.variable("NHW", inits["NHW"], "Normal Hours Worked kh/ftj/y")
    NLPR = sys.variable("NLPR", description="Normal LPR (1)")
    OCLR = sys.variable("OCLR", description="Optimal Capital Labour Ratio kcu/ftj")
    OPWO = sys.variable("OPWO", description="OPtimal WOrkforce Mp")
    PART = sys.variable("PART", description="Participation (1)")
    PSW = sys.variable("PSW", description="Perceived Surplus Workforce (1)")
    PURA = sys.variable("PURA", inits["PURA"], "Perceived Unemployment RAte (1)")
    ROCECLR = sys.variable("ROCECLR", description="ROC in ECLR 1/y")
    ROCWSO = sys.variable("ROCWSO", description="ROC in WSO - Table 1/y")
    TCT = sys.variable("TCT", description="Time to Change Tooling y")
    UNEM = sys.variable("UNEM", description="UNEMployed Mp")
    UR = sys.variable("UR", description="UNemployment RAte (1)")
    UPT = sys.variable("UPT", description="Unemployment perception time y")
    WAP = sys.variable("WAP", description="Working Age Population Mp")
    WARA = sys.variable("WARA", inits["WARA"], "WAge RAte dollar/ph")
    WASH = sys.variable("WASH", description="WAge Share (1)")
    WEOCLR = sys.variable("WEOCLR", inits["WEOCLR"], "Wage Effect on Optimal CLR (1)")
    WF = sys.variable("WF", inits["WF"], "WorkForce Mp")
    WRER = sys.variable("WRER", description="Wage Rate Erosion Rate 1/y")
    WRE = sys.variable("WRE", description="Wage Rate Erosion dollar/ph/y")
    WSO = sys.variable("WSO", inits["WSO"], "Worker Share of Output (1)")
    A20PA = sys.variable("A20PA")
    CAP = sys.variable("CAP")
    GDPP = sys.variable("GDPP")
    IR = sys.variable("IR")
    IPP = sys.variable("IPP")
    OUTP = sys.variable("OUTP")
    add_equation(eqs, AGIW, WARA * AHW)
    add_equation(eqs, AHW, NHW / PFTJ)
    add_equation(eqs, AHW1980, inits["NHW"] / PFTJ80)
    add_equation(eqs, AVWO, WAP * LPR)
    add_equation(eqs, CECLR, ROCECLR * ECLR)
    add_equation(eqs, CHWO, (OPWO - WF) / HFD)
    add_equation(eqs, CWSO, WSO * ROCWSO)
    add_equation(eqs, CWRA, WARA * ROCWSO)
    add_equation(eqs, D(ECLR), CECLR)
    add_equation(eqs, GDPPEROCCLR, max(0, 1 + GDPPEROCCLRM * (GDPP / GDPP1980 - 1)))
    add_equation(eqs, ENLPR2022, ramp(t, GENLPR / IPP, 2022, 2022 + IPP))
    add_equation(eqs, HFD, TYLD / 3)
    add_equation(eqs, HWMGDPP, 1 + TENHW * (GDPP / GDPP1980 - 1))
    add_equation(eqs, IWEOCLR, 1 + WSOECLR * (WSO / inits["WSO"] - 1))
    add_equation(eqs, ILPR, NLPR - PSW)
    add_equation(eqs, LAPR, (OUTP * PRUN) / LAUS)
    add_equation(eqs, LAUS, WF * AHW)
    add_equation(eqs, LAUS80, inits["WF"] * AHW1980)
    smooth(eqs, LPR, ILPR, TELLM)
    add_equation(eqs, LTEWSO, WSO * RWER)
    smooth(eqs, NHW, inits["NHW"] * HWMGDPP, TAHW)
    add_equation(eqs, NLPR, NLPR80 * (1 + WSOELPR * (WSO / inits["WSO"] - 1)) + ENLPR2022)
    add_equation(eqs, OCLR, ECLR * WEOCLR)
    add_equation(eqs, OPWO, (CAP / OCLR) * PFTJ)
    add_equation(eqs, PART, LPR * (1 - PURA))
    add_equation(eqs, PSW, AUR * (1 + PUELPR * (PURA / AUR - 1)))
    smooth(eqs, PURA, UR, UPT)
    add_equation(eqs, ROCECLR, ROCECLR80 * GDPPEROCCLR)
    add_equation(eqs, ROCWSO, withlookup(PURA / AUR, [(0.0, 0.06), (0.5, 0.02), (1.0, 0.0), (1.5, -0.007), (2.0, -0.01)]))
    add_equation(eqs, TCT, TYLD / 3)
    add_equation(eqs, UNEM, max(0, AVWO - WF))
    add_equation(eqs, UPT, TYLD / 3)
    add_equation(eqs, UR, UNEM / AVWO)
    add_equation(eqs, WAP, A20PA)
    add_equation(eqs, D(WARA), CWRA - WRE)
    add_equation(eqs, WASH, WARA / LAPR)
    smooth(eqs, WEOCLR, IWEOCLR, TCT)
    add_equation(eqs, D(WF), CHWO)
    add_equation(eqs, WRE, WARA * WRER)
    add_equation(eqs, WRER, IR * (1 - FIC))
    add_equation(eqs, D(WSO), CWSO - LTEWSO)
    return sys


def labour_market_full_support(name="lab", params=None, inits=None, tables=None, ranges=None):
    """The LabourMarket sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    A20PA = sys.variable("A20PA", description="Population.Aged 20-Pension Age Mp")
    CAP = sys.variable("CAP", description="Output.CAPacity Gcu")
    GDPP = sys.variable("GDPP", description="Population.GDP per Person kDollar/p/y")
    IR = sys.variable("IR", description="Inventory.Inflation Rate 1/y")
    IPP = sys.variable("IPP", description="Wellbeing.Introduction Period for Policy y")
    OUTP = sys.variable("OUTP", description="Inventory.OUTput Gu/y")
    add_equation(eqs, A20PA, interpolate(t, tables["A20PA"], ranges["A20PA"]))
    add_equation(eqs, CAP, interpolate(t, tables["CAP"], ranges["CAP"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, IR, interpolate(t, tables["IR"], ranges["IR"]))
    add_equation(eqs, IPP, interpolate(t, tables["IPP"], ranges["IPP"]))
    add_equation(eqs, OUTP, interpolate(t, tables["OUTP"], ranges["OUTP"]))
    return sys


def labour_market_partial_support(name="lab", params=None, inits=None, tables=None, ranges=None):
    """The LabourMarket sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    A20PA = sys.variable("A20PA", description="Population.Aged 20-Pension Age Mp")
    CAP = sys.variable("CAP", description="Output.CAPacity Gcu")
    GDPP = sys.variable("GDPP", description="Population.GDP per Person kDollar/p/y")
    IR = sys.variable("IR", description="Inventory.Inflation Rate 1/y")
    IPP = sys.variable("IPP", description="Wellbeing.Introduction Period for Policy y")
    OUTP = sys.variable("OUTP", description="Inventory.OUTput Gu/y")
    add_equation(eqs, A20PA, interpolate(t, tables["A20PA"], ranges["A20PA"]))
    add_equation(eqs, CAP, interpolate(t, tables["CAP"], ranges["CAP"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, IR, interpolate(t, tables["IR"], ranges["IR"]))
    add_equation(eqs, IPP, interpolate(t, tables["IPP"], ranges["IPP"]))
    add_equation(eqs, OUTP, interpolate(t, tables["OUTP"], ranges["OUTP"]))
    return sys
