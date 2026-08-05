"""Figures of the Inventory sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import inv_run
from .subsystems import inventory

__all__ = ["inv_run_solution", "fig_inv"]


@cache
def inv_run_solution():
    """The solution of the Inventory sector run, computed once and kept."""
    return solve(inv_run(), (1980, 2100), dt=0.015625)


def _variables_inv():
    inv = inventory()
    return [
        (inv.PNIS, 0, 2, "PNIS"),
        (inv.PRI, 0, 1.5, "PRI"),
        (inv.DELDI, 0.9, 1.1, "DELDI"),
        (inv.IR, -0.1, 0.1, "IR"),
        (inv.PI, 0, 4, "PI"),
    ]


def fig_inv(**kwargs):
    """Plot the main variables of the Inventory sector run."""
    return plotvariables(
        inv_run_solution(),
        (1980, 2040),
        _variables_inv(),
        title="Inventory sector plots",
        showaxis=True,
        showlegend=True,
        **kwargs,
    )
