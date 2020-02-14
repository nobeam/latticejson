# LatticeJSON

LatticeJSON is a JSON based lattice file format. JSON is able to describe complex data structures,
has a human readable syntax and is available in all common programming language. It is therefore an
appropriate choice to characterize the magnetic lattice of a particle accelerator.

## Specification
This repository contains the
[Specification of LatticeJSON](https://github.com/andreasfelix/latticejson/blob/master/latticejson/schema.json)
in form of a [JSON Schema](https://json-schema.org).


## Example

A LatticeJSON file for a FODO lattice:
```json
{
  "name": "FODO_RING",
  "description": "This is the simplest possible strong focusing lattice.",
  "elements": {
    "D1": ["Drift", {"length": 0.55}],
    "Q1": ["Quadrupole", {"length": 0.2, "k1": 1.2}],
    "Q2": ["Quadrupole", {"length": 0.4, "k1": -1.2}],
    "B1": ["Dipole", {"length": 1.5, "angle": 0.392701, "e1": 0.1963505, "e2": 0.1963505}]
  },
  "sub_lattices": {
    "FODO": ["Q1", "D1", "B1", "D1", "Q2", "D1", "B1", "D1", "Q1"]
  },
  "lattice": ["FODO", "FODO", "FODO", "FODO", "FODO", "FODO", "FODO", "FODO"]
}

```


# LatticeJSON CLI
[![Python Version](https://img.shields.io/pypi/pyversions/latticejson)](https://pypi.org/project/latticejson/)
[![PyPI](https://img.shields.io/pypi/v/latticejson.svg)](https://pypi.org/project/latticejson/)
[![CI](https://github.com/andreasfelix/latticejson/workflows/CI/badge.svg)](https://github.com/andreasfelix/latticejson/actions?query=workflow%3ACI)

This repository also contains a Python based command-line tool which is able validate
and convert LatticeJSON files into other common lattice file formats and vice versa.

You can install and update it using pip or pipenv:
```sh
pip install -U latticejson
```

Validate a LatticeJSON file:
```sh
latticejson validate /path/to/lattice.json
```

Convert an elegant lattice file to the LatticeJSON format:
```sh
latticejson convert --to json /path/to/lattice.lte
```

Autoformat one or more LatticeJSON files:
```sh
latticejson autoformat /path/to/lattice.json ...
```

To activate Bash completion add
```
eval "$(_LATTICEJSON_COMPLETE=source latticejson)"
```

to your `.bashrc`. Or, create an activation script with:
```
_LATTICEJSON_COMPLETE=source latticejson > latticejson-complete.sh
```

## License
[GNU General Public License v3.0](https://github.com/andreasfelix/latticejson/blob/master/LICENSE)
