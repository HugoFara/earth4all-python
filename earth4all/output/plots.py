"""Figures of the Output sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import output_run
from .subsystems import output

__all__ = ["out_run_solution", "fig_out"]


@cache
def out_run_solution():
    """The solution of the Output sector run, computed once and kept."""
    return solve(output_run(), (1980, 2100), dt=0.015625)


def _variables_out():
    out = output()
    return [
        (out.CUCPIS, 0, 100000, "Capacity under construction PIS (Gcu)"),
        (out.CUCPUS, 0, 30000, "Capacity under construction PUS (Gcu)"),
        (out.OGR, -0.1, 0.1, "Output growth rate (1/y)"),
        (out.OLY, 0, 350000, "Output last year (G$/y)"),
        (out.ORO, 0, 350000, "Optimal real output (Gu/y)"),
    ]


def fig_out(**kwargs):
    """Plot the main variables of the Output sector run."""
    kwargs.setdefault("showaxis", False)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        out_run_solution(),
        (1980, 2100),
        _variables_out(),
        title="Output sector plots",
        **kwargs,
    )
