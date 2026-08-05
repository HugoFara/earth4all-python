"""The LabourMarket sector of the Earth4All model."""

from .initialisations import getinitialisations
from .parameters import getparameters
from .plots import fig_lab, lab_run_solution
from .scenarios import lab_run
from .subsystems import labour_market, labour_market_full_support, labour_market_partial_support
from .tables import getranges, gettables

__all__ = [
    "labour_market",
    "labour_market_full_support",
    "labour_market_partial_support",
    "lab_run",
    "lab_run_solution",
    "fig_lab",
    "getinitialisations",
    "getparameters",
    "getranges",
    "gettables",
]
