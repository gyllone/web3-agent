from typing import Any, Optional
from pydantic import BaseModel, field_validator
from eth_utils import is_address


class UserContext(BaseModel):
    """The context of the user request."""

    address: Optional[str] = None

    @field_validator("address", mode="before")
    @classmethod
    def check_address(cls, v: Any) -> Any:
        if v is not None:
            if is_address(v):
                return v
            else:
                raise ValueError(f"Invalid address {v}")


