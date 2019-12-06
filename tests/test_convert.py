import os
from latticejson import convert_file

dir_name = os.path.dirname(__file__)


def test_convert():
    file_path = os.path.join(dir_name, "data", "fodo.json")
    convert_file(file_path, "json", "elegant")
