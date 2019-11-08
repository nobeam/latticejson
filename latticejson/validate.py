import os
import json
import fastjsonschema

dir_name = os.path.dirname(__file__)
schema_path = os.path.join(dir_name, 'schema.json')

with open(schema_path) as schema_file:
    schema = json.load(schema_file)

validate = fastjsonschema.compile(schema)


def validate_file(file_path: str):
    with open(file_path) as lattice_file:
        data = json.load(lattice_file)

    validate(data)
