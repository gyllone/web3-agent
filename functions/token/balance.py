from typing import Optional, LiteralString, Callable, Awaitable
from pydantic.v1 import BaseModel, Field
from web3 import Web3, AsyncWeb3
from web3.types import ABI
from web3.utils.address import to_checksum_address

from config.chain import ChainConfig, TokenMetadata
from functions.wrapper import FunctionWrapper


class BalanceArgs(BaseModel):
    account: str = Field(description="The account address to query balance for")
    token_symbol: Optional[str] = Field(None, description="The symbol of the token")
    token_contract: Optional[str] = Field(None, description="The token contract address of the token")


class BalanceResult(BaseModel):
    amount: float


class BalanceGetter(FunctionWrapper[BalanceArgs, BalanceResult]):
    chain_config: ChainConfig
    web3: Optional[Web3]
    async_web3: Optional[AsyncWeb3]

    abi: ABI = [
        {
            "inputs": [{"name": "account", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        }
    ]

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
        return "balance_of"

    @classmethod
    def description(cls) -> LiteralString:
        return "useful for when you query token balance"

    def _get_token(self, symbol: Optional[str], address: Optional[str]) -> TokenMetadata:
        if symbol is not None:
            if symbol in self.chain_config.token_cache_by_symbol:
                return self.chain_config.token_cache_by_symbol[symbol]
            else:
                raise ValueError(f"{symbol} not found in token symbol cache")
        elif address is not None:
            if address in self.chain_config.token_cache_by_address:
                return self.chain_config.token_cache_by_address[address]
            else:
                raise ValueError(f"{address} not found in token address cache")
        else:
            raise ValueError("Either token symbol or token address must be provided")

    @property
    def function(self) -> Optional[Callable[..., BalanceResult]]:
        if self.web3:
            def _balance_of(
                account: str,
                token_symbol: Optional[str] = None,
                token_contract: Optional[str] = None,
            ) -> BalanceResult:
                assert self.web3 is not None
                token = self._get_token(token_symbol, token_contract)
                contract = self.web3.eth.contract(
                    address=to_checksum_address(token.address),
                    abi=self.abi,
                )
                balance = contract.functions.balanceOf(to_checksum_address(account)).call()
                return BalanceResult(amount=balance / (10 ** token.decimals))

            return _balance_of
        else:
            return None

    @property
    def async_function(self) -> Optional[Callable[..., Awaitable[BalanceResult]]]:
        if self.async_web3:
            async def _balance_of(
                account: str,
                token_symbol: Optional[str] = None,
                token_contract: Optional[str] = None,
            ) -> BalanceResult:
                assert self.async_web3 is not None
                token = self._get_token(token_symbol, token_contract)
                contract = self.async_web3.eth.contract(
                    address=to_checksum_address(token.address),
                    abi=self.abi,
                )
                balance = await contract.functions.balanceOf(to_checksum_address(account)).call()
                return BalanceResult(amount=balance / (10 ** token.decimals))

            return _balance_of
        else:
            return None
