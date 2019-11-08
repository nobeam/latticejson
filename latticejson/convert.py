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
    'Bend': 'CSBEND',
    'Quad': 'KQUAD',
    'Sext': 'KSEXT',
    'Cell': 'LINE',
    'main_cell': 'RING',
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
    elements_dict = lattice_dict['elements']
    cells_dict = lattice_dict['cells']

    elements_string = []
    for name, element in elements_dict.items():
        attributes = ', '.join(f'{JSON_TO_ELEGANT[key]}={value}' for key, value in element.items() if key != 'type')
        type_ = JSON_TO_ELEGANT[element['type']]
        elements_string.append(ELEGANT_ELEMENT_TEMPLATE(name=name, type=type_, attributes=attributes))

    ordered_cells = order_cells(cells_dict)
    cells_string = [ELEGANT_CELL_TEMPLATE(name=name, objects=', '.join(cells_dict[name])) for name in ordered_cells]
    cells_string.append(ELEGANT_CELL_TEMPLATE(name=lattice_dict['name'], objects=', '.join(lattice_dict['main_cell'])))
    return '\n'.join(elements_string + cells_string)


def order_cells(cells_dict: Dict[str, List[str]]):
    cells_dict_copy = cells_dict.copy()
    ordered_cells = []

    def _order_cells(name, cell: List[str]):
        for cell_name in cell:
            if cell_name in cells_dict_copy:
                _order_cells(cell_name, cells_dict_copy[cell_name])

        ordered_cells.append(name)
        cells_dict_copy.pop(name)

    for name, cell in cells_dict.items():
        _order_cells(name, cell)

    return ordered_cells
