"""Figures of the Public sector."""

from functools import cache

from ..plotting import plotvariables
from ..system import solve
from .scenarios import public_run
from .subsystems import public

__all__ = ["pub_run_solution", "fig_pub"]


@cache
def pub_run_solution():
    """The solution of the Public sector run, computed once and kept."""
    return solve(public_run(), (1980, 2100), dt=0.015625)


def _variables_pub():
    pub = public()
    return [
        (pub.DRTA, 0, 0.1, "DRTA"),
        (pub.GSSGDP, 0, 1, "GSSGDP"),
        (pub.PSP, 0, 10, "PSP"),
        (pub.TFPEE5TA, 0, 5, "TFPEE5TA"),
        (pub.XECTAGDP, -1, 1, "XECTAGDP"),
    ]


def fig_pub(**kwargs):
    """Plot the main variables of the Public sector run."""
    return plotvariables(
        pub_run_solution(),
        (1980, 2100),
        _variables_pub(),
        title="Public sector plots",
        showaxis=False,
        showlegend=True,
        **kwargs,
    )
