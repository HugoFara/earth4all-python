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
        (foo.CRLA, 0, 2000, "Cropland (Mha)"),
        (foo.CRUS, 0, 8000, "Crop use (Mt/y)"),
        (foo.CRUSP, 0, 1.2, "Crop use per person (t-crop/p/y)"),
        (foo.FEUS, 0, 200, "Fertilizer use (Mt/y)"),
        (foo.FRA, 0, 1, "Fraction regenerative agriculture (1)"),
        (foo.TFA, 0, 4000, "Total forest area (Mha)"),
    ]


def fig_fl(**kwargs):
    """Plot the main variables of the FoodLand sector run."""
    kwargs.setdefault("showaxis", True)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        foo_run_solution(),
        (1980, 2100),
        _variables_foo(),
        title="Food and land sector plots",
        **kwargs,
    )
