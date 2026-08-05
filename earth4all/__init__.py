"""Earth4All: a Python implementation of the Earth4All integrated assessment model.

This is a port of `Earth4All.jl <https://github.com/worlddynamics/Earth4All.jl>`_,
itself an implementation of the April 2023 Vensim version of the Earth4All model.
The twelve sectors of the model are one subpackage each; `scenarios` composes
them, and `solutions` runs them:

    >>> from earth4all import run_tltl_solution
    >>> solution = run_tltl_solution()
    >>> solution["pop.POP"][-1]  # world population in 2100, in millions
"""

from . import (
    climate, demand, energy, finance, foodland, inventory, labourmarket, other,
    output, plotting, population, public, tables, wellbeing,
)
from .functions import (
    clip, interpolate, pulse, ramp, step, withlookup,
)
from .plots import fig_baserun_comparison, fig_baserun_gl, fig_baserun_tltl
from .plotting import plot_two_solutions, plotvariables
from .scenarios import run_e4a, run_gl, run_tltl, sector_names, sector_systems
from .solutions import run_e4a_solution, run_gl_solution, run_tltl_solution
from .system import compose, solve, variable_connections

__version__ = "0.1.0"

__all__ = [
    "climate", "demand", "energy", "finance", "foodland", "inventory",
    "labourmarket", "other", "output", "population", "public", "wellbeing",
    "plotting", "tables",
    "run_tltl", "run_gl", "run_e4a", "sector_systems", "sector_names",
    "run_tltl_solution", "run_gl_solution", "run_e4a_solution",
    "fig_baserun_tltl", "fig_baserun_gl", "fig_baserun_comparison",
    "plotvariables", "plot_two_solutions",
    "compose", "solve", "variable_connections",
    "clip", "interpolate", "pulse", "ramp", "step", "withlookup",
    "__version__",
]
