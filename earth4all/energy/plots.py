"""Figures of the Energy sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import energy_run
from .subsystems import energy

__all__ = ["ene_run_solution", "fig_en"]


@cache
def ene_run_solution():
    """The solution of the Energy sector run, computed once and kept."""
    return solve(energy_run(), (1980, 2100), dt=0.015625)


def _variables_en():
    ene = energy()
    return [
        (ene.CE, 0, 7000, "Cost of energy (G$/y)"),
    ]


def fig_en(**kwargs):
    """Plot the main variables of the Energy sector run."""
    kwargs.setdefault("showaxis", True)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        ene_run_solution(),
        (1980, 2100),
        _variables_en(),
        title="Energy sector plots",
        **kwargs,
    )
