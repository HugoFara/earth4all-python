"""Building, composing and solving systems of equations."""

import math

import pytest

from earth4all.functions import add_equation
from earth4all.symbolics import D, Equation
from earth4all.system import ODESystem, compose, solve, variable_connections


def exponential_growth(rate=0.1):
    sector = ODESystem("g")
    stock = sector.variable("stock", init=1.0, description="A growing stock")
    flow = sector.variable("flow", description="Its inflow")
    growth = sector.parameter("growth", rate)
    add_equation(sector.equations, flow, growth * stock)
    add_equation(sector.equations, D(stock), flow)
    return sector


def test_a_stock_grows_as_its_equation_says():
    solution = solve(compose([exponential_growth()]), (0, 10), dt=0.0001)
    assert solution["g.stock"][-1] == pytest.approx(math.exp(1), rel=1e-3)


def test_the_solution_holds_the_auxiliary_variables_too():
    solution = solve(compose([exponential_growth()]), (0, 1), dt=0.01)
    assert solution["g.flow"][0] == pytest.approx(0.1)


def test_a_variable_can_be_reached_by_name_or_by_object():
    sector = exponential_growth()
    solution = solve(compose([sector]), (0, 1), dt=0.01)
    assert solution[sector.stock][-1] == solution["g.stock"][-1] == solution["stock"][-1]


def test_the_time_points_are_the_ones_asked_for():
    solution = solve(compose([exponential_growth()]), (1980, 2100), dt=0.015625)
    assert len(solution) == 7681
    assert solution.t[0] == 1980
    assert solution.t[-1] == pytest.approx(2100)


def test_composition_connects_a_variable_to_the_sector_that_defines_it():
    producer = ODESystem("p")
    supply = producer.variable("supply")
    add_equation(producer.equations, supply, 3.0)

    consumer = ODESystem("c")
    consumed = consumer.variable("supply")
    doubled = consumer.variable("doubled")
    add_equation(consumer.equations, doubled, 2 * consumed)

    systems = [producer, consumer]
    model = compose(systems, variable_connections(systems))
    solution = solve(model, (0, 1), dt=0.5)
    assert solution["c.doubled"][0] == 6.0


def test_a_variable_defined_twice_cannot_be_connected():
    first, second = ODESystem("a"), ODESystem("b")
    add_equation(first.equations, first.variable("x"), 1.0)
    add_equation(second.equations, second.variable("x"), 2.0)
    with pytest.raises(ValueError, match="unique names"):
        variable_connections([first, second])


def test_an_algebraic_loop_is_reported():
    sector = ODESystem("s")
    first, second = sector.variable("first"), sector.variable("second")
    add_equation(sector.equations, first, second + 1)
    add_equation(sector.equations, second, first + 1)
    with pytest.raises(ValueError, match="algebraic loop"):
        compose([sector])


def test_a_stock_without_an_initial_value_is_reported():
    sector = ODESystem("s")
    stock = sector.variable("stock")
    add_equation(sector.equations, D(stock), 1.0)
    with pytest.raises(ValueError, match="no initial value"):
        compose([sector])


def test_a_missing_definition_is_reported():
    sector = ODESystem("s")
    add_equation(sector.equations, sector.variable("x"), sector.variable("y") + 1)
    with pytest.raises(ValueError, match="defined by no equation"):
        compose([sector])


def test_the_generated_source_reads_like_the_equations():
    source, _ = compose([exponential_growth()]).source()
    assert "g__stock = y[0]" in source
    assert "g__flow = (0.1 * g__stock)" in source


def test_connection_equations_can_be_given_by_hand():
    producer = ODESystem("p")
    add_equation(producer.equations, producer.variable("supply"), 3.0)
    consumer = ODESystem("c")
    consumed = consumer.variable("supply")
    add_equation(consumer.equations, consumer.variable("used"), consumed)
    model = compose(
        [producer, consumer], [Equation(consumed, producer.supply)]
    )
    assert solve(model, (0, 1), dt=1)["c.used"][0] == 3.0
