from abc import abstractmethod
from pydantic import BaseModel
from langchain.tools import BaseTool


class ToolMaker(BaseModel):

    @abstractmethod
    def make_tool(self, **kwargs) -> BaseTool:
        raise NotImplementedError
