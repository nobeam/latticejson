import json
from pathlib import Path
from typing import AnyStr, Tuple, Union
from urllib.parse import urlparse
from urllib.request import urlopen

from . import convert
from .format import format_json
from .validate import validate as _validate


def load(location: Union[AnyStr, Path], file_format=None, validate=True) -> dict:
    """Deserialize a lattice file to LatticeJSON-compliant dictionary.

    :param location: path-like or url-like
    :type location: Union[AnyStr, Path]
    :param file_format: File format of the lattice file
    :type file_format: str, optional
    :param validate: Whether to validate the input file.
    :type validate: bool
    :return dict: Deserialized lattice file
    """
    return load_string(*_load_file(location, file_format), validate)


def load_string(string: str, input_format: str, validate: bool = True) -> dict:
    """Deserialize a string to a LatticeJSON-compliant dictionary.

    :param string str: Content of the input lattice file.
    :param input_format: Input format of the input lattice file.
    :type input_format: str, optional
    :param input_format str: Input format of the input lattice file.
    :param validate: Whether to validate the input file.
    :type validate: bool
    :return dict: Returns deserialized lattice file as dict.
    """
    if input_format == "json":
        latticejson = json.loads(string)
    elif input_format == "lte":
        latticejson = convert.from_elegant(string)
    elif input_format == "madx":
        latticejson = convert.from_madx(string)
    else:
        raise NotImplementedError(f"Unknown lattice file format: {input_format}.")

    if validate:
        _validate(latticejson)
    return latticejson


def _load_file(location: Union[AnyStr, Path], file_format=None) -> Tuple[str, str]:
    """Return the content of the file at a given path or URL.

    :param location: path-like or url-like
    :type location: Union[AnyStr, Path]
    :param file_format: File format
    :type file_format: str, optional
    :return dict: Content of file as string
    """
    parse_result = urlparse(str(location))
    path = Path(parse_result.path)
    if file_format is None:
        file_format = path.suffix[1:]

    is_path = parse_result.scheme == ""
    if is_path:
        text = Path(location).read_text()
    else:
        text = urlopen(location).read()
    return text, file_format


def save(latticejson: dict, path: str, output_format=None):
    """Serialize LatticeJSON-compliant dictionary to different lattice file formats.

    :param latticejson dict: A LatticeJSON-compliant dictionary.
    :param path Union[AnyStr, Path]: Output path.
    :param output_format str: Output format.
    :raises NotImplementedError: Is raised for unknown lattice file formats.
    """
    path = Path(path)
    if output_format is None:
        output_format = path.suffix[1:]

    path.write_text(save_string(latticejson, output_format))


def save_string(latticejson: dict, output_format: str) -> str:
    """Serialize LatticeJSON-compliant dictionary to different lattice file formats.

    :param latticejson dict: A LatticeJSON-compliant dictionary.
    :param output_format str: Output format.
    :raises NotImplementedError: Is raised for unknown lattice file formats.
    :return: Returns lattice file in `output_format` as string.
    :rtype: str
    """
    if output_format == "json":
        return format_json(latticejson)
    elif output_format == "lte":
        return convert.to_elegant(latticejson)
    elif output_format == "madx":
        return convert.to_madx(latticejson)
    raise NotImplementedError(f"Converting to {output_format} is not implemented!")
