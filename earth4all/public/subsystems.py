"""Equations of the Public sector.

Transcribed from `src/public/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, ramp, smooth
from ..symbolics import D, ifelse, log, max, min, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def public(name="pub", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Public sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    OW2022 = sys.parameter("OW2022", params["OW2022"], "Observed Warming in 2022 deg C")
    CTA2022 = sys.parameter("CTA2022", params["CTA2022"], "Cost of TAs in 2022 GDollar/y")
    CTPIS = sys.parameter("CTPIS", params["CTPIS"], "Construction time PIS y")
    DROTA1980 = sys.parameter("DROTA1980", params["DROTA1980"], "Domestic ROTA in 1980 1/y")
    EDROTA2022 = sys.parameter("EDROTA2022", params["EDROTA2022"], "Extra Domestic ROTA in 2022 1/y")
    FUATA = sys.parameter("FUATA", params["FUATA"], "Fraction Unprofitable Activity in TAs")
    GDPTL = sys.parameter("GDPTL", params["GDPTL"], "GDPpp of Technology Leader kDollar/p/k")
    IIEEROTA = sys.parameter("IIEEROTA", params["IIEEROTA"], "sIIEeoROTA<0: Inequality Index Effect on ROTA")
    IPR1980 = sys.parameter("IPR1980", params["IPR1980"], "Infrastructure Purchases Ratio in 1980 y")
    IPRVPSS = sys.parameter("IPRVPSS", params["IPRVPSS"], "sIPReoVPSS>0: Infrastructure Purchase Ratio effect on Value of Pubblic Services Supplied")
    IPT = sys.parameter("IPT", params["IPT"], "Investment planning time y")
    MIROTA2022 = sys.parameter("MIROTA2022", params["MIROTA2022"], "Max Imported ROTA from 2022 1/y")
    OWETFP = sys.parameter("OWETFP", params["OWETFP"], "sOWeoTFP<0: Observed Warming Effect on Total Factor Productivity")
    SC1980 = sys.parameter("SC1980", params["SC1980"], "State Capacity in 1980 (fraction of GDP)")
    SCROTA = sys.parameter("SCROTA", params["SCROTA"], "sSCeoROTA>0: State Capacity effect on Rate Of Technological Advance")
    XETAC2022 = sys.parameter("XETAC2022", params["XETAC2022"], "XExtra TA Cost in 2022 (share of GDP)")
    XETAC2100 = sys.parameter("XETAC2100", params["XETAC2100"], "XExtra TA Cost in 2100 (share of GDP)")
    CTFP = sys.variable("CTFP", description="Change in TFP 1/y")
    DRTA = sys.variable("DRTA", description="Domestic Rate of Technological Advance 1/y")
    ECTAF2022 = sys.variable("ECTAF2022", description="Extra Cost of TAs From 2022 GDollar/y")
    ECTAGDP = sys.variable("ECTAGDP", description="Extra Cost of TAs as share of GDP (1)")
    GSSGDP = sys.variable("GSSGDP", description="Govmnt Spending as Share of GDP")
    IPR = sys.variable("IPR", description="Infrastructure Purchases Ratio y")
    IROTA = sys.variable("IROTA", description="Imported ROTA 1/y")
    ITFP = sys.variable("ITFP", description="Indicated TFP (1)")
    OWTFP = sys.variable("OWTFP", description="OWeoTFP")
    PLUA = sys.variable("PLUA", description="Productivity Loss from Unprofitable Activity (1)")
    PPP = sys.variable("PPP", description="Productivity of Public Purchases (1)")
    PSEP = sys.variable("PSEP", description="Public SErvices per Person kdollar/p/y")
    PSP = sys.variable("PSP", description="Public Spending per Person kDollar/p/y")
    RROTAI = sys.variable("RROTAI", description="Reduction in ROTA from Inequality 1/y")
    RTA = sys.variable("RTA", description="Rate of Technological Advance 1/y")
    RTFPUA = sys.variable("RTFPUA", inits["RTFPUA"], "Reduction in TFP from Unprofitable Activity (1)")
    SC = sys.variable("SC", description="State Capacity (fraction of GDP)")
    TFPEE5TA = sys.variable("TFPEE5TA", inits["TFPEE5TA"], "TFP Excluding Effect of 5TAs (1)")
    TFPIE5TA = sys.variable("TFPIE5TA", description="TFP Including Effect of 5TAs (1)")
    VPSS = sys.variable("VPSS", description="Value of Public Services Supplied GDollar/y")
    XECTAGDP = sys.variable("XECTAGDP", description="XExtra Cost of TAs as share of GDP (1)")
    CPUS = sys.variable("CPUS")
    CTA = sys.variable("CTA")
    GDP = sys.variable("GDP")
    GDPP = sys.variable("GDPP")
    GPU = sys.variable("GPU")
    GS = sys.variable("GS")
    INEQI = sys.variable("INEQI")
    OW = sys.variable("OW")
    POP = sys.variable("POP")
    add_equation(eqs, CTFP, RTA * TFPEE5TA)
    add_equation(eqs, DRTA, (DROTA1980 + ifelse(t > 2022, EDROTA2022, 0) * (1 + SCROTA * ((SC / SC1980) - 1))))
    add_equation(eqs, ECTAF2022, max(0, CTA - CTA2022))
    add_equation(eqs, ECTAGDP, ECTAF2022 / GDP)
    add_equation(eqs, GSSGDP, GS / GDP)
    add_equation(eqs, IPR, CPUS / GPU)
    add_equation(eqs, IROTA, ifelse(t > 2022, max(0, MIROTA2022 * (1 - 1 * (GDPP / GDPTL - 1))), 0))
    add_equation(eqs, ITFP, TFPEE5TA * OWTFP)
    add_equation(eqs, OWTFP, ifelse(t > 2022, 1 + OWETFP * (OW / OW2022 - 1), 1))
    add_equation(eqs, PLUA, ECTAGDP * FUATA)
    add_equation(eqs, PPP, max(0, 1 + IPRVPSS * log(IPR / IPR1980)))
    add_equation(eqs, PSEP, VPSS / POP)
    add_equation(eqs, PSP, GS / POP)
    add_equation(eqs, D(TFPEE5TA), CTFP)
    add_equation(eqs, RROTAI, min(1, 1 + IIEEROTA * (INEQI / 1 - 1)))
    add_equation(eqs, RTA, (DRTA + 0) * RROTAI + IROTA)
    smooth(eqs, RTFPUA, PLUA, IPT + CTPIS)
    add_equation(eqs, SC, VPSS / GDP)
    add_equation(eqs, TFPIE5TA, TFPEE5TA * (1 - RTFPUA))
    add_equation(eqs, VPSS, GPU * PPP)
    add_equation(eqs, XECTAGDP, XETAC2022 + ramp(t, (XETAC2100 - XETAC2022) / 78, 2022, 2022 + 78))
    return sys


def public_full_support(name="pub", params=None, inits=None, tables=None, ranges=None):
    """The Public sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    CPUS = sys.variable("CPUS", description="Output.Capacity PUS Gcu")
    CTA = sys.variable("CTA", description="Other performance indicators.Cost of TAs Gdollar/y")
    GDP = sys.variable("GDP", description="Inventory.GDP Gdollar/y")
    GDPP = sys.variable("GDPP", description="Population.GDP per person kDollar/p/y")
    GPU = sys.variable("GPU", description="Demand.Govmnt purchases Gdollar/y")
    GS = sys.variable("GS", description="Demand.Govmnt spending Gdollar/y")
    INEQI = sys.variable("INEQI", description="Demand.Inequality index (1980=1)")
    OW = sys.variable("OW", description="Climate.Observed warming deg C")
    POP = sys.variable("POP", description="Population.Population Mp")
    add_equation(eqs, CPUS, interpolate(t, tables["CPUS"], ranges["CPUS"]))
    add_equation(eqs, CTA, interpolate(t, tables["CTA"], ranges["CTA"]))
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, GPU, interpolate(t, tables["GPU"], ranges["GPU"]))
    add_equation(eqs, GS, interpolate(t, tables["GS"], ranges["GS"]))
    add_equation(eqs, INEQI, interpolate(t, tables["INEQI"], ranges["INEQI"]))
    add_equation(eqs, OW, interpolate(t, tables["OW"], ranges["OW"]))
    add_equation(eqs, POP, interpolate(t, tables["POP"], ranges["POP"]))
    return sys


def public_partial_support(name="pub", params=None, inits=None, tables=None, ranges=None):
    """The Public sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    CPUS = sys.variable("CPUS", description="Output.Capacity PUS Gcu")
    CTA = sys.variable("CTA", description="Other performance indicators.Cost of TAs Gdollar/y")
    GDP = sys.variable("GDP", description="Inventory.GDP Gdollar/y")
    GDPP = sys.variable("GDPP", description="Population.GDP per person kDollar/p/y")
    GPU = sys.variable("GPU", description="Demand.Govmnt purchases Gdollar/y")
    GS = sys.variable("GS", description="Demand.Govmnt spending Gdollar/y")
    INEQI = sys.variable("INEQI", description="Demand.Inequality index (1980=1)")
    OW = sys.variable("OW", description="Climate.Observed warming deg C")
    POP = sys.variable("POP", description="Population.Population Mp")
    add_equation(eqs, CPUS, interpolate(t, tables["CPUS"], ranges["CPUS"]))
    add_equation(eqs, CTA, interpolate(t, tables["CTA"], ranges["CTA"]))
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, GPU, interpolate(t, tables["GPU"], ranges["GPU"]))
    add_equation(eqs, GS, interpolate(t, tables["GS"], ranges["GS"]))
    add_equation(eqs, INEQI, interpolate(t, tables["INEQI"], ranges["INEQI"]))
    add_equation(eqs, OW, interpolate(t, tables["OW"], ranges["OW"]))
    add_equation(eqs, POP, interpolate(t, tables["POP"], ranges["POP"]))
    return sys
