"""A minimal symbolic layer, playing the role of ModelingToolkit in the Julia code.

Sector equations are written with ordinary Python operators over `Expr` nodes.
Building an equation therefore records an expression tree instead of computing a
number, which lets `earth4all.system` sort the equations by dependency and emit
one compiled Python function for the whole model.

Only what the Earth4All equations need is implemented: arithmetic, comparisons,
and the handful of functions listed in `_FUNCTIONS`.
"""

import builtins
import math

__all__ = [
    "Expr", "Const", "Variable", "Time", "t", "Parameter", "BinaryOp", "UnaryOp",
    "FunctionCall", "Derivative", "Equation", "D", "value_of", "exp", "log", "sqrt",
    "min", "max", "ifelse", "abs", "register_function",
]


def _wrap(x):
    """Turn a plain number into a `Const`, leave expressions untouched."""
    if isinstance(x, Expr):
        return x
    if isinstance(x, (int, float)):
        return Const(float(x))
    raise TypeError(f"cannot use {x!r} of type {type(x).__name__} in an equation")


class Expr:
    """Base class of every node of an equation tree."""

    __array_priority__ = 1000  # keep numpy from taking over the operators

    def __add__(self, other):
        return BinaryOp("+", self, _wrap(other))

    def __radd__(self, other):
        return BinaryOp("+", _wrap(other), self)

    def __sub__(self, other):
        return BinaryOp("-", self, _wrap(other))

    def __rsub__(self, other):
        return BinaryOp("-", _wrap(other), self)

    def __mul__(self, other):
        return BinaryOp("*", self, _wrap(other))

    def __rmul__(self, other):
        return BinaryOp("*", _wrap(other), self)

    def __truediv__(self, other):
        return BinaryOp("/", self, _wrap(other))

    def __rtruediv__(self, other):
        return BinaryOp("/", _wrap(other), self)

    def __pow__(self, other):
        return BinaryOp("**", self, _wrap(other))

    def __rpow__(self, other):
        return BinaryOp("**", _wrap(other), self)

    def __neg__(self):
        return UnaryOp("-", self)

    def __pos__(self):
        return self

    def __lt__(self, other):
        return BinaryOp("<", self, _wrap(other))

    def __le__(self, other):
        return BinaryOp("<=", self, _wrap(other))

    def __gt__(self, other):
        return BinaryOp(">", self, _wrap(other))

    def __ge__(self, other):
        return BinaryOp(">=", self, _wrap(other))

    def __bool__(self):
        raise TypeError(
            "an equation expression has no truth value; use ifelse(cond, a, b) "
            "instead of a Python if/and/or"
        )

    def dependencies(self):
        """The set of `Variable` nodes this expression reads."""
        found = set()
        self._collect(found)
        return found

    def _collect(self, found):
        raise NotImplementedError

    def emit(self, ctx):
        """Return Python source evaluating this node, registering literals in `ctx`."""
        raise NotImplementedError


class Const(Expr):
    def __init__(self, value):
        self.value = float(value)

    def _collect(self, found):
        pass

    def emit(self, ctx):
        return repr(self.value)

    def __repr__(self):
        return repr(self.value)


class Variable(Expr):
    """A time-dependent quantity, either a stock or an auxiliary variable.

    `system` is the name of the sector that declared it; the pair
    (system, name) is what makes two variables distinct, exactly as the
    namespacing of composed `ODESystem`s does in Julia.
    """

    def __init__(self, name, system=None, init=None, description=""):
        self.name = name
        self.system = system
        self.init = init
        self.description = description

    @property
    def full_name(self):
        return f"{self.system}.{self.name}" if self.system else self.name

    @property
    def code_name(self):
        return f"{self.system}__{self.name}" if self.system else self.name

    def _collect(self, found):
        found.add(self)

    def emit(self, ctx):
        return self.code_name

    def __repr__(self):
        return self.full_name

    def __hash__(self):
        return hash((self.system, self.name))

    def __eq__(self, other):
        if isinstance(other, Variable):
            return (self.system, self.name) == (other.system, other.name)
        return NotImplemented


class Time(Variable):
    """The independent variable of the model.

    It is not a model variable: nothing defines it and nothing needs to be
    solved for it, so it never appears among the dependencies of an equation.
    """

    def __init__(self):
        super().__init__("t", description="Time instants")

    def _collect(self, found):
        pass

    def emit(self, ctx):
        return "t"


t = Time()


class Parameter(Expr):
    """A constant of the model, fixed when the sector is built."""

    def __init__(self, name, value, system=None, description=""):
        self.name = name
        self.value = float(value)
        self.system = system
        self.description = description

    @property
    def full_name(self):
        return f"{self.system}.{self.name}" if self.system else self.name

    def _collect(self, found):
        pass

    def emit(self, ctx):
        return repr(self.value)

    def __repr__(self):
        return f"{self.full_name}={self.value}"


class BinaryOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def _collect(self, found):
        self.left._collect(found)
        self.right._collect(found)

    def emit(self, ctx):
        return f"({self.left.emit(ctx)} {self.op} {self.right.emit(ctx)})"

    def __repr__(self):
        return f"({self.left!r} {self.op} {self.right!r})"


class UnaryOp(Expr):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def _collect(self, found):
        self.operand._collect(found)

    def emit(self, ctx):
        return f"({self.op}{self.operand.emit(ctx)})"

    def __repr__(self):
        return f"({self.op}{self.operand!r})"


class FunctionCall(Expr):
    """A call to one of the model functions, e.g. `exp`, `ramp` or `withlookup`.

    Arguments that are not expressions (lookup tables, for instance) are stored
    as they are and emitted as constants of the generated module.
    """

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def _collect(self, found):
        for arg in self.args:
            if isinstance(arg, Expr):
                arg._collect(found)

    def emit(self, ctx):
        parts = []
        for arg in self.args:
            if isinstance(arg, Expr):
                parts.append(arg.emit(ctx))
            else:
                parts.append(ctx.constant(arg))
        return f"{ctx.function(self.name)}({', '.join(parts)})"

    def __repr__(self):
        return f"{self.name}({', '.join(map(repr, self.args))})"


class Derivative:
    """The left-hand side `D(x)` of a stock equation."""

    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return f"D({self.variable!r})"


def D(variable):
    """Time derivative of `variable`; only valid on the left-hand side of an equation."""
    if not isinstance(variable, Variable):
        raise TypeError("D() can only be applied to a variable")
    return Derivative(variable)


class Equation:
    """`lhs ~ rhs`, with `lhs` either a variable or its derivative."""

    def __init__(self, lhs, rhs):
        if not isinstance(lhs, (Variable, Derivative)):
            raise TypeError("the left-hand side must be a variable or D(variable)")
        self.lhs = lhs
        self.rhs = _wrap(rhs)

    @property
    def is_derivative(self):
        return isinstance(self.lhs, Derivative)

    @property
    def variable(self):
        return self.lhs.variable if self.is_derivative else self.lhs

    def __repr__(self):
        return f"{self.lhs!r} ~ {self.rhs!r}"


def value_of(x):
    """The numeric value of a constant expression, used for initial values."""
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, (Const, Parameter)):
        return float(x.value)
    if isinstance(x, UnaryOp) and x.op == "-":
        return -value_of(x.operand)
    if isinstance(x, BinaryOp):
        left, right = value_of(x.left), value_of(x.right)
        return {
            "+": lambda: left + right,
            "-": lambda: left - right,
            "*": lambda: left * right,
            "/": lambda: left / right,
            "**": lambda: left**right,
        }[x.op]()
    if isinstance(x, FunctionCall):
        return _FUNCTIONS[x.name](*[value_of(a) for a in x.args])
    raise TypeError(f"{x!r} is not constant, so it cannot be used as an initial value")


def _lifted(name, numeric):
    """Build a function that computes on numbers but records a node on expressions."""

    def call(*args):
        if builtins.any(isinstance(a, Expr) for a in args):
            return FunctionCall(name, [_wrap(a) if isinstance(a, (int, float)) else a for a in args])
        return numeric(*args)

    call.__name__ = name
    return call


def _ifelse(condition, if_true, if_false):
    return if_true if condition else if_false


# Functions usable inside equations. They shadow the numeric builtins on purpose:
# `max(0, X)` has to work whether `X` is a number or an expression.
exp = _lifted("exp", math.exp)
log = _lifted("log", math.log)
sqrt = _lifted("sqrt", math.sqrt)
abs = _lifted("abs", builtins.abs)
min = _lifted("min", builtins.min)
max = _lifted("max", builtins.max)
ifelse = _lifted("ifelse", _ifelse)

_FUNCTIONS = {
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
    "abs": builtins.abs,
    "min": builtins.min,
    "max": builtins.max,
    "ifelse": _ifelse,
}


def register_function(name, implementation):
    """Make `implementation` callable from generated code under `name`."""
    _FUNCTIONS[name] = implementation
    return _lifted(name, implementation)
