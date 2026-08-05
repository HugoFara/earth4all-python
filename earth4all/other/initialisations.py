"""Initial values of the stocks of the Other sector."""

_inits = {
    "PGDPP": 6.4 * 0.93,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
