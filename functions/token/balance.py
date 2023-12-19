from typing import Optional, LiteralString, Callable, Awaitable
from pydantic.v1 import BaseModel, Field
from web3 import Web3, AsyncWeb3
from web3.types import ABIFunction
from web3.utils.address import to_checksum_address

from config.chain import ChainConfig, TokenMetadata
from functions.wrapper import FunctionWrapper


class BalanceArgs(BaseModel):
    symbol: Optional[str] = Field(description="The symbol of the token")
    token: Optional[str] = Field(description="The token contract address")
    account: str = Field(description="The user address")


class BalanceResult(BaseModel):
    amount: float


class BalanceGetter(FunctionWrapper[BalanceArgs, BalanceResult]):
    chain_config: ChainConfig
    web3: Optional[Web3]
    async_web3: Optional[AsyncWeb3]

    abi: ABIFunction = {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }

    def __init__(
        self,
        *,
        chain_config: ChainConfig,
        web3: Optional[Web3] = None,
        async_web3: Optional[AsyncWeb3] = None,
    ):
        if not web3 and not async_web3:
            raise ValueError("Either web3 or async_web3 must be provided")
        self.chain_config = chain_config
        self.web3 = web3
        self.async_web3 = async_web3

    @classmethod
    def name(cls) -> LiteralString:
        return "get_token_balance"

    @classmethod
    def description(cls) -> LiteralString:
        return "useful for when you get token balance for some address"

    def _get_token(self, symbol: Optional[str], token: Optional[str]) -> TokenMetadata:
        if symbol is not None:
            if symbol in self.chain_config.token_cache_by_symbol:
                return self.chain_config.token_cache_by_symbol[symbol]
            else:
                raise ValueError(f"{symbol} not found in token list")
        elif token is not None:
            if token in self.chain_config.token_cache_by_address:
                return self.chain_config.token_cache_by_address[token]
            else:
                raise ValueError(f"{token} not found in token list")
        else:
            raise ValueError("Either symbol or token address must be provided")

    @property
    def function(self) -> Optional[Callable[..., BalanceResult]]:
        if self.web3:
            def _balance_of(symbol: Optional[str], token: Optional[str], account: str) -> BalanceResult:
                assert self.web3 is not None
                token_metadata = self._get_token(symbol, token)
                contract = self.web3.eth.contract(
                    address=to_checksum_address(token_metadata.address),
                    abi=self.abi,
                )
                balance = contract.functions.balanceOf(to_checksum_address(account)).call()
                return BalanceResult(amount=balance / (10 ** token_metadata.decimals))

            return _balance_of
        else:
            return None

    @property
    def async_function(self) -> Optional[Callable[..., Awaitable[BalanceResult]]]:
        if self.async_web3:
            async def _balance_of(symbol: Optional[str], token: Optional[str], account: str) -> BalanceResult:
                assert self.async_web3 is not None
                token_metadata = self._get_token(symbol, token)
                contract = self.async_web3.eth.contract(
                    address=to_checksum_address(token_metadata.address),
                    abi=self.abi,
                )
                balance = await contract.functions.balanceOf(to_checksum_address(account)).call()
                return BalanceResult(amount=balance / (10 ** token_metadata.decimals))

            return _balance_of
        else:
            return None
