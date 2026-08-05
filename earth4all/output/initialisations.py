"""Initial values of the stocks of the Output sector."""

_inits = {
    "CUCPIS": 10072.5,  # Taken from Vensim table
    "CUCPUS": 909.5,  # Taken from Vensim table
    "ETFP": 1,
    "FACNC": 1.05149,  # Taken from Vensim table
    "LAUS": 3060,  # Taken from Labour and market sector
    "OLY": 26497.1,  # Taken from Vensim table
    "WSO": 0.5,  # Taken from Labour and market sector
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
