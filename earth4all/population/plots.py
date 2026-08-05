"""Figures of the Population sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import pop_run
from .subsystems import population

__all__ = ["pop_run_solution", "fig_pop"]


@cache
def pop_run_solution():
    """The solution of the Population sector run, computed once and kept."""
    return solve(pop_run(), (1980, 2100), dt=0.015625)


def _variables_pop():
    pop = population()
    return [
        (pop.BIRTHS, 0, 140, "Births Mp/y"),
        (pop.LE60, 0, 40, "LE at 60 y"),
        (pop.POP, 3000, 11000, "Population Mp"),
    ]


def fig_pop(**kwargs):
    """Plot the main variables of the Population sector run."""
    kwargs.setdefault("showaxis", False)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        pop_run_solution(),
        (1980, 2100),
        _variables_pop(),
        title="Population sector plots",
        **kwargs,
    )
