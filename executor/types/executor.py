from abc import abstractmethod
from typing import Any
from pydantic import validator

from executor.types.json_item import Instruction
from executor.types.io import Input, Output


_executor_format = """
# {name}
{description}
## Inputs
{input}
## Outputs
{output}
"""


class Executor(Instruction):
    input: Input
    output: Output

    @classmethod
    @validator("input", pre=True)
    def validate_input(cls, _input: Any):
        if not isinstance(_input, Input):
            raise ValueError("input must be Input")

    @classmethod
    @validator("output", pre=True)
    def validate_output(cls, output: Any):
        if not isinstance(output, Output):
            raise ValueError("output must be Output")

    @classmethod
    def instruction(cls) -> str:
        return _executor_format.format(
            name=cls.title(),
            usage=cls.description(),
            input=cls.input_instruction(),
            output=cls.output_instruction(),
        )

    @classmethod
    def title(cls) -> str:
        return cls.schema()["title"]

    @classmethod
    def description(cls) -> str:
        return cls.schema()["description"]

    @classmethod
    def input_instruction(cls) -> str:
        return cls.__annotations__["input"].instruction()

    @classmethod
    def output_instruction(cls) -> str:
        return cls.__annotations__["output"].instruction()

    def execute(self, _input: Input, **kwargs) -> Output:
        raise NotImplementedError

    async def async_execute(self, _input: Input, **kwargs) -> Output:
        raise NotImplementedError
