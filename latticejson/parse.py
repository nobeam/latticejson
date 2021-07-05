import math
from abc import ABC, abstractproperty
from pathlib import Path

from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError

from .exceptions import UndefinedVariableError

BASE_DIR = Path(__file__).resolve().parent

with (BASE_DIR / "elegant.lark").open() as file:
    ELEGANT_PARSER = Lark(file, parser="lalr", maybe_placeholders=True)
    file.seek(0)
    RPN_PARSER = Lark(file, parser="lalr", start="start_rpn")

with (BASE_DIR / "madx.lark").open() as file:
    MADX_PARSER = Lark(file, parser="lalr", maybe_placeholders=True)
    file.seek(0)
    ARITHMETIC_PARSER = Lark(file, parser="lalr", start="start_artih")


@v_args(inline=True)
class ArithmeticTransformer(Transformer):
    def __init__(self, variables=None):
        if variables is None:
            self._variables = {"pi": math.pi, "twopi": 2 * math.pi, "e": math.e}
        else:
            self._variables = variables

    @property
    def variables(self):
        return self._variables

    identity = lambda self, object: object
    number = float
    word = str
    from operator import add, sub, mul, truediv as div, neg, pow

    def assignment(self, name, value):
        self.variables[name.lower()] = value
        return value

    def function(self, function, operand):
        # some math functions are named differently in Python
        function = {"arctan": "atan"}.get(function, function)
        return getattr(math, function.lower())(operand)

    def variable(self, name):
        try:
            return self.variables[name.lower()]
        except KeyError:
            # There is no syntactic distinction between a variable and a string.
            # The best thing we can do is to test if it is a variable or not.
            return name
            # raise UndefinedVariableError(name)


@v_args(inline=True)
class RPNTransformer(ArithmeticTransformer):
    def assignment(self, value, name):
        return super().assignment(name, value)

    def function(self, operand, function):
        return super().function(function, operand)


@v_args(inline=True)
class AbstractLatticeFileTransformer(ABC, Transformer):
    REVERSED_SUFFIX = "_reversed"

    @abstractproperty
    def variables(self):
        pass

    def transform(self, tree):
        self.elements = {}
        self.lattices = {}
        self.commands = []
        super().transform(tree)
        return dict(
            elements=self.elements,
            lattices=self.lattices,
            commands=self.commands,
            variables=self.variables,
        )

    int = int
    float = float
    word = str
    name = lambda self, item: item.value.lower()
    string = lambda self, item: item[1:-1]

    def element(self, name, type_, *attributes):
        self.elements[name.lower()] = type_.lower(), dict(attributes)

    def attribute(self, name, value):
        return name.lower(), value

    def lattice(self, name, arangement):
        self.lattices[name.lower()] = list(arangement)

    def arrangement(self, multiplier, is_reversed, *items):
        multiplier = int(multiplier) if multiplier is not None else 1
        if is_reversed is not None:
            multiplier *= -1

        if multiplier < 0:
            items = items[::-1]

        return [x for _ in range(abs(multiplier)) for y in items for x in y]

    def ref_name(self, mutliplier, is_reversed, name):
        name = str(name).lower()
        multiplier = int(mutliplier) if mutliplier is not None else 1
        if is_reversed is not None:
            multiplier *= -1

        if multiplier < 0:
            name = self.reverse_object(name)

        return abs(multiplier) * (name,)

    def reverse_object(self, name):
        if name.endswith(self.REVERSED_SUFFIX):
            reversed_name = name[: -len(self.REVERSED_SUFFIX)]
        else:
            reversed_name = name + self.REVERSED_SUFFIX
        if reversed_name in self.lattices or reversed_name in self.elements:
            pass
        elif name in self.lattices:
            self.lattices[reversed_name] = [
                self.reverse_object(obj_name)
                for obj_name in reversed(self.lattices[name])
            ]
        elif name in self.elements:
            # a bend with different exit and entrance angles must be reversed
            # for all other elements we can return the old reference
            # TODO: must other elemetns be reversed too?
            type_, attrs = self.elements[name]
            if type_ not in {"sbend", "csbend"} or attrs.get("e1") == attrs.get("e2"):
                return name

            attrs = attrs.copy()
            attrs["e1"], attrs["e2"] = attrs["e2"], attrs["e1"]
            self.elements[reversed_name] = type_, attrs
        return reversed_name

    def command(self, *items):
        self.commands.append(items)


@v_args(inline=True)
class MADXTransformer(ArithmeticTransformer, AbstractLatticeFileTransformer):
    def sequence(self, name, *items):
        *attributes, elements = items
        self.lattices[name.lower()] = elements
        self.commands.append(("name", name))

    def seq_element(self, name, value):
        return name.lower(), value

    def seq_elements(self, *elements):
        return list(elements)


@v_args(inline=True)
class ElegantTransformer(RPNTransformer, AbstractLatticeFileTransformer):
    def __init__(self):
        super().__init__()
        self.calc = Calculator(rpn=True)
        self.calc.transformer._variables = self._variables

    def string(self, item):
        s = item[1:-1]
        try:  # There is no syntactic distinction between a string and a variable.
            return self.calc(s)
        except LarkError:  # Just a string
            return s


class Calculator:
    """Can evaluate simple arithmetic expressions. Used to test ArithmeticParser."""

    def __init__(self, rpn=False):
        self.parser = RPN_PARSER if rpn else ARITHMETIC_PARSER
        self.transformer = RPNTransformer() if rpn else ArithmeticTransformer()

    def __call__(self, expression):
        return self.transformer.transform(self.parser.parse(expression))


def parse_elegant(string: str):
    tree = ELEGANT_PARSER.parse(string + "\n")  # TODO: remove "\n" when lark has EOF
    return ElegantTransformer().transform(tree)


def parse_madx(string: str):
    tree = MADX_PARSER.parse(string)
    return MADXTransformer().transform(tree)
