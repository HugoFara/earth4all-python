"""The model itself: its structure, its scenarios, and its agreement with Vensim.

The comparison with Vensim needs the `VensimOutput` folder of the Julia
repository; the tests that use it are skipped when it is not next to this one.
"""

from pathlib import Path

import pytest

import earth4all
from earth4all.scenarios import run_gl, run_tltl, sector_systems
from earth4all.system import solve
from earth4all.validation import all_mre

VENSIM_OUTPUT = Path(__file__).parent.parent.parent / "Earth4All.jl" / "VensimOutput"
needs_vensim = pytest.mark.skipif(
    not VENSIM_OUTPUT.is_dir(), reason="the Vensim reference runs are not available"
)


@pytest.fixture(scope="module")
def tltl():
    model = run_tltl()
    return model, solve(model, (1980, 2100), dt=0.015625)


@pytest.fixture(scope="module")
def gl():
    model = run_gl()
    return model, solve(model, (1980, 2100), dt=0.015625)


def test_every_sector_is_composed():
    assert len(sector_systems()) == 12
    assert len(earth4all.sector_names()) == 12


def test_the_model_has_the_stocks_and_variables_of_the_twelve_sectors(tltl):
    model, _ = tltl
    assert len(model.stocks) == 105
    assert len(model.variables) == 638


def test_the_scenarios_differ_only_by_their_parameters():
    tltl_model, gl_model = run_tltl(), run_gl()
    assert len(tltl_model.equations) == len(gl_model.equations)
    assert [v.full_name for v in tltl_model.variables] == \
           [v.full_name for v in gl_model.variables]


def test_too_little_too_late_gets_hotter_than_the_giant_leap(tltl, gl):
    _, tltl_solution = tltl
    _, gl_solution = gl
    assert tltl_solution["cli.OW"][-1] > gl_solution["cli.OW"][-1]


def test_the_giant_leap_lives_better(tltl, gl):
    _, tltl_solution = tltl
    _, gl_solution = gl
    assert gl_solution["wel.AWBI"][-1] > tltl_solution["wel.AWBI"][-1]
    assert gl_solution["dem.INEQ"][-1] < tltl_solution["dem.INEQ"][-1]


def test_population_peaks_within_the_century(tltl):
    _, solution = tltl
    population = solution["pop.POP"]
    assert 8000 < population.max() < 10000
    assert population.argmax() < len(population) - 1


@needs_vensim
@pytest.mark.parametrize(
    "scenario, sector, tolerance",
    [
        ("TLTL", "climate", 0.01), ("TLTL", "finance", 0.01),
        ("TLTL", "foodland", 0.05), ("TLTL", "inventory", 0.05),
        ("TLTL", "output", 0.05), ("TLTL", "population", 0.05),
        ("TLTL", "public", 0.05), ("TLTL", "wellbeing", 0.05),
        ("GL", "foodland", 0.05), ("GL", "population", 0.05),
        ("GL", "wellbeing", 0.05),
    ],
)
def test_a_sector_follows_the_vensim_run(scenario, sector, tolerance, tltl, gl):
    model, solution = tltl if scenario == "TLTL" else gl
    _, per_sector = all_mre(scenario, solution, model.systems, VENSIM_OUTPUT)
    assert per_sector[sector] < tolerance


# The largest relative error each sector reaches against the Vensim run, over
# every variable and every one of the 7681 time points. Most sectors stay within
# a percent; the loose ones are dominated by a rate that crosses zero, where the
# relative error says more about the six digits Vensim exports than about the
# model. See the "Agreement with Vensim" section of the README.
_TLTL_TOLERANCES = {
    "climate": 0.01, "demand": 10.0, "energy": 27.0, "finance": 0.01,
    "foodland": 0.02, "inventory": 0.02, "labourmarket": 4.0, "other": 0.25,
    "output": 0.02, "population": 0.02, "public": 0.03, "wellbeing": 0.03,
}


@needs_vensim
def test_the_whole_run_stays_close_to_vensim(tltl):
    """Every variable of every sector, at every one of the 7681 time points."""
    model, solution = tltl
    _, per_sector = all_mre("TLTL", solution, model.systems, VENSIM_OUTPUT)
    too_far = {
        name: error
        for name, error in per_sector.items()
        if error > _TLTL_TOLERANCES[name]
    }
    assert not too_far
