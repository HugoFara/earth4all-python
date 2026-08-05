"""Figures of the Wellbeing sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import wellbeing_run
from .subsystems import wellbeing

__all__ = ["wel_run_solution", "fig_wb"]


@cache
def wel_run_solution():
    """The solution of the Wellbeing sector run, computed once and kept."""
    return solve(wellbeing_run(), (1980, 2100), dt=0.015625)


def _variables_wb():
    wel = wellbeing()
    return [
        (wel.AWBI, 0, 4, "Average WellBeing Index"),
    ]


def fig_wb(**kwargs):
    """Plot the main variables of the Wellbeing sector run."""
    kwargs.setdefault("showaxis", False)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        wel_run_solution(),
        (1980, 2100),
        _variables_wb(),
        title="Wellbeing sector plots",
        **kwargs,
    )
