import json
from pathlib import Path
from typing import Dict, List
from warnings import warn

from .exceptions import UnknownAttributeWarning, UnknownElementTypeWarning
from .parse import parse_elegant, parse_madx
from .utils import sort_lattices
from .validate import schema_version

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
    root = lattice_data.get("root", tuple(lattices.keys())[-1])
    title = lattice_data.get("title", "")
    return dict(
        version=str(schema_version),
        title=title,
        root=root,
        elements=elements,
        lattices=lattices,
    )


def to_elegant(latticejson: dict) -> str:
    """Convert a LatticeJSON dict to the elegant lattice file format.

    :param lattice_dict dict: dict in LatticeJSON format
    :return: string with in elegant lattice file format
    """
    elements = latticejson["elements"]
    lattices = latticejson["lattices"]

    strings = [f"! TITLE: {latticejson['title']}"]
    element_template = "{}: {}, {}".format
    # TODO: check if equivalent type exists in elegant
    for name, (type_, attributes) in elements.items():
        attrs = ", ".join(f"{TO_ELEGANT[k]}={v}" for k, v in attributes.items())
        elegant_type = TO_ELEGANT[type_]
        strings.append(element_template(name, elegant_type, attrs))

    lattice_template = "{}: line=({})".format
    for name, children in sort_lattices(latticejson).items():
        strings.append(lattice_template(name, ", ".join(children)))

    strings.append(f"USE, {latticejson['root']}\n")
    return "\n".join(strings)


def to_madx(latticejson: dict) -> str:
    """Convert a LatticeJSON dict to the MADX lattice file format.

    :param lattice_dict dict: dict in LatticeJSON format
    :return: string with in elegant lattice file format
    """
    elements = latticejson["elements"]
    lattices = latticejson["lattices"]

    strings = [f"TITLE, \"{latticejson['title']}\";"]
    element_template = "{}: {}, {};".format
    # TODO: check if equivalent type exists in madx
    for name, (type_, attributes) in elements.items():
        attrs = ", ".join(f"{TO_MADX[k]}={v}" for k, v in attributes.items())
        elegant_type = TO_MADX[type_]
        strings.append(element_template(name, elegant_type, attrs))

    lattice_template = "{}: line=({});".format
    for name, children in sort_lattices(latticejson).items():
        strings.append(lattice_template(name, ", ".join(children)))

    strings.append(f"USE, SEQUENCE={latticejson['root']};\n")
    return "\n".join(strings)
