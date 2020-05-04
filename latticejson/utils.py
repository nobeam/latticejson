from warnings import warn
from itertools import chain


def tree(latticejson, name=None):
    lattices = latticejson["lattices"]

    def _tree(name, prefix=""):
        string = f"{name}\n"
        if name in lattices:
            *other, last = lattices[name]
            for child in other:
                string += f"{prefix}├─── {_tree(child, prefix + '│   ')}"
            string += f"{prefix}└─── {_tree(last, prefix + '    ')}"
        return string

    return _tree(latticejson["root"] if name is None else name)


def sort_lattices(latticejson, root=None, keep_unused=False):
    """Returns a sorted dict of lattice objects."""
    lattices = latticejson["lattices"]
    lattices_set = set(lattices)
    lattices_sorted = {}

    def _sort_lattices(name):
        lattices_set.remove(name)
        for child in lattices[name]:
            if child in lattices_set:
                _sort_lattices(child)
        lattices_sorted[name] = lattices[name]

    _sort_lattices(root if root is not None else latticejson["root"])
    if keep_unused:
        while len(lattices_set) > 0:
            _sort_lattices(lattices_set.pop())
    else:
        for lattice in lattices_set:
            warn(f"Discard unused lattice '{lattice}'.")
    return lattices_sorted


def remove_unused(latticejson, root=None, warn_unused=False):
    """Remove unused objects starting from the `root` lattice. Also sorts lattices."""
    if root is None:
        root = latticejson["root"]
    elements = latticejson["elements"]
    lattices = latticejson["lattices"]
    elements_set = set(elements)
    lattices_set = set(lattices)
    elements_new = {}
    lattices_new = {}

    def _remove_unused(name):
        try:
            elements_set.remove(name)
        except KeyError:
            pass
        else:
            elements_new[name] = elements[name]
            return

        try:
            lattices_set.remove(name)
        except KeyError:
            pass
        else:
            lattice = lattices[name]
            for child in lattice:
                _remove_unused(child)
            lattices_new[name] = lattices[name]

    _remove_unused(root)
    latticejson_new = latticejson.copy()
    latticejson_new["root"] = root
    latticejson_new["elements"] = elements_new
    latticejson_new["lattices"] = lattices_new
    if warn_unused:
        for obj in chain(elements_set, lattices_set):
            warn(f"Discard unused object '{obj}'.")
    return latticejson_new
