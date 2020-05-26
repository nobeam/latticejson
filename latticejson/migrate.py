def migrate(data: dict, initial: int, final: int) -> dict:
    data = data.copy()
    for from_, to, func in _VERSION_MAPS:
        if from_ >= initial and (final is None or to <= final):
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
    data["lattices"] = data.pop("sub_lattices")
    data["lattices"]["__MAIN__"] = data.pop("lattice")
    data["root"] = "__MAIN__"
    info = data.pop("description", False)
    if info:
        data["info"] = info

    for _, attributes in data["elements"].values():
        info = attributes.pop("description", False)
        if info:
            attributes["info"] = info


_VERSION_MAPS = (0, 1, _0_to_1), (1, 2, _1_to_2)
MAX_VERSION = _VERSION_MAPS[-1][1]
