import click
import json
from pathlib import Path

from .validate import validate_file
from .io import convert_file
from .parse import parse_elegant as _parse_elegant


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument("output_format")
@click.argument("file", type=click.Path(exists=True))
def convert(**kwargs):
    """Convert a latticeJSON or elegant file into another format."""
    output_format = kwargs["output_format"].lower()
    if output_format in ("latticejson", "lj", "json"):
        output_format = "latticejson"
    elif output_format in ("elegant", "ele", "lte"):
        output_format = "elegant"
    else:
        raise Exception(f"Unknown format {output_format}")

    res = convert_file(kwargs["file"], output_format)
    print(res)


@main.command()
@click.argument("file", type=click.Path(exists=True))
def validate(**kwargs):
    """Validate a latticeJSON lattice file."""
    validate_file(kwargs["file"])


@main.command()
@click.argument("file", type=click.Path(exists=True))
def parse_elegant(**kwargs):
    """Parse elegant file but do not convert to latticeJSON."""
    text = Path(kwargs["file"]).read_text()
    print(json.dumps(_parse_elegant(text), indent=4))
