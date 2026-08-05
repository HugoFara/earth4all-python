"""The Wellbeing sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_wb, wel_run_solution
from .scenarios import wellbeing_run
from .subsystems import wellbeing, wellbeing_full_support, wellbeing_partial_support
from .tables import getranges, gettables

__all__ = [
    "wellbeing",
    "wellbeing_full_support",
    "wellbeing_partial_support",
    "wellbeing_run",
    "wel_run_solution",
    "fig_wb",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
