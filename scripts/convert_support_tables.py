"""Convert `src/tables.jl` of Earth4All.jl into the data file of this package.

`src/tables.jl` holds one tabulated trajectory per variable, taken from a run of
the whole model, which is what lets a single sector be run on its own. There are
about fifty of them, each with the 7681 values of a run, so they are stored as a
compressed array file rather than as Python source.

    python scripts/convert_support_tables.py ../Earth4All.jl
"""

import argparse
import re
from pathlib import Path

import numpy as np

ENTRY = re.compile(r":(\w+) => \(([^)]*)\)", re.DOTALL)


def parse_dictionary(source, name):
    """Read the `name = Dict{...}(...)` literal out of `source`."""
    start = re.search(rf"^{name} = Dict\{{[^(]*\}}\(", source, re.MULTILINE).end()
    depth, index = 1, start
    while depth:
        depth += {"(": 1, ")": -1}.get(source[index], 0)
        index += 1
    return source[start:index - 1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("julia_root", type=Path, help="the root of the Earth4All.jl clone")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "earth4all" / "data" / "support_tables.npz",
    )
    args = parser.parse_args()

    source = (args.julia_root / "src" / "tables.jl").read_text()
    # Some tables are kept in the Julia file only as comments.
    source = re.sub(r"^\s*#.*$", "", source, flags=re.MULTILINE)
    arrays = {}

    for key, body in ENTRY.findall(parse_dictionary(source, "_tables")):
        values = [float(v) for v in body.replace("\n", " ").split(",") if v.strip()]
        if key in arrays:
            # The Julia dictionary literal keeps the last of two equal keys.
            print(f"note: {key} appears twice, keeping the last table")
        arrays[key] = np.array(values, dtype=float)

    for key, body in ENTRY.findall(parse_dictionary(source, "_ranges")):
        bounds = [float(v) for v in body.split(",") if v.strip()]
        arrays[f"range:{key}"] = np.array(bounds, dtype=float)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output, **arrays)
    tables = sum(1 for key in arrays if not key.startswith("range:"))
    print(f"wrote {tables} tables to {args.output}")


if __name__ == "__main__":
    main()
