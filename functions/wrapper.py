import inspect
from abc import abstractmethod
from inspect import signature
from typing import get_args, Union, TypeVar, Type, Generic, LiteralString, Callable, Optional, Awaitable
from pydantic.v1 import BaseModel
from langchain.tools import BaseTool, StructuredTool
from langchain.callbacks.manager import CallbackManagerForChainRun, AsyncCallbackManagerForChainRun
from langchain.schema.runnable import Runnable, RunnableConfig, RunnableLambda


Input = TypeVar("Input", bound=BaseModel, contravariant=True)
Output = TypeVar("Output", bound=BaseModel, covariant=True)

RunnableFunc = Union[
    Callable[[Input], Output],
    Callable[[Input, RunnableConfig], Output],
    Callable[[Input, CallbackManagerForChainRun], Output],
    Callable[[Input, CallbackManagerForChainRun, RunnableConfig], Output],
]
AsyncRunnableFunc = Union[
    Callable[[Input], Awaitable[Output]],
    Callable[[Input, RunnableConfig], Awaitable[Output]],
    Callable[[Input, AsyncCallbackManagerForChainRun], Awaitable[Output]],
    Callable[
        [Input, AsyncCallbackManagerForChainRun, RunnableConfig],
        Awaitable[Output],
    ],
]

ToolFunc = Callable[..., Output]
AsyncToolFunc = Callable[..., Awaitable[Output]]


class FunctionWrapper(Generic[Input, Output]):
    """A wrapper which wraps a function to either a runnable or a tool."""

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
        """The type of output this runnable accepts specified as a type annotation."""
        for c in cls.__orig_bases__:  # type: ignore[attr-defined]
            type_args = get_args(c)
            if type_args and len(type_args) == 2:
                return type_args[1]
        raise TypeError(f"{cls.__name__} doesn't have an inferable output type.")

    @property
    def function(self) -> Optional[Callable[[Input], Output]]:
        return None

    @property
    def async_function(self) -> Optional[Callable[[Input], Awaitable[Output]]]:
        return None

    @property
    def _runnable_func(self) -> Optional[RunnableFunc]:
        return self.function

    @property
    def _async_runnable_func(self) -> Optional[AsyncRunnableFunc]:
        return self.async_function

    @property
    def _tool_func(self) -> Optional[ToolFunc]:
        if self.function:
            params = list(signature(self.function).parameters.values())
            param = params[0]
            assert inspect.isclass(param.annotation)
            fields = param.annotation.__fields__.keys()

            def _func(*args) -> Output:
                if len(args) != len(fields):
                    raise ValueError(f"Expected {len(fields)} args, got {len(args)}")
                _input = param.annotation(**dict(zip(fields, args)))
                assert self.function is not None
                return self.function(_input)

            return _func
        else:
            return None

    @property
    def _async_tool_func(self) -> Optional[AsyncToolFunc]:
        if self.async_function:
            params = list(signature(self.async_function).parameters.values())
            param = params[0]
            assert inspect.isclass(param.annotation)
            fields = param.annotation.__fields__.keys()

            async def _async_func(*args) -> Output:
                if len(args) != len(fields):
                    raise ValueError(f"Expected {len(fields)} args, got {len(args)}")
                _input = param.annotation(**dict(zip(fields, args)))
                assert self.async_function is not None
                return await self.async_function(_input)

            return _async_func
        else:
            return None

    @property
    def runnable(self) -> Runnable[Input, Output]:
        if self._runnable_func:
            return RunnableLambda(self._runnable_func, afunc=self._async_runnable_func)
        elif self._async_runnable_func:
            return RunnableLambda[Input, Output](self._async_runnable_func)
        else:
            raise NotImplementedError("must define at least one process function")

    def tool(self, **kwargs) -> BaseTool:
        return StructuredTool.from_function(
            func=self._tool_func,
            coroutine=self._async_tool_func,
            name=self.name(),
            description=self.description(),
            args_schema=self.input_type(),
            **kwargs,
        )
