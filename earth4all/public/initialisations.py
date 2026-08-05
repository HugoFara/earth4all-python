"""Initial values of the stocks of the Public sector."""

_inits = {
    "RTFPUA": 0,  # Taken from Vensim table
    "TFPEE5TA": 1,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
