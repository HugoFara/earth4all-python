"""Initial values of the stocks of the Energy sector."""

_inits = {
    "EEPI2022": 1,
    "REC": 300,
    "ACSWCF1980": 10,
    "FEC": 980,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
