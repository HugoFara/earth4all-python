"""The tabulated trajectories used when a sector is run on its own.

They come from `src/tables.jl` of Earth4All.jl: one series per variable, taken
from a run of the whole model, so that a sector can be given the values of the
variables the other sectors would have computed. `scripts/convert_support_tables.py`
turns the Julia file into the array file this module reads.
"""

from functools import cache
from pathlib import Path

import numpy as np

__all__ = ["gettables", "getranges"]

_DATA_FILE = Path(__file__).parent / "data" / "support_tables.npz"


@cache
def _load():
    with np.load(_DATA_FILE) as data:
        tables, ranges = {}, {}
        for key in data.files:
            if key.startswith("range:"):
                low, high = data[key]
                ranges[key[len("range:"):]] = (float(low), float(high))
            else:
                tables[key] = tuple(data[key].tolist())
    return tables, ranges


def gettables():
    """A copy of the tabulated trajectories, keyed by variable name."""
    return dict(_load()[0])


def getranges():
    """A copy of the time range each tabulated trajectory spans."""
    return dict(_load()[1])
