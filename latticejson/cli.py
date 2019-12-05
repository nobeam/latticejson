import click
from .validate import validate_file
from .convert import convert_file


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument('input_format')
@click.argument('output_format')
@click.argument('file', type=click.Path(exists=True))
def convert(**kwargs):
    x = convert_file(kwargs['file'], kwargs['input_format'], kwargs['output_format'])
    print(x)


@main.command()
@click.argument('file', type=click.Path(exists=True))
def validate(**kwargs):
    validate_file(kwargs['file'])
