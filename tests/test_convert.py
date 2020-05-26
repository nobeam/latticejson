import json
from pathlib import Path
from pprint import pprint as print

from latticejson.convert import from_elegant, to_elegant

base_dir = Path(__file__).resolve().parent / "data"
fodo_lte = (base_dir / "fodo.lte").read_text()
fodo_json = json.loads((base_dir / "fodo.json").read_text())


def test_to_elegant():
    expected = (
        "! TITLE: FODO Lattice\n"
        "M1: MARK, \n"
        "D1: DRIF, L=0.55\n"
        "Q1: KQUAD, L=0.2, K1=1.2\n"
        "Q2: KQUAD, L=0.4, K1=-1.2\n"
        "B1: CSBEND, L=1.5, ANGLE=0.39269908169872414, E1=0.19634954084936207, "
        "E2=0.19634954084936207\n"
        "CELL: LINE=(M1, Q1, D1, B1, D1, Q2, D1, B1, D1, Q1)\n"
        "RING: LINE=(CELL, CELL, CELL, CELL, CELL, CELL, CELL, CELL)\n"
        "USE, RING\n"
    )

    elegant = to_elegant(fodo_json)
    print(elegant)
    assert expected == elegant


def test_from_elegant():
    latticejson = from_elegant(fodo_lte)
    latticejson.pop("title")
    fodo_json.pop("info")
    fodo_json.pop("title")
    print(latticejson)
    assert sorted(latticejson.items()) == sorted(fodo_json.items())


# Uncomment to test for elegant examples
# def test_all_elegant_examples():
#     elegant_examples = Path.home() / "Git/elegant/examples"
#     path_list = list(elegant_examples.rglob("*.lte"))
#     for path in path_list:
#         print(path)
#         latticejson = elegant_to_latticejson(path.read_text())
#         print(latticejson)
#         input()
