from abc import abstractmethod
from typing import get_args, TypeVar, Type, Generic, LiteralString, Callable, Optional, Awaitable
from pydantic import BaseModel
from langchain.tools import BaseTool, Tool
from langchain.schema.runnable import Runnable, RunnableLambda


Input = TypeVar("Input", bound=BaseModel, contravariant=True)
Output = TypeVar("Output", bound=BaseModel, covariant=True)


class AgentMaker(Generic[Input, Output]):

    @classmethod
    @abstractmethod
    def name(cls) -> LiteralString:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def description(cls) -> LiteralString:
        raise NotImplementedError

    @classmethod
    def input_type(cls) -> Type[Input]:
        """The type of input this runnable accepts specified as a type annotation."""
        for c in cls.__orig_bases__:  # type: ignore[attr-defined]
            type_args = get_args(c)
            if type_args and len(type_args) == 2:
                return type_args[0]
        raise TypeError(f"{cls.__name__} doesn't have an inferable input type.")

    @classmethod
    def output_type(cls) -> Type[Output]:
        for c in cls.__orig_bases__:  # type: ignore[attr-defined]
            type_args = get_args(c)
            if type_args and len(type_args) == 2:
                return type_args[1]
        raise TypeError(f"{cls.__name__} doesn't have an inferable output type.")

    @property
    def processor(self) -> Optional[Callable[[Input], Output]]:
        return None

    @property
    def async_processor(self) -> Optional[Callable[[Input], Awaitable[Output]]]:
        return None

    # TODO: add callback manager
    def wrap_runnable(self, **kwargs) -> Runnable[Input, Output]:
        if self.processor:
            return RunnableLambda(self.processor, afunc=self.async_processor)
        if self.async_processor:
            return RunnableLambda(self.async_processor)
        raise NotImplementedError("must define at least one process function")

    def wrap_tool(self, **kwargs) -> BaseTool:
        return Tool.from_function(
            self.processor,
            self.name(),
            self.description(),
            args_schema=self.input_type(),
            coroutine=self.async_processor,
            **kwargs,
        )
