"""The model functions of `src/functions.jl`: DYNAMO/Vensim primitives and the
helpers used to declare delays and smoothings.

Each of them works on numbers and on equation expressions alike, so the sector
code reads the same whether it is being built symbolically or evaluated.
"""

from bisect import bisect_right

from .symbolics import D, Equation, register_function

__all__ = [
    "add_equation", "delay_n", "ramp", "smooth", "clip", "step", "pulse",
    "interpolate", "withlookup", "Lookup",
]


def add_equation(eqs, lhs, rhs):
    """Add the equation `lhs ~ rhs` to the list `eqs` of equations."""
    eqs.append(Equation(lhs, rhs))


def delay_n(eqs, x, rt, lv, delay, order):
    """Add an N'th order exponential delay of `x`.

    `lv` and `rt` are the lists of the `order` level and rate variables; the
    delayed signal is the last rate, `rt[order - 1]`.
    """
    add_equation(eqs, rt[0], lv[0] / (delay / order))
    add_equation(eqs, D(lv[0]), x - rt[0])
    for d in range(1, order):
        add_equation(eqs, rt[d], lv[d] / (delay / order))
        add_equation(eqs, D(lv[d]), rt[d - 1] - rt[d])


def smooth(eqs, x, input_, delay_time):
    """Add the equation making `x` an exponential smooth of `input_`."""
    add_equation(eqs, D(x), (input_ - x) / delay_time)


def _ramp(x, slope, startx, endx):
    if x > startx:
        return slope * (x - startx) if x < endx else slope * (endx - startx)
    return 0.0


def _clip(returnifgte, returniflt, inputvalue, threshold):
    return returnifgte if inputvalue >= threshold else returniflt


def _step(inputvalue, returnifgte, threshold):
    return _clip(returnifgte, 0.0, inputvalue, threshold)


def _pulse(inputvalue, start, width):
    return float(inputvalue >= start) * float(inputvalue < start + width)


class Lookup:
    """A tabulated function of one variable, linearly interpolated.

    Outside `[xs[0], xs[-1]]` the value at the closest end of the table is
    returned, as `TABHL` in DYNAMO and `WITH LOOKUP` in Vensim do.
    """

    __slots__ = ("xs", "ys")

    def __init__(self, xs, ys):
        self.xs = [float(v) for v in xs]
        self.ys = [float(v) for v in ys]
        if len(self.xs) != len(self.ys):
            raise ValueError("a lookup needs as many x values as y values")

    @classmethod
    def over_range(cls, yvalues, xrange):
        """Build a lookup whose x values are `len(yvalues)` points spanning `xrange`."""
        x1, xn = float(xrange[0]), float(xrange[1])
        n = len(yvalues)
        if n == 1:
            return cls([x1], yvalues)
        # The same formula as Julia's LinRange, exact at both ends.
        xs = [(x1 * (n - 1 - i) + xn * i) / (n - 1) for i in range(n)]
        return cls(xs, yvalues)

    @classmethod
    def over_pairs(cls, pairs):
        return cls([p[0] for p in pairs], [p[-1] for p in pairs])

    def __call__(self, x):
        xs, ys = self.xs, self.ys
        if x < xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]
        i = bisect_right(xs, x) - 1
        x1, x2 = xs[i], xs[i + 1]
        y1, y2 = ys[i], ys[i + 1]
        return y1 + (x - x1) * ((y2 - y1) / (x2 - x1))

    def __repr__(self):
        return f"Lookup({len(self.xs)} points from {self.xs[0]} to {self.xs[-1]})"


def _lookup(x, table):
    return table(x)


ramp = register_function("ramp", _ramp)
ramp.__doc__ = """Return 0 until `startx`, then a slope of `slope` up to `endx`, then a
constant. This function corresponds to the `RAMP` function of the Vensim language."""

clip = register_function("clip", _clip)
clip.__doc__ = """Return `returnifgte` if `inputvalue` is greater than or equal to
`threshold`, `returniflt` otherwise. This function corresponds to the `CLIP` (also
called `FIFGE`) function of the DYNAMO language."""

step = register_function("step", _step)
step.__doc__ = """Return 0 if `inputvalue` is smaller than `threshold`, `returnifgte`
otherwise. This function corresponds to the `STEP` function of the DYNAMO language."""

pulse = register_function("pulse", _pulse)
pulse.__doc__ = """Return 1 from `start` and for a duration of `width`, and 0 at all
other times. This function corresponds to the `PULSE` function of the Vensim language."""

lookup = register_function("lookup", _lookup)
lookup.__doc__ = """Evaluate the tabulated function `table` at `x`."""


def interpolate(x, yvalues, xrange):
    """Interpolate the table `yvalues`, whose x values span `xrange`, at `x`.

    This function corresponds to the `TABHL` function of the DYNAMO language.
    """
    return lookup(x, Lookup.over_range(yvalues, xrange))


def withlookup(x, pairs):
    """Interpolate at `x` the table given as a list of `(x, y)` pairs.

    This function corresponds to the `WITH LOOKUP` function of Vensim.
    """
    return lookup(x, Lookup.over_pairs(pairs))
