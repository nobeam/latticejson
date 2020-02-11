import click
import json
from pathlib import Path
import itertools

from .validate import validate_file
from .io import convert as _convert
from .parse import parse_elegant as _parse_elegant
from .format import CompactJSONEncoder
from .migrate import migrate as _migrate


FORMATS = "json", "lte"
dump_latticejson = lambda obj: json.dumps(obj, cls=CompactJSONEncoder, indent=4)


@click.group()
@click.version_option()
def main():
    pass


@main.command()
# @click.argument("file", type=click.Path(exists=True))
@click.argument("file")
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
    """Convert FILE (path or url) to another lattice file format."""
    click.echo(_convert(file, from_, to))


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
    click.echo(dump_latticejson(_parse_elegant(text)))


@main.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    help="Don't write the files back, just output the formatted files.",
)
def autoformat(files, dry_run):
    """Format a LatticeJSON file."""
    for path in itertools.chain.from_iterable(
        path.rglob("*.json") if path.is_dir() else (path,) for path in map(Path, files)
    ):
        latticejson = json.loads(path.read_text())
        formatted = dump_latticejson(latticejson)
        click.secho(f"reformatted {path}", bold=True)
        if dry_run:
            click.echo(formatted)
        else:
            path.write_text(formatted)


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--from", "from_", required=True, help="Initial version")
@click.option("--to", required=True, help="Final version")
def migrate(file, from_, to):
    """Migrate old LatticeJSON files to newer versions."""
    text = Path(file).read_text()
    initial_version = from_.split(".")
    final_version = to.split(".")
    latticejson = _migrate(json.loads(text), initial_version, final_version)
    click.echo(dump_latticejson(latticejson))
