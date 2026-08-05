"""Initial values of the stocks of the Inventory sector."""

_inits = {
    "DELDI": 1,
    "EPP": 28087,  # Taken from Vensim table
    "INV": 11234.8,  # Taken from Vensim table
    "PRIN": 1,  # Taken from Vensim table
    "PRI": 1,
    "RS": 28087,
    "SSWI": 1,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
