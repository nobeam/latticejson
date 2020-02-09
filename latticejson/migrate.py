import sys


def migrate(initial: dict, initial_version: tuple, final_version: tuple):
    function = getattr(
        sys.modules[__name__],
        f"migrate_{'_'.join(initial_version)}_to_{'_'.join(final_version)}",
        None,
    )
    if function is None:
        raise NotImplementedError(f"Unkown versions {initial_version}, {final_version}")

    return function(initial)


def migrate_0_0_2_to_0_0_3(initial: dict):
    final = initial.copy()
    elements_final = {}
    for name, attributes in final["elements"].items():
        type_ = attributes.pop("type")
        elements_final[name] = type_, attributes

    final["elements"] = elements_final
    return final
