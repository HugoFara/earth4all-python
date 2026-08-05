"""Solutions of the scenarios of the whole model.

The model is integrated the way the Vensim model is: explicit Euler over
1980–2100 with a step of 1/64 of a year, which gives 7681 time points.
"""

from .scenarios import run_e4a, run_gl, run_tltl
from .system import solve

__all__ = ["run_tltl_solution", "run_gl_solution", "run_e4a_solution", "TIME_STEP"]

TIME_STEP = 0.015625
TIME_SPAN = (1980, 2100)


def run_tltl_solution(**kwargs):
    """Solve the *Too Little Too Late* scenario."""
    return solve(run_tltl(**kwargs), TIME_SPAN, dt=TIME_STEP)


def run_gl_solution(**kwargs):
    """Solve the *Giant Leap* scenario."""
    return solve(run_gl(**kwargs), TIME_SPAN, dt=TIME_STEP)


def run_e4a_solution(**kwargs):
    """Solve the model with the parameters and initial values given."""
    return solve(run_e4a(**kwargs), TIME_SPAN, dt=TIME_STEP)
