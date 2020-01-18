import os
from latticejson import convert_file

dir_name = os.path.dirname(__file__)


def test_convert():
    file_path = os.path.join(dir_name, "data", "fodo.json")
    convert_file(file_path, "json", "elegant")


def test_elegant_to_latticejson():
    from latticejson.convert import elegant_to_latticejson
    from pprint import pprint as print

    file_path = os.path.join(dir_name, "data", "fodo.lte")
    with open(file_path) as file:
        string = file.read()

    d = elegant_to_latticejson(string)
    print(d)


def test_mad_to_latticejson():
    from latticejson.convert import mad_to_latticejson
    from pprint import pprint as print

    file_path = os.path.join(dir_name, "data", "fodo.mad")
    with open(file_path) as file:
        string = file.read()

    d = mad_to_latticejson(string)
    print(d)

