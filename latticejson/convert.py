from typing import List, Tuple, Dict
import json
import warnings
from pathlib import Path

from .validate import validate
from .parser import parse_elegant


LATTICEJSON_ELEGANT_MAPPING: Dict[str, Tuple] = {
    "Drift": ("DRIF", "DRIFT",),
    "Dipole": ("CSBEND", "SBEND", "BEND",),
    "Quadrupole": ("KQUAD", "QUAD",),
    "Sextupole": ("KSEXT", "SEXT",),
    "Lattice": ("LINE",),
    "length": ("L",),
    "angle": ("ANGLE",),
    "e1": ("E1",),
    "e2": ("E2",),
    "k1": ("K1",),
    "k2": ("K2",),
}


JSON_TO_ELEGANT = {k: v[0] for k, v in LATTICEJSON_ELEGANT_MAPPING.items()}
ELEGANT_TO_JSON = {v: k for k, tup in LATTICEJSON_ELEGANT_MAPPING.items() for v in tup}
ELEGANT_ELEMENT_TEMPLATE = "{name}: {type}, {attributes}".format
ELEGANT_LATTICE_TEMPLATE = "{name}: LINE=({objects})".format


def elegant_to_latticejson(string):
    """Convert an elegant lattice file to a latticeJSON dict.

    :param str string: input lattice file as string
    :param lattice_name: name of the lattice
    :type str, optional
    :param description: description of the lattice
    :type str, optional
    :return: dict in latticeJSON format
    """
    elegant_dict = parse_elegant(string)

    elements = {}
    for name, (elegant_type, elegant_attributes) in elegant_dict["elements"].items():
        latticejson_type = ELEGANT_TO_JSON.get(elegant_type)
        if latticejson_type is None:
            elements[name] = "Drift", {"length": elegant_attributes["L"]}
            warnings.warn(f"Element with type {elegant_type} gets replaced by Drift.")
            continue

        attributes = {}
        elements[name] = latticejson_type, attributes
        for elegant_key, value in elegant_attributes.items():
            latticejson_key = ELEGANT_TO_JSON.get(elegant_key)
            if latticejson_key is not None:
                attributes[latticejson_key] = value
            else:
                warnings.warn(f"Ignoring attribute {elegant_key} of element {name}.")

    lattices = elegant_dict["lattices"]
    lattice_name, main_lattice = lattices.popitem()  # use last lattice as main_lattice
    return dict(
        name=lattice_name,
        lattice=main_lattice,
        sub_lattices=lattices,
        elements=elements,
    )


def latticejson_to_elegant(lattice_dict) -> str:
    """Convert latticeJSON dict to elegant lattice file format.
    :param dict: dict in latticeJSON format
    :return: string with in elegant lattice file format
    """
    elements = lattice_dict["elements"]
    sub_lattices = lattice_dict["sub_lattices"]

    strings = []
    for name, element in elements.items():
        type_ = JSON_TO_ELEGANT[element.pop("type")]
        attributes = ", ".join(f"{JSON_TO_ELEGANT[k]}={v}" for k, v in element.items())
        string = ELEGANT_ELEMENT_TEMPLATE(name=name, type=type_, attributes=attributes)
        strings.append(string)

    for name in order_lattices(sub_lattices):
        objects = ", ".join(sub_lattices[name])
        strings.append(ELEGANT_LATTICE_TEMPLATE(name=name, objects=objects))

    name = lattice_dict["name"]
    objects = ", ".join(lattice_dict["lattice"])
    strings.append(ELEGANT_LATTICE_TEMPLATE(name=name, objects=objects))
    strings.append("\n")
    return "\n".join(strings)


def order_lattices(cells_dict: Dict[str, List[str]]):
    """Order a dict of lattices."""

    cells_dict_copy = cells_dict.copy()
    ordered_cells = []

    def _order_lattices(name, cell: List[str]):
        for lattice_name in cell:
            if lattice_name in cells_dict_copy:
                _order_lattices(lattice_name, cells_dict_copy[lattice_name])

        ordered_cells.append(name)
        cells_dict_copy.pop(name)

    for name, cell in cells_dict.items():
        _order_lattices(name, cell)

    return ordered_cells

