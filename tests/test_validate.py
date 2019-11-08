import os
from latticejson.validate import validate_file

dir_name = os.path.dirname(__file__)


def test_validate():
    file_path = os.path.join(dir_name, 'data', 'fodo.json')
    validate_file(file_path)
