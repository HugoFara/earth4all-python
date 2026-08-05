"""Running the Wellbeing sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import wellbeing, wellbeing_full_support

__all__ = ["wellbeing_run"]


def wellbeing_run(tables=None, ranges=None, **kwargs):
    """Compose the Wellbeing sector with the tabulated values it needs."""
    wel = wellbeing(name="wel", **kwargs)
    wel_sup = wellbeing_full_support(
        name="wel_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [wel, wel_sup]

    connection_eqs = [
        Equation(wel.GDPP, wel_sup.GDPP),
        Equation(wel.INEQ, wel_sup.INEQ),
        Equation(wel.LPR, wel_sup.LPR),
        Equation(wel.PSP, wel_sup.PSP),
        Equation(wel.PWA, wel_sup.PWA),
        Equation(wel.WDI, wel_sup.WDI),
    ]

    return compose(systems, connection_eqs)
