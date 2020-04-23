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


class UnknownElementWarning(UserWarning):
    """Raised if there is no equivalent LatticeJSON element."""

    def __init__(self, name, type_, *args, **kwargs):
        message = f"Replacing element {name} ({type_}) with Drift."
        super().__init__(message, *args, **kwargs)


class UnknownAttributeWarning(UserWarning):
    """Raised if there is no equivalent LatticeJSON attribute."""

    def __init__(self, attribute, element, *args, **kwargs):
        message = f"Ignoring attribute {attribute} of {element}."
        super().__init__(message, *args, **kwargs)


class UndefinedVariableError(Exception):
    """Raised if a rpn variable is not defined."""

    def __init__(self, name, *args, **kwargs):
        super().__init__(f"The variable '{name}' is not defined!", *args, **kwargs)
