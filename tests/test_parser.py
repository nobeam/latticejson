import os
from pprint import pprint
from latticejson.parser import elegant_parser, elegant_transformer


path = (
    "/home/felix/Git/hzb/lattice-development/lattices_B2"
    "BII_2016-06-10_user_Sym_noID_DesignLattice1996.lte"
)

base = os.path.dirname(__file__)
path = os.path.join(base, "data", "fodo.lte")
path = "/home/felix/Git/elegant/lattices-examples/chicaneOpt.lte"


def test_elegant_parser():
    with open(path) as file:
        string = file.read()

    tree = elegant_parser.parse(string)
    res = elegant_transformer.transform(tree)

    print("\n")
    # print(tree.pretty())
    pprint(res)
