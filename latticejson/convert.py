from typing import List, Dict
import json

from .validate import validate


def convert_file(file_path, input_format, output_format):
    if input_format == "json" and output_format == "elegant":
        with open(file_path) as lattice_file:
            lattice_dict = json.load(lattice_file)

        validate(lattice_dict)
        return convert_json_to_elegant(lattice_dict)
    else:
        raise NotImplementedError(f"Unknown formats: {input_format}, {output_format}")


JSON_TO_ELEGANT = {
    "Drift": "DRIF",
    "Dipole": "CSBEND",
    "Quadrupole": "KQUAD",
    "Sextupole": "KSEXT",
    "Lattice": "LINE",
    "length": "L",
    "angle": "ANGLE",
    "e1": "e1",
    "e2": "e2",
    "k1": "K1",
    "k2": "K2",
}

ELEGANT_TO_JSON = {value: key for key, value in JSON_TO_ELEGANT.items()}

ELEGANT_ELEMENT_TEMPLATE = "{name}: {type}, {attributes}".format
ELEGANT_CELL_TEMPLATE = "{name}: LINE=({objects})".format


def elegant_to_json(elegant_string)
    lines = re.sub("[ \t]", "", file.read()).splitlines()
    lines = [line for line in lines if line and line[0] != "#"]

    # divide lines into object_name, type, parameter and comment
    length = len(lines)
    object_name = [""] * length
    type = [""] * length
    parameters = [""] * length
    comments = [""] * length
    following_lines = []
    starting_line = 0
    for i, line in enumerate(lines):
        # save comments
        _split = line.split("#")
        if len(_split) > 1:
            comments[i] = _split[1]
        _split = _split[0]

        # divide into starting and following lines
        _split = _split.split(":")
        if len(_split) > 1:
            starting_line = i
            object_name[i] = _split[0]
            _split = _split[1].split(",", maxsplit=1)
            type[i] = _split[0]
            parameters[i] = _split[1]
        else:
            following_lines.append(i)
            parameters[starting_line] += _split[0]
            if comments[i]:
                comments[starting_line] += " " + comments[i]

    # delete following lines (in reverse order)
    for i in following_lines[::-1]:
        del object_name[i]
        del comments[i]
        del parameters[i]

    # create and execute string
    lis = [
        f'{object_name[i]} = {type[i]}("{object_name[i]}", {parameters[i]}, comment="{comments[i]}")'
        for i in range(len(object_name))
    ]
    string = "\n".join(lis)
    # print(string)
    exec(string)
    return list(locals().values())[-1]


def convert_json_to_elegant(lattice_dict):
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
        ELEGANT_CELL_TEMPLATE(name=name, objects=", ".join(sub_lattices[name]))
        for name in ordered_lattices
    ]
    lattices_string.append(
        ELEGANT_CELL_TEMPLATE(
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
