from pathlib import Path
import json
from .convert import elegant_to_latticejson
from .validate import validate


def read(path):
    """Read/validate lattice file and return latticeJSON dict."""
    path = Path(path)
    suffix = path.suffix
    text = path.read_text()
    if suffix == ".json":
        latticejson = json.loads(text)
    elif suffix == ".lte":
        latticejson = elegant_to_latticejson(text)
    else:
        raise NotImplementedError(f"Unkown file fromat {suffix}")

    validate(latticejson)
    return latticejson
