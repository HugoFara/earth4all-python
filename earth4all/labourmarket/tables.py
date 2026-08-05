"""Tabulated functions of the LabourMarket sector."""

_tables = {
    "ROCWSO": (0.06, 0.02, 0, -0.007, -0.01),
}

_ranges = {
    "ROCWSO": (0, 2),
}


def gettables():
    """A copy of the tabulated functions of the sector."""
    return dict(_tables)


def getranges():
    """A copy of the ranges over which the tabulated functions are defined."""
    return dict(_ranges)
