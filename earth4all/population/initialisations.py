"""Initial values of the stocks of the Population sector."""

_inits = {
    "A0020": 2170,
    "A2040": 1100,
    "A4060": 768,
    "A60PL": 382,
    "DEATHS": 30,
    "EGDPP": 6.4,
    "EPA": 0,
    "LE": 67,
    "PA": 62,
    "PASS20": 100,
    "PASS40": 64,
    "PASS60": 38,
}


def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
