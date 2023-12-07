import json
from abc import abstractmethod
from typing import Iterable, Dict
from pydantic import BaseModel, root_validator


_json_format = """```json
{{
{format}
}}"""


class Instruction(BaseModel):

    @classmethod
    @abstractmethod
    def instruction(cls) -> str:
        pass


class JsonItem(Instruction):

    @root_validator(pre=True)
    def validate(cls, values):
        schema = cls.schema()
        properties: Dict = schema["properties"]
        for item in properties.values():
            cls._check_item(item)
        return values

    @classmethod
    def _check_item(cls, item: Dict):
        tp = item["type"]
        if tp in ["string", "number", "integer", "boolean"]:
            return
        elif tp == "array":
            item = item["items"]
            if item:
                cls._check_item(item)
        elif tp == "object":
            if "additionalProperties" in item:
                cls._check_item(item["additionalProperties"])
        else:
            raise TypeError(f"unknown type {tp}")

    @staticmethod
    def default_value(item: Dict):
        tp = item["type"]
        if tp == "string":
            return ""
        elif tp == "number":
            return 0.0
        elif tp == "integer":
            return 0
        elif tp == "boolean":
            return False
        elif tp == "array":
            return []
        elif tp == "object":
            return {}

    @classmethod
    @abstractmethod
    def _format_lines(cls) -> Iterable[str]:
        pass

    @classmethod
    def instruction(cls) -> str:
        format_str = "\n".join(cls._format_lines())
        return _json_format.format(format=format_str)

    @classmethod
    def example(cls) -> str:
        args = {}
        schema = cls.schema()
        properties: Dict = schema["properties"]
        for name, item in properties.items():
            if "default" in item:
                args[name] = item["default"]
            else:
                tp = item["type"]
                if tp == "string":
                    args[name] = "foo"
                elif tp == "number":
                    args[name] = 0.0
                elif tp == "integer":
                    args[name] = 0
                elif tp == "boolean":
                    args[name] = False
                elif tp == "null":
                    args[name] = None
                elif tp == "array":


                    args[name] = []
                elif tp == "object":
                    args[name] = {}
        return json.dumps(args, indent="\t")



if __name__ == "__main__":
    from typing import List, Dict, Optional
    from pydantic import Field


    class A(JsonItem):
        a: int = Field(0)
        b: float = Field(0.2, description="bbbb")
        c: Optional[List[Dict]] = Field(0, description="cccc")
        d: Dict[str, Dict[str, Dict]] = Field({}, description="dddd")

        @classmethod
        def _format_lines(cls) -> Iterable[str]:
            return ["foo"]


    x = A(a=1, b=2, c=[], d={})
    print(A.example())
    print(x.schema_json(indent="  "))
