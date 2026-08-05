"""Running the Other sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import other, other_full_support

__all__ = ["other_run"]


def other_run(tables=None, ranges=None, **kwargs):
    """Compose the Other sector with the tabulated values it needs."""
    oth = other(name="oth", **kwargs)
    oth_sup = other_full_support(
        name="oth_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [oth, oth_sup]

    connection_eqs = [
        Equation(oth.CE, oth_sup.CE),
        Equation(oth.COFO, oth_sup.COFO),
        Equation(oth.GDPP, oth_sup.GDPP),
        Equation(oth.INEQ, oth_sup.INEQ),
        Equation(oth.POP, oth_sup.POP),
    ]

    return compose(systems, connection_eqs)
