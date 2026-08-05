"""Running the Population sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import population, population_full_support

__all__ = ["pop_run"]


def pop_run(tables=None, ranges=None, **kwargs):
    """Compose the Population sector with the tabulated values it needs."""
    pop = population(name="pop", **kwargs)
    pop_sup = population_full_support(
        name="pop_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [pop, pop_sup]

    connection_eqs = [
        Equation(pop.GDP, pop_sup.GDP),
        Equation(pop.IPP, pop_sup.IPP),
        Equation(pop.OW, pop_sup.OW),
    ]

    return compose(systems, connection_eqs)
