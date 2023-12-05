from abc import abstractmethod
from typing import Any
from pydantic import BaseModel, validator
from langchain.output_parsers import PydanticOutputParser


class BaseExecutor(BaseModel):
    input: BaseModel
    output: BaseModel

    @classmethod
    @validator("input", pre=True)
    def validate_input(cls, _input: Any):
        if not isinstance(_input, BaseModel):
            raise TypeError("input must be BaseModel")

    @classmethod
    @validator("output", pre=True)
    def validate_output(cls, output: Any):
        if not isinstance(output, BaseModel):
            raise TypeError("output must be BaseModel")

    @classmethod
    @abstractmethod
    def description(cls) -> str:
        pass

    def format_instruction(self) -> str:
        pass