def test_flattened_element_sequence(fodo_json):
    from latticejson.utils import flattened_element_sequence

    sequence = list(flattened_element_sequence(fodo_json, start_lattice="cell"))
    assert ["q1", "d1", "b1", "d1", "q2", "d1", "b1", "d1", "q1"] == sequence
