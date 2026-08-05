"""Systems of equations, their composition, and their numerical solution.

This module plays the role that ModelingToolkit and WorldDynamics play in the
Julia code: a sector declares its variables and equations in an `ODESystem`,
`compose` puts sectors together, and `solve` integrates the result.

Composition works exactly as in Julia: a variable that a sector uses without
defining it is connected to the variable of the same name in the sector that
does define it, which assumes that no two distinct variables share a name.
"""

import numpy as np

from .symbolics import Equation, Parameter, Variable

__all__ = ["ODESystem", "Model", "compose", "variable_connections", "solve", "Solution"]


class ODESystem:
    """The variables, parameters and equations of one sector.

    A sector function creates a system, declares what it needs, fills
    `system.equations`, and returns the system.
    """

    def __init__(self, name):
        self.name = name
        self.equations = []
        self.declared_variables = []
        self.declared_parameters = []

    def variable(self, name, init=None, description=""):
        """Declare a variable of this system, with an optional initial value."""
        var = Variable(name, system=self.name, init=init, description=description)
        self.declared_variables.append(var)
        return var

    def variable_array(self, name, count, init=None, description=""):
        """Declare `count` variables, named `name_1` to `name_<count>`.

        The Julia code writes these as `(LV_DEATHS(t))[1:ORDER]`; here they come
        back as a plain Python list, so the last one is `rt[order - 1]`.
        """
        return [
            self.variable(f"{name}_{i + 1}", init=init, description=description)
            for i in range(count)
        ]

    def parameter(self, name, value, description=""):
        """Declare a parameter of this system."""
        par = Parameter(name, value, system=self.name, description=description)
        self.declared_parameters.append(par)
        return par

    def __getattr__(self, name):
        """Give access to a declared variable or parameter, as `cli.OW` does in Julia."""
        for declared in self.__dict__.get("declared_variables", ()):
            if declared.name == name:
                return declared
        for declared in self.__dict__.get("declared_parameters", ()):
            if declared.name == name:
                return declared
        raise AttributeError(
            f"the system {self.__dict__.get('name')!r} declares nothing named {name!r}"
        )

    def defined_variables(self):
        """The variables this system gives an equation for."""
        return {eq.variable for eq in self.equations}

    def used_variables(self):
        """The variables appearing on the right-hand side of this system's equations."""
        used = set()
        for eq in self.equations:
            used |= eq.rhs.dependencies()
        return used

    def input_variables(self):
        """The variables this system reads but does not define."""
        return self.used_variables() - self.defined_variables()

    def __repr__(self):
        return f"ODESystem({self.name}, {len(self.equations)} equations)"


def variable_connections(systems):
    """Return the equations connecting the variables shared by `systems`.

    Every variable that a system uses without defining is matched, by name, with
    the variable of the system that defines it.
    """
    providers = {}
    for system in systems:
        for var in system.defined_variables():
            if var.name in providers:
                other = providers[var.name]
                raise ValueError(
                    f"the variable {var.name} is defined both in {other.system} "
                    f"and in {var.system}; composition needs unique names"
                )
            providers[var.name] = var

    connections = []
    for system in systems:
        for var in sorted(system.input_variables(), key=lambda v: v.name):
            provider = providers.get(var.name)
            if provider is None:
                raise ValueError(
                    f"the variable {var.full_name} is used but defined by no system"
                )
            connections.append(Equation(var, provider))
    return connections


class _CodegenContext:
    """Collects the literals and functions the generated model code refers to."""

    def __init__(self):
        self.constants = []
        self.functions = {}

    def constant(self, value):
        self.constants.append(value)
        return f"_k{len(self.constants) - 1}"

    def function(self, name):
        from .symbolics import _FUNCTIONS

        if name not in _FUNCTIONS:
            raise KeyError(f"unknown function {name!r} in an equation")
        self.functions[name] = _FUNCTIONS[name]
        return f"_f_{name}"


def _tuple_source(names):
    """The source of a tuple of the given names, empty tuple included."""
    names = list(names)
    return "(" + ", ".join(names) + (",)" if names else ")")


class Model:
    """A composed set of equations, ready to be solved.

    Its equations are split into the stocks, integrated over time, and the
    auxiliary variables, computed from the stocks and from time at every step.
    """

    def __init__(self, equations, systems=()):
        self.equations = list(equations)
        self.systems = list(systems)
        self._sort_equations()
        self._compiled = None

    def _sort_equations(self):
        stock_equations, aux_equations = [], []
        for eq in self.equations:
            (stock_equations if eq.is_derivative else aux_equations).append(eq)

        by_variable = {}
        for eq in aux_equations:
            if eq.variable in by_variable:
                raise ValueError(f"the variable {eq.variable.full_name} has two equations")
            by_variable[eq.variable] = eq

        self.stocks = [eq.variable for eq in stock_equations]
        stock_set = set(self.stocks)
        for var in self.stocks:
            if var in by_variable:
                raise ValueError(
                    f"{var.full_name} is both a stock and an auxiliary variable"
                )
            if var.init is None:
                raise ValueError(f"the stock {var.full_name} has no initial value")

        # Depth-first topological sort, following the order in which the sectors
        # wrote their equations so that the generated code reads like the model.
        ordered, state = [], {}
        for equation in aux_equations:
            self._visit(equation, by_variable, stock_set, state, ordered, [])

        self.stock_equations = stock_equations
        self.aux_equations = ordered
        self.auxiliaries = [eq.variable for eq in ordered]
        self.variables = self.stocks + self.auxiliaries
        self._index = {var: i for i, var in enumerate(self.variables)}

    def _visit(self, equation, by_variable, stock_set, state, ordered, path):
        mark = state.get(equation.variable)
        if mark == "done":
            return
        if mark == "visiting":
            cycle = " -> ".join(v.full_name for v in path + [equation.variable])
            raise ValueError(f"the equations contain an algebraic loop: {cycle}")
        state[equation.variable] = "visiting"
        for dependency in sorted(equation.rhs.dependencies(), key=lambda v: v.full_name):
            if dependency in stock_set:
                continue
            producer = by_variable.get(dependency)
            if producer is None:
                raise ValueError(
                    f"{dependency.full_name}, used by {equation.variable.full_name}, "
                    "is defined by no equation"
                )
            self._visit(producer, by_variable, stock_set, state, ordered,
                        path + [equation.variable])
        state[equation.variable] = "done"
        ordered.append(equation)

    def source(self):
        """The Python source of the function evaluating the whole model.

        The generated function takes the time, the list of the current values of
        the stocks, and two lists it fills with the derivatives of the stocks and
        with the values of the auxiliary variables. Lists of plain floats, rather
        than arrays, keep the arithmetic on Python floats, which is what makes
        the seven thousand steps of a run bearable.
        """
        context = _CodegenContext()
        lines = ["def _evaluate(t, y, dy, aux):"]
        for i, var in enumerate(self.stocks):
            lines.append(f"    {var.code_name} = y[{i}]")
        for eq in self.aux_equations:
            lines.append(f"    {eq.variable.code_name} = {eq.rhs.emit(context)}")
        for i, eq in enumerate(self.stock_equations):
            lines.append(f"    _d{i} = {eq.rhs.emit(context)}")
        lines.append(
            "    dy[:] = "
            + _tuple_source(f"_d{i}" for i in range(len(self.stock_equations)))
        )
        lines.append(
            "    aux[:] = "
            + _tuple_source(var.code_name for var in self.auxiliaries)
        )
        return "\n".join(lines), context

    def compile(self):
        """Compile the model into a function `(t, y, dy, aux)`."""
        if self._compiled is None:
            source, context = self.source()
            namespace = {f"_f_{n}": f for n, f in context.functions.items()}
            namespace.update({f"_k{i}": k for i, k in enumerate(context.constants)})
            exec(compile(source, "<earth4all model>", "exec"), namespace)
            self._compiled = namespace["_evaluate"]
        return self._compiled

    def initial_state(self):
        return [float(var.init) for var in self.stocks]

    def variable(self, name):
        """Look a variable up by `name` or by `sector.name`."""
        matches = [
            var for var in self.variables
            if var.full_name == name or var.name == name
        ]
        if not matches:
            raise KeyError(f"no variable named {name!r} in the model")
        if len(matches) > 1:
            names = ", ".join(v.full_name for v in matches)
            raise KeyError(f"{name!r} is ambiguous, it could be any of {names}")
        return matches[0]

    def index(self, var):
        if isinstance(var, str):
            var = self.variable(var)
        return self._index[var]

    def __repr__(self):
        return (
            f"Model({len(self.stocks)} stocks, {len(self.auxiliaries)} auxiliary "
            f"variables)"
        )


def compose(systems, connection_eqs=()):
    """Put `systems` together into a single model, adding `connection_eqs`."""
    equations = []
    for system in systems:
        equations.extend(system.equations)
    equations.extend(connection_eqs)
    return Model(equations, systems)


class Solution:
    """The trajectories of every variable of a model.

    Indexing accepts a variable, a `"sector.name"` string, or a bare variable
    name when it is unambiguous: `solution["cli.OW"]` and `solution[cli.OW]`
    both give the observed warming over time.
    """

    def __init__(self, model, t, values):
        self.model = model
        self.t = t
        self.values = values

    def __getitem__(self, var):
        return self.values[:, self.model.index(var)]

    def __contains__(self, var):
        try:
            self.model.index(var)
        except KeyError:
            return False
        return True

    def __len__(self):
        return len(self.t)

    def dataframe(self):
        """The whole solution as a pandas DataFrame indexed by time."""
        import pandas as pd

        return pd.DataFrame(
            self.values,
            index=pd.Index(self.t, name="t"),
            columns=[var.full_name for var in self.model.variables],
        )

    def __repr__(self):
        return (
            f"Solution({len(self.t)} time points from {self.t[0]:g} to "
            f"{self.t[-1]:g}, {len(self.model.variables)} variables)"
        )


def solve(model, tspan=(1980, 2100), dt=1 / 64, method="euler"):
    """Integrate `model` over `tspan`.

    The default is the explicit Euler method with the time step of the Vensim
    model, which is what the Julia code uses; any other value of `method` is
    passed to `scipy.integrate.solve_ivp`, which then samples the solution at
    the same time points.
    """
    evaluate = model.compile()
    n_stocks = len(model.stocks)
    n_aux = len(model.auxiliaries)
    start, stop = float(tspan[0]), float(tspan[1])
    n_steps = int(round((stop - start) / dt))
    times = start + dt * np.arange(n_steps + 1)

    values = np.empty((n_steps + 1, n_stocks + n_aux), dtype=float)
    dy = [0.0] * n_stocks
    aux = [0.0] * n_aux

    if method == "euler":
        y = model.initial_state()
        for step in range(n_steps + 1):
            time = start + dt * step
            evaluate(time, y, dy, aux)
            values[step, :n_stocks] = y
            values[step, n_stocks:] = aux
            if step < n_steps:
                y = [value + dt * slope for value, slope in zip(y, dy)]
    else:
        from scipy.integrate import solve_ivp

        def rhs(time, state):
            evaluate(time, state.tolist(), dy, aux)
            return dy

        result = solve_ivp(
            rhs, (start, stop), model.initial_state(), t_eval=times, method=method,
        )
        if not result.success:
            raise RuntimeError(f"the integration failed: {result.message}")
        for step, time in enumerate(times):
            state = result.y[:, step].tolist()
            evaluate(time, state, dy, aux)
            values[step, :n_stocks] = state
            values[step, n_stocks:] = aux

    return Solution(model, times, values)
