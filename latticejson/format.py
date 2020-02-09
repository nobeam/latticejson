import json


class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder which only indents the first two levels."""

    def encode(self, obj, level=0):
        if isinstance(obj, dict) and level < 2:
            items_indent = (level + 1) * self.indent * " "
            items_string = ",\n".join(
                f"{items_indent}{json.dumps(key)}: {self.encode(value, level=level+1)}"
                for key, value in obj.items()
            )
            dict_indent = level * self.indent * " "
            newline = "\n" if level == 0 else ""
            return f"{{\n{items_string}\n{dict_indent}}}{newline}"
        else:
            return json.dumps(obj)
