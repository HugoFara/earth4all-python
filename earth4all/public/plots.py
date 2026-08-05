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
        (pub.DRTA, 0, 0.1, "Domestic rate of technological advance (1/y)"),
        (pub.GSSGDP, 0, 1, "Government spending as share of GDP (1)"),
        (pub.PSP, 0, 10, "Public spending per person (k$/p/y)"),
        (pub.TFPEE5TA, 0, 5, "TFP excluding the effect of the 5 turnarounds (1)"),
        (pub.XECTAGDP, -1, 1, "Extra cost of the turnarounds as share of GDP (1)"),
    ]


def fig_pub(**kwargs):
    """Plot the main variables of the Public sector run."""
    kwargs.setdefault("showaxis", False)
    kwargs.setdefault("showlegend", True)
    return plotvariables(
        pub_run_solution(),
        (1980, 2100),
        _variables_pub(),
        title="Public sector plots",
        **kwargs,
    )
