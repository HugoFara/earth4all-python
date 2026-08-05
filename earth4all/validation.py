"""Comparing a solution with the reference values exported from Vensim.

The `VensimOutput` folder of Earth4All.jl holds, for each scenario and each
sector, the trajectory Vensim computes for every variable of that sector. A
variable is matched with its reference series by its description, which is the
name it carries in Vensim.
"""

from pathlib import Path

import numpy as np

__all__ = [
    "read_vensim_dataset", "compare", "sector_errors", "all_mre",
    "max_relative_error",
]

_SKIPPED_PREFIXES = ("LV functions", "RT functions")


def read_vensim_dataset(path, to_be_removed):
    """Read a dataset exported from Vensim into a dictionary of series.

    `to_be_removed` is the run name Vensim appends to every variable name, for
    instance `" : E4A-220501 TLTL"`.
    """
    dataset = {}
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        fields = line.split("\t")
        name = fields[0].replace('"', "")
        name = name.replace(to_be_removed, "").replace(" (Year)", "")
        name = name.replace("$", "dollar")
        dataset[name.lower()] = np.array([float(v) for v in fields[1:]])
    return dataset


def compare(a, b, epsilon):
    """The largest relative difference between the series `a` and `b`.

    With `epsilon` negative the symmetric relative difference is used, which
    stays meaningful when both series cross zero; otherwise `epsilon` is added
    to the denominator to keep small values from blowing the error up.

    Returns the error, the two values it was reached at, and their index.
    """
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if epsilon >= 0:
        errors = np.abs(a - b) / (np.abs(b) + epsilon)
    else:
        denominator = np.abs(a) + np.abs(b)
        errors = np.divide(
            2 * np.abs(a - b), denominator,
            out=np.zeros_like(denominator), where=denominator != 0,
        )
    index = int(np.argmax(errors))
    return float(errors[index]), float(a[index]), float(b[index]), index


def _comparable_variables(system):
    """The variables of `system` that Vensim also reports."""
    for variable in system.declared_variables:
        description = variable.description
        if not description or description == "Time instants":
            continue
        if description.startswith(_SKIPPED_PREFIXES):
            continue
        yield variable


def sector_errors(solution, system, dataset, epsilon=1, n_points=None):
    """The relative error of every variable of `system`, largest first."""
    n_points = len(solution.t) if n_points is None else n_points
    errors = {}
    for variable in _comparable_variables(system):
        reference = dataset.get(variable.description.lower())
        if reference is None or variable not in solution:
            continue
        error, _, _, index = compare(
            solution[variable][:n_points], reference[:n_points], epsilon
        )
        errors[variable.description] = (error, index)
    return dict(sorted(errors.items(), key=lambda item: -item[1][0]))


def max_relative_error(solution, system, dataset, epsilon=1, n_points=None,
                       verbose=False):
    """The largest relative error over the variables of one sector."""
    errors = sector_errors(solution, system, dataset, epsilon, n_points)
    if verbose:
        for description, (error, _) in errors.items():
            print(f"{description}\t{error}")
    return max((error for error, _ in errors.values()), default=0.0)


# The name of the file Vensim exports for each sector system.
_SECTOR_FILES = {
    "cli": "climate", "dem": "demand", "ene": "energy", "fin": "finance",
    "foo": "foodland", "inv": "inventory", "lab": "labourmarket", "oth": "other",
    "out": "output", "pop": "population", "pub": "public", "wel": "wellbeing",
}


def all_mre(scenario, solution, systems, vensim_root, epsilon=1, verbose=False):
    """Compare a whole solution with the Vensim run of the same scenario.

    `scenario` is the name Vensim used, `"TLTL"` or `"GL"`, and `systems` the
    sector systems the solution was computed from. Returns the largest relative
    error and the largest error of each sector.
    """
    vensim_root = Path(vensim_root)
    suffix = f" : E4A-220501 {scenario}"
    per_sector = {}
    for system in systems:
        name = _SECTOR_FILES[system.name]
        dataset = read_vensim_dataset(
            vensim_root / scenario.lower() / f"{name}.txt", suffix
        )
        errors = sector_errors(solution, system, dataset, epsilon)
        per_sector[name] = max((error for error, _ in errors.values()), default=0.0)
        if verbose:
            print(f"==== {name.upper()} ==== {per_sector[name]}")
            for description, (variable_error, index) in errors.items():
                print(f"    {description}\t{variable_error}\tat t={solution.t[index]}")
    return max(per_sector.values(), default=0.0), per_sector
