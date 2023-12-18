from typing import Dict, List
from pydantic import BaseModel, Field, field_validator, model_validator
from eth_utils import is_address

from config.base import BaseConfig


class TokenMetadata(BaseModel):
    name: str
    symbol: str
    address: str
    decimal: int

    @field_validator("address")
    @classmethod
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

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate token list."""
        tokens = values.get("tokens", [])
        token_cache_by_symbol = {}
        token_cache_by_address = {}
        for token in tokens:
            token_cache_by_symbol[token.symbol] = token
            token_cache_by_address[token.symbol] = token
        values["token_cache_by_symbol"] = token_cache_by_symbol
        values["token_cache_by_address"] = token_cache_by_address
        return values
