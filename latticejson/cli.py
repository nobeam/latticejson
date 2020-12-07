import itertools
import json
import sys
from pathlib import Path

import click

from . import __version__, io, parse
from .format import format_json
from .migrate import MAX_VERSION
from .migrate import migrate as _migrate
from .validate import parse_version, schema, validate_file

FORMATS = "json", "lte", "madx"


@click.group(context_settings=dict(max_content_width=120))
@click.version_option(
    message=(f"LatticeJSON CLI, version {__version__}\n{schema['title']}")
)
def cli():
    pass


@cli.command()
@click.option(
    "--file",
    type=click.File("r"),
    default=sys.stdin,
    help="Path to the lattice file to convert. Defaults to stdin.",
)
@click.option(
    "--from",
    "from_",
    required=True,
    type=click.Choice(FORMATS, case_sensitive=False),
    help="Source format",
)
@click.option(
    "--to",
    required=True,
    type=click.Choice(FORMATS, case_sensitive=False),
    help="Destination format",
)
@click.option(
    "--validate/--no-validate", default=True, help="Whether to validate the input file."
)
def convert(file, from_, to, validate):
    """Convert stdin or FILE to another lattice file format."""
    with file:
        data = file.read()
    click.echo(io.save_string(io.load_string(data, from_, validate), to))


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
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--final", type=int, default=MAX_VERSION, show_default=True, help="Final version."
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    help="Don't write the files back, just output the formatted files.",
)
def migrate(files, final, dry_run):
    """Migrate old LatticeJSON files to newer versions."""
    for path in itertools.chain.from_iterable(
        path.rglob("*.json") if path.is_dir() else (path,) for path in map(Path, files)
    ):
        data = json.loads(path.read_text())
        initial = parse_version(data["version"]).major
        latticejson = _migrate(data, initial, final)
        formatted = format_json(latticejson)
        click.secho(f"Migrated {path} from version {initial} to {final}", bold=True)
        if dry_run:
            click.echo(formatted)
        else:
            path.write_text(formatted)


@cli.group()
def utils():
    """Some useful utilities."""
    pass


@utils.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--lattice", "-l", type=str, help="Root lattice of tree.")
@click.option(
    "--format",
    "format_",
    type=click.Choice(FORMATS, case_sensitive=False),
    help="Source format [optional, default: use file extension]",
)
def tree(file, lattice, format_):
    """Print tree of elements for a given LatticeJSON file."""
    from .utils import tree

    data = io.load(file, format_, validate)
    click.echo(tree(data, lattice))


@utils.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--lattice", "-l", type=str, help="New root lattice [Default: current]")
@click.option("--warn-unused", "-w", is_flag=True, help="Log removed lattices.")
@click.option(
    "--validate/--no-validate", default=True, help="Whether to validate the input file."
)
def remove_unused(file, lattice, warn_unused, validate):
    """Remove unused objects from a LatticeJSON file."""
    from .utils import remove_unused

    data = remove_unused(io.load(file, validate=validate), lattice, warn_unused)
    click.echo(format_json(data))


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
