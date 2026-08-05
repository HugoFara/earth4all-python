"""Initial values of the stocks of the Climate sector."""

_inits = {
    "N2OA": 1.052,
    "CH4A": 2.5,
    "CO2A": 2600,
    "ISCEGA": 12,
    "PWA": 0.4,
    "EHS": 0,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
