"""Equations of the Climate sector.

Transcribed from `src/climate/subsystems.jl` of Earth4All.jl, which
transcribes the Vensim model. Each equation is kept on a single line,
however long, so that the three can be read side by side.
"""

from ..functions import add_equation, interpolate, ramp, smooth, withlookup
from ..symbolics import D, exp, ifelse, t
from ..system import ODESystem
from .initialisations import _inits
from .parameters import _params
from .tables import _ranges, _tables


def climate(name="cli", params=None, inits=None, tables=None, ranges=None):
    """The equations of the Climate sector."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    GDP = sys.variable("GDP")
    IPP = sys.variable("IPP")
    FEUS = sys.variable("FEUS")
    CRSU = sys.variable("CRSU")
    CO2EI = sys.variable("CO2EI")
    CO2ELULUC = sys.variable("CO2ELULUC")
    CCCSt = sys.parameter("CCCSt", params["CCCSt"], "Cost of CCS Dollar/tCO2")
    ERDN2OKF2022 = sys.parameter("ERDN2OKF2022", params["ERDN2OKF2022"], "Extra rate of decline in N2O per kg fertilizer from 2022")
    RDN2OKF = sys.parameter("RDN2OKF", params["RDN2OKF"], "Rate of decline in N2O per kg fertilizer 1/y")
    KN2OKF1980 = sys.parameter("KN2OKF1980", params["KN2OKF1980"], "kg N2O per kg fertilizer in 1980 ")
    N2OA1980 = sys.parameter("N2OA1980", params["N2OA1980"], "N2O in atm in 1980 GtN2O")
    MAT = sys.parameter("MAT", params["MAT"], "Mass of ATmosphere Zt")
    LN2OA = sys.parameter("LN2OA", params["LN2OA"], "Life of N2O in atmosphere y")
    GN2OPP = sys.parameter("GN2OPP", params["GN2OPP"], "GtN2O per ppm")
    ERDCH4KC2022 = sys.parameter("ERDCH4KC2022", params["ERDCH4KC2022"], "Extra rate of decline in CH4 per kg crop after 2022 1/y")
    RDCH4KC = sys.parameter("RDCH4KC", params["RDCH4KC"], "Rate of decline in CH4 per kg crop 1/y")
    KCH4KC1980 = sys.parameter("KCH4KC1980", params["KCH4KC1980"], "kg CH4 per kg crop in 1980")
    CH4A1980 = sys.parameter("CH4A1980", params["CH4A1980"], "CH4 in atm in 1980 GtCH4")
    LCH4A = sys.parameter("LCH4A", params["LCH4A"], "Life of CH4 in atmosphere y")
    GCH4PP = sys.parameter("GCH4PP", params["GCH4PP"], "GtCH4 per ppm")
    OBWA2022 = sys.parameter("OBWA2022", params["OBWA2022"], "OBserved WArming in 2022 deg C")
    SOWLCO2 = sys.parameter("SOWLCO2", params["SOWLCO2"], "sOWeoLoCO2>0")
    LECO2A1980 = sys.parameter("LECO2A1980", params["LECO2A1980"], "Life of extra CO2 in atmosphere in 1980 y")
    CO2A1850 = sys.parameter("CO2A1850", params["CO2A1850"], "CO2 in atmosphere in 1850 GtCO2")
    TCO2PTCH4 = sys.parameter("TCO2PTCH4", params["TCO2PTCH4"], "tCO2 per tCH4")
    DACCO22100 = sys.parameter("DACCO22100", params["DACCO22100"], "Direct Air Capture of CO2 in 2100 GtCO2/y")
    GCO2PP = sys.parameter("GCO2PP", params["GCO2PP"], "GtCO2 per ppm")
    TCO2ETN2O = sys.parameter("TCO2ETN2O", params["TCO2ETN2O"], "tCO2e/tN2O")
    TCO2ETCH4 = sys.parameter("TCO2ETCH4", params["TCO2ETCH4"], "tCO2e/tCH4")
    TCO2ETCO2 = sys.parameter("TCO2ETCO2", params["TCO2ETCO2"], "tCO2e/tCO2")
    ALGAV = sys.parameter("ALGAV", params["ALGAV"], "ALbedo global average")
    ALIS = sys.parameter("ALIS", params["ALIS"], "ALbedo Ice and snow")
    GLSU = sys.parameter("GLSU", params["GLSU"], "GLobal SUrface Mkm2")
    ISCEGA1980 = sys.parameter("ISCEGA1980", params["ISCEGA1980"], "Ice and snow cover excluding Greenland and Antarctica in 1980 Mkm2")
    TRSS1980 = sys.parameter("TRSS1980", params["TRSS1980"], "Transfer rate surface-space in 1980 1/y")
    MRS1980 = sys.parameter("MRS1980", params["MRS1980"], "Melting rate surface in 1980 1/y")
    WA1980 = sys.parameter("WA1980", params["WA1980"], "Warming in 1980 deg C")
    SVDR = sys.parameter("SVDR", params["SVDR"], "Surface vs deep rate")
    AI1980 = sys.parameter("AI1980", params["AI1980"], "Amount of ice in 1980 MKm3")
    TPM3I = sys.parameter("TPM3I", params["TPM3I"], "Ton per m3 ice")
    HRMI = sys.parameter("HRMI", params["HRMI"], "Heat required to melt ice kJ/kg")
    OWWV = sys.parameter("OWWV", params["OWWV"], "sOWeoWV>0")
    WVC1980 = sys.parameter("WVC1980", params["WVC1980"], "Water Vapour Concentration in 1980 g/kg")
    WVF1980 = sys.parameter("WVF1980", params["WVF1980"], "Water Vapour Feedback in 1980 W/m2")
    WVWVF = sys.parameter("WVWVF", params["WVWVF"], "sWVeoWVF>0")
    WFEH = sys.parameter("WFEH", params["WFEH"], "Warming from Extra Heat deg/ZJ")
    EH1980 = sys.parameter("EH1980", params["EH1980"], "Extra Heat in 1980 ZJ")
    TRSA1980 = sys.parameter("TRSA1980", params["TRSA1980"], "Transfer rate surface-abyss in 1980 1/y")
    PD = sys.parameter("PD", params["PD"], "Perception delay y")
    KN2OEKF = sys.variable("KN2OEKF", description="kg N2O emission per kg fertiliser")
    MMN2OE = sys.variable("MMN2OE", description="Man-made N2O emissions GtN2O/y")
    NN2OE = sys.variable("NN2OE", description="Natural N2O emissions GtN2O/y")
    N2OE = sys.variable("N2OE", description="N2O emissions GtN2O/y")
    N2OC1980 = sys.variable("N2OC1980", description="N2O conc in 1980 ppm")
    N2OA = sys.variable("N2OA", inits["N2OA"], "N2O in Atmosphere GtN2O")
    N2OBD = sys.variable("N2OBD", description="N2O BreakDown GtN2O/y")
    N2OCA = sys.variable("N2OCA", description="N2O concentration in atm ppm")
    N2OFPP = sys.variable("N2OFPP", description="N2O forcing per ppm W/m2/ppm")
    FN2O = sys.variable("FN2O", description="Forcing from N2O W/m2")
    KCH4EKC = sys.variable("KCH4EKC", description="kg CH4 emission per kg crop")
    MMCH4E = sys.variable("MMCH4E", description="Man-made CH4 emissions GtCH4/y")
    NCH4E = sys.variable("NCH4E", description="Natural CH4 emissions GtCH4/y")
    CH4E = sys.variable("CH4E", description="CH4 emissions GtCH4/y")
    CH4C1980 = sys.variable("CH4C1980", description="CH4 conc in 1980 ppm")
    CH4A = sys.variable("CH4A", inits["CH4A"], "CH4 in Atmosphere GtCH4")
    CH4BD = sys.variable("CH4BD", description="CH4 BreakDown GtCH4/y")
    CH4CA = sys.variable("CH4CA", description="CH4 concentration in atm ppm")
    CH4FPP = sys.variable("CH4FPP", description="CH4 forcing per ppm W/m2/ppm")
    FCH4 = sys.variable("FCH4", description="Forcing from CH4 W/m2")
    OWLCO2 = sys.variable("OWLCO2", description="OWeoLoCO2")
    LECO2A = sys.variable("LECO2A", description="Life of extra CO2 in atm y")
    CO2FCH4 = sys.variable("CO2FCH4", description="CO2 from CH4 GtCO2/y")
    CO2AB = sys.variable("CO2AB", description="CO2 absorption GtCO2/y")
    CO2E = sys.variable("CO2E", description="CO2 emissions GtCO2/y")
    CO2GDP = sys.variable("CO2GDP", description="CO2 per GDP (kgCO2/Dollar)")
    CAC = sys.variable("CAC", description="Cost of air capture GDollar/y")
    DACCO2 = sys.variable("DACCO2", description="Direct Air Capture of CO2 GtCO2/y")
    CO2A = sys.variable("CO2A", inits["CO2A"], "CO2 in Atmosphere GtCO2")
    CO2CA = sys.variable("CO2CA", description="CO2 concentration in atm ppm")
    CO2FPP = sys.variable("CO2FPP", description="CO2 forcing per ppm W/m2/ppm")
    FCO2 = sys.variable("FCO2", description="Forcing from CO2 W/m2")
    FOG = sys.variable("FOG", description="Forcing from other gases W/m2")
    MMF = sys.variable("MMF", description="Man-made Forcing W/m2")
    GHGE = sys.variable("GHGE", description="GHG emissions GtCO2e/y")
    AL1980 = sys.variable("AL1980", description="ALbedo in 1980 (1)")
    AL = sys.variable("AL", description="ALbedo (1)")
    TRHGS = sys.variable("TRHGS", description="Transfer rate for heat going to space 1/y")
    HTS = sys.variable("HTS", description="Heat to space ZJ/y")
    MRS = sys.variable("MRS", description="Melting rate surface 1/y")
    MRDI = sys.variable("MRDI", description="Melting rate deep ice 1/y")
    ECIM = sys.variable("ECIM", description="Extra cooling from ice melt ZJ/y")
    MEL = sys.variable("MEL", description="Melting Mha/y")
    ISCEGA = sys.variable("ISCEGA", inits["ISCEGA"], "Ice and snow cover excl G&A Mkm2")
    ISC = sys.variable("ISC", description="Ice and snow cover Mha")
    WVC = sys.variable("WVC", description="Water Vapor Concentration g/kg")
    WVF = sys.variable("WVF", description="Water Vapour Feedback W/m2")
    TMMF = sys.variable("TMMF", description="Total man-made forcing W/m2")
    EWFF = sys.variable("EWFF", description="Extra Warming from forcing ZJ/y")
    OW = sys.variable("OW", description="OBserved WArming deg C")
    REHE = sys.variable("REHE", description="Risk of extreme heat event (1)")
    PWA = sys.variable("PWA", inits["PWA"], "Perceived WArming deg C")
    TRHGA = sys.variable("TRHGA", description="Transfer rate for heat going to abyss 1/y")
    HDO = sys.variable("HDO", description="Heat to deep ocean ZJ/y")
    EHS = sys.variable("EHS", inits["EHS"], "Extra heat in surface ZJ")
    add_equation(eqs, KN2OEKF, KN2OKF1980 * exp(-(RDN2OKF) * (t - 1980)) * ifelse(t > 2022, exp(-(ERDN2OKF2022) * (t - 2022)), 1))
    add_equation(eqs, MMN2OE, FEUS * KN2OEKF / 1000)
    add_equation(eqs, NN2OE, withlookup(t, [(1980.0, 0.009), (2020.0, 0.009), (2099.27, 0.0)]))
    add_equation(eqs, N2OE, NN2OE + MMN2OE)
    add_equation(eqs, N2OC1980, N2OA1980 / MAT)
    add_equation(eqs, D(N2OA), N2OE - N2OBD)
    add_equation(eqs, N2OBD, N2OA / LN2OA)
    add_equation(eqs, N2OCA, N2OA / GN2OPP)
    add_equation(eqs, N2OFPP, withlookup(t, [(1980.0, 0.43), (2000.0, 0.64), (2010.0, 0.73), (2020.0, 0.8), (2100.0, 1.0)]))
    add_equation(eqs, FN2O, N2OCA * N2OFPP)
    add_equation(eqs, KCH4EKC, KCH4KC1980 * exp(-(RDCH4KC) * (t - 1980)) * ifelse(t > 2022, exp(-(ERDCH4KC2022) * (t - 2022)), 1))
    add_equation(eqs, MMCH4E, CRSU * KCH4EKC / 1000)
    add_equation(eqs, NCH4E, withlookup(t, [(1980.0, 0.19), (2020.0, 0.19), (2100.0, 0.19)]))
    add_equation(eqs, CH4E, NCH4E + MMCH4E)
    add_equation(eqs, CH4C1980, CH4A1980 / MAT)
    add_equation(eqs, D(CH4A), CH4E - CH4BD)
    add_equation(eqs, CH4BD, CH4A / LCH4A)
    add_equation(eqs, CH4CA, CH4A / GCH4PP)
    add_equation(eqs, CH4FPP, withlookup(t, [(1980.0, 0.82), (2000.0, 0.94), (2020.0, 1.01), (2100.0, 1.1)]))
    add_equation(eqs, FCH4, CH4CA * CH4FPP)
    add_equation(eqs, OWLCO2, ifelse(t > 2022, 1 + SOWLCO2 * (OW / OBWA2022 - 1), 1))
    add_equation(eqs, LECO2A, LECO2A1980 * OWLCO2)
    add_equation(eqs, CO2FCH4, CH4BD * TCO2PTCH4)
    add_equation(eqs, CO2AB, (CO2A - CO2A1850) / LECO2A)
    add_equation(eqs, CO2E, CO2EI + CO2ELULUC - DACCO2)
    add_equation(eqs, CO2GDP, (CO2E / GDP) * 1000)
    add_equation(eqs, CAC, DACCO2 * CCCSt)
    add_equation(eqs, DACCO2, ifelse(t > 2022, ramp(t, (DACCO22100) / IPP, 2022, 2022 + IPP), 0))
    add_equation(eqs, D(CO2A), CO2E - CO2AB + 2 * CO2FCH4)  # STRANGE EQUATION!
    add_equation(eqs, CO2CA, CO2A / GCO2PP)
    add_equation(eqs, CO2FPP, withlookup(t, [(1980.0, 0.0032), (1990.0, 0.0041), (2000.0, 0.0046), (2020.0, 0.0051), (2100.0, 0.006)]))
    add_equation(eqs, FCO2, CO2CA * CO2FPP)
    add_equation(eqs, FOG, withlookup(t, [(1980.0, 0.18), (2000.0, 0.36), (2020.0, 0.39), (2050.0, 0.37), (2100.0, 0.0)]))
    add_equation(eqs, MMF, FCO2 + FOG + FCH4 + FN2O)
    add_equation(eqs, GHGE, CO2E * TCO2ETCO2 + CH4E * TCO2ETCH4 + N2OE * TCO2ETN2O)
    add_equation(eqs, AL1980, (ISCEGA1980 * ALIS + (GLSU - ISCEGA1980) * ALGAV) / GLSU)
    add_equation(eqs, AL, (ISCEGA * ALIS + (GLSU - ISCEGA) * ALGAV) / GLSU)
    add_equation(eqs, TRHGS, (TRSS1980 * ((OW + 297) / 297)) * (AL / AL1980))
    add_equation(eqs, HTS, EHS * TRHGS)  # EHS
    add_equation(eqs, MRS, MRS1980 * (OW / WA1980))
    add_equation(eqs, MRDI, MRS / SVDR)
    add_equation(eqs, ECIM, MRDI * AI1980 * TPM3I * HRMI)
    add_equation(eqs, MEL, ISCEGA * MRS)
    add_equation(eqs, D(ISCEGA), -MEL)
    add_equation(eqs, ISC, ISCEGA * 100)
    add_equation(eqs, WVC, WVC1980 * (1 + OWWV * (OW / WA1980 - 1)))
    add_equation(eqs, WVF, WVF1980 * (1 + WVWVF * (WVC / WVC1980 - 1)))
    add_equation(eqs, TMMF, MMF + WVF)
    add_equation(eqs, EWFF, (TMMF * GLSU) * 31.5 / 1000)
    add_equation(eqs, OW, WA1980 + (EHS - EH1980) * WFEH)
    add_equation(eqs, REHE, withlookup(OW, [(0.0, 1.0), (1.2, 4.8), (2.0, 8.6), (2.9, 14.0), (5.2, 40.0)]))
    add_equation(eqs, TRHGA, TRSA1980 * ((OW + 287) / 287))
    add_equation(eqs, HDO, EHS * TRHGA)
    add_equation(eqs, D(EHS), EWFF - ECIM - HDO - HTS)
    smooth(eqs, PWA, OW, PD)
    return sys


def climate_full_support(name="cli", params=None, inits=None, tables=None, ranges=None):
    """The Climate sector variables that other sectors provide, read from tabulated runs of the whole model instead."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    GDP = sys.variable("GDP", description="Inventory.GDP GDollar/y")
    IPP = sys.variable("IPP", description="Wellbeing.Introduction period for policy y")
    FEUS = sys.variable("FEUS", description="Food and land.Fertilizer use Mt/y")
    CRSU = sys.variable("CRSU", description="Food and land.Crop supply (after 20% waste) Mt-crop/y")
    CO2EI = sys.variable("CO2EI", description="Energy.CO2 from energy and industry GtCO2/y")
    CO2ELULUC = sys.variable("CO2ELULUC", description="Food and land.CO2 emissions from LULUC GtCO2/y")
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, IPP, interpolate(t, tables["IPP"], ranges["IPP"]))
    add_equation(eqs, FEUS, interpolate(t, tables["FEUS"], ranges["FEUS"]))
    add_equation(eqs, CRSU, interpolate(t, tables["CRSU"], ranges["CRSU"]))
    add_equation(eqs, CO2EI, interpolate(t, tables["CO2EI"], ranges["CO2EI"]))
    add_equation(eqs, CO2ELULUC, interpolate(t, tables["CO2ELULUC"], ranges["CO2ELULUC"]))
    return sys


def climate_partial_support(name="cli", params=None, inits=None, tables=None, ranges=None):
    """The Climate sector variables of the sectors that are not part of a partial run, read from tabulated runs of the whole model."""
    params = _params if params is None else params
    inits = _inits if inits is None else inits
    tables = _tables if tables is None else tables
    ranges = _ranges if ranges is None else ranges
    sys = ODESystem(name)
    eqs = sys.equations

    GDP = sys.variable("GDP", description="Inventory.GDP GDollar/y")
    IPP = sys.variable("IPP", description="Wellbeing.Introduction period for policy y")
    FEUS = sys.variable("FEUS", description="Food and land.Fertilizer use Mt/y")
    CRSU = sys.variable("CRSU", description="Food and land.Crop supply (after 20% waste) Mt-crop/y")
    CO2EI = sys.variable("CO2EI", description="Energy.CO2 from energy and industry GtCO2/y")
    CO2ELULUC = sys.variable("CO2ELULUC", description="Food and land.CO2 emissions from LULUC GtCO2/y")
    add_equation(eqs, GDP, interpolate(t, tables["GDP"], ranges["GDP"]))
    add_equation(eqs, IPP, interpolate(t, tables["IPP"], ranges["IPP"]))
    add_equation(eqs, FEUS, interpolate(t, tables["FEUS"], ranges["FEUS"]))
    add_equation(eqs, CRSU, interpolate(t, tables["CRSU"], ranges["CRSU"]))
    add_equation(eqs, CO2EI, interpolate(t, tables["CO2EI"], ranges["CO2EI"]))
    add_equation(eqs, CO2ELULUC, interpolate(t, tables["CO2ELULUC"], ranges["CO2ELULUC"]))
    return sys
