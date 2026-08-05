"""Equations of the Output sector.

Transcribed from `src/output/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, smooth, withlookup
from ..symbolics import D, ifelse, max, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def output(name="out", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Output sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    # DOCUMENTED PARAMETERS
    CAPPIS1980 = sys.parameter("CAPPIS1980", params["CAPPIS1980"], "CAP PIS in 1980 Gcu")
    CAPPUS1980 = sys.parameter("CAPPUS1980", params["CAPPUS1980"], "CAP PUS in 1980 Gcu")
    CC1980 = sys.parameter("CC1980", params["CC1980"], "Cost of Capacity in 1980 dollar/cu")
    CTPIS = sys.parameter("CTPIS", params["CTPIS"], "Construction Time PIS y")
    CTPUS = sys.parameter("CTPUS", params["CTPUS"], "Construction Time PUS y")
    EMCUC = sys.parameter("EMCUC", params["EMCUC"], "Extra Mult on CUC, to avoid initial transient in investment share of GDP")
    FCI = sys.parameter("FCI", params["FCI"], "Foreign Capital Inflow Gdollar/y")
    LCPIS1980 = sys.parameter("LCPIS1980", params["LCPIS1980"], "Life of Capacity PIS in 1980 y")
    OW2022 = sys.parameter("OW2022", params["OW2022"], "OBserved WArming in 2022 deg C")
    OWECCM = sys.parameter("OWECCM", params["OWECCM"], "sOWeoCOC>0: Observed Warming Effect on Cost of Capacity Multiplier")
    OWELCM = sys.parameter("OWELCM", params["OWELCM"], "sOWeoLOC<0: Observed Warming Effect on Life of Capacity Multiplier")
    USPIS2022 = sys.parameter("USPIS2022", params["USPIS2022"], "Unconventional Stimulus in PIS from 2022 (share of GDP)")
    USPUS2022 = sys.parameter("USPUS2022", params["USPUS2022"], "Unconventional Stimulus in PUS from 2022 (share of GDP)")
    # UNDOCUMENTED PARAMETERS
    CBCEFRA = sys.parameter("CBCEFRA", params["CBCEFRA"], "sCBCeoFRA<0: Corporate Borrowing Cost Effect on FRA")
    CUCPIS1980 = sys.parameter("CUCPIS1980", (params["CAPPIS1980"] / params["LCPIS1980"]) * params["CTPIS"] * params["EMCUC"], "CUC PIS in 1980 Gcu")
    ED1980 = sys.parameter("ED1980", params["ED1980"], "Excess Demand in 1980")
    EDEFRA = sys.parameter("EDEFRA", params["EDEFRA"], "sEDeoFRA>0: Excess Demand Effect on FRA")
    EDELCM = sys.parameter("EDELCM", params["EDELCM"], "sEDeoLOC>0: Excess Demand Effect on Life of Capacity")
    FRA1980 = sys.parameter("FRA1980", params["FRA1980"], "FRA in 1980")
    FRACAM = sys.parameter("FRACAM", params["FRACAM"], "FRACA Min")
    GDPP1980 = sys.parameter("GDPP1980", params["GDPP1980"], "GDP per Person in 1980")
    GDPPEFRACA = sys.parameter("GDPPEFRACA", params["GDPPEFRACA"], "sGDPppeoFRACA<0: GDP per Person Effect on FRACA")
    IPT = sys.parameter("IPT", params["IPT"], "Investment Planning Time y")
    JOBS1980 = sys.parameter("JOBS1980", params["JOBS1980"], "JOBS in 1980 M-ftj")
    KAPPA = sys.parameter("KAPPA", params["KAPPA"], "Kappa")
    LAMBDA = sys.parameter("LAMBDA", params["LAMBDA"], "Lambda")
    LAUS1980 = sys.parameter("LAUS1980", params["LAUS1980"], "Labour Use in 1980 Gph/y")
    OG1980 = sys.parameter("OG1980", params["OG1980"], "Output Growth in 1980 1/y (to avoid transient)")
    OO1980 = sys.parameter("OO1980", params["OO1980"], "Optimal output in 1980 Gu/y")
    PRUN = sys.parameter("PRUN", params["CU1980"] * (1 + params["MA1980"]), "Price per Unit dollar/u")
    TOED = sys.parameter("TOED", params["TOED"], "Time to observe excess demand y")
    WSOEFRA = sys.parameter("WSOEFRA", params["WSOEFRA"], "sWSOeoFRA<0: Worker Share of Output Effect on FRA")
    # DOCUMENTED VARIABLES
    AVCA = sys.variable("AVCA", description="AVailable CApital Gdollar/y")
    CAPIS = sys.variable("CAPIS", description="Capacity Addition PIS Gcu/y")
    CAPUS = sys.variable("CAPUS", description="Capacity Addition PUS Gcu/y")
    CDPIS = sys.variable("CDPIS", description="Capacity Discard PIS Gcu/y")
    CDPUS = sys.variable("CDPUS", description="Capacity Discard PUS Gcu/y")
    CIPIS = sys.variable("CIPIS", description="Capacity Initiation PIS Gcu/y")
    CIPUS = sys.variable("CIPUS", description="Capacity Initiation PUS Gcu/y")
    COCA = sys.variable("COCA", description="COst of CApacity dollar/cu")
    CPIS = sys.variable("CPIS", params["CAPPIS1980"], "Capacity PIS Gcu")
    CPUS = sys.variable("CPUS", params["CAPPUS1980"], "Capacity PUS Gcu")
    CRR = sys.variable("CRR", description="Capacity Renewal Rate 1/y")
    CUCPIS = sys.variable("CUCPIS", inits["CUCPIS"], "Capacity Under Construction PIS Gcu")
    CUCPIS1980 = sys.variable("CUCPIS1980", description="CUC PIS in 1980 Gcu")
    CUCPUS = sys.variable("CUCPUS", inits["CUCPUS"], "Capacity Under Construction PUS Gcu")
    CUCPUS1980 = sys.variable("CUCPUS1980", description="CUC PUS in 1980 Gcu")
    ECR = sys.variable("ECR", description="Effect of Capacity Renewal 1/y")
    ETFP = sys.variable("ETFP", inits["ETFP"], "Embedded TFP (1)")
    INCPIS = sys.variable("INCPIS", description="Investment in New Capacity PIS Gdollar/y")
    LCPUS = sys.variable("LCPUS", description="Life of Capacity PUS y")
    LCPUS1980 = sys.variable("LCPUS1980", description="Life of Capacity PUS in 1980 y")
    OBSGIPIS = sys.variable("OBSGIPIS", description="Off-Balance Sheet Govmnt Inv in PIS (share of GDP)")
    OBSGIPUS = sys.variable("OBSGIPUS", description="Off-Balance-Sheet Govmnt Inv in PUS (share of GDP)")
    OWECC = sys.variable("OWECC", description="OWeoCOC (1)")
    OWELC = sys.variable("OWELC", description="OWeoLOC (1)")
    # UNDOCUMENTED VARIABLES
    CBCEFCA = sys.variable("CBCEFCA", description="CBC Effect on Flow to Capacity Addion (1)")
    CAP = sys.variable("CAP", description="CAPacity Gcu")
    EDE = sys.variable("EDE", description="Excess DEmand (1)")
    EDEFCA = sys.variable("EDEFCA", description="ED Effect on Flow to Capacity Addition (1)")
    EDELC = sys.variable("EDELC", description="Excess Demand Effect on Life of Capacity (1)")
    FACNC = sys.variable("FACNC", inits["FACNC"], "Fraction of Available Capital to New Capacity (1)")
    FRACAMGDPPL = sys.variable("FRACAMGDPPL", description="FRACA Mult from GDPpP - Line (1)")
    FRACAMGDPPT = sys.variable("FRACAMGDPPT", description="FRACA Mult from GDPpP - Table (1)")
    ISGDP = sys.variable("ISGDP", description="Investment Share of GDP (1)")
    LCPIS = sys.variable("LCPIS", description="Life of Capacity PIS y")
    OGR = sys.variable("OGR", params["OG1980"], "Output Growth Rate 1/y")
    OLY = sys.variable("OLY", inits["OLY"], "Output Last Year Gdollar/y")
    OOV = sys.variable("OOV", description="Optimal Ouput - Value Gdollar/y")
    ORO = sys.variable("ORO", description="Optimal Real Output Gu/y")
    PEDE = sys.variable("PEDE", 1, "Perceived Excess DEmand (1)")
    WSOEFCA = sys.variable("WSOEFCA", description="WSO Effect on Flow to Capacity Addition (1)")
    # TO BE DELETED
    # @variables FACNC(t) [description = "Fraction of Available Capital to New Capacity (1)"]
    # @variables LCPIS(t) [description = "Life of Capacity PIS y"]
    CBC = sys.variable("CBC")
    CBC1980 = sys.variable("CBC1980")
    GDP = sys.variable("GDP")
    GDPP = sys.variable("GDPP")
    GIPC = sys.variable("GIPC")
    ITFP = sys.variable("ITFP")
    LAUS = sys.variable("LAUS")
    OW = sys.variable("OW")
    TS = sys.variable("TS")
    TPP = sys.variable("TPP")
    WASH = sys.variable("WASH")
    # DOCUMENTED EQUATIONS
    add_equation(eqs, AVCA, TS + FCI)
    add_equation(eqs, CAPIS, CUCPIS / CTPIS)
    add_equation(eqs, CAPUS, CUCPUS / CTPUS)
    add_equation(eqs, CIPIS, max((INCPIS + OBSGIPIS * GDP) / COCA, 0))
    add_equation(eqs, CIPUS, max((GIPC + OBSGIPUS * GDP) / COCA, 0))
    add_equation(eqs, CDPIS, CPIS / LCPIS)
    add_equation(eqs, CDPUS, CPUS / LCPUS)
    add_equation(eqs, COCA, CC1980 * OWECC)
    add_equation(eqs, D(CPIS), CAPIS - CDPIS)
    add_equation(eqs, D(CPUS), CAPUS - CDPUS)
    add_equation(eqs, CRR, CAPIS / CPIS)
    add_equation(eqs, D(CUCPIS), CIPIS - CAPIS)
    add_equation(eqs, CUCPIS1980, (CAPPIS1980 / LCPIS1980) * CTPIS * EMCUC)
    add_equation(eqs, D(CUCPUS), CIPUS - CAPUS)
    add_equation(eqs, CUCPUS1980, (CAPPUS1980 / LCPUS1980) * CTPUS * EMCUC)
    add_equation(eqs, ECR, (ITFP - ETFP) * CRR)
    add_equation(eqs, D(ETFP), ECR)
    add_equation(eqs, INCPIS, AVCA * FACNC)
    add_equation(eqs, LCPUS, LCPUS1980)
    add_equation(eqs, LCPUS1980, 15 * OWELC)
    add_equation(eqs, OBSGIPIS, ifelse(t > 2022, USPIS2022, 0))
    add_equation(eqs, OBSGIPUS, ifelse(t > 2022, 0.01 + USPUS2022, 0.01))
    add_equation(eqs, OWECC, ifelse(t > 2022, 1 + OWECCM * (OW / OW2022 - 1), 1))
    add_equation(eqs, OWELC, ifelse(t > 2022, 1 + OWELCM * (OW / OW2022 - 1), 1))
    # UNDOCUMENTED EQUATIONS
    add_equation(eqs, CAP, CPIS + CPUS)
    add_equation(eqs, CBCEFCA, 1 + CBCEFRA * (CBC / CBC1980 - 1))
    add_equation(eqs, EDE, TPP / OOV)
    add_equation(eqs, EDEFCA, 1 + EDEFRA * (PEDE / ED1980 - 1))
    add_equation(eqs, EDELC, 1 + EDELCM * (PEDE / ED1980 - 1))
    smooth(eqs, FACNC, FRA1980 * FRACAMGDPPL * (WSOEFCA + CBCEFCA + EDEFCA) / 3, IPT)
    add_equation(eqs, FRACAMGDPPL, max(FRACAM, 1 + GDPPEFRACA * (GDPP / GDPP1980 - 1)))
    add_equation(eqs, FRACAMGDPPT, withlookup(GDPP / GDPP1980, [(0.0, 1.0), (1.0, 1.0), (2.0, 0.85), (2.1, 0.84), (4.0, 0.65), (8.0, 0.55), (16.0, 0.5)]))
    add_equation(eqs, ISGDP, (INCPIS + GIPC) / GDP)
    add_equation(eqs, LCPIS, (LCPIS1980 * OWELC) / EDELC)
    smooth(eqs, OGR, (ORO - OLY) / OLY, 1)
    smooth(eqs, OLY, ORO, 1)
    add_equation(eqs, OOV, ORO * PRUN)
    add_equation(eqs, ORO, OO1980 * ((CPIS + CPUS) / (CAPPIS1980 + CAPPUS1980))**KAPPA * (LAUS / LAUS1980)**LAMBDA * (ETFP))
    smooth(eqs, PEDE, EDE, TOED)
    add_equation(eqs, WSOEFCA, 1 + WSOEFRA * (WASH / inits["WSO"] - 1))
    # TO BE DELETED
    # add_equation!(eqs, FACNC ~ WorldDynamics.interpolate(t, tables[:FACNC], ranges[:FACNC]))
    # add_equation!(eqs, LCPIS ~ WorldDynamics.interpolate(t, tables[:LCPIS], ranges[:LCPIS]))
    return sys


def output_full_support(name="out", params=None, inits=None, tables=None, ranges=None):
    """The Output sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    CBC = sys.variable("CBC", description="Finance.Corporate Borrowing Cost 1/y")
    CBC1980 = sys.variable("CBC1980", description="Finance.Corporate Borrowing Cost in 1980 1/y")
    GDP = sys.variable("GDP", description="Inventory.GDP GDollar/y")
    GDPP = sys.variable("GDPP", description="Population.GDP per Person kdollar/p/y")
    GIPC = sys.variable("GIPC", description="Demand.Govmnt Investment in Public Capacity Gdollar/y")
    ITFP = sys.variable("ITFP", description="Public.Indicated TFP")
    LAUS = sys.variable("LAUS", description="Labour and market.LAbour USe Gph/y")
    OW = sys.variable("OW", description="Climate.Observed warming deg C")
    TS = sys.variable("TS", description="Demand.TOtal SAvings Gdollar/y")
    TPP = sys.variable("TPP", description="Demand.Total Purchasing Power Gdollar/y")
    WASH = sys.variable("WASH", description="Labour and market.WAge SHare")
    add_equation(eqs, CBC, interpolate(t, tables["CBC"], ranges["CBC"]))
    add_equation(eqs, CBC1980, interpolate(t, tables["CBC1980"], ranges["CBC1980"]))
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, GIPC, interpolate(t, tables["GIPC"], ranges["GIPC"]))
    add_equation(eqs, ITFP, interpolate(t, tables["ITFP"], ranges["ITFP"]))
    add_equation(eqs, LAUS, interpolate(t, tables["LAUS"], ranges["LAUS"]))
    add_equation(eqs, OW, interpolate(t, tables["OW"], ranges["OW"]))
    add_equation(eqs, TS, interpolate(t, tables["TS"], ranges["TS"]))
    add_equation(eqs, TPP, interpolate(t, tables["TPP"], ranges["TPP"]))
    add_equation(eqs, WASH, interpolate(t, tables["WASH"], ranges["WASH"]))
    return sys


def output_partial_support(name="out", params=None, inits=None, tables=None, ranges=None):
    """The Output sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    CBC = sys.variable("CBC", description="Finance.Corporate Borrowing Cost 1/y")
    CBC1980 = sys.variable("CBC1980", description="Finance.Corporate Borrowing Cost in 1980 1/y")
    GDP = sys.variable("GDP", description="Inventory.GDP GDollar/y")
    GDPP = sys.variable("GDPP", description="Population.GDP per Person kdollar/p/y")
    GIPC = sys.variable("GIPC", description="Demand.Govmnt Investment in Public Capacity Gdollar/y")
    ITFP = sys.variable("ITFP", description="Public.Indicated TFP (1)")
    LAUS = sys.variable("LAUS", description="Labour and market.LAbour USe Gph/y")
    OW = sys.variable("OW", description="Climate.Observed warming deg C")
    TS = sys.variable("TS", description="Demand.TOtal SAvings Gdollar/y")
    TPP = sys.variable("TPP", description="Demand.Total Purchasing Power Gdollar/y")
    WASH = sys.variable("WASH", description="Labour and market.WAge SHare")
    add_equation(eqs, CBC, interpolate(t, tables["CBC"], ranges["CBC"]))
    add_equation(eqs, CBC1980, interpolate(t, tables["CBC1980"], ranges["CBC1980"]))
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, GDPP, interpolate(t, tables["GDPP"], ranges["GDPP"]))
    add_equation(eqs, GIPC, interpolate(t, tables["GIPC"], ranges["GIPC"]))
    add_equation(eqs, ITFP, interpolate(t, tables["ITFP"], ranges["ITFP"]))
    add_equation(eqs, LAUS, interpolate(t, tables["LAUS"], ranges["LAUS"]))
    add_equation(eqs, OW, interpolate(t, tables["OW"], ranges["OW"]))
    add_equation(eqs, TS, interpolate(t, tables["TS"], ranges["TS"]))
    add_equation(eqs, TPP, interpolate(t, tables["TPP"], ranges["TPP"]))
    add_equation(eqs, WASH, interpolate(t, tables["WASH"], ranges["WASH"]))
    return sys
