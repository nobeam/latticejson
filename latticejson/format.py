# from
# from https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92

import json


class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small lists on single lines."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o):
        """Encode JSON object *o* with respect to single line lists."""
        if isinstance(o, (list, tuple)):
            return "[" + ", ".join(json.dumps(el) for el in o) + "]"
        elif isinstance(o, dict):
            self.indentation_level += 1
            output = [
                self.indent_str + f"{json.dumps(k)}: {self.encode(v)}"
                for k, v in o.items()
            ]
            self.indentation_level -= 1
            return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"
        else:
            return json.dumps(o)

    @property
    def indent_str(self) -> str:
        return " " * self.indentation_level * self.indent
