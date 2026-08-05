"""Running the Demand sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import demand, demand_full_support

__all__ = ["demand_run"]


def demand_run(tables=None, ranges=None, **kwargs):
    """Compose the Demand sector with the tabulated values it needs."""
    dem = demand(name="dem", **kwargs)
    dem_sup = demand_full_support(
        name="dem_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [dem, dem_sup]

    connection_eqs = [
        Equation(dem.ECTAF2022, dem_sup.ECTAF2022),
        Equation(dem.EGDPP, dem_sup.EGDPP),
        Equation(dem.GBC, dem_sup.GBC),
        Equation(dem.IPP, dem_sup.IPP),
        Equation(dem.NI, dem_sup.NI),
        Equation(dem.POP, dem_sup.POP),
        Equation(dem.WBC, dem_sup.WBC),
        Equation(dem.WF, dem_sup.WF),
        Equation(dem.WSO, dem_sup.WSO),
    ]

    return compose(systems, connection_eqs)
