def test_flattened_element_sequence(fodo_json):
    from latticejson.utils import flattened_element_sequence

    sequence = list(flattened_element_sequence(fodo_json, start_lattice="CELL"))
    assert ["Q1", "D1", "B1", "D1", "Q2", "D1", "B1", "D1", "Q1"] == sequence
