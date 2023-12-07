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


class JsonData(Instruction):

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
        if tp in ["string", "number", "integer", "boolean", "null"]:
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

    @classmethod
    @abstractmethod
    def _format_lines(cls) -> Iterable[str]:
        pass

    @classmethod
    def instruction(cls) -> str:
        format_str = "\n".join(cls._format_lines())
        return _json_format.format(format=format_str)


if __name__ == "__main__":
    from typing import List, Dict, Optional
    from pydantic import Field


    class B(BaseModel):
        b: int


    class A(JsonData):
        a: int = Field(description="aaaa")
        b: float = Field(description="bbbb")
        c: Optional[List[Dict]] = Field(description="cccc")
        d: Dict[str, Dict[str, Dict]] = Field(description="dddd")

        @classmethod
        def _format_lines(cls) -> Iterable[str]:
            return ["foo"]


    x = A(a=1, b=2, c=[], d={})
    print(x.schema_json(indent="  "))
