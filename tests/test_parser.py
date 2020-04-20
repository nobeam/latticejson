from pathlib import Path
from pprint import pprint

base = Path(__file__).resolve().parent / "data"


def test_elegant_parser():
    from latticejson.parse import ELEGANT_PARSER, ElegantTransformer

    path_list = [base / "fodo.lte", base / "scratch.lte"]

    """Uncomment to test all elegant examples"""
    # elegant_examples = Path.home() / "Git/elegant/examples"
    # path_list = list(elegant_examples.rglob("*.lte"))

    for path in path_list:
        print(path)
        tree = ELEGANT_PARSER.parse(Path(path).read_text())
        res = ElegantTransformer().transform(tree)
        pprint(res)
        print("\n")
    print(f"Tested {len(path_list)} lattices!")


def test_rpn_parser():
    from latticejson.parse import Calculator

    rpn_calculator = Calculator(rpn=True)
    assert 5 == rpn_calculator.evaluate("15 7 1 1 + - / 3 * 2 1 1 + + -")

    rpn_calculator.evaluate("5 sto x")
    assert 5 == rpn_calculator.evaluate("x")
    assert 10 == rpn_calculator.evaluate("x 2 *")

    for string in "1", "1.0", "1.", ".1", "1e-10":
        assert float(string) == rpn_calculator.evaluate(string)


def test_arithmetic():
    import math
    from latticejson.parse import Calculator

    calculator = Calculator()
    variables = calculator.variables
    math_dict = math.__dict__
    expressions = (
        "1 + 1 - 1",
        "-+-4 / (-2 + -3)",
        "3 ** 3 ** 3",
        "3 ** (3 ** 3)",
        "-1 * -4 ** 2.2",
        "variable + sin(pi)",
    )

    calculator.evaluate("variable := 1.2 / tanh(.11)")  # python eval has no assignment
    for expression in expressions:
        print(expression, "=", calculator.evaluate(expression))
        assert eval(expression, variables, math_dict) == calculator.evaluate(expression)


def test_parse_madx():
    from latticejson.parse import MADX_PARSER, MADXTransformer

    tree = MADX_PARSER.parse((base / "fodo.madx").read_text())
    # tree = MADX_PARSER.parse(
    #     Path("/home/felix/Downloads/BESSYII_StandardUser.madx").read_text()
    # )
    print(tree)
    print(tree.pretty())
    print(MADXTransformer().transform(tree))
