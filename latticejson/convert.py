import json
from pathlib import Path
from typing import Dict, List
from warnings import warn

from .exceptions import UnknownAttributeWarning, UnknownElementTypeWarning
from .parse import parse_elegant, parse_madx

NAME_MAP = json.loads((Path(__file__).parent / "map.json").read_text())["map"]
TO_ELEGANT = {x: y[0][0] for x, *y in NAME_MAP}
FROM_ELEGANT = {y: x for x, *tup in NAME_MAP for y in tup[0]}
TO_MADX = {x: y[1][0] for x, *y in NAME_MAP}
FROM_MADX = {y: x for x, *tup in NAME_MAP for y in tup[1]}


def from_elegant(string):
    """Convert an elegant lattice file to a LatticeJSON dict.

    :param str string: input lattice file as string
    :param lattice_name: name of the lattice
    :type str, optional
    :param description: description of the lattice
    :type str, optional
    :return: dict in LatticeJSON format
    """
    return _map_names(parse_elegant(string), FROM_ELEGANT)


def from_madx(string):
    """Convert a MADX lattice file to a LatticeJSON dict.

    :param str string: input lattice file as string
    :param lattice_name: name of the lattice
    :type str, optional
    :param description: description of the lattice
    :type str, optional
    :return: dict in LatticeJSON format
    """
    return _map_names(parse_madx(string), FROM_MADX)


def _map_names(lattice_data: dict, name_map: dict):
    elements = {}
    for name, (other_type, other_attributes) in lattice_data["elements"].items():
        latticejson_type = name_map.get(other_type)
        if latticejson_type is None:
            elements[name] = ["Drift", {"length": other_attributes.get("L", 0)}]
            warn(UnknownElementTypeWarning(name, other_type))
            continue

        attributes = {}
        elements[name] = [latticejson_type, attributes]
        for other_key, value in other_attributes.items():
            latticejson_key = name_map.get(other_key)
            if latticejson_key is not None:
                attributes[latticejson_key] = value
            else:
                warn(UnknownAttributeWarning(other_key, name))

    lattices = lattice_data["lattices"]
    lattice_name, main_lattice = lattices.popitem()  # use last lattice as main_lattice
    return dict(
        name=lattice_name,
        lattice=main_lattice,
        sub_lattices=lattices,
        elements=elements,
    )


def to_elegant(latticejson: dict) -> str:
    """Convert a LatticeJSON dict to the elegant lattice file format.

    :param lattice_dict dict: dict in LatticeJSON format
    :return: string with in elegant lattice file format
    """
    elements = latticejson["elements"]
    sub_lattices = latticejson["sub_lattices"]

    strings = [f"! TITLE: {latticejson['name']}"]
    element_template = "{}: {}, {}".format
    for name, (type_, attributes) in elements.items():
        attrs = ", ".join(f"{TO_ELEGANT[k]}={v}" for k, v in attributes.items())
        elegant_type = TO_ELEGANT[type_]
        strings.append(element_template(name, elegant_type, attrs))

    lattice_template = "{}: LINE=({})".format
    for name in sort_lattices(sub_lattices):
        strings.append(lattice_template(name, ", ".join(sub_lattices[name])))

    strings.append(lattice_template("__MAIN__", ", ".join(latticejson["lattice"])))
    strings.append("USE, __MAIN__\n")
    return "\n".join(strings)


def to_madx(latticejson: dict) -> str:
    """Convert a LatticeJSON dict to the MADX lattice file format.

    :param lattice_dict dict: dict in LatticeJSON format
    :return: string with in elegant lattice file format
    """
    elements = latticejson["elements"]
    sub_lattices = latticejson["sub_lattices"]

    strings = [f"TITLE, \"{latticejson['name']}\";"]
    element_template = "{}: {}, {};".format
    for name, (type_, attributes) in elements.items():
        attrs = ", ".join(f"{TO_MADX[k]}={v}" for k, v in attributes.items())
        elegant_type = TO_MADX[type_]
        strings.append(element_template(name, elegant_type, attrs))

    lattice_template = "{}: LINE=({});".format
    for name in sort_lattices(sub_lattices):
        strings.append(lattice_template(name, ", ".join(sub_lattices[name])))

    strings.append(lattice_template("__MAIN__", ", ".join(latticejson["lattice"])))
    strings.append("USE, __MAIN__;\n")
    return "\n".join(strings)


def sort_lattices(lattices: Dict[str, List[str]]) -> List[str]:
    """Returns a sorted list of lattice names for a given dict of lattices."""

    lattices_set = set(lattices)
    lattice_names = []

    def _sort_lattices(name):
        for child_name in lattices[name]:
            if child_name in lattices_set:
                lattices_set.remove(child_name)
                _sort_lattices(child_name)

        lattice_names.append(name)

    while len(lattices_set) > 0:
        _sort_lattices(lattices_set.pop())

    return lattice_names
