from typing import Optional, Tuple

Version = Tuple[int, int, int]


def migrate(data: dict, initial: Version, final: Optional[Version] = None) -> dict:
    data = data.copy()
    for from_, to, func in _VERSION_MAPS:
        if initial >= from_ and (final is None or final <= to):
            func(data)
    return data


def _0_to_1(data: dict):
    data["version"] = "1.0"
    elements = data["elements"]
    for name, attributes in elements.items():
        elements[name] = attributes.pop("type"), attributes


def _1_to_2(data: dict):
    data["version"] = "2.0"
    data["title"] = data.pop("name")
    data["info"] = data.pop("description")
    data["lattices"] = data.pop("sub_lattices")
    data["lattices"]["__MAIN__"] = data.pop("lattice")
    data["root"] = "__MAIN__"
    for element in data["elements"]:
        info = element.pop("description", False)
        if info:
            element["info"] = info


_VERSION_MAPS = (0, 1, _0_to_1), (1, 2, _1_to_2)
