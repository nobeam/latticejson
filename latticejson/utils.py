from warnings import warn


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


# TODO: Work in progress!
def remove_unused(latticejson, root=None):
    elements = latticejson["elements"]
    lattices = latticejson["lattices"]
    elements_new = {}
    lattices_new = {}

    def _remove_unused(name):
        element = elements.get(name)
        if name in elements:
            elements_new[name] = elements[name]
        ...

    _remove_unused(root if root is not None else latticejson["root"])
