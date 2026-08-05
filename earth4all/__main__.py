"""Run a scenario from the command line.

    python -m earth4all tltl --plot baserun.png --csv baserun.csv
"""

import argparse

from .plots import fig_baserun_comparison, fig_baserun_gl, fig_baserun_tltl
from .solutions import run_gl_solution, run_tltl_solution

SCENARIOS = {
    "tltl": (run_tltl_solution, fig_baserun_tltl, "Too Little Too Late"),
    "gl": (run_gl_solution, fig_baserun_gl, "Giant Leap"),
}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="earth4all", description=__doc__)
    parser.add_argument(
        "scenario", choices=[*SCENARIOS, "both"], default="tltl", nargs="?",
        help="the scenario to run; 'both' compares the two",
    )
    parser.add_argument("--plot", metavar="FILE", help="write the base run figure to FILE")
    parser.add_argument("--csv", metavar="FILE", help="write every variable to FILE")
    parser.add_argument(
        "--show", action="append", default=[], metavar="VARIABLE",
        help="print the 2100 value of a variable, for instance pop.POP",
    )
    args = parser.parse_args(argv)

    if args.scenario == "both":
        solution = run_tltl_solution()
        figure = fig_baserun_comparison
        title = "Too Little Too Late against Giant Leap"
    else:
        solve_it, figure, title = SCENARIOS[args.scenario]
        solution = solve_it()

    print(f"{title}: {solution}")
    for name in args.show or ["pop.POP", "pop.GDPP", "wel.AWBI", "cli.OW", "dem.INEQ"]:
        print(f"  {name} in {solution.t[-1]:.0f}: {solution[name][-1]:.4g}")

    if args.csv:
        solution.dataframe().to_csv(args.csv)
        print(f"wrote {args.csv}")
    if args.plot:
        figure().savefig(args.plot, dpi=120)
        print(f"wrote {args.plot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
