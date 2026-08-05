"""The scenarios of the whole Earth4All model.

Two of them are the scenarios of the book: *Too Little Too Late*, where the
world keeps going as it does, and *Giant Leap*, where the five turnarounds are
carried out. They differ only by the parameters listed in `run_gl`.
"""

from . import (
    climate, demand, energy, finance, foodland, inventory, labourmarket, other,
    output, population, public, wellbeing,
)
from .system import compose, variable_connections

__all__ = ["run_tltl", "run_gl", "run_e4a", "sector_systems", "sector_names"]


def sector_systems(**kwargs):
    """Build the twelve sector systems, each with its own parameters and initial values."""
    return [
        demand.demand(name="dem", **kwargs.get("dem", {})),
        climate.climate(name="cli", **kwargs.get("cli", {})),
        energy.energy(name="ene", **kwargs.get("ene", {})),
        finance.finance(name="fin", **kwargs.get("fin", {})),
        foodland.foodland(name="foo", **kwargs.get("foo", {})),
        inventory.inventory(name="inv", **kwargs.get("inv", {})),
        labourmarket.labour_market(name="lab", **kwargs.get("lab", {})),
        other.other(name="oth", **kwargs.get("oth", {})),
        output.output(name="out", **kwargs.get("out", {})),
        population.population(name="pop", **kwargs.get("pop", {})),
        public.public(name="pub", **kwargs.get("pub", {})),
        wellbeing.wellbeing(name="wel", **kwargs.get("wel", {})),
    ]


def sector_names():
    """The names of the sectors, in the order Vensim exports them."""
    return [
        "climate", "demand", "energy", "finance", "foodland", "inventory",
        "labourmarket", "other", "output", "population", "public", "wellbeing",
    ]


def run_tltl(**kwargs):
    """The *Too Little Too Late* scenario, the model with its default parameters."""
    systems = sector_systems(**kwargs)
    return compose(systems, variable_connections(systems))


def run_gl(
    cli_ps=None,
    dem_ps=None,
    ene_ps=None,
    foo_ps=None,
    out_ps=None,
    pop_ps=None,
    pub_ps=None,
    **kwargs,
):
    """The *Giant Leap* scenario: the default model with the turnaround policies on."""
    cli_ps = climate.getparameters() if cli_ps is None else cli_ps
    cli_ps["ERDN2OKF2022"] = 0.01
    cli_ps["ERDCH4KC2022"] = 0.01
    cli_ps["DACCO22100"] = 8

    dem_ps = demand.getparameters() if dem_ps is None else dem_ps
    dem_ps["EETF2022"] = 0.02
    dem_ps["EGTRF2022"] = 0.01
    dem_ps["EPTF2022"] = 0.02
    dem_ps["ETGBW"] = 0.2
    dem_ps["FETPO"] = 0.8
    dem_ps["FGDC2022"] = 0.1
    dem_ps["GEIC"] = 0.02

    ene_ps = energy.getparameters() if ene_ps is None else ene_ps
    ene_ps["GFCO2SCCS"] = 0.9
    ene_ps["EROCEPA2022"] = 0.004
    ene_ps["GFNE"] = 1
    ene_ps["GREF"] = 1

    foo_ps = foodland.getparameters() if foo_ps is None else foo_ps
    foo_ps["GCWR"] = 0.2
    foo_ps["GFNRM"] = 0.5
    foo_ps["GFRA"] = 0.5

    out_ps = output.getparameters() if out_ps is None else out_ps
    out_ps["USPIS2022"] = 0.01
    out_ps["USPUS2022"] = 0.01

    pop_ps = population.getparameters() if pop_ps is None else pop_ps
    pop_ps["GEFR"] = 0.2

    pub_ps = public.getparameters() if pub_ps is None else pub_ps
    pub_ps["MIROTA2022"] = 0.005

    return run_e4a(
        cli_pars=cli_ps,
        dem_pars=dem_ps,
        ene_pars=ene_ps,
        foo_pars=foo_ps,
        out_pars=out_ps,
        pop_pars=pop_ps,
        pub_pars=pub_ps,
        **kwargs,
    )


def run_e4a(
    cli_pars=None, dem_pars=None, ene_pars=None, fin_pars=None, foo_pars=None,
    inv_pars=None, lab_pars=None, oth_pars=None, out_pars=None, pop_pars=None,
    pub_pars=None, wel_pars=None,
    cli_inits=None, dem_inits=None, ene_inits=None, fin_inits=None, foo_inits=None,
    inv_inits=None, lab_inits=None, oth_inits=None, out_inits=None, pop_inits=None,
    pub_inits=None, wel_inits=None,
):
    """The model with the parameters and initial values of every sector spelled out.

    This is the scenario to use to explore the model: pass a dictionary from
    `<sector>.getparameters()`, modified as needed, for the sectors to change.
    """
    sectors = {
        "cli": (cli_pars, cli_inits), "dem": (dem_pars, dem_inits),
        "ene": (ene_pars, ene_inits), "fin": (fin_pars, fin_inits),
        "foo": (foo_pars, foo_inits), "inv": (inv_pars, inv_inits),
        "lab": (lab_pars, lab_inits), "oth": (oth_pars, oth_inits),
        "out": (out_pars, out_inits), "pop": (pop_pars, pop_inits),
        "pub": (pub_pars, pub_inits), "wel": (wel_pars, wel_inits),
    }
    settings = {
        abbreviation: {
            key: value
            for key, value in (("params", params), ("inits", inits))
            if value is not None
        }
        for abbreviation, (params, inits) in sectors.items()
    }
    systems = sector_systems(**settings)
    return compose(systems, variable_connections(systems))
