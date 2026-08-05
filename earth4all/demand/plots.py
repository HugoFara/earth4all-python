"""Figures of the Demand sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import demand_run
from .subsystems import demand

__all__ = ["dem_run_solution", "fig_dem"]


@cache
def dem_run_solution():
    """The solution of the Demand sector run, computed once and kept."""
    return solve(demand_run(), (1980, 2100), dt=0.015625)


def _variables_dem():
    dem = demand()
    return [
        (dem.CSGDP, 0, 1, "Consumption share of GDP (1)"),
        (dem.SSGDP, 0, 1, "Savings share of GDP (1)"),
        (dem.GSGDP, 0, 1, "Government share of GDP (1)"),
        (dem.NI, 0, 400000, "National income (G$/y)"),
        (dem.GDB, 0, 2, "Government debt burden (y)"),
        (dem.WDB, 0, 2, "Worker debt burden (y)"),
    ]


def fig_dem(**kwargs):
    """Plot the main variables of the Demand sector run."""
    kwargs.setdefault("showaxis", True)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        dem_run_solution(),
        (1980, 2100),
        _variables_dem(),
        title="Demand sector plots",
        **kwargs,
    )
