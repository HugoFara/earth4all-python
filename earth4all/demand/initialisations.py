"""Initial values of the stocks of the Demand sector."""

_inits = {
    "ETF2022": 0,  # No extra taxes before 2022
    "FGBW": 0.3,  # Equal to fraction transfer in 1980
    "POCI": 7081,  # It was OCI in 1980
    "WD": 7406.88,
    "PWCIN": 13000,
    "PGCIN": 5400,
    "GNI": 6531.07,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
