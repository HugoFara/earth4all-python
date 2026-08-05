"""Initial values of the stocks of the Finance sector."""

_inits = {
    "CCSD": 0.04,  # Taken from Vensim table
    "ELTI": 0.02,
    "PI": 0.02,
    "PU": 0.0326951,
    "CBSR": 0.02,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
