from typing import Optional, List, Generic, TypeVar, Type
from pydantic import BaseModel, Field
from langchain.schema import BaseOutputParser
from langchain.output_parsers.json import parse_and_check_json_markdown
from langchain.output_parsers.pydantic import PydanticOutputParser


T = TypeVar("T", bound=BaseModel)


# class ArgumentSchema(Generic[T], BaseModel):
#     """A schema for a parameter from a structured output parser."""
#
#     object: Type[T]
#
#     name: str
#     description: str
#     type: str = "string"
#     optional: bool = False
#
#     _line_format = '\t"{name}": {type}  // {description} (optional: {optional})'
#
#     @classmethod
#     def from_argument(cls, argument: BaseModel) -> "ArgumentSchema":
#         schema = argument.schema()
#         return ArgumentSchema(
#             name=self.name,
#             description=self.description,
#             type=self.type,
#             optional=self.optional,
#         )
#
#     def format_line(self) -> str:
#         return self._line_format.format(
#             name=self.name, description=self.description, type=self.type, optional=self.optional
#         )


# class ArgumentsOutputParser(BaseOutputParser):
#     """Parse the output of an LLM call to arguments."""
#
#     argument_schemas: List[ArgumentSchema]
#
#     _template = """```json
# {{
# {format}
# }}"""
#
#     @classmethod
#     def from_argument_schemas(cls, argument_schemas: List[ArgumentSchema]) -> "ArgumentsOutputParser":
#         return cls(argument_schemas=argument_schemas)
#
#     def get_format_instructions(self) -> str:
#         return self._template.format(
#             format="\n".join([schema.format_line() for schema in self.argument_schemas])
#         )
#
#     def parse(self, text: str) -> dict[str, str]:
#         expected_keys = [schema.name for schema in self.argument_schemas]
#         return parse_and_check_json_markdown(text, expected_keys)
#
#     @property
#     def _type(self) -> str:
#         return "arguments"


class ExecutorOutputParser(BaseOutputParser[T]):
    """Parse the output of an LLM call to executor."""

    object: Type[T]

    _line_format = '\t"{name}": {type}  // {description} (optional: {optional})'
    _json_format = """```
json
{{
{format}
}}"""
    _pydantic_format = """
function name: {name}

"""

    def parse(self, text: str) -> T:
        pass

    def get_format_instructions(self) -> str:
        schema = self.object.schema()




