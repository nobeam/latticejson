from pathlib import Path
from pprint import pprint
from latticejson.parser import parse_elegant, RPNCalculator

base = Path(__file__).resolve().parent / "data"
path_list = [base / "scratch.lte"]
# path_list = [base / "fodo.lte"]

# path_list = [
#     "/home/felix/Git/hzb/lattice-development/lattices_B2"
#     "BII_2016-06-10_user_Sym_noID_DesignLattice1996.lte"
# ]

# Uncomment to test all elegant examples
elegant_examples = Path.home() / "Git/elegant/examples"
path_list = list(elegant_examples.rglob("*.lte"))
# path_list = [elegant_examples / "constructOrbitBump1/par.lte"]


def test_elegant_parser():
    for path in path_list:
        print(path)
        with open(path) as file:
            string = file.read()

        res = parse_elegant(string)
        # pprint(res)
        # print("\n")
    print(f"tested {len(path_list)} lattices!")


def test_rpn_parser():
    rpn_calculator = RPNCalculator()
    assert 5 == rpn_calculator.calculate("15 7 1 1 + - / 3 * 2 1 1 + + -")

    rpn_calculator.assign("x", 5)
    assert 5 == rpn_calculator.calculate("x")
    assert 10 == rpn_calculator.calculate("x 2 *")

    for string in "1", "1.0", "1.", ".1", "-12e34":
        assert float(string) == rpn_calculator.calculate(string)
