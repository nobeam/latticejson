import click
import json
from pathlib import Path

from .validate import validate_file
from .io import convert as _convert
from .parse import parse_elegant as _parse_elegant
from .format import CompactJSONEncoder
from .migrate import migrate as _migrate


FORMATS = "json", "lte"
print_latticejson = lambda obj: print(json.dumps(obj, cls=CompactJSONEncoder, indent=4))


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--from",
    "from_",
    type=click.Choice(FORMATS, case_sensitive=False),
    help="Source format [optional, default: use file extension]",
)
@click.option(
    "--to",
    required=True,
    type=click.Choice(FORMATS, case_sensitive=False),
    help="Destination format",
)
def convert(file, from_, to):
    """Convert a LatticeJSON or elegant file into another format."""
    path = Path(file)
    if from_ is None:
        from_ = path.suffix[1:]

    print(_convert(path.read_text(), from_, to))


@main.command()
@click.argument("file", type=click.Path(exists=True))
def validate(file):
    """Validate a LatticeJSON lattice file."""
    validate_file(file)


@main.command()
@click.argument("file", type=click.Path(exists=True))
def parse_elegant(file):
    """Parse elegant file but do not convert to LatticeJSON."""
    text = Path(file).read_text()
    print(json.dumps(_parse_elegant(text), cls=CompactJSONEncoder, indent=4))


@main.command()
@click.argument("file", type=click.Path(exists=True))
def autoformat(file):
    """Format a LatticeJSON file."""
    latticejson = json.loads(Path(file).read_text())
    print(json.dumps(latticejson, cls=CompactJSONEncoder, indent=4))


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--from", "from_", required=True, help="Initial version")
@click.option("--to", required=True, help="Final version")
def migrate(file, from_, to):
    """Migrate old LatticeJSON files to newer versions."""
    text = Path(file).read_text()
    initial_version = from_.split(".")
    final_version = to.split(".")
    res = _migrate(json.loads(text), initial_version, final_version)
    print(json.dumps(res, cls=CompactJSONEncoder, indent=4))
