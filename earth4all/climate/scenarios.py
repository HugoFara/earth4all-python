"""Running the Climate sector on its own.

The sector needs variables that other sectors compute; they are read from the
tabulated values of a full run of the model, which is what the `_full_support`
system provides.
"""

from ..symbolics import Equation
from ..system import compose
from ..tables import getranges as support_ranges
from ..tables import gettables as support_tables
from .subsystems import climate, climate_full_support

__all__ = ["climate_run"]


def climate_run(tables=None, ranges=None, **kwargs):
    """Compose the Climate sector with the tabulated values it needs."""
    cli = climate(name="cli", **kwargs)
    cli_sup = climate_full_support(
        name="cli_sup",
        tables=support_tables() if tables is None else tables,
        ranges=support_ranges() if ranges is None else ranges,
        **kwargs,
    )

    systems = [cli, cli_sup]

    connection_eqs = [
        Equation(cli.GDP, cli_sup.GDP),
        Equation(cli.IPP, cli_sup.IPP),
        Equation(cli.FEUS, cli_sup.FEUS),
        Equation(cli.CRSU, cli_sup.CRSU),
        Equation(cli.CO2EI, cli_sup.CO2EI),
        Equation(cli.CO2ELULUC, cli_sup.CO2ELULUC),
    ]

    return compose(systems, connection_eqs)
