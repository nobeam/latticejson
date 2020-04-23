import click
import json
from pathlib import Path
import itertools

from . import __version__
from .validate import validate_file
from . import io
from .format import format_json
from .migrate import migrate as _migrate
from . import parse


FORMATS = "json", "lte", "madx"


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
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
    click.echo(io.save_string(io.load(file, from_), to))


@cli.command()
@click.argument("file", type=click.Path(exists=True))
def validate(file):
    """Validate a LatticeJSON lattice file."""
    validate_file(file)


@cli.command()
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
        formatted = format_json(latticejson)
        click.secho(f"reformatted {path}", bold=True)
        if dry_run:
            click.echo(formatted)
        else:
            path.write_text(formatted)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--from", "from_", required=True, help="Initial version")
@click.option("--to", required=True, help="Final version")
def migrate(file, from_, to):
    """Migrate old LatticeJSON files to newer versions."""
    text = Path(file).read_text()
    initial_version = from_.split(".")
    final_version = to.split(".")
    latticejson = _migrate(json.loads(text), initial_version, final_version)
    click.echo(format_json(latticejson))


@cli.group()
def debug():
    """Some useful commands for debugging/development."""
    pass


@debug.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--transform", "-t", is_flag=True, help="Print transformed tree.")
def parse_elegant(file, transform):
    """Print parse tree of elegant lattice file."""
    text = Path(file).read_text()
    if transform:
        click.echo(format_json(parse.parse_elegant(text)))
    else:
        click.echo(parse.ELEGANT_PARSER.parse(text).pretty())


@debug.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--transform", "-t", is_flag=True, help="Print transformed tree.")
def parse_madx(file, transform):
    """Print parse tree of madx lattice file."""
    text = Path(file).read_text()
    if transform:
        click.echo(format_json(parse.parse_madx(text)))
    else:
        click.echo(parse.MADX_PARSER.parse(text).pretty())
