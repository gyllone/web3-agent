from abc import abstractmethod
from typing import get_args, Union, TypeVar, Type, Generic, LiteralString, Callable, Optional, Awaitable
from pydantic import BaseModel
from langchain.tools import BaseTool, Tool
from langchain.callbacks.manager import CallbackManagerForChainRun, AsyncCallbackManagerForChainRun
from langchain.schema.runnable import Runnable, RunnableConfig, RunnableLambda


Input = TypeVar("Input", bound=BaseModel, contravariant=True)
Output = TypeVar("Output", bound=BaseModel, covariant=True)

Processor = Union[
    Callable[[Input], Output],
    Callable[[Input, RunnableConfig], Output],
    Callable[[Input, CallbackManagerForChainRun], Output],
    Callable[[Input, CallbackManagerForChainRun, RunnableConfig], Output],
]
AsyncProcessor = Union[
    Callable[[Input], Awaitable[Output]],
    Callable[[Input, RunnableConfig], Awaitable[Output]],
    Callable[[Input, AsyncCallbackManagerForChainRun], Awaitable[Output]],
    Callable[
        [Input, AsyncCallbackManagerForChainRun, RunnableConfig],
        Awaitable[Output],
    ],
]


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
    def processor(self) -> Optional[Processor]:
        return None

    @property
    def async_processor(self) -> Optional[AsyncProcessor]:
        return None

    @property
    def runnable(self) -> Runnable[Input, Output]:
        if self.processor:
            return RunnableLambda(self.processor, afunc=self.async_processor)
        if self.async_processor:
            return RunnableLambda[Input, Output](self.async_processor)
        raise NotImplementedError("must define at least one process function")

    def tool(self, **kwargs) -> BaseTool:
        return Tool.from_function(
            self.processor,
            self.name(),
            self.description(),
            args_schema=self.input_type(),
            coroutine=self.async_processor,
            **kwargs,
        )
