from typing import Dict, List, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from eth_utils import is_address

from config.base import BaseConfig


class TokenMetadata(BaseModel):
    name: str
    symbol: str
    address: str
    decimals: int

    @classmethod
    @field_validator("address", mode="before")
    def check_address(cls, v):
        if is_address(v):
            return v
        else:
            raise ValueError(f"Invalid address {v}")


class ChainMetadata(BaseModel):
    chain_id: int
    name: str
    native_coin_symbol: str
    rpc_url: str


class ChainConfig(BaseConfig):
    chain: ChainMetadata
    """chain metadata"""
    tokens: List[TokenMetadata]
    """tokens: list of tokens on chain"""

    token_cache_by_symbol: Dict[str, TokenMetadata] = Field(default={}, exclude=True)  #: :meta private:
    token_cache_by_address: Dict[str, TokenMetadata] = Field(default={}, exclude=True)  #: :meta private:

    @classmethod
    @model_validator(mode="after")
    def validate_environment(cls, **values) -> Any:
        """Validate token list."""
        tokens = values["tokens"]
        token_cache_by_symbol = values["token_cache_by_symbol"]
        token_cache_by_address = values["token_cache_by_address"]
        for token in tokens:
            token_cache_by_symbol[token.symbol] = token
            token_cache_by_address[token.address] = token
        return values
