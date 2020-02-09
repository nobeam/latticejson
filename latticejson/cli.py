import click
import json
from pathlib import Path

from .validate import validate_file
from .io import convert_file
from .parse import parse_elegant as _parse_elegant
from .format import CompactJSONEncoder
from .migrate import migrate as _migrate


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--to",
    required=True,
    type=click.Choice(["json", "lte"], case_sensitive=False),
    help="Destination format.",
)
def convert(file, to):
    """Convert a LatticeJSON or elegant file into another format."""
    print(convert_file(file, to))


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
    print(json.dumps(_parse_elegant(text), indent=4))


@main.command()
@click.argument("file", type=click.Path(exists=True))
def autoformat(file):
    """Format a LatticeJson file."""
    latticejson = json.loads(Path(file).read_text())
    print(json.dumps(latticejson, cls=CompactJSONEncoder, indent=4))


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--from", "from_", required=True, help="Initial version")
@click.option("--to", required=True, help="Final version")
def migrate(file, from_, to):
    """Migrate old LatticeJSON formats to newer versions."""
    text = Path(file).read_text()
    initial_version = from_.split(".")
    final_version = to.split(".")
    print(f"Migrating {file} from {initial_version} to {final_version}")
    res = _migrate(json.loads(text), initial_version, final_version)
    print(json.dumps(res, cls=CompactJSONEncoder, indent=4))
