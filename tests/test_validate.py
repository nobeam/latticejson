import os
import pytest
from latticejson.validate import validate_file
from latticejson import UndefinedObjectError

dir_name = os.path.dirname(__file__)


def test_validate():
    file_path = os.path.join(dir_name, "data", "fodo.json")
    validate_file(file_path)

    file_path = os.path.join(dir_name, "data", "test_undefined.json")
    with pytest.raises(UndefinedObjectError):
        validate_file(file_path)
