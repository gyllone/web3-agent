from typing import Dict, Iterable, List

from executor.types.json_item import JsonItem


_input_format = "- **{name}** `{type}` *{optional}*\n\n\t{description}"
_output_format = "- **{name}** `{type}`\n\n\t{description}"


class Input(JsonItem):

    @classmethod
    def _format_fields(cls) -> Iterable[str]:
        schema = cls.schema()
        properties: Dict = schema["properties"]
        required: List = schema.get("required", [])
        return [
            _input_format.format(
                name=name,
                type=item["type"],
                optional="required" if name in required else "optional",
                description=item.get("description", "Nothing"),
            ) for name, item in properties.items()
        ]


class Output(JsonItem):

    @classmethod
    def _format_fields(cls) -> Iterable[str]:
        schema = cls.schema()
        properties: Dict = schema["properties"]
        return [
            _output_format.format(
                name=name,
                type=item["type"],
                description=item.get("description", "Nothing"),
            ) for name, item in properties.items()
        ]
