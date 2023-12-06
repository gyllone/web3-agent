from abc import abstractmethod
from typing import Any, List, Dict
from pydantic import BaseModel, validator

from executor.types.base import Instruction
from executor.types.input import Input
from executor.types.output import Output


_executor_format = """
{name}
{description}
{input}
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
        schema = cls.schema()
        return _executor_format.format(
            name=schema.get("name", "unknown"),
            description=schema.get("description", "nothing"),
            input=cls.input.instruction(),
            output=cls.output.instruction(),
        )
