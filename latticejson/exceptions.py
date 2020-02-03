class UndefinedObjectError(Exception):
    """Raised if an object is referenced within a lattice but no definition is found.

    :param str object_name: Name of the undfined object.
    :param str lattice_name: Name of the lattice which contains the undefined object.
    """

    def __init__(self, object_name, lattice_name):
        super().__init__(
            f"The Object {object_name} is referenced in {lattice_name} "
            "but no definition was found!"
        )


class UndefinedRPNVariableError(Exception):
    """Raised if a rpn variable is not defined."""

    def __init__(self, name, *args, **kwargs):
        super().__init__(f"RPN variable {name} is not defined!", *args, **kwargs)
