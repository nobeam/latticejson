from pathlib import Path
import json
import fastjsonschema
from .exceptions import UndefinedObjectError

schema_path = Path(__file__).resolve().parent / "schema.json"
schema = json.loads(schema_path.read_text())
validate_syntax = fastjsonschema.compile(schema)


# TODO: maybe it is better to use jsonschema instead:
# It is significantly slower but has more verbose error messages
# Uncomment to validate with jsonschema instead
# def validate_syntax(data):
#     import jsonschema
#
#     return jsonschema.validate(data, schema, types={"array": (list, tuple)})


def validate_file(path: str):
    data = json.loads(Path(path).read_text())
    validate(data)


def validate(data):
    # validate syntax
    validate_syntax(data)

    # validate lattice file contains all referenced elements and sublattices
    elements = data["elements"]
    sub_lattices = data.get("sub_lattices", {})
    all_lattices = {data["name"]: data["lattice"], **sub_lattices}

    for lattice_name, lattice_tree in all_lattices.items():
        for object_name in lattice_tree:
            if object_name not in elements and object_name not in sub_lattices:
                raise UndefinedObjectError(object_name, lattice_name)
