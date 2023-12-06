from abc import abstractmethod
from typing import Iterable
from pydantic import BaseModel


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

    @classmethod
    @abstractmethod
    def _format_lines(cls) -> Iterable[str]:
        pass

    @classmethod
    def instruction(cls) -> str:
        format_str = "\n".join(cls._format_lines())
        return _json_format.format(format=format_str)
