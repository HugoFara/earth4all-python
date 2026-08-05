"""Parameters of the Finance sector."""

_params = {
    "FSRT": 1,
    "GRCR": 0,
    "IEFT": 10,
    "INSR": 0.7,
    "IPTCB": 1,
    "IT": 0.02,
    "NBBM": 0.005,
    "NBOM": 0.015,
    "NSR": 0.02,
    "SRAT": 1,
    "UNSR": -1.5,
    "UPTCB": 1,
    "UT": 0.05,
}


def getparameters():
    """A copy of the parameters, to be modified and passed back to the sector."""
    return dict(_params)
