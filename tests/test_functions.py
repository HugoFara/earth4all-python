"""The model functions, on numbers and on expressions."""

import math

import pytest

from earth4all.functions import (
    Lookup, add_equation, clip, delay_n, interpolate, pulse, ramp, smooth, step,
    withlookup,
)
from earth4all.symbolics import D, Expr, exp, ifelse, max, min, t
from earth4all.system import ODESystem, compose, solve


def test_ramp_holds_before_start_and_after_end():
    assert ramp(1980, 2, 2000, 2010) == 0
    assert ramp(2005, 2, 2000, 2010) == 10
    assert ramp(2050, 2, 2000, 2010) == 20


def test_clip_and_step():
    assert clip(1, -1, 5, 5) == 1
    assert clip(1, -1, 4.9, 5) == -1
    assert step(4, 7, 5) == 0
    assert step(5, 7, 5) == 7


def test_pulse_lasts_for_its_width():
    assert pulse(1999, 2000, 3) == 0
    assert pulse(2000, 2000, 3) == 1
    assert pulse(2002.9, 2000, 3) == 1
    assert pulse(2003, 2000, 3) == 0


def test_lookup_interpolates_and_clamps():
    table = Lookup([0, 1, 2], [10, 20, 40])
    assert table(-1) == 10
    assert table(0) == 10
    assert table(0.5) == 15
    assert table(1.5) == 30
    assert table(2) == 40
    assert table(9) == 40


def test_interpolate_spreads_the_table_over_the_range():
    assert interpolate(1980, (0.0, 1.0, 3.0), (1980, 2100)) == 0
    assert interpolate(2040, (0.0, 1.0, 3.0), (1980, 2100)) == 1
    assert interpolate(2070, (0.0, 1.0, 3.0), (1980, 2100)) == 2


def test_withlookup_takes_pairs():
    assert withlookup(1990, [(1980.0, 0.0), (2000.0, 1.0)]) == 0.5


def test_functions_build_expressions_when_given_one():
    assert isinstance(ramp(t, 1, 2000, 2010), Expr)
    assert isinstance(max(0, t), Expr)
    assert isinstance(interpolate(t, (0.0, 1.0), (1980, 2100)), Expr)


def test_numeric_functions_stay_numeric():
    assert max(2, 3) == 3
    assert min(2, 3) == 2
    assert ifelse(True, 1, 2) == 1
    assert exp(0) == 1


def test_an_expression_has_no_truth_value():
    with pytest.raises(TypeError):
        bool(t > 2000)


def test_smooth_follows_its_input():
    sector = ODESystem("s")
    smoothed = sector.variable("smoothed", init=0.0)
    smooth(sector.equations, smoothed, 1.0, 2.0)
    solution = solve(compose([sector]), (0, 10), dt=0.001)
    # An exponential smooth of a step reaches 1 - exp(-t / delay).
    assert solution["s.smoothed"][-1] == pytest.approx(1 - math.exp(-5), abs=1e-3)


def test_delay_of_order_one_is_an_exponential_delay():
    sector = ODESystem("s")
    levels = sector.variable_array("lv", 1, init=0.0)
    rates = sector.variable_array("rt", 1)
    delay_n(sector.equations, 1.0, rates, levels, 2.0, 1)
    solution = solve(compose([sector]), (0, 10), dt=0.001)
    assert solution["s.rt_1"][-1] == pytest.approx(1 - math.exp(-5), abs=1e-3)


def test_add_equation_records_the_equation():
    sector = ODESystem("s")
    stock = sector.variable("stock", init=1.0)
    add_equation(sector.equations, D(stock), stock)
    assert len(sector.equations) == 1
    assert sector.equations[0].is_derivative
