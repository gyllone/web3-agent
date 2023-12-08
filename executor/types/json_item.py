import json

from abc import abstractmethod
from typing import Iterable, Dict, Any
from pydantic import root_validator

from executor.types.instruction import Instruction


_json_item_format = """{fields}

Example:
```json
{example}
```"""


class JsonItem(Instruction):

    @root_validator(pre=True)
    def validate(cls, values):
        schema = cls.schema()
        properties: Dict = schema["properties"]
        for item in properties.values():
            cls._check_item(item)
        return values

    @staticmethod
    def _check_item(item: Dict):
        if "type" not in item:
            raise TypeError("must define type in item")
        tp = item["type"]
        if tp in ["string", "number", "integer", "boolean"]:
            return
        elif tp == "array":
            item = item["items"]
            if item:
                JsonItem._check_item(item)
            else:
                raise TypeError("must define item in array")
        elif tp == "object":
            if "additionalProperties" in item:
                JsonItem._check_item(item["additionalProperties"])
            else:
                raise TypeError("must define additionalProperties in object")
        else:
            raise TypeError(f"unknown type {tp}")

    @staticmethod
    def _default_value(item: Dict) -> Any:
        if "type" not in item:
            raise TypeError("must define type in item")
        tp = item["type"]
        if tp == "string":
            return "hello"
        elif tp == "number":
            return 1.23
        elif tp == "integer":
            return 123
        elif tp == "boolean":
            return False
        elif tp == "array":
            item = item["items"]
            if item:
                return [JsonItem._default_value(item)]
            else:
                raise TypeError("must define item in array")
        elif tp == "object":
            if "additionalProperties" in item:
                value = JsonItem._default_value(item["additionalProperties"])
                return {
                    "foo": value,
                    "bar": value,
                }
            else:
                raise TypeError("must define additionalProperties in object")
        else:
            raise TypeError(f"unknown type {tp}")

    @classmethod
    @abstractmethod
    def _format_fields(cls) -> Iterable[str]:
        pass

    @classmethod
    def instruction(cls) -> str:
        fields = "\n".join(cls._format_fields())
        example = cls.json_example()
        return _json_item_format.format(fields=fields, example=example)

    @classmethod
    def json_example(cls) -> str:
        schema = cls.schema()
        properties: Dict = schema["properties"]
        args = {name: cls._default_value(item) for name, item in properties.items()}
        return json.dumps(args, indent="  ")
