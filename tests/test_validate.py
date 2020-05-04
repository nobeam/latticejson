from pathlib import Path

import pytest

from latticejson.exceptions import UndefinedObjectError
from latticejson.validate import validate_file

base_dir = Path(__file__).resolve().parent / "data"


def test_validate():
    file_path = base_dir / "fodo.json"
    validate_file(file_path)

    file_path = base_dir / "test_undefined.json"
    with pytest.raises(UndefinedObjectError):
        validate_file(file_path)
