if __name__ == "__main__":
    from typing import List, Dict, Optional
    from pydantic import Field, BaseModel

    from executor.types.input import Input
    from executor.types.output import Output
    from executor.types.executor import Executor

    class TestInput(Input):
        a: str = Field(description="This is a description of a.")
        b: Optional[int] = Field(description="This is a description of b.")
        c: Optional[float] = Field(description="This is a description of c.")
        d: List[str] = Field(description="This is a description of d.")
        e: Dict[str, str]

    class TestOutput(Output):
        a: str = Field(description="This is a description of a.")
        b: int = Field(description="This is a description of b.")
        c: float = Field(description="This is a description of c.")
        d: List[str] = Field(description="This is a description of d.")
        e: Dict[str, str]

    class TestExecutor(Executor):
        input: TestInput
        output: TestOutput

    class B(BaseModel):
        b: int

    class A(BaseModel):
        a: B

    print(A.schema_json(indent=2))
