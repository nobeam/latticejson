import json
from pathlib import Path

import fastjsonschema
from packaging import version as _version

from .exceptions import IncompatibleVersionError, UndefinedObjectError

parse_version = _version.parse
schema_path = Path(__file__).resolve().parent / "schema.json"
schema = json.loads(schema_path.read_text())
schema_version = parse_version(schema["title"][28:])


def validate_file(path: str):
    data = json.loads(Path(path).read_text())
    validate(data)


def validate(data):
    if not "version" in data:
        raise Exception("Unknown LatticeJSON version.")

    version = parse_version(data["version"])
    if version > schema_version:
        raise IncompatibleVersionError("Use 'pip install -U latticejson' to update.")

    if version.major < schema_version.major:
        raise IncompatibleVersionError("Use 'latticejson migrate' to update file.")

    validate_syntax(data)
    validate_defined_objects(data)


validate_syntax = fastjsonschema.compile(schema)


# TODO: use this if validation fails... maybe it is better to use jsonschema instead:
# It is significantly slower but has more verbose error messages
# Uncomment to validate with jsonschema instead
# def validate_syntax(data):
#     import jsonschema
#
#     return jsonschema.validate(data, schema, types={"array": (list, tuple)})


def validate_defined_objects(data):
    """Validate whether all referenced elements and sub-lattices are definied."""
    elements = data["elements"]
    lattices = data["lattices"]

    for lattice_name, lattice_tree in lattices.items():
        for object_name in lattice_tree:
            if object_name not in elements and object_name not in lattices:
                raise UndefinedObjectError(object_name, lattice_name)
