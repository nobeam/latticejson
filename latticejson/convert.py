from typing import List, Tuple, Dict
from pathlib import Path
import json
import warnings

from .validate import validate
from .parse import parse_elegant


LATTICEJSON_ELEGANT_MAP: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("Drift", ("DRIF", "DRIFT")),
    ("Dipole", ("CSBEND", "SBEND", "BEND")),
    ("Quadrupole", ("KQUAD", "QUAD", "QUADRUPOLE")),
    ("Sextupole", ("KSEXT", "SEXT", "SEXTUPOLE")),
    ("Lattice", ("LINE",)),
    ("length", ("L",)),
    ("angle", ("ANGLE",)),
    ("e1", ("E1",)),
    ("e2", ("E2",)),
    ("k1", ("K1",)),
    ("k2", ("K2",)),
)
JSON_TO_ELE: Dict[str, str] = {x: y[0] for x, y in LATTICEJSON_ELEGANT_MAP}
ELE_TO_JSON: Dict[str, str] = {y: x for x, tup in LATTICEJSON_ELEGANT_MAP for y in tup}


def latticejson_to_elegant(lattice_dict) -> str:
    """Convert LatticeJSON dict to elegant lattice file format.
    :param dict: dict in LatticeJSON format
    :return: string with in elegant lattice file format
    """
    elements = lattice_dict["elements"]
    sub_lattices = lattice_dict["sub_lattices"]

    strings = []
    element_template = "{}: {}, {}".format
    for name, (type_, attributes) in elements.items():
        attrs = ", ".join(f"{JSON_TO_ELE[k]}={v}" for k, v in attributes.items())
        elegant_type = JSON_TO_ELE[type_]
        strings.append(element_template(name, elegant_type, attrs))

    lattice_template = "{}: LINE=({})".format
    for name in sort_lattices(sub_lattices):
        strings.append(lattice_template(name, ", ".join(sub_lattices[name])))

    name = lattice_dict["name"]
    strings.append(lattice_template(name, ", ".join(lattice_dict["lattice"])))
    strings.append("\n")
    return "\n".join(strings)


def elegant_to_latticejson(string):
    """Convert an elegant lattice file to a LatticeJSON dict.

    :param str string: input lattice file as string
    :param lattice_name: name of the lattice
    :type str, optional
    :param description: description of the lattice
    :type str, optional
    :return: dict in LatticeJSON format
    """
    elegant_dict = parse_elegant(string)

    elements = {}
    for name, (elegant_type, elegant_attributes) in elegant_dict["elements"].items():
        latticejson_type = ELE_TO_JSON.get(elegant_type)
        if latticejson_type is None:
            elements[name] = ["Drift", {"length": elegant_attributes.get("L", 0)}]
            warnings.warn(f"{name} with type {elegant_type} is replaced by Drift.")
            continue

        attributes = {}
        elements[name] = [latticejson_type, attributes]
        for elegant_key, value in elegant_attributes.items():
            latticejson_key = ELE_TO_JSON.get(elegant_key)
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


def sort_lattices_old(lattices: Dict[str, List[str]]) -> List[str]:
    """Returns a sorted list of lattice names for a given dict of lattices."""

    lattices_copy = lattices.copy()
    lattice_names = []

    def _sort_lattices(name, arrangement: List[str]):
        for child_name in arrangement:
            if child_name in lattices_copy:
                _sort_lattices(child_name, lattices_copy[child_name])

        lattice_names.append(name)
        lattices_copy.pop(name)

    for name, arrangement in lattices.items():
        _sort_lattices(name, arrangement)

    return lattice_names


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
