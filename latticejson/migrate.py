from typing import Tuple, Optional

Version = Tuple[int, int, int]


def migrate(data: dict, initial: Version, data: Optional(Version) = None) -> dict:
    data = data.copy()
    for from_, to, func in _VERSION_MAPS:
        if initial >= from_ and (data is None or data <= to):
            func(data)
    return data


_VERSION_MAPS = (
    ((0, 0, 2), (0, 0, 3), _0_0_2_to_0_0_3),
    ((0, 1, 0), (0, 2, 0), _0_1_0_to_0_2_0),
)


def _0_0_2_to_0_0_3(data: dict):
    elements = data["elements"]
    for name, attributes in elements.items():
        elements[name] = attributes.pop("type"), attributes


def _0_1_0_to_0_2_0(data: dict):
    data["title"] = data.pop("name")
    data["info"] = data.pop("description")
    data["lattices"] = data.pop("sub_lattices")
    data["lattices"]["__MAIN__"] = data.pop("lattice")
    data["root"] = "__MAIN__"
    for element in data["elements"]:
        info = element.pop("description", False)
        if info:
            element["info"] = info
