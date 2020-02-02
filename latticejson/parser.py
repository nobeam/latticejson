import re
from pathlib import Path
import operator as op
import math
from lark import Lark, Transformer, v_args
from lark.exceptions import VisitError
from typing import List, Tuple, Dict

DIR_NAME = Path(__file__).resolve().parent
ELEGANT_GRAMMAR_PATH = DIR_NAME / "elegant.lark"
RPN_GRAMMAR_PATH = DIR_NAME / "rpn.lark"

with open(ELEGANT_GRAMMAR_PATH) as file:
    ELEGANT_GRAMMAR = file.read()

with open(RPN_GRAMMAR_PATH) as file:
    RPN_GRAMMAR = file.read()

ELEGANT_PARSER = Lark(ELEGANT_GRAMMAR, parser="lalr", start="file")
RPN_PARSER = Lark(RPN_GRAMMAR, parser="lalr", start="start")
RPN_OPERATORS = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv, "%": op.mod}


class UndefinedRPNVariableError(Exception):
    """Raised if a rpn variable is not defined."""

    def __init__(self, name, *args, **kwargs):
        super().__init__(f"RPN variable {name} is not defined!", *args, **kwargs)


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
        name = name.lower()
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
    name = word = str
    string = lambda self, item: item[1:-1]
    file = lambda self, *objects: objects
    ref_name = lambda self, item: [item.value]
    # TODO: better inverse object/arangement
    ref_name_inv = lambda self, item: [item[0] + "_INV"]

    def transform(self, tree):
        self.rpn_calculator = RPNCalculator()
        self.elements = {}
        self.lattices = {}
        self.commands = []
        super().transform(tree)
        return dict(
            elements=self.elements, lattices=self.lattices, commands=self.commands
        )

    def element(self, name, type_, *attributes):
        self.elements[name] = {"type": type_, **dict(attributes)}

    def attribute(self, name, value):
        if isinstance(value, str):
            try:
                value = self.rpn_calculator.execute(value)
            except VisitError:
                pass
        return name, value

    def lattice(self, name, arangement):
        self.lattices[name] = {"type": "line", "line": arangement}

    def arrangement(self, *items) -> List:
        return [sub_item for item in items for sub_item in item]

    def mul_object(self, number, object) -> List:
        return number * object

    def rpn_store(self, rpn_string):
        return self.rpn_calculator.execute(rpn_string)

    def command(self, items):
        self.commands.append(items)


def parse_elegant(string: str):
    tree = ELEGANT_PARSER.parse(string + "\n")  # TODO: remove "\n" when lark has EOF
    return ElegantTransformer().transform(tree)
