"""Running the Finance sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import finance, finance_full_support

__all__ = ["finance_run"]


def finance_run(tables=None, ranges=None, **kwargs):
    """Compose the Finance sector with the tabulated values it needs."""
    fin = finance(name="fin", **kwargs)
    fin_sup = finance_full_support(
        name="fin_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [fin, fin_sup]

    connection_eqs = [
        Equation(fin.OGR, fin_sup.OGR),
        Equation(fin.IR, fin_sup.IR),
        Equation(fin.UR, fin_sup.UR),
    ]

    return compose(systems, connection_eqs)
