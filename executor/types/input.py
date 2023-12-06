from typing import Dict, Iterable

from executor.types.base import JsonData


_input_format = '\t"{name}": {type}  // {description} (optional: {optional})'


class Input(JsonData):

    @classmethod
    def _format_lines(cls) -> Iterable[str]:
        schema = cls.schema()
        properties: Dict = schema.get("properties", {})
        required = schema.get("required", [])
        return [
            _input_format.format(
                name=name,
                type=item.get("type", "undefined"),
                description=item.get("description", "nothing"),
                optional=name not in required,
            ) for name, item in properties.items()
        ]
