


def print_tree(latticejson, name=None):
    sub_lattices = latticejson["sub_lattices"]
    lattice = latticejson["lattice"] if name is None else sub_lattices[name]

    def _tree_as_string(name, prefix=""):
        string = name + "\n"
        sub_lattice = sub_lattices.get(name)
        if sub_lattice is not None:
            for obj in sub_lattice[:-1]:
                string += f"{prefix}├─── "
                string += _tree_as_string(obj, prefix + "│   ")

            string += f"{prefix}└─── "
            string += _tree_as_string(sub_lattice[-1], prefix + "    ")
        return string

