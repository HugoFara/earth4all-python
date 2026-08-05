"""The Population sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_pop, pop_run_solution
from .scenarios import pop_run
from .subsystems import population, population_full_support, population_partial_support
from .tables import getranges, gettables

__all__ = [
    "population",
    "population_full_support",
    "population_partial_support",
    "pop_run",
    "pop_run_solution",
    "fig_pop",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
