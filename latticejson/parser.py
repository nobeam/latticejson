from lark import Lark, Transformer

)


class ElegantTransformer(Transformer):
    def __init__(self):
        self.elements = {}
        self.lattices = {}

    def file(self, objects):
        return objects

    def name(self, s):
        (s,) = s
        return s[:]

    def type_(self, s):
        (s,) = s
        return s[:]

    def number(self, n):
        (n,) = n
        return float(n)

    def element(self, items):
        name, type_, attributes = items
        return {"name": name, "type": type_, **attributes}

    def attributes(self, items):
        return {key: value for key, value in items}

    def attribute(self, items):
        key, value = items
        return key, value

    def lattice(self, items):
        name, lattice = items
        return {"name": name, "lattice": lattice}

    def names(self, items):
        return items

with open("elegant.lark") as file:
    elegant_grammar = file.read()

elegant_parser = Lark(elegant_grammar, parser="lalr", start="file"
elegant_transformer = ElegantTransformer()