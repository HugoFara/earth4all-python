"""The Other sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_oth, oth_run_solution
from .scenarios import other_run
from .subsystems import other, other_full_support, other_partial_support
from .tables import getranges, gettables

__all__ = [
    "other",
    "other_full_support",
    "other_partial_support",
    "other_run",
    "oth_run_solution",
    "fig_oth",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
