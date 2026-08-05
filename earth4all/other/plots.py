"""Figures of the Other sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import other_run
from .subsystems import other

__all__ = ["oth_run_solution", "fig_oth"]


@cache
def oth_run_solution():
    """The solution of the Other sector run, computed once and kept."""
    return solve(other_run(), (1980, 2100), dt=0.015625)


def _variables_oth():
    oth = other()
    return [
        (oth.CTA, 0, 20000, "CTA"),
        (oth.PB15, 0, 10000, "PB15"),
        (oth.RGGDPP, 0, 0.04, "RGGDPP"),
    ]


def fig_oth(**kwargs):
    """Plot the main variables of the Other sector run."""
    kwargs.setdefault("showaxis", False)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        oth_run_solution(),
        (1980, 2100),
        _variables_oth(),
        title="Other sector plots",
        **kwargs,
    )
