from typing import Dict, Iterable, List

from executor.types.base import JsonItem


_input_format = "- **{name}** `{type}` *{optional}*\n{description}"


class Input(JsonItem):

    @classmethod
    def _format_lines(cls) -> Iterable[str]:
        schema = cls.schema()
        properties: Dict = schema["properties"]
        required: List = schema.get("required", [])
        return [
            _input_format.format(
                name=name,
                type=item["type"],
                optional="required" if name in required else "optional",
                description=item.get("description", "nothing"),
            ) for name, item in properties.items()
        ]
