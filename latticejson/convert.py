from typing import List, Dict
import json

from .validate import validate


def convert_file(file_path, input_format, output_format):
    if input_format == 'json' and output_format == 'elegant':
        with open(file_path) as lattice_file:
            lattice_dict = json.load(lattice_file)

        validate(lattice_dict)
        return convert_json_to_elegant(lattice_dict)
    else:
        raise NotImplementedError(f'Unknown formats: {input_format}, {output_format}')


JSON_TO_ELEGANT = {
    'Drift': 'DRIF',
    'Dipole': 'CSBEND',
    'Quadrupole': 'KQUAD',
    'Sextupole': 'KSEXT',
    'Lattice': 'LINE',
    'length': 'L',
    'angle': 'ANGLE',
    'e1': 'e1',
    'e2': 'e2',
    'k1': 'K1',
    'k2': 'K2',
}

ELEGANT_TO_JSON = dict(reversed(tup) for tup in JSON_TO_ELEGANT.items())

ELEGANT_ELEMENT_TEMPLATE = '{name}: {type}, {attributes}'.format
ELEGANT_CELL_TEMPLATE = '{name}: LINE=({objects})'.format


def convert_json_to_elegant(lattice_dict):
    elements = lattice_dict['elements']
    sub_lattices = lattice_dict['sub_lattices']

    elements_string = []
    for name, element in elements.items():
        attributes = ', '.join(f'{JSON_TO_ELEGANT[key]}={value}' for key, value in element.items() if key != 'type')
        type_ = JSON_TO_ELEGANT[element['type']]
        elements_string.append(ELEGANT_ELEMENT_TEMPLATE(name=name, type=type_, attributes=attributes))

    ordered_lattices = order_lattices(sub_lattices)
    lattices_string = [
        ELEGANT_CELL_TEMPLATE(name=name, objects=', '.join(sub_lattices[name])) for name in ordered_lattices
    ]
    lattices_string.append(ELEGANT_CELL_TEMPLATE(name=lattice_dict['name'], objects=', '.join(lattice_dict['lattice'])))
    return '\n'.join(elements_string + lattices_string)


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
