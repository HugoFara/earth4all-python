"""Running the FoodLand sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import foodland, foodland_full_support

__all__ = ["foodland_run"]


def foodland_run(tables=None, ranges=None, **kwargs):
    """Compose the FoodLand sector with the tabulated values it needs."""
    foo = foodland(name="foo", **kwargs)
    foo_sup = foodland_full_support(
        name="foo_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [foo, foo_sup]

    connection_eqs = [
        Equation(foo.CO2CA, foo_sup.CO2CA),
        Equation(foo.GDP, foo_sup.GDP),
        Equation(foo.GDPP, foo_sup.GDPP),
        Equation(foo.IPP, foo_sup.IPP),
        Equation(foo.OW, foo_sup.OW),
        Equation(foo.POP, foo_sup.POP),
    ]

    return compose(systems, connection_eqs)
