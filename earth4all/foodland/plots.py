"""Figures of the FoodLand sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import foodland_run
from .subsystems import foodland

__all__ = ["foo_run_solution", "fig_fl"]


@cache
def foo_run_solution():
    """The solution of the FoodLand sector run, computed once and kept."""
    return solve(foodland_run(), (1980, 2100), dt=0.015625)


def _variables_foo():
    foo = foodland()
    return [
        (foo.CRLA, 0, 2000, "CRLA"),
        (foo.CRUS, 0, 8000, "CRUS"),
        (foo.CRUSP, 0, 1.2, "CRUSP"),
        (foo.FEUS, 0, 200, "FEUS"),
        (foo.FRA, 0, 1, "FRA"),
        (foo.TFA, 0, 4000, "TFA"),
    ]


def fig_fl(**kwargs):
    """Plot the main variables of the FoodLand sector run."""
    return plotvariables(
        foo_run_solution(),
        (1980, 2100),
        _variables_foo(),
        title="Food and land sector plots",
        showaxis=True,
        showlegend=True,
        **kwargs,
    )
