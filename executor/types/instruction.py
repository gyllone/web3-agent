from abc import abstractmethod
from pydantic import BaseModel


class Instruction(BaseModel):

    @classmethod
    @abstractmethod
    def instruction(cls) -> str:
        pass
