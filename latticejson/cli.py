import click
from .validate import validate_file
from .io import convert_file


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument("output_format")
@click.argument("file", type=click.Path(exists=True))
def convert(**kwargs):
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
    validate_file(kwargs["file"])
