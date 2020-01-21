import os
import operator as op
import math
from lark import Lark, Transformer, v_args
from typing import List, Tuple, Dict

DIR_NAME = os.path.dirname(__file__)
ELEGANT_GRAMMAR_PATH = os.path.join(DIR_NAME, "elegant.lark")

with open(ELEGANT_GRAMMAR_PATH) as file:
    ELEGANT_GRAMMAR = file.read()


class ElegantTransformer(Transformer):
    int = v_args(inline=True)(int)
    float = v_args(inline=True)(float)
    string = lambda self, items: items[0][1:-1]
    name = lambda self, items: items[0].value
    word = lambda self, items: items[0].value
    file = lambda self, objects: objects
    attribute = tuple
    ref_name = lambda self, items: [items[0].value]
    ref_name_inv = lambda self, items: [items[0][0] + "_INV"]
    command = lambda self, items: items

    def element(self, items) -> Dict:
        name, type_, *attributes = items
        attributes = dict(attributes)
        return {"name": name, "type": type_, **attributes}

    def lattice(self, items) -> Dict:
        name, arangement = items
        return {"name": name, "type": "line", "line": arangement}

    def arrangement(self, items) -> List:
        return [sub_item for item in items for sub_item in item]

    @v_args(inline=True)
    def multiply_object(self, number, object) -> List:
        return number * object

    @v_args(inline=True)
    def rpn(self, result, name) -> Tuple:
        return name, result

    @v_args(inline=True)
    def rpn_binary(self, operand_1, operand_2, operator):
        return rpn_operators[operator](operand_1, operand_2)

    @v_args(inline=True)
    def rpn_unary(self, operand, operator):
        return getattr(math, operator)(operand)

    # rpn_unary_op = lambda self, items: getattr(math, items[0])
    rpn_constant = lambda self, items: getattr(math, items[0])


rpn_operators = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv, "%": op.mod}

elegant_parser = Lark(ELEGANT_GRAMMAR, parser="lalr", start="file")
elegant_transformer = ElegantTransformer()
