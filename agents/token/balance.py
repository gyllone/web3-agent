from typing import Optional, LiteralString, Callable
from pydantic import BaseModel, Field
from web3 import Web3, AsyncWeb3

from agents.maker import AgentMaker

BalanceOfABI = """
[
    {
        "constant":true,
        "inputs":[{"name":"_owner","type":"address"}],
        "name":"balanceOf",
        "outputs":[{"name":"balance","type":"uint256"}],
        "type":"function"
    }
]
"""


class BalanceArgs(BaseModel):
    symbol: str = Field(description="The symbol of the token")
    user_address: str = Field(description="The user address")


class BalanceResult(BaseModel):
    amount: float


class BalanceGetter(AgentMaker[BalanceArgs, BalanceResult]):
    web3: Optional[Web3]
    async_web3: Optional[AsyncWeb3]

    def __init__(self):
        pass

    @classmethod
    def name(cls) -> LiteralString:
        return "get_token_balance"

    @classmethod
    def description(cls) -> LiteralString:
        return "Get token balance for the user"

    @property
    def processor(self) -> Optional[Callable[[BalanceArgs], BalanceResult]]:
        def balance_of(arg: BalanceArgs) -> BalanceResult:
            