def tree(latticejson, name=None):
    lattices = latticejson["lattices"]

    def _tree(name, prefix=""):
        string = f"{name}\n"
        if name in lattices:
            *other, last = lattices[name]
            for child in other:
                string += f"{prefix}├─── {self._print_tree(child, prefix + '│   ')}"
            string += f"{prefix}└─── {self._print_tree(last, prefix + '    ')}"
        return string

    return _tree(latticejson["root"] if name is None else name)


def sort_lattices(lattices, start_lattice):
    lattice_names = []
    lattices_set = set(lattices)

    def _sort_lattices(name):
        for child in lattices[name]:
            if child in lattices_set:
                _sort_lattices(child)
                lattices_set.remove(name)
        lattice_names.append(name)

    _sort_lattices(start_lattice)
    for lattice in lattices_set:
        warn(f"{lattice} is unused and is discarded.", stacklevel=2)
    return lattice_names
