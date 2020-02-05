from typing import List, Tuple, Dict
from pathlib import Path
import operator as op
import math
from lark import Lark, Transformer, v_args
from lark.exceptions import VisitError
import itertools
from .exceptions import UndefinedRPNVariableError


DIR_NAME = Path(__file__).resolve().parent
ELEGANT_GRAMMAR = (DIR_NAME / "elegant.lark").read_text()
RPN_GRAMMAR = (DIR_NAME / "rpn.lark").read_text()

ELEGANT_PARSER = Lark(
    ELEGANT_GRAMMAR, parser="lalr", start="file", maybe_placeholders=True
)
RPN_PARSER = Lark(RPN_GRAMMAR, parser="lalr", start="start")
RPN_OPERATORS = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv, "%": op.mod}


@v_args(inline=True)
class RPNTransformer(Transformer):
    int = int
    float = float
    word = str

    def transform(self, tree, variables):
        self.variables = variables
        return super().transform(tree)

    def rpn_store(self, result, name) -> Tuple:
        self.variables[name] = result
        return result

    def rpn_unary(self, operand, operator):
        return getattr(math, operator)(operand)

    def rpn_binary(self, operand_1, operand_2, operator):
        return RPN_OPERATORS[operator](operand_1, operand_2)

    def rpn_variable(self, name):
        try:
            return self.variables[name]
        except KeyError:
            raise UndefinedRPNVariableError(name)


class RPNCalculator:
    def __init__(self):
        self.rpn_transformer = RPNTransformer()
        self.variables = {"pi": math.pi, "e": math.e}

    def execute(self, string):
        tree = RPN_PARSER.parse(string)
        return self.rpn_transformer.transform(tree, self.variables)


@v_args(inline=True)
class ElegantTransformer(Transformer):
    int = int
    float = float
    word = str
    name = lambda self, item: item.value.upper()
    string = lambda self, item: item[1:-1]

    def transform(self, tree):
        self.rpn_calculator = RPNCalculator()
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
                value = self.rpn_calculator.execute(value)
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

    def rpn_store(self, rpn_string):
        return self.rpn_calculator.execute(rpn_string)

    def command(self, *items):
        self.commands.append(items)


def parse_elegant(string: str):
    tree = ELEGANT_PARSER.parse(string + "\n")  # TODO: remove "\n" when lark has EOF
    return ElegantTransformer().transform(tree)
