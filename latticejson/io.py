from typing import Tuple, Dict, Union, AnyStr
from pathlib import Path
import json
from .convert import elegant_to_latticejson, latticejson_to_elegant
from .validate import validate
from urllib.parse import urlparse
from urllib.request import urlopen


def load(location: str, file_format=None) -> Dict:
    """Deserialize the lattice file at `location` to Python dictionary.

    :param location: path-like or url-like string which locates the lattice file
    :type location: Union[AnyStr, Path]
    :param file_format str: File format of the lattice file
    :type file_format: str, optional
    :return dict: Deserialized lattice file
    """
    return load_string(*_load_location(location, file_format))


def load_string(text: str, file_format: str) -> Dict:
    """Deserialize and validate `text` to a LatticeJSON dict."""
    if file_format == "json":
        latticejson = json.loads(text)
    elif file_format == "lte":
        latticejson = elegant_to_latticejson(text)
    else:
        raise NotImplementedError(f"Unkown file file_format {file_format}.")

    validate(latticejson)
    return latticejson


def convert(location, input_format, output_format) -> str:
    return convert_string(*_load_location(location, input_format), output_format)


def convert_string(text, input_format, output_format) -> str:
    """Convert lattice file to format.

    :param text str: Content of the input lattice file.
    :param input_format str: Input format of the source lattice file.
    :param output_format str: Ouput format of the new lattice file.
    :raises NotImplementedError: Is raised for unkown lattice file formats.
    :return: Returns new lattice file as string
    :rtype: str
    """
    lattice_json = load_string(text, input_format)
    if output_format == "json":
        return json.dumps(lattice_json, indent=4)
    elif output_format == "lte":
        return latticejson_to_elegant(lattice_json)
    raise NotImplementedError(f"Converting to {output_format} is not implemented!")


def _load_location(location, file_format=None) -> Tuple[str, str]:
    """Return the content of the file at `location` as string.

    :param location: path-like or url-like
    :type location: Union[AnyStr, Path]
    :param file_format: File format of the lattice file
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
