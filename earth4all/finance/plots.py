"""Figures of the Finance sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import finance_run
from .subsystems import finance

__all__ = ["fin_run_solution", "fig_fin"]


@cache
def fin_run_solution():
    """The solution of the Finance sector run, computed once and kept."""
    return solve(finance_run(), (1980, 2100), dt=0.015625)


def _variables_fin():
    fin = finance()
    return [
        (fin.UR, 0, 0.1, "Unemployment rate"),
        (fin.CBC, 0, 0.1, "Corporate borrowing cost"),
        (fin.CBSR, 0, 0.1, "Central bank signal rate"),
        (fin.GBC, 0, 0.1, "Government borrowing cost"),
        (fin.WBC, 0, 0.1, "Worker borrowing cost"),
        (fin.IR, -0.05, 0.05, "Inflation rate"),
    ]


def fig_fin(**kwargs):
    """Plot the main variables of the Finance sector run."""
    return plotvariables(
        fin_run_solution(),
        (2010, 2030),
        _variables_fin(),
        title="Finance sector plots",
        showaxis=True,
        showlegend=True,
        **kwargs,
    )
