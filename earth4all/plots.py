"""The base run figures of the whole model.

They show the six variables the Earth4All book puts on its first figure: how
many people there are, how well they live, and how hot it gets.
"""

from . import climate, demand, population, wellbeing
from .plotting import plot_two_solutions, plotvariables
from .solutions import run_gl_solution, run_tltl_solution

__all__ = ["fig_baserun_tltl", "fig_baserun_gl", "fig_baserun_comparison"]


def _variables():
    pop = population.population(name="pop")
    wel = wellbeing.wellbeing(name="wel")
    cli = climate.climate(name="cli")
    dem = demand.demand(name="dem")
    return [
        (pop.POP, 0, 10000, "Population"),
        # The Julia code stops this axis at 2.4, which the Giant Leap runs past.
        (wel.AWBI, 0, 3.5, "Average wellbeing"),
        (pop.GDPP, 0, 60, "GDP per person"),
        (wel.STE, 0, 2, "Social tension"),
        (dem.INEQ, 0, 1.6, "Inequality"),
        (cli.OW, 0, 4, "Global warming"),
    ]


def fig_baserun_tltl(**kwargs):
    """Plot the base run of the *Too Little Too Late* scenario."""
    return plotvariables(
        run_tltl_solution(),
        (1980, 2100),
        _variables(),
        title="Too Little too Late model base run plot",
        showaxis=True,
        showlegend=True,
        **kwargs,
    )


def fig_baserun_gl(**kwargs):
    """Plot the base run of the *Giant Leap* scenario."""
    return plotvariables(
        run_gl_solution(),
        (1980, 2100),
        _variables(),
        title="Giant Leap model base run plot",
        showaxis=True,
        showlegend=True,
        **kwargs,
    )


def fig_baserun_comparison(**kwargs):
    """Put the two scenarios side by side, one panel per variable."""
    return plot_two_solutions(
        "Too Little Too Late",
        run_tltl_solution(),
        "Giant Leap",
        run_gl_solution(),
        [(variable, label) for variable, _, _, label in _variables()],
        **kwargs,
    )
