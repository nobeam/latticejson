from pathlib import Path
import math
from lark import Lark, Transformer, v_args
from .exceptions import UndefinedRPNVariableError


@v_args(inline=True)
class ArithmeticTransformer(Transformer):
    from operator import add, sub, mul, truediv as div, neg, pow

    identity = lambda self, object: object
    number = float

    def transform(self, tree, calculator):
        self.calculator = calculator
        return super().transform(tree)

    def assignment(self, name, value):
        if self.calculator.rpn:
            name, value = value, name
        self.calculator.variables[name.lower()] = value
        return value

    def function(self, function, operand):
        if self.calculator.rpn:
            operand, function = function, operand
        return getattr(math, function.lower())(operand)

    def variable(self, name):
        try:
            return self.calculator.variables[name.lower()]
        except KeyError:
            raise UndefinedRPNVariableError(name)


class Calculator:
    def __init__(self, rpn=False):
        self.rpn = rpn
        self.variables = {"pi": math.pi, "e": math.e}
        self.parser = RPN_PARSER if rpn else ARITHMETIC_PARSER
        self.transformer = ARITHMETIC_TRANSFORMER

    def evaluate(self, string):
        tree = self.parser.parse(string)
        print()  # TODO: remove!
        print(tree.pretty())
        return self.transformer.transform(tree, self)


@v_args(inline=True)
class ElegantTransformer(Transformer):
    int = int
    float = float
    word = str
    name = lambda self, item: item.value.upper()
    string = lambda self, item: item[1:-1]

    def transform(self, tree):
        self.rpn_calculator = Calculator(rpn=True)
        self.elements = {}
        self.lattices = {}
        self.commands = []
        super().transform(tree)
        return dict(
            elements=self.elements,
            lattices=self.lattices,
            commands=self.commands,
            variables=self.rpn_calculator.variables.copy(),
        )

    def element(self, name, type_, *attributes):
        self.elements[name.upper()] = type_, dict(attributes)

    def attribute(self, name, value):
        if isinstance(value, str):
            try:
                value = self.rpn_calculator.evaluate(value)
            except:
                pass
        return name.upper(), value

    def lattice(self, name, arangement):
        self.lattices[name.upper()] = list(arangement)

    def arrangement(self, multiplier, is_reversed, *items):
        multiplier = int(multiplier) if multiplier is not None else 1
        if is_reversed is not None:
            multiplier *= -1

        if multiplier < 0:
            items = items[::-1]

        return [x for _ in range(abs(multiplier)) for y in items for x in y]

    def ref_name(self, mutliplier, is_reversed, name):
        name = str(name).upper()
        multiplier = int(mutliplier) if mutliplier is not None else 1
        if is_reversed is not None:
            multiplier *= -1

        if multiplier < 0:
            name_regular = name
            name += "_REV"
            if name_regular in self.lattices:
                line = self.lattices[name_regular][::-1]
                self.lattices[name] = line
            elif name_regular in self.elements:
                self.elements[name] = "REVERSED_ELEMENT", {"ref": name_regular}

        return abs(multiplier) * (name,)

    def assignment(self, rpn_string):
        return self.rpn_calculator.evaluate(rpn_string)

    def command(self, *items):
        self.commands.append(items)


@v_args(inline=True)
class MADXTransformer(Transformer):
    int = int
    float = float
    word = str
    name = lambda self, item: item.value.upper()
    string = lambda self, item: item[1:-1]

    def start(self, *children):
        pass


DIR_NAME = Path(__file__).resolve().parent

ELEGANT_GRAMMAR = (DIR_NAME / "elegant.lark").read_text()
ELEGANT_PARSER = Lark(ELEGANT_GRAMMAR, parser="lalr", maybe_placeholders=True)
RPN_GRAMMAR = (DIR_NAME / "rpn.lark").read_text()
RPN_PARSER = Lark(RPN_GRAMMAR, parser="lalr")

ARITHMETIC_GRAMMER = (DIR_NAME / "arithmetic.lark").read_text()
ARITHMETIC_PARSER = Lark(ARITHMETIC_GRAMMER, parser="lalr")
ARITHMETIC_TRANSFORMER = ArithmeticTransformer()

MADX_GRAMMAR = (DIR_NAME / "madx.lark").read_text()
MADX_PARSER = Lark(MADX_GRAMMAR, parser="lalr", maybe_placeholders=True, debug=True)


def parse_elegant(string: str):
    tree = ELEGANT_PARSER.parse(string + "\n")  # TODO: remove "\n" when lark has EOF
    return ElegantTransformer().transform(tree)


def parse_madx(string: str):
    raise NotImplementedError
    tree = MADX_PARSER.parse(string)
    return MADXTransformer().transform(tree)
