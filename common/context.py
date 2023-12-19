from pydantic import BaseModel


class Context(BaseModel):
    """The context of the user request."""

    address: str
