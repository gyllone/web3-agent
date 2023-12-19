from inspect import signature, Signature
from abc import abstractmethod
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
    def function(self) -> Optional[Callable[..., Output]]:
        return None

    @property
    def async_function(self) -> Optional[Callable[..., Awaitable[Output]]]:
        return None

    @property
    def tool_func(self) -> Optional[ToolFunc]:
        if self.function:
            input_fields = {
                name: (field.annotation, field.default)
                for name, field in self.input_type().__fields__.items()
            }
            func_params = {
                name: (param.annotation, param.default if param.default is not Signature.empty else None)
                for name, param in signature(self.function).parameters.items()
            }
            if input_fields != func_params:
                raise TypeError(f"input fields {input_fields} and function parameters {func_params} don't match")
        return self.function

    @property
    def async_tool_func(self) -> Optional[AsyncToolFunc]:
        if self.async_function:
            input_fields = {
                name: (field.annotation, field.default)
                for name, field in self.input_type().__fields__.items()
            }
            func_params = {
                name: (param.annotation, param.default if param.default is not Signature.empty else None)
                for name, param in signature(self.async_function).parameters.items()
            }
            if input_fields != func_params:
                raise TypeError("input fields and function parameters don't match")
        return self.async_function

    @property
    def runnable_func(self) -> Optional[RunnableFunc]:
        if self.function:
            def _func(_input: Input) -> Output:
                assert self.function is not None
                return self.function(**_input.dict())
            return _func
        else:
            return None

    @property
    def async_runnable_func(self) -> Optional[AsyncRunnableFunc]:
        if self.async_function:
            async def _async_func(_input: Input) -> Output:
                assert self.async_function is not None
                return await self.async_function(**_input.dict())
            return _async_func
        else:
            return None

    @property
    def runnable(self) -> Runnable[Input, Output]:
        if self.runnable_func:
            return RunnableLambda(self.runnable_func, afunc=self.async_runnable_func)
        elif self.async_runnable_func:
            return RunnableLambda[Input, Output](self.async_runnable_func)
        else:
            raise NotImplementedError("must define at least one process function")

    def tool(self, **kwargs) -> BaseTool:
        return StructuredTool.from_function(
            func=self.tool_func,
            coroutine=self.async_tool_func,
            name=self.name(),
            description=self.description(),
            args_schema=self.input_type(),
            **kwargs,
        )
