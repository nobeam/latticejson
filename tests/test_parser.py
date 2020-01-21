import os
from pprint import pprint
from latticejson.parser import elegant_parser, elegant_transformer

base = os.path.dirname(__file__)
path_list = [os.path.join(base, "data", "scratch.lte")]

# path = (
#     "/home/felix/Git/hzb/lattice-development/lattices_B2"
#     "BII_2016-06-10_user_Sym_noID_DesignLattice1996.lte"
# )

path_list = ["/home/felix/Git/elegant/lattices-examples/ptb.lte"]
base_path = "/home/felix/Git/elegant/lattices-examples"
path_list = [os.path.join(base_path, file) for file in os.listdir(base_path)]


def test_elegant_parser():
    for path in path_list:
        print(path)
        with open(path) as file:
            string = file.read()

        tree = elegant_parser.parse(string)
        res = elegant_transformer.transform(tree)

        # print(tree.pretty())
        # print(f"\n{res}")
