"""Figures of the Climate sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import climate_run
from .subsystems import climate

__all__ = ["cli_run_solution", "fig_cli"]


@cache
def cli_run_solution():
    """The solution of the Climate sector run, computed once and kept."""
    return solve(climate_run(), (1980, 2100), dt=0.015625)


def _variables_cli():
    cli = climate()
    return [
        (cli.OW, 0, 4, "Observed warming deg C"),
        (cli.CO2E, 0, 44, "CO2 emissions GtCO2/y"),
        (cli.CO2CA, 0, 600, "CO2 concentration in atm ppm"),
        (cli.MMF, 0, 8, "Man-made forcing W/m2"),
        (cli.ISCEGA, 0, 20, "Ice and snow cover excl G&A Mkm"),
        (cli.WVF, 0, 8, "Water vapour feedback W/m2"),
    ]


def fig_cli(**kwargs):
    """Plot the main variables of the Climate sector run."""
    return plotvariables(
        cli_run_solution(),
        (1980, 2100),
        _variables_cli(),
        title="Climate sector plots",
        showaxis=True,
        showlegend=True,
        **kwargs,
    )
