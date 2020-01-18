from typing import List, Dict, Tuple
from math import pi
import re
import json

from .validate import validate


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
PATTERN_LATTICE = re.compile(r"LINE=\((.*)\)")  # TODO: check if correct


def elegant_to_latticejson(string, name="", description=""):
    """Convert an elegant lattice file to a latticeJSON dict.

    :param str string: input lattice file as string
    :param name: name of the lattice
    :type str, optional
    :param description: description of the lattice
    :type str, optional
    :return: dict in latticeJSON format
    """
    string = re.sub("[\t ]", "", string)  # Remove all whitespace
    string = re.sub("!.*\n", "\n", string)  # Remove all ! comments
    string = re.sub("&\n", "", string)  # Join lines which end with &
    string = re.sub("\n+", "\n", string)  # Remove all \n
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
                element = {"type": ELEGANT_TO_JSON[type_]}
                for key, value in attributes:
                    element[ELEGANT_TO_JSON[key]] = float(value)

                elements[label] = element
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


LATTICEJSON_MAD_MAPPING: Dict[str, Tuple] = {
    "Drift": ("DRIFT",),
    "Dipole": ("SBEND", "RBEND"),
    "Quadrupole": ("QUADRUPOLE",),
    "Sextupole": ("SEXTUPOLE",),
    "Lattice": ("LINE",),
    "length": ("L",),
    "angle": ("ANGLE",),
    "e1": ("E1",),
    "e2": ("E2",),
    "k1": ("K1",),
    "k2": ("K2",),
}

JSON_TO_MAD = {k: v[0] for k, v in LATTICEJSON_MAD_MAPPING.items()}
MAD_TO_JSON = {v: k for k, tup in LATTICEJSON_MAD_MAPPING.items() for v in tup}
MAD_ELEMENT_TEMPLATE = ELEGANT_ELEMENT_TEMPLATE
MAD_LATTICE_TEMPLATE = ELEGANT_LATTICE_TEMPLATE

MAD_CONSTS = dict(PI=pi, TWOPI=2 * pi, DEGRAD=180 / pi, RADDEG=180 / pi)
MAD_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
MAD_CONTROL = {"TITLE", "USE"}


def mad_to_latticejson(string, name="", description=""):
    """Convert a MAD lattice file to a latticeJSON dict.

    :param str string: input lattice file as string
    :param name: name of the lattice
    :type str, optional
    :param description: description of the lattice
    :type str, optional
    :return: dict in latticeJSON format
    """
    string = re.sub("[\t ]", "", string)  # Remove all whitespace
    string = re.sub(MAD_COMMENT, "", string)  # remove /* */ comments
    string = re.sub("//.*\n", "\n", string)  # Remove all // comments
    string = re.sub("\n+", "", string)  # Remove all empty lines
    string = string.rstrip(";")  # Remove trailing ;
    lines = string.split(";")

    elements = {}
    lattices = {}
    variables = {}
    label = None
    title = ""
    try:
        for line in lines:
            if ":=" in line:
                symbol, expr = line.split(":=")
                variables[symbol] = eval(expr, MAD_CONSTS, variables)
            elif ":" in line:
                label, definition = line.split(":")
                match = re.match(PATTERN_LATTICE, definition)
                if match:
                    lattices[label] = match.group(1).split(",")
                else:
                    type_, *attributes = definition.split(",")
                    attributes = [attribute.split("=") for attribute in attributes]
                    element = {"type": MAD_TO_JSON[type_]}
                    for key, expr in attributes:
                        result = eval(expr, MAD_CONSTS, variables)
                        element[MAD_TO_JSON[key]] = result

                    elements[label] = element
            else:
                keyword, value = line.split(",", maxsplit=1)
                keyword = keyword.upper()
                if keyword == "TITLE":
                    title = value
                elif keyword in ("START", STOP)
                else:
                    raise Exception(f"Cannot parse line: {line}")
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
    return "\n".join(strings) + "\n"


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
