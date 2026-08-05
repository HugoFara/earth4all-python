"""Running the Public sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import public, public_full_support

__all__ = ["public_run"]


def public_run(tables=None, ranges=None, **kwargs):
    """Compose the Public sector with the tabulated values it needs."""
    pub = public(name="pub", **kwargs)
    pub_sup = public_full_support(
        name="pub_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [pub, pub_sup]

    connection_eqs = [
        Equation(pub.CPUS, pub_sup.CPUS),
        Equation(pub.CTA, pub_sup.CTA),
        Equation(pub.GDP, pub_sup.GDP),
        Equation(pub.GDPP, pub_sup.GDPP),
        # The Julia code connects `GP` here, which no system declares; the
        # variable the Public sector reads from Demand is `GPU`.
        Equation(pub.GPU, pub_sup.GPU),
        Equation(pub.GS, pub_sup.GS),
        Equation(pub.INEQI, pub_sup.INEQI),
        Equation(pub.OW, pub_sup.OW),
        Equation(pub.POP, pub_sup.POP),
    ]

    return compose(systems, connection_eqs)
