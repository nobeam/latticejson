from pathlib import Path
from pprint import pprint as print
import json
from latticejson.convert import latticejson_to_elegant, elegant_to_latticejson

base_dir = Path(__file__).resolve().parent / "data"
with open(base_dir / "fodo.lte") as file:
    fodo_lte = file.read()

with open(base_dir / "fodo.json") as file:
    fodo_json = json.load(file)


def test_latticejson_to_elegant():
    elegant = latticejson_to_elegant(fodo_json)
    print(elegant)


def test_elegant_to_latticejson():
    latticejson = elegant_to_latticejson(fodo_lte)
    print(latticejson)
