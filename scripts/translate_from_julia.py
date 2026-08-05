"""Translate the Julia sources of Earth4All.jl into the sector modules of this package.

The Julia code declares its parameters, initialisations, tables and equations in
a very regular way, so the translation is mechanical. Keeping it as a script
documents where every Python sector module comes from and makes it possible to
replay the port after a change upstream.

    python scripts/translate_from_julia.py ../Earth4All.jl

The generated modules are meant to be read and edited afterwards; the script is
a starting point, not a build step.
"""

import argparse
import re
import sys
from pathlib import Path

SECTORS = {
    "climate": ("Climate", "climate", "cli"),
    "demand": ("Demand", "demand", "dem"),
    "energy": ("Energy", "energy", "ene"),
    "finance": ("Finance", "finance", "fin"),
    "foodland": ("FoodLand", "foodland", "foo"),
    "inventory": ("Inventory", "inventory", "inv"),
    "labourmarket": ("LabourMarket", "labour_market", "lab"),
    "other": ("Other", "other", "oth"),
    "output": ("Output", "output", "out"),
    "population": ("Population", "population", "pop"),
    "public": ("Public", "public", "pub"),
    "wellbeing": ("Wellbeing", "wellbeing", "wel"),
}

# Every name the generated equations may use, with where it comes from.
IMPORTABLE = {
    "add_equation": "..functions",
    "delay_n": "..functions",
    "interpolate": "..functions",
    "pulse": "..functions",
    "ramp": "..functions",
    "smooth": "..functions",
    "step": "..functions",
    "clip": "..functions",
    "withlookup": "..functions",
    "D": "..symbolics",
    "exp": "..symbolics",
    "ifelse": "..symbolics",
    "log": "..symbolics",
    "max": "..symbolics",
    "min": "..symbolics",
    "sqrt": "..symbolics",
    "t": "..symbolics",
    "ODESystem": "..system",
}


def translate_expression(text):
    """Rewrite a Julia expression into the equivalent Python one."""
    text = text.replace("IfElse.ifelse", "ifelse")
    text = text.replace("WorldDynamics.interpolate", "interpolate")
    text = text.replace("≥", ">=").replace("≤", "<=").replace("≠", "!=")
    text = re.sub(r"\[:(\w+)\]", r'["\1"]', text)
    text = re.sub(r"\bInt64\(", "int(", text)
    text = text.replace("^", "**")
    # Julia indexes from one, Python from zero.
    text = re.sub(r"\[ORDER\]", "[ORDER - 1]", text)
    return text


def parse_dictionary(source, name):
    """Read a `name = Dict{...}(:KEY => value, ...)` literal out of `source`."""
    match = re.search(rf"^{name} = Dict\{{[^(]*\}}\(", source, re.MULTILINE)
    if match is None:
        return None
    start = match.end()
    depth = 1
    index = start
    while depth:
        if source[index] == "(":
            depth += 1
        elif source[index] == ")":
            depth -= 1
        index += 1
    body = source[start:index - 1]
    entries, comments = [], []
    for entry, value in re.findall(r":(\w+) =>\s*(\([^)]*\)|[^,\n]+)", body):
        line_comment = ""
        comment = re.search(rf":{entry} =>[^\n]*?#\s*(.*)$", body, re.MULTILINE)
        if comment:
            line_comment = comment.group(1).strip().rstrip(",")
        value = value.strip().rstrip(",").strip()
        if value.startswith("("):
            numbers = [v.strip() for v in value[1:-1].split(",") if v.strip()]
            value = "(" + ", ".join(numbers) + ("," if len(numbers) == 1 else "") + ")"
        entries.append((entry, value, line_comment))
        comments.append(line_comment)
    return entries


def render_dictionary(entries, name, wrap_tuples=False):
    lines = [f"{name} = {{"]
    for key, value, comment in entries:
        if wrap_tuples and value.startswith("(") and len(value) > 70:
            numbers = value[1:-1].split(", ")
            lines.append(f'    "{key}": (')
            for number in numbers:
                lines.append(f"        {number},")
            lines.append("    ),")
        else:
            suffix = f"  # {comment}" if comment else ""
            lines.append(f'    "{key}": {value},{suffix}')
    lines.append("}")
    return "\n".join(lines)


def translate_values_file(path, title, dict_names):
    source = path.read_text()
    blocks = [f'"""{title}"""', ""]
    for name in dict_names:
        entries = parse_dictionary(source, name)
        if entries is None:
            continue
        blocks.append(render_dictionary(entries, name, wrap_tuples=True))
        blocks.append("")
    return "\n".join(blocks)


DESCRIPTION = re.compile(r'\s*\[description = "(.*)"\]\s*$')
PARAMETER = re.compile(r"@parameters (\w+) = (.+)$")
ARRAY_VARIABLE = re.compile(r"@variables \((\w+)\(t\)\)\[1:ORDER\] = fill\((.+), ORDER\)$")
VARIABLE = re.compile(r"@variables (\w+)\(t\)(?: = (.+))?$")


def translate_declaration(line):
    """Rewrite a `@parameters` or `@variables` declaration, or return None."""
    description = ""
    match = DESCRIPTION.search(line)
    if match:
        description, line = match[1], line[:match.start()].strip()
    described = f', "{description}"' if description else ""

    match = PARAMETER.match(line)
    if match:
        value = translate_expression(match[2])
        return f'{match[1]} = sys.parameter("{match[1]}", {value}{described})'

    match = ARRAY_VARIABLE.match(line)
    if match:
        initial = translate_expression(match[2])
        return (
            f'{match[1]} = sys.variable_array("{match[1]}", ORDER, '
            f"{initial}{described})"
        )

    match = VARIABLE.match(line)
    if match:
        if match[2] is None:
            described = f'description="{description}"' if description else ""
            return f'{match[1]} = sys.variable("{match[1]}"' \
                   + (f", {described})" if described else ")")
        initial = translate_expression(match[2])
        return f'{match[1]} = sys.variable("{match[1]}", {initial}{described})'

    return None

EQUATION = re.compile(r"add_equation!\(eqs, (.+?) ~ (.+)\)\s*$")
SMOOTH = re.compile(r"smooth!\(eqs, (.+)\)\s*$")
DELAY = re.compile(r"delay_n!\(eqs, (.+)\)\s*$")
FUNCTION = re.compile(r"function (\w+)\(; name, params=_params.*\)")
ORDER_LINE = re.compile(r"ORDER = Int64\(params\[:ORDER\]\)")


def split_comment(line):
    """Split a Julia line into its code and its trailing comment."""
    in_string = False
    for index, character in enumerate(line):
        if character == '"':
            in_string = not in_string
        elif character == "#" and not in_string:
            return line[:index].strip(), line[index + 1:].strip()
    return line, ""


def translate_subsystems(path, sector, module_docstring):
    """Translate one `<sector>/subsystems.jl` file."""
    default_name = SECTORS[sector][2]
    body, used = [], set()
    for raw in path.read_text().splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped == "end" or stripped.startswith("include(") \
                or stripped.startswith("@register_symbolic") \
                or stripped.startswith("@variables t") \
                or stripped.startswith("D = Differential"):
            continue

        stripped, trailing_comment = split_comment(stripped)
        if not stripped:
            body.append("    # " + trailing_comment)
            continue

        match = FUNCTION.match(stripped)
        if match:
            if body:
                body.append("")
                body.append("")
            body.append(
                f'def {match[1]}(name="{default_name}", params=None, inits=None,'
                f" tables=None, ranges=None):"
            )
            body.append(f'    """{docstring_for(match[1], sector)}"""')
            body.append("    params = _params if params is None else params")
            body.append("    inits = _inits if inits is None else inits")
            body.append("    tables = _tables if tables is None else tables")
            body.append("    ranges = _ranges if ranges is None else ranges")
            body.append("    sys = ODESystem(name)")
            body.append("    eqs = sys.equations")
            body.append("")
            used.add("ODESystem")
            continue

        if stripped.startswith("eqs = []"):
            continue
        if stripped.startswith("return ODESystem"):
            body.append("    return sys")
            continue
        if ORDER_LINE.match(stripped):
            body.append('    ORDER = int(params["ORDER"])')
            continue

        translated = translate_declaration(stripped)
        if translated is None:
            match = EQUATION.match(stripped)
            if match:
                translated = (
                    f"add_equation(eqs, {translate_expression(match[1])}, "
                    f"{translate_expression(match[2])})"
                )
            elif SMOOTH.match(stripped):
                translated = f"smooth(eqs, {translate_expression(SMOOTH.match(stripped)[1])})"
            elif DELAY.match(stripped):
                translated = f"delay_n(eqs, {translate_expression(DELAY.match(stripped)[1])})"
            else:
                raise SystemExit(f"{path}: cannot translate {stripped!r}")

        for name in IMPORTABLE:
            if re.search(rf"\b{name}\b", translated):
                used.add(name)
        if trailing_comment:
            translated += f"  # {trailing_comment}"
        body.append("    " + translated)

    imports = {}
    for name in sorted(used):
        imports.setdefault(IMPORTABLE[name], []).append(name)
    header = [f'"""{module_docstring}"""', ""]
    for module in ["..functions", "..symbolics", "..system"]:
        if module in imports:
            header.append(f"from {module} import {', '.join(imports[module])}")
    header.append("from .initialisations import _inits")
    header.append("from .parameters import _params")
    header.append("from .tables import _ranges, _tables")
    header.append("")
    header.append("")
    return "\n".join(header + body) + "\n"


def docstring_for(function_name, sector):
    pretty = SECTORS[sector][0]
    if function_name.endswith("_full_support"):
        return (
            f"The {pretty} sector variables that other sectors provide, read from "
            "tabulated runs of the whole model instead."
        )
    if function_name.endswith("_partial_support"):
        return (
            f"The {pretty} sector variables of the sectors that are not part of a "
            "partial run, read from tabulated runs of the whole model."
        )
    return f"The equations of the {pretty} sector."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("julia_root", type=Path, help="the root of the Earth4All.jl clone")
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).parent.parent / "earth4all"
    )
    args = parser.parse_args()

    source_root = args.julia_root / "src"
    for sector, (pretty, _, _) in SECTORS.items():
        target = args.output / sector
        target.mkdir(parents=True, exist_ok=True)
        (target / "parameters.py").write_text(
            translate_values_file(
                source_root / sector / "parameters.jl",
                f"Parameters of the {pretty} sector.",
                ["_params"],
            )
            + PARAMETERS_ACCESSOR
        )
        (target / "initialisations.py").write_text(
            translate_values_file(
                source_root / sector / "initialisations.jl",
                f"Initial values of the stocks of the {pretty} sector.",
                ["_inits"],
            )
            + INITIALISATIONS_ACCESSOR
        )
        (target / "tables.py").write_text(
            translate_values_file(
                source_root / sector / "tables.jl",
                f"Tabulated functions of the {pretty} sector.",
                ["_tables", "_ranges"],
            )
            + TABLES_ACCESSORS
        )
        (target / "subsystems.py").write_text(
            translate_subsystems(
                source_root / sector / "subsystems.jl",
                sector,
                f"Equations of the {pretty} sector.\n\n"
                f"Transcribed from `src/{sector}/subsystems.jl` of Earth4All.jl, which\n"
                "transcribes the Vensim model. Each equation is kept on a single line,\n"
                "however long, so that the three can be read side by side.\n",
            )
        )
        print(f"translated {sector}", file=sys.stderr)


PARAMETERS_ACCESSOR = '''

def getparameters():
    """A copy of the parameters, to be modified and passed back to the sector."""
    return dict(_params)
'''

INITIALISATIONS_ACCESSOR = '''

def getinitialisations():
    """A copy of the initial values, to be modified and passed back to the sector."""
    return dict(_inits)
'''

TABLES_ACCESSORS = '''

def gettables():
    """A copy of the tabulated functions of the sector."""
    return dict(_tables)


def getranges():
    """A copy of the ranges over which the tabulated functions are defined."""
    return dict(_ranges)
'''

if __name__ == "__main__":
    main()
