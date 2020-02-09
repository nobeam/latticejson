import json


class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder which only indents the first two level."""

    def encode(self, obj, level=0):
        """Encode JSON object *obj*."""
        if isinstance(obj, (list, tuple)):
            return f"[{', '.join(json.dumps(el) for el in obj)}]"
        elif isinstance(obj, dict) and level < 2:
            indent = (level + 1) * self.indent * " "
            items = ",\n".join(
                f"{indent}{json.dumps(key)}: {self.encode(value, level=level+1)}"
                for key, value in obj.items()
            )
            return f"{{\n{items}\n{level * self.indent * ' '}}}"
        else:
            return json.dumps(obj)
