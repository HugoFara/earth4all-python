"""The Climate sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_cli, cli_run_solution
from .scenarios import climate_run
from .subsystems import climate, climate_full_support, climate_partial_support
from .tables import getranges, gettables

__all__ = [
    "climate",
    "climate_full_support",
    "climate_partial_support",
    "climate_run",
    "cli_run_solution",
    "fig_cli",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
