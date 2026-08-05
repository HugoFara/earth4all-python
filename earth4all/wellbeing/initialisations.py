"""Initial values of the stocks of the Wellbeing sector."""

_inits = {
    "ORP": 0,
    "PAWBI": 0.65,
    "RD": 30,
    "STE": 1.3,
    "STR": 0.6,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
