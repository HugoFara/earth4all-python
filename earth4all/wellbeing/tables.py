"""Tabulated functions of the Wellbeing sector."""

_tables = {
    "IEST": (1, 1, 0),
    "PSESTR": (0, 1),
}

_ranges = {
    "IEST": (0, 2),
    "PSESTR": (0, 1),
}


def gettables():
    """A copy of the tabulated functions of the sector."""
    return dict(_tables)


def getranges():
    """A copy of the ranges over which the tabulated functions are defined."""
    return dict(_ranges)
