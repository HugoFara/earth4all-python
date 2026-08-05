"""Render the figures the README shows.

    python scripts/render_figures.py

Run it again after a change to the model or to the plots, and commit whatever
moved.
"""

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # the figures are written, never shown
sys.path.insert(0, str(Path(__file__).parent.parent))  # run without installing

from earth4all import (  # noqa: E402  (the two lines above come first)
    fig_baserun_comparison, fig_baserun_gl, fig_baserun_tltl,
)

FIGURES = {
    "baserun-tltl.png": fig_baserun_tltl,
    "baserun-gl.png": fig_baserun_gl,
    "scenario-comparison.png": fig_baserun_comparison,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).parent.parent / "figures"
    )
    parser.add_argument("--dpi", type=int, default=110)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    for name, draw in FIGURES.items():
        draw().savefig(args.output / name, dpi=args.dpi)
        print(f"wrote {args.output / name}")


if __name__ == "__main__":
    main()
