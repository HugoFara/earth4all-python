"""Plots of the variables of a solution, in the style of the WorldDynamics figures.

Every variable is drawn against its own vertical axis, so that quantities with
very different magnitudes — a population in millions of people and a temperature
in degrees — can be read on the same figure.

The Julia code draws with PlotlyJS; here the drawing is done with matplotlib,
which is the one dependency the rest of the package does not already need.
"""

__all__ = ["plotvariables", "plot_two_solutions"]

# Distinguishable at a glance, and readable when printed in grey.
_COLOURS = [
    "#4269d0", "#efb118", "#ff725c", "#6cc5b0", "#3ca951",
    "#a463f2", "#97bbf5", "#9c6b4e", "#ff8ab7", "#9498a0",
]

_AXIS_OFFSET = 55  # points between two stacked vertical axes
_TICKS = 6  # ticks per vertical axis; the same count on all of them lines them up
_GRID = {"color": "#9aa0a6", "linewidth": 0.6, "alpha": 0.45}
_MINOR_GRID = {"color": "#9aa0a6", "linewidth": 0.4, "alpha": 0.2}


def _year_axis(axes):
    """Tick the horizontal axis on whole years, with one minor tick between."""
    from matplotlib.ticker import AutoMinorLocator, MaxNLocator

    axes.xaxis.set_major_locator(MaxNLocator(nbins="auto", integer=True))
    axes.xaxis.set_minor_locator(AutoMinorLocator(2))


def _draw_grid(axes, vertical=True, horizontal=True):
    """Put a grid behind the lines, with lighter lines between the labelled ones."""
    axes.set_axisbelow(True)
    if vertical:
        axes.grid(axis="x", which="major", **_GRID)
        axes.grid(axis="x", which="minor", **_MINOR_GRID)
    if horizontal:
        axes.grid(axis="y", which="major", **_GRID)


def plotvariables(
    solution,
    xrange=(1980, 2100),
    variables=(),
    title="",
    showaxis=True,
    showlegend=True,
    showgrid=True,
    figsize=(11, 6),
):
    """Draw `variables` of `solution` over `xrange` on a single figure.

    Each entry of `variables` is a `(variable, ymin, ymax, label)` tuple, as in
    the Julia code: the bounds set the scale of that variable's own axis.

    Every vertical axis is given the same number of ticks, so they fall at the
    same heights and one horizontal gridline can be read against all of them.
    """
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LinearLocator

    figure, axes = plt.subplots(figsize=figsize)
    start, stop = xrange[-2], xrange[-1]
    times = solution.t
    window = (times >= start) & (times <= stop)

    labelled = []
    for index, (variable, ymin, ymax, label) in enumerate(variables):
        # A variable given no label of its own goes by the name it carries in
        # Vensim, rather than by nothing at all.
        label = label or getattr(variable, "description", "")
        colour = _COLOURS[index % len(_COLOURS)]
        target = axes if index == 0 else axes.twinx()
        if index > 1:
            target.spines["right"].set_position(("outward", _AXIS_OFFSET * (index - 1)))
        line, = target.plot(
            times[window], solution[variable][window], color=colour, label=label or None,
        )
        if label:
            labelled.append((line, label))
        target.set_ylim(ymin, ymax)
        target.yaxis.set_major_locator(LinearLocator(_TICKS))
        if showaxis:
            target.tick_params(axis="y", colors=colour)
            target.spines["right" if index else "left"].set_color(colour)
        else:
            target.tick_params(axis="y", left=False, right=False, labelleft=False,
                               labelright=False)

    axes.set_xlim(start, stop)
    axes.set_xlabel("Year")
    _year_axis(axes)
    if showgrid:
        # Without the labels of the vertical axes, a horizontal line reads
        # against nothing, so only the years get a grid.
        _draw_grid(axes, horizontal=showaxis)
    if title:
        axes.set_title(title)
    if showlegend and labelled:
        axes.legend(*zip(*labelled), loc="upper left")
    figure.tight_layout()
    return figure


def plot_two_solutions(
    name1, solution1, name2, solution2, variables, xrange=(1980, 2100),
    showgrid=True, figsize=(11, 6),
):
    """Compare the same variables in two solutions, one panel per variable.

    Each panel has a vertical axis of its own, so its grid can be read straight
    off: where a curve turns over, and at what value.
    """
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(
        len(variables), 1, figsize=(figsize[0], 2.4 * len(variables)), squeeze=False,
        sharex=True,
    )
    start, stop = xrange[-2], xrange[-1]
    for panel, (variable, label) in zip(axes[:, 0], variables):
        for solution, name, colour, style in (
            (solution1, name1, _COLOURS[0], "--"),
            (solution2, name2, _COLOURS[2], ":"),
        ):
            window = (solution.t >= start) & (solution.t <= stop)
            panel.plot(
                solution.t[window], solution[variable][window],
                color=colour, linestyle=style, label=name,
            )
        panel.set_ylabel(label)
        panel.set_xlim(start, stop)
        _year_axis(panel)
        if showgrid:
            _draw_grid(panel)
    axes[0, 0].legend(loc="upper left")
    axes[-1, 0].set_xlabel("Year")
    figure.tight_layout()
    return figure
