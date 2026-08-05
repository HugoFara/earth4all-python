"""Initial values of the stocks of the LabourMarket sector."""

_inits = {
    "ECLR": 41,
    "ILPR": 0.8,  # Taken from Vensim table
    "LAPR": 7.343,  # Taken from Vensim table
    "LAUS": 3060,  # Taken from Vensim table
    "NHW": 2,
    "PURA": 0.05,
    "WARA": 3.6715,  # Taken from Vensim table
    "WEOCLR": 1,  # Taken from Vensim table
    "WF": 1530,
    "WSO": 0.5,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
