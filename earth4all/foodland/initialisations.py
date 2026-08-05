"""Initial values of the stocks of the FoodLand sector."""

_inits = {
    "BALA": 3000,
    "CRLA": 1450,
    "GRLA": 3300,
    "FOLA": 1100,
    "OGFA": 2600,
    "SQICA": 1,
    "URLA": 215,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
