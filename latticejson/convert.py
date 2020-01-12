from typing import List, Dict, Tuple
import re
import json

from .validate import validate


def convert_file(file_path, input_format, output_format):
    if input_format == "json" and output_format == "elegant":
        with open(file_path) as lattice_file:
            lattice_dict = json.load(lattice_file)

        validate(lattice_dict)
        return latticejson_to_elegant(lattice_dict)
    if input_format == "elegant" and output_format == "json":
        with open(file_path) as file:
            string = file.read()

        return elegant_to_latticejson(string)
    else:
        raise NotImplementedError(f"Unknown formats: {input_format}, {output_format}")


LATTICEJSON_ELEGANT_MAPPING: Dict[str, Tuple] = {
    "Drift": ("DRIFT", "DRIF",),
    "Dipole": ("CSBEND", "SBEND", "BEND",),
    "Quadrupole": ("KQUAD", "QUAD", "QUADRUPOLE",),
    "Sextupole": ("KSEXT", "SEXT", "SEXTUPOLE",),
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
PATTERN_LATTICE = re.compile(r"LINE=\((.*)\)")  # TODO: check if correct


def elegant_to_latticejson(string, name="", description=""):
    """Convert elegant lattice file format to latticeJSON dict.

    :param str string: input lattice file as string
    :param name: name of the lattice
    :type str, optional
    :param description: description of the lattice
    :type str, optional
    :return: dict in latticeJSON format
    """
    string = re.sub("[\t ]", "", string)  # Remove all whitespace
    string = re.sub("!.*\n", "\n", string)  # Remove all comments
    string = re.sub("&\n", "", string)  # Join lines which end with &
    string = re.sub("\n+", "\n", string)  # Remove all empty lines
    string = string.lstrip("\n")  # Remove possible leading newline

    elements = {}
    lattices = {}
    lines = string.splitlines()
    label = None
    try:
        for line in lines:
            label, definition = line.split(":")
            match = re.match(PATTERN_LATTICE, definition)
            if match:
                lattices[label] = match.group(1).split(",")
            else:
                type_, *attributes = definition.split(",")
                attributes = [attribute.split("=") for attribute in attributes]
                # TODO: attributes are currently strings
                tmp = dict(
                    (ELEGANT_TO_JSON[key.upper()], value) for key, value in attributes
                )
                elements[label] = {"type": ELEGANT_TO_JSON[type_], **tmp}
    except:
        raise Exception(f"Cannot parse line: {line}")

    main_lattice = lattices.pop(label)  # last lattice is used as main lattice
    return dict(
        name=name,
        description=description,
        lattice=main_lattice,
        sub_lattices=lattices,
        elements=elements,
    )


def latticejson_to_elegant(lattice_dict):
    """Convert latticeJSON dict to elegant lattice file format.

    :param dict: dict in latticeJSON format
    :return: string with in elegant lattice file format
    """
    elements = lattice_dict["elements"]
    sub_lattices = lattice_dict["sub_lattices"]

    elements_string = []
    for name, element in elements.items():
        attributes = ", ".join(
            f"{JSON_TO_ELEGANT[key]}={value}"
            for key, value in element.items()
            if key != "type"
        )
        type_ = JSON_TO_ELEGANT[element["type"]]
        elements_string.append(
            ELEGANT_ELEMENT_TEMPLATE(name=name, type=type_, attributes=attributes)
        )

    ordered_lattices = order_lattices(sub_lattices)
    lattices_string = [
        ELEGANT_LATTICE_TEMPLATE(name=name, objects=", ".join(sub_lattices[name]))
        for name in ordered_lattices
    ]
    lattices_string.append(
        ELEGANT_LATTICE_TEMPLATE(
            name=lattice_dict["name"], objects=", ".join(lattice_dict["lattice"])
        )
    )
    return "\n".join(elements_string + lattices_string)


def order_lattices(cells_dict: Dict[str, List[str]]):
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
