from abc import abstractmethod
from pydantic import BaseModel
from langchain.tools import BaseTool


class ToolMaker(BaseModel):

    @classmethod
    @abstractmethod
    def make_tool(cls, **kwargs) -> BaseTool:
        raise NotImplementedError
