import json
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def base_dir():
    return Path(__file__).resolve().parent / "tests" / "data"


@pytest.fixture(scope="session")
def fodo_lte(base_dir):
    return (base_dir / "fodo.lte").read_text()


@pytest.fixture(scope="session")
def fodo_json(base_dir):
    return json.loads((base_dir / "fodo.json").read_text())
