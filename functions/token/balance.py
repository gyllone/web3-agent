from typing import Any, Optional, LiteralString, Callable, Awaitable
from pydantic.v1 import BaseModel, Field, validator
from web3 import Web3, AsyncWeb3
from web3.types import ABI
from web3.utils.address import to_checksum_address

from config.chain import ChainConfig, TokenMetadata
from functions.wrapper import FunctionWrapper
from common.utils import check_address


class BalanceArgs(BaseModel):
    account: Optional[str] = Field(None, description="The account address to query balance for")
    token_symbol: Optional[str] = Field(None, description="The symbol of the token")
    token_contract: Optional[str] = Field(None, description="The contract address of the token")

    @validator("account", pre=True)
    @classmethod
    def check_account(cls, v: Any) -> Any:
        if v is not None:
            return check_address(v)

    @validator("token_contract", pre=True)
    @classmethod
    def check_token_contract(cls, v: Any) -> Any:
        if v is not None:
            return check_address(v)


class BalanceGetter(FunctionWrapper[BalanceArgs, float]):
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

        super().__init__()

    @classmethod
    def name(cls) -> LiteralString:
        return "balance_of"

    @classmethod
    def description(cls) -> LiteralString:
        return "useful for when you query token balance"

    def _get_token(self, symbol: Optional[str], contract: Optional[str]) -> TokenMetadata:
        if symbol is not None:
            if symbol in self.chain_config.token_cache_by_symbol:
                return self.chain_config.token_cache_by_symbol[symbol]
            else:
                raise ValueError(f"{symbol} not found in token symbol cache")
        elif contract is not None:
            if contract in self.chain_config.token_cache_by_address:
                return self.chain_config.token_cache_by_address[contract]
            else:
                raise ValueError(f"{contract} not found in token address cache")
        else:
            raise ValueError("Either token symbol or token address must be provided")

    @property
    def tool_func(self) -> Optional[Callable[..., float]]:
        if self.web3:
            def _balance_of(
                account: Optional[str] = None,
                token_symbol: Optional[str] = None,
                token_contract: Optional[str] = None,
                **kwargs,
            ) -> float:
                assert self.web3 is not None

                token = self._get_token(token_symbol, token_contract)
                account = account or kwargs.get("user", None)
                if account is None:
                    raise ValueError("Either account or user must be provided")
                account = to_checksum_address(account)
                if token.address is None:
                    # native coin balance
                    balance = self.web3.eth.get_balance(account)
                else:
                    # ERC20 token balance
                    contract = self.web3.eth.contract(
                        address=to_checksum_address(token.address),
                        abi=self.abi,
                    )
                    balance = contract.functions.balanceOf(account).call()
                return balance / (10 ** token.decimals)

            return _balance_of
        else:
            return None

    @property
    def async_tool_func(self) -> Optional[Callable[..., Awaitable[float]]]:
        if self.async_web3:
            async def _balance_of(
                account: str,
                token_symbol: Optional[str] = None,
                token_contract: Optional[str] = None,
            ) -> float:
                assert self.async_web3 is not None
                token = self._get_token(token_symbol, token_contract)
                if token.address is None:
                    # native coin balance
                    balance = await self.async_web3.eth.get_balance(to_checksum_address(account))
                else:
                    # ERC20 token balance
                    contract = self.async_web3.eth.contract(
                        address=to_checksum_address(token.address),
                        abi=self.abi,
                    )
                    balance = await contract.functions.balanceOf(to_checksum_address(account)).call()
                return balance / (10 ** token.decimals)

            return _balance_of
        else:
            return None
