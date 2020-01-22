from pathlib import Path
from pprint import pprint
from latticejson.parser import parse_elegant

base = Path(__file__).parent.absolute()
home = Path.home()
path_list = [base / "data" / "scratch.lte"]

# path_list = [
#     "/home/felix/Git/hzb/lattice-development/lattices_B2"
#     "BII_2016-06-10_user_Sym_noID_DesignLattice1996.lte"
# ]

## Uncomment to test all elegant examples
elegant_examples = home / "Git" / "elegant" / "examples"
path_list = list(elegant_examples.rglob("*.lte"))
# path_list = [elegant_example / "spear.lte"]


def test_elegant_parser():
    for path in path_list:
        print(path)
        with open(path) as file:
            string = file.read()

        res = parse_elegant(string)
        # print(f"\n{res}")
    print(f"tested {len(path_list)} lattices!")
