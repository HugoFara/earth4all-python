"""Running the Inventory sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import inventory, inventory_full_support

__all__ = ["inv_run"]


def inv_run(tables=None, ranges=None, **kwargs):
    """Compose the Inventory sector with the tabulated values it needs."""
    inv = inventory(name="inv", **kwargs)
    inv_sup = inventory_full_support(
        name="inv_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [inv, inv_sup]

    connection_eqs = [
        Equation(inv.ORO, inv_sup.ORO),
        Equation(inv.TPP, inv_sup.TPP),
    ]

    return compose(systems, connection_eqs)
