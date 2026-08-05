"""Running the Energy sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import energy, energy_full_support

__all__ = ["energy_run"]


def energy_run(tables=None, ranges=None, **kwargs):
    """Compose the Energy sector with the tabulated values it needs."""
    ene = energy(name="ene", **kwargs)
    ene_sup = energy_full_support(
        name="ene_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [ene, ene_sup]

    connection_eqs = [
        Equation(ene.GDPP, ene_sup.GDPP),
        Equation(ene.POP, ene_sup.POP),
        Equation(ene.IPP, ene_sup.IPP),
        Equation(ene.GDP, ene_sup.GDP),
        Equation(ene.CAC, ene_sup.CAC),
    ]

    return compose(systems, connection_eqs)
