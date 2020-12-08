def test_to_elegant(fodo_json):
    from latticejson.convert import to_elegant

    elegant = to_elegant(fodo_json)
    print(elegant)


def test_from_elegant(fodo_lte):
    from latticejson.convert import from_elegant

    latticejson = from_elegant(fodo_lte)
    print(latticejson)


def test_elegant_nested_reversed(base_dir):
    """If a lattices is reversed, its sublattices must be reversed too."""
    from latticejson.convert import from_elegant
    from latticejson.utils import flattened_element_sequence

    lattice_file = (base_dir / "nested_reversed_lattice.lte").read_text()
    lattice = from_elegant(lattice_file)
    flattend_sequence = list(flattened_element_sequence(lattice))
    assert ["d2", "d3", "d2", "d1", "d1"] == flattend_sequence


# Uncomment to test for elegant examples
# def test_all_elegant_examples():
#     elegant_examples = Path.home() / "Git/elegant/examples"
#     path_list = list(elegant_examples.rglob("*.lte"))
#     for path in path_list:
#         print(path)
#         latticejson = elegant_to_latticejson(path.read_text())
#         print(latticejson)
#         input()
