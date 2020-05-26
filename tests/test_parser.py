from pathlib import Path
from pprint import pprint

import pytest

data_path = Path(__file__).resolve().parent / "data"


def test_elegant_parser():
    from latticejson.parse import ELEGANT_PARSER, ElegantTransformer
    from latticejson.convert import _map_names, FROM_ELEGANT

    path_list = [data_path / "fodo.lte", data_path / "scratch.lte"]

    """Uncomment to test all elegant examples"""
    # elegant_examples = Path.home() / "Git/elegant/examples"
    # path_list = list(elegant_examples.rglob("*.lte"))

    for path in path_list:
        print(path)
        tree = ELEGANT_PARSER.parse(Path(path).read_text())
        elegant_dict = ElegantTransformer().transform(tree)
        # pprint(elegant_dict)
        # pprint(_map_namest(elegant_dict, FROM_ELEGANT))
        # print("\n")
    print(f"Tested {len(path_list)} lattices!")


def test_rpn_parser():
    from latticejson.parse import Calculator

    rpn_calculator = Calculator(rpn=True)
    assert 5 == rpn_calculator("15 7 1 1 + - / 3 * 2 1 1 + + -")

    rpn_calculator("5 sto x")
    assert 5 == rpn_calculator("x")
    assert 10 == rpn_calculator("x 2 *")

    for string in "1", "1.0", "1.", ".1", "1e-10":
        assert float(string) == rpn_calculator(string)


def test_arithmetic_parser():
    import math
    from latticejson.parse import Calculator

    calculator = Calculator()
    variables = calculator.transformer.variables
    math_dict = math.__dict__
    expressions = (
        "1 + 2 * 3",  # precendence of operators
        "1 - 1 - 1",  # left-to-right subtraction
        "1 / 2 / 3",  # left-to-right division
        "4 ** 3 ** 2 + 1",  # serial exponentiation
        "4 ** (3 ** 2 + 1)",  # parenthesis
        "-+-4 / (-2 + -3)",  # multiple unary operations
        "-.02e+2 / +4e1 ** 2.2e-1",  # scientific notation
        "variable + sin(pi)",  # use variable and math function
    )

    calculator("variable := 1.2 / tanh(.11)")  # python eval has no assignment
    for expression in expressions:
        print(expression, "=", calculator(expression))
        assert eval(expression, variables, math_dict) == calculator(expression)


def test_madx_parser():
    from latticejson.parse import MADX_PARSER, MADXTransformer
    from latticejson.convert import _map_names, FROM_MADX
    from latticejson.exceptions import UnknownAttributeWarning

    tree = MADX_PARSER.parse((data_path / "fodo.madx").read_text())
    madx_dict = MADXTransformer().transform(tree)
    with pytest.warns(UnknownAttributeWarning):
        latticejson = _map_names(madx_dict, FROM_MADX)
    # print()
    # print(tree.pretty())
    # pprint(madx_dict)
    # pprint(latticejson)