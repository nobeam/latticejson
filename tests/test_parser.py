from pathlib import Path
from pprint import pprint
from latticejson.parser import parse_elegant, RPNCalculator

base = Path(__file__).resolve().parent / "data"
path_list = [base / "fodo.lte", base / "scratch.lte"]

"""Uncomment to test all elegant examples"""
# elegant_examples = Path.home() / "Git/elegant/examples"
# path_list = list(elegant_examples.rglob("*.lte"))


def test_parse_elegant():
    for path in path_list:
        print(path)
        with open(path) as file:
            string = file.read()

        res = parse_elegant(string)
        pprint(res)
        print("\n")
    print(f"tested {len(path_list)} lattices!")


def test_rpn_parser():
    rpn_calculator = RPNCalculator()
    assert 5 == rpn_calculator.execute("15 7 1 1 + - / 3 * 2 1 1 + + -")

    rpn_calculator.execute("5 sto x")
    assert 5 == rpn_calculator.execute("x")
    assert 10 == rpn_calculator.execute("x 2 *")

    for string in "1", "1.0", "1.", ".1", "-12e34":
        assert float(string) == rpn_calculator.execute(string)
