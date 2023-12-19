from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from eth_utils import is_address

from config.base import BaseConfig


class TokenMetadata(BaseModel):
    name: str
    symbol: str
    decimals: int
    address: Optional[str] = None

    @field_validator("address", mode="before")
    @classmethod
    def check_address(cls, v: Any) -> Any:
        if v is not None:
            if is_address(v):
                return v
            else:
                raise ValueError(f"Invalid address {v}")


class ChainMetadata(BaseModel):
    chain_id: int
    name: str
    rpc_url: str


class ChainConfig(BaseConfig):
    chain: ChainMetadata
    """chain metadata"""
    tokens: List[TokenMetadata]
    """tokens: list of tokens on chain"""

    token_cache_by_symbol: Dict[str, TokenMetadata] = Field(default={}, exclude=True)  #: :meta private:
    token_cache_by_address: Dict[str, TokenMetadata] = Field(default={}, exclude=True)  #: :meta private:

    @model_validator(mode="after")
    @classmethod
    def validate_environment(cls, value: Any) -> Any:
        """Validate token list."""
        assert isinstance(value, ChainConfig)
        for token in value.tokens:
            value.token_cache_by_symbol[token.symbol] = token
            if token.address is None:
                raise ValueError(f"Token {token.symbol} has no address")
            value.token_cache_by_address[token.address] = token
        return value