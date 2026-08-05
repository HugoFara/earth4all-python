"""Parameters of the Other sector."""

_params = {
    "TEGR": 4,
    "INELOK": -0.5,
    "NK": 0.3,
}


def getparameters():
    """A copy of the parameters, to be modified and passed back to the sector."""
    return dict(_params)
