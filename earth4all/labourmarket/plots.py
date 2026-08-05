"""Figures of the LabourMarket sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import lab_run
from .subsystems import labour_market

__all__ = ["lab_run_solution", "fig_lab"]


@cache
def lab_run_solution():
    """The solution of the LabourMarket sector run, computed once and kept."""
    return solve(lab_run(), (1980, 2100), dt=0.015625)


def _variables_lab():
    lab = labour_market()
    return [
        (lab.WF, 0, 6000, "Workforce"),
        (lab.WSO, 0, 1, "Worker share of output"),
        (lab.UNRA, 0, 0.1, "Unemployment rate"),
    ]


def fig_lab(**kwargs):
    """Plot the main variables of the LabourMarket sector run."""
    return plotvariables(
        lab_run_solution(),
        (1980, 2100),
        _variables_lab(),
        title="Labour Market sector plots",
        showaxis=False,
        showlegend=True,
        **kwargs,
    )
