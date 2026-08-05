"""Running the Output sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import output, output_full_support

__all__ = ["output_run"]


def output_run(tables=None, ranges=None, **kwargs):
    """Compose the Output sector with the tabulated values it needs."""
    out = output(name="out", **kwargs)
    out_sup = output_full_support(
        name="out_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [out, out_sup]

    connection_eqs = [
        Equation(out.CBC, out_sup.CBC),
        Equation(out.CBC1980, out_sup.CBC1980),
        Equation(out.GDP, out_sup.GDP),
        Equation(out.GDPP, out_sup.GDPP),
        Equation(out.GIPC, out_sup.GIPC),
        Equation(out.ITFP, out_sup.ITFP),
        Equation(out.LAUS, out_sup.LAUS),
        Equation(out.OW, out_sup.OW),
        Equation(out.TS, out_sup.TS),
        Equation(out.TPP, out_sup.TPP),
        Equation(out.WASH, out_sup.WASH),
    ]

    return compose(systems, connection_eqs)
