from abc import abstractmethod
from typing import Any
from pydantic import BaseModel, validator
from langchain.output_parsers import PydanticOutputParser


class BaseExecutor(BaseModel):
    input: BaseModel
    output: BaseModel
from typing import Any, List
from pydantic import BaseModel, validator
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


class BaseExecutor(BaseModel):
    id: str
    input: List[BaseModel]
    output: List[BaseModel]

    @classmethod
    @validator("input", pre=True)
    def validate_input(cls, _input: Any):
        if not isinstance(_input, BaseModel):
            raise TypeError("input must be BaseModel")
        if isinstance(_input, List):
            for item in _input:
                if not isinstance(item, BaseModel):
                    raise ValueError("Item must be pydantic model")
        else:
            raise ValueError("Input must be a list")

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
        if isinstance(output, List):
            for item in output:
                if not isinstance(item, BaseModel):
                    raise ValueError("Item must be pydantic model")
        else:
            raise ValueError("Output must be a list")

    def format_instruction(self) -> str:
        input_schema = [item.schema() for item in self.input]