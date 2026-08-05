"""Render the figures of the README and the per-sector gallery.

    python scripts/render_figures.py              # everything
    python scripts/render_figures.py --scenarios  # the two base runs only
    python scripts/render_figures.py --sectors    # the twelve sectors only

Run it again after a change to the model or to the plots, and commit whatever
moved. The gallery page, `figures/README.md`, is written from the same list, so
it never falls out of step with the images.
"""

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # the figures are written, never shown
sys.path.insert(0, str(Path(__file__).parent.parent))  # run without installing

import earth4all  # noqa: E402  (the two lines above come first)

SCENARIO_FIGURES = {
    "baserun-tltl.png": (earth4all.fig_baserun_tltl, "Too Little Too Late base run"),
    "baserun-gl.png": (earth4all.fig_baserun_gl, "Giant Leap base run"),
    "scenario-comparison.png": (earth4all.fig_baserun_comparison, "The two compared"),
}

# What each sector figure shows, in the order the sectors are usually listed.
SECTOR_FIGURES = [
    ("climate", "Climate", earth4all.climate.fig_cli,
     "Warming, the gases behind it, and the ice left."),
    ("demand", "Demand", earth4all.demand.fig_dem,
     "How output is split between consumption, savings and the state, "
     "and how much debt households and governments carry."),
    ("energy", "Energy", earth4all.energy.fig_en,
     "The cost of the energy the world uses."),
    ("finance", "Finance", earth4all.finance.fig_fin,
     "The signal rate the central bank sets and the borrowing costs that "
     "follow it, over the two decades around 2020."),
    ("foodland", "Food and land", earth4all.foodland.fig_fl,
     "Cropland, what is grown on it, the fertiliser it takes, and the land "
     "left to regenerate."),
    ("inventory", "Inventory", earth4all.inventory.fig_inv,
     "Stocks against desired stocks, and the inflation that comes of the gap."),
    ("labourmarket", "Labour market", earth4all.labourmarket.fig_lab,
     "The size of the workforce, its share of output, and unemployment."),
    ("other", "Other", earth4all.other.fig_oth,
     "The cost of the turnarounds, the people below the poverty line, and the "
     "growth of output per person."),
    ("output", "Output", earth4all.output.fig_out,
     "The capital stock in private and public hands, and the output it yields."),
    ("population", "Population", earth4all.population.fig_pop,
     "Births, life expectancy past sixty, and the population that results."),
    ("public", "Public", earth4all.public.fig_pub,
     "Public spending, the tax that funds it, and the productivity it buys."),
    ("wellbeing", "Wellbeing", earth4all.wellbeing.fig_wb,
     "The average wellbeing index, which the whole model is built to explain."),
]

GALLERY_HEADER = """# Figures

Drawn by `python scripts/render_figures.py`, from the model in this repository.

## The two scenarios

| Too Little Too Late | Giant Leap |
| --- | --- |
| ![Too Little Too Late base run](baserun-tltl.png) | ![Giant Leap base run](baserun-gl.png) |

The same six variables with the scenarios drawn on top of each other:

![The two scenarios compared](scenario-comparison.png)

## The twelve sectors

Each sector is run on its own here, with the variables the other eleven would
have given it read from tabulated runs of the whole model, which is what
`<sector>.<name>_run()` composes. Every figure is the one its `fig_*` function
draws, with the vertical axes shown.
"""


def render_scenarios(output, dpi):
    for name, (draw, _) in SCENARIO_FIGURES.items():
        draw().savefig(output / name, dpi=dpi)
        print(f"wrote {output / name}")


def render_sectors(output, dpi):
    (output / "sectors").mkdir(parents=True, exist_ok=True)
    for directory, _, draw, _ in SECTOR_FIGURES:
        path = output / "sectors" / f"{directory}.png"
        draw(showaxis=True).savefig(path, dpi=dpi)
        print(f"wrote {path}")


def write_gallery(output):
    lines = [GALLERY_HEADER]
    for directory, title, _, description in SECTOR_FIGURES:
        lines.append(f"### {title}\n")
        lines.append(f"{description}\n")
        lines.append(f"![{title} sector](sectors/{directory}.png)\n")
    (output / "README.md").write_text("\n".join(lines))
    print(f"wrote {output / 'README.md'}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).parent.parent / "figures"
    )
    parser.add_argument("--dpi", type=int, default=110)
    parser.add_argument("--scenarios", action="store_true", help="the base runs only")
    parser.add_argument("--sectors", action="store_true", help="the sector figures only")
    args = parser.parse_args()

    everything = not (args.scenarios or args.sectors)
    args.output.mkdir(parents=True, exist_ok=True)
    if everything or args.scenarios:
        render_scenarios(args.output, args.dpi)
    if everything or args.sectors:
        render_sectors(args.output, args.dpi)
    if everything:
        write_gallery(args.output)


if __name__ == "__main__":
    main()
