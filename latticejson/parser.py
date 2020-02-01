import re
from pathlib import Path
import operator as op
import math
from lark import Lark, Transformer, v_args
from typing import List, Tuple, Dict

DIR_NAME = Path(__file__).resolve().parent
ELEGANT_GRAMMAR_PATH = DIR_NAME / "elegant.lark"
RPN_GRAMMAR_PATH = DIR_NAME / "rpn.lark"

with open(ELEGANT_GRAMMAR_PATH) as file:
    ELEGANT_GRAMMAR = file.read()

with open(RPN_GRAMMAR_PATH) as file:
    RPN_GRAMMAR = file.read()

ELEGANT_PARSER = Lark(ELEGANT_GRAMMAR, start="file")
RPN_PARSER = Lark(RPN_GRAMMAR, parser="lalr", start="rpn_expr")
RPN_OPERATORS = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv, "%": op.mod}


@v_args(inline=True)
class RPNTransformer(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variables = {"pi": math.pi, "e": math.e}

    int = int
    float = float

    def rpn(self, result, name) -> Tuple:
        return name, result

    def rpn_unary(self, operand, operator):
        return getattr(math, operator)(operand)

    def rpn_binary(self, operand_1, operand_2, operator):
        return RPN_OPERATORS[operator](operand_1, operand_2)

    def rpn_variable(self, name):
        name = name.lower()
        try:
            return self.variables[name]
        except KeyError:
            raise Exception(f"Variable {name} is not defined!")


class RPNCalculator:
    def __init__(self):
        self.transformer = RPNTransformer()
        self.varibales = self.transformer.variables

    def calculate(self, string):
        return self.transformer.transform(RPN_PARSER.parse(string))

    def assign(self, name, value):
        self.varibales[name] = value


@v_args(inline=True)
class ElegantTransformer(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._variables = {"pi": math.pi, "e": math.e}

    int = int
    float = float
    name = word = rpn_store = str
    string = lambda self, item: item[1:-1]
    file = lambda self, *objects: objects
    attribute = lambda self, name, value: (name, value)
    ref_name = lambda self, item: [item.value]
    ref_name_inv = lambda self, item: [item[0] + "_INV"]
    command = lambda self, *items: items

    def element(self, name, type_, *attributes) -> Dict:
        return {"name": name, "type": type_, **dict(attributes)}

    def lattice(self, name, arangement) -> Dict:
        return {"name": name, "type": "line", "line": arangement}

    def arrangement(self, *items) -> List:
        return [sub_item for item in items for sub_item in item]

    def mul_object(self, number, object) -> List:
        return number * object


def parse_elegant(string: str):
    tree = ELEGANT_PARSER.parse(string + "\n")  # TODO: remove "\n" when lark has EOF
    return ElegantTransformer().transform(tree)
