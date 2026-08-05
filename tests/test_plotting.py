"""The figures: what they draw, and the grid they draw it on."""

import matplotlib

matplotlib.use("Agg")

import pytest  # noqa: E402  (the backend has to be set first)

from earth4all.functions import add_equation  # noqa: E402
from earth4all.plotting import plot_two_solutions, plotvariables  # noqa: E402
from earth4all.symbolics import D, t  # noqa: E402
from earth4all.system import ODESystem, compose, solve  # noqa: E402


@pytest.fixture(scope="module")
def solution():
    sector = ODESystem("s")
    rising = sector.variable("rising", init=0.0)
    large = sector.variable("large")
    add_equation(sector.equations, D(rising), 1.0)
    add_equation(sector.equations, large, 1000 * (t + 1))
    return solve(compose([sector]), (1980, 2100), dt=1.0)


def variables_of(solution):
    return [
        (solution.model.variable("s.rising"), 0, 120, "Rising"),
        (solution.model.variable("s.large"), 0, 250000, "Large"),
    ]


def test_one_line_is_drawn_per_variable(solution):
    figure = plotvariables(solution, (1980, 2100), variables_of(solution))
    assert sum(len(axes.lines) for axes in figure.axes) == 2


def test_each_variable_keeps_the_scale_it_was_given(solution):
    figure = plotvariables(solution, (1980, 2100), variables_of(solution))
    assert [axes.get_ylim() for axes in figure.axes] == [(0, 120), (0, 250000)]


def test_the_vertical_axes_have_their_ticks_at_the_same_heights(solution):
    """What lets one horizontal gridline be read against every scale at once."""
    figure = plotvariables(solution, (1980, 2100), variables_of(solution))
    heights = [
        [(tick - axes.get_ylim()[0]) / (axes.get_ylim()[1] - axes.get_ylim()[0])
         for tick in axes.get_yticks()]
        for axes in figure.axes
    ]
    assert heights[0] == pytest.approx(heights[1])


def test_the_grid_is_on_by_default_and_behind_the_lines(solution):
    figure = plotvariables(solution, (1980, 2100), variables_of(solution))
    axes = figure.axes[0]
    assert axes.xaxis.get_gridlines()[0].get_visible()
    assert axes.yaxis.get_gridlines()[0].get_visible()
    assert axes.get_axisbelow()


def test_the_grid_can_be_turned_off(solution):
    figure = plotvariables(solution, (1980, 2100), variables_of(solution), showgrid=False)
    assert not figure.axes[0].xaxis.get_gridlines()[0].get_visible()


def test_hiding_the_axes_leaves_only_the_years_gridded(solution):
    """A horizontal line reads against nothing once the scales are gone."""
    figure = plotvariables(
        solution, (1980, 2100), variables_of(solution), showaxis=False
    )
    axes = figure.axes[0]
    assert axes.xaxis.get_gridlines()[0].get_visible()
    assert not axes.yaxis.get_gridlines()[0].get_visible()


def test_comparing_two_solutions_gives_a_panel_per_variable(solution):
    figure = plot_two_solutions(
        "first", solution, "second", solution,
        [(solution.model.variable("s.rising"), "Rising"),
         (solution.model.variable("s.large"), "Large")],
    )
    assert len(figure.axes) == 2
    assert all(len(panel.lines) == 2 for panel in figure.axes)
    assert all(panel.xaxis.get_gridlines()[0].get_visible() for panel in figure.axes)
