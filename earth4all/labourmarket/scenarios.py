"""Running the LabourMarket sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import labour_market, labour_market_full_support

__all__ = ["lab_run"]


def lab_run(tables=None, ranges=None, **kwargs):
    """Compose the LabourMarket sector with the tabulated values it needs."""
    lab = labour_market(name="lab", **kwargs)
    lab_sup = labour_market_full_support(
        name="lab_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [lab, lab_sup]

    connection_eqs = [
        Equation(lab.A20PA, lab_sup.A20PA),
        Equation(lab.CAP, lab_sup.CAP),
        Equation(lab.GDPP, lab_sup.GDPP),
        Equation(lab.IR, lab_sup.IR),
        Equation(lab.IPP, lab_sup.IPP),
        Equation(lab.OUTP, lab_sup.OUTP),
    ]

    return compose(systems, connection_eqs)
