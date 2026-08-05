"""The Demand sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_dem, dem_run_solution
from .scenarios import demand_run
from .subsystems import demand, demand_full_support, demand_partial_support
from .tables import getranges, gettables

__all__ = [
    "demand",
    "demand_full_support",
    "demand_partial_support",
    "demand_run",
    "dem_run_solution",
    "fig_dem",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
