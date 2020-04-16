import json
from pathlib import Path

data = json.loads(Path("fodo.json").read_text())
element_name = "Q1"
type_, attributes = data["elements"][element_name]
length = attributes["length"]
print(f"The element {element_name} is a {type_} and is {length} meters long.")
