import json
from typing import Dict, List
from os import PathLike
from pydantic import BaseModel, Field, validator, root_validator
from eth_utils import is_address
from langchain.llms.openai import OpenAIChat


class TokenMetadata(BaseModel):
    name: str
    symbol: str
    address: str

    @validator("address", pre=True)
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


class ChainConfig(BaseModel):
    chain: ChainMetadata
    """chain_id: chain metadata"""
    tokens: List[TokenMetadata]

    cache_by_symbol: Dict[str, TokenMetadata] = Field(default={}, exclude=True)
    cache_by_address: Dict[str, TokenMetadata] = Field(default={}, exclude=True)

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate token list."""
        tokens = values.get("tokens", {})
        cache_by_symbol = {}
        cache_by_address = {}
        for chain_id, token_list in tokens.items():
            for token in token_list:
                cache_by_symbol[token.symbol] = token
                cache_by_address[token.symbol] = token
        values["cache_by_symbol"] = cache_by_symbol
        values["cache_by_address"] = cache_by_address
        return values
