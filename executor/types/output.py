from typing import Dict, Iterable

from executor.types.base import JsonData


_output_format = '\t"{name}": {type}  // {description}'


class Output(JsonData):

    @classmethod
    def _format_lines(cls) -> Iterable[str]:
        schema = cls.schema()
        properties: Dict = schema.get("properties", {})
        return [
            _output_format.format(
                name=name,
                type=item.get("type", "undefined"),
                description=item.get("description", "nothing"),
            ) for name, item in properties.items()
        ]
