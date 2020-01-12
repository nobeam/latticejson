import os
import json
import fastjsonschema

dir_name = os.path.dirname(__file__)
schema_path = os.path.join(dir_name, "schema.json")

with open(schema_path) as schema_file:
    schema = json.load(schema_file)

validate_syntax = fastjsonschema.compile(schema)


class UndefinedObjectError(Exception):
    """Raised if an object is referenced within a lattice but no definition is found.

    :param str object_name: Name of the undfined object.
    :param str lattice_name: Name of the lattice which contains the undefined object.
    """

    def __init__(self, object_name, lattice_name):
        super().__init__(
            f"The Object {object_name} is referenced in {lattice_name} "
            "but no definition was found!"
        )


def validate_file(file_path: str):
    with open(file_path) as file:
        data = json.load(file)

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
