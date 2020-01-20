import os
from lark import Lark, Transformer, v_args
from typing import List, Tuple, Dict

DIR_NAME = os.path.dirname(__file__)
ELEGANT_GRAMMAR_PATH = os.path.join(DIR_NAME, "elegant.lark")

with open(ELEGANT_GRAMMAR_PATH) as file:
    ELEGANT_GRAMMAR = file.read()


class ElegantTransformer(Transformer):
    file = lambda self, objects: objects
    name = lambda self, items: items[0].value
    type = lambda self, items: items[0].value
    attribute = tuple
    int = v_args(inline=True)(int)
    float = v_args(inline=True)(float)

    def element(self, items) -> Dict:
        name, type_, *attributes = items
        attributes = dict(attributes)
        return {"name": name, "type": type_, **attributes}

    def lattice(self, items) -> Dict:
        name, arangement = items
        return {"name": name, "type": "line", "line": arangement}

    def arrangement(self, items) -> List:
        arrangement = []
        for item in items:
            if isinstance(item, str):
                arrangement.append(item)
            elif isinstance(item, list):
                arrangement.extend(item)
            else:
                raise Exception(f"Unable to parse arrangement {items}!")
        return arrangement

    def reverse_object(self, items) -> List:
        items.reverse()
        return items

    @v_args(inline=True)
    def multiply_object(self, number, object) -> List:
        return number * object


elegant_parser = Lark(ELEGANT_GRAMMAR, parser="lalr", start="file")
elegant_transformer = ElegantTransformer()
