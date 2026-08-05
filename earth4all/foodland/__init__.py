"""The FoodLand sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_fl, foo_run_solution
from .scenarios import foodland_run
from .subsystems import foodland, foodland_full_support, foodland_partial_support
from .tables import getranges, gettables

__all__ = [
    "foodland",
    "foodland_full_support",
    "foodland_partial_support",
    "foodland_run",
    "foo_run_solution",
    "fig_fl",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
