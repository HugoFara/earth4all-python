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
        (inv.PNIS, 0, 2, "Pink noise in sales (1)"),
        (inv.PRI, 0, 1.5, "Perceived relative inventory (1)"),
        (inv.DELDI, 0.9, 1.1, "Delivery delay index (1)"),
        (inv.IR, -0.1, 0.1, "Inflation rate (1/y)"),
        # The Julia list ends on `inv.PI`, which the Inventory sector does not
        # declare. `PI` belongs to Finance, which a run of this sector alone
        # does not include, so the figure is left with the four above.
    ]


def fig_inv(**kwargs):
    """Plot the main variables of the Inventory sector run."""
    kwargs.setdefault("showaxis", True)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        inv_run_solution(),
        (1980, 2040),
        _variables_inv(),
        title="Inventory sector plots",
        **kwargs,
    )
