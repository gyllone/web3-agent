from typing import Dict, Iterable, List

from executor.types.base import JsonData


_input_format = '\t"{name}": {type}  // {description} (optional: {optional})'


class Input(JsonData):

    @classmethod
    def _format_lines(cls) -> Iterable[str]:
        schema = cls.schema()
        properties: Dict = schema["properties"]
        required: List = schema.get("required", [])
        return [
            _input_format.format(
                name=name,
                type=item.get("type", "undefined"),
                description=item.get("description", ""),
                optional=name not in required,
            ) for name, item in properties.items()
        ]
