from abc import abstractmethod
from typing import LiteralString
from pydantic import BaseModel
from langchain.tools import BaseTool


class ToolMaker(BaseModel):

    @classmethod
    @abstractmethod
    def name(cls) -> LiteralString:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def description(cls) -> LiteralString:
        raise NotImplementedError

    @abstractmethod
    def make_tool(self, **kwargs) -> BaseTool:
        raise NotImplementedError
