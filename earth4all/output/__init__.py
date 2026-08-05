"""The Output sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_out, out_run_solution
from .scenarios import output_run
from .subsystems import output, output_full_support, output_partial_support
from .tables import getranges, gettables

__all__ = [
    "output",
    "output_full_support",
    "output_partial_support",
    "output_run",
    "out_run_solution",
    "fig_out",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
