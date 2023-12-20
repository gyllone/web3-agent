import httpx

from httpx import AsyncClient
from typing import Any, LiteralString, Optional, Callable, Awaitable
from pydantic.v1 import BaseModel, Field, validator

from functions.wrapper import FunctionWrapper
from common.utils import check_address
from config.chain import ChainConfig


class RoutingQueryArgs(BaseModel):
    token_in_address: str = Field(description="Contract address of the token to swap in")
    token_out_address: str = Field(description="Contract address of the token to swap out")
    amount: int = Field(description="Amount of the token to swap in")
    tp: str = Field(description='Type of the swap event, must be either "exactIn" or "exactOut"')
    recipient: str = Field(description="Recipient of token out")
    protocol: str = Field("v3", description="Protocol to use")
    enable_universal_router: bool = Field(False, description="Enable universal router")

    @validator("token_in_address", pre=True)
    @classmethod
    def check_token_in_address(cls, v: Any) -> Any:
        if v is not None:
            return check_address(v)

    @validator("token_out_address", pre=True)
    @classmethod
    def check_token_out_address(cls, v: Any) -> Any:
        if v is not None:
            return check_address(v)


class RoutingResult(BaseModel):
    simulation_status: str = Field(description="Simulation status")
    simulation_error: bool = Field(description="Simulation error")
    block_number: str = Field(description="Block number of the routing query simulated at")
    gas_estimate_usd: str = Field(description="Gas estimated in USD for the swap transaction")
    routing: str = Field(description="Routing query string")
    amount_decimals: str = Field(description="Amount decimals")
    quote_decimals: str = Field(description="Decimals of the quote")


class RoutingResponse(BaseModel):
    block_number: str = Field(alias="blockNumber", description="Block number of the routing transaction")
    amount_decimals: str = Field(alias="amountDecimals", description="Decimals of the amount")
    quote_decimals: str = Field(alias="quoteDecimals", description="Decimals of the quote")
    gas_estimate_usd: str = Field(alias="gasUseEstimateUSD", description="Gas estimate in USD")
    simulation_status: str = Field(alias="simulationStatus", description="Simulation status")
    simulation_error: bool = Field(alias="simulationError", description="Simulation error")
    routing: str = Field(alias="routeString", description="Routing string")


class RoutingQuerier(FunctionWrapper[RoutingQueryArgs, RoutingResponse]):
    """Query routing information from the routing service."""

    chain_config: ChainConfig
    base_url: str

    def __init__(self, *, chain_config: ChainConfig, base_url: str):
        self.chain_config = chain_config
        self.base_url = base_url

        super().__init__()

    @classmethod
    def name(cls) -> LiteralString:
        return "routing_querier"

    @classmethod
    def description(cls) -> LiteralString:
        return "Query routing information from the routing service"

    @property
    def tool_func(self) -> Optional[Callable[..., RoutingResponse]]:
        def _query_routing(
            token_in_address: str,
            token_out_address: str,
            amount: int,
            tp: str,
            recipient: str,
            protocols: str = "v3",
            enable_universal_router: bool = False,
        ) -> RoutingResponse:
            """Query routing information from the routing service."""
            resp = httpx.get(
                self.base_url,
                params={
                    "tokenInChainId": self.chain_config.chain.chain_id,
                    "tokenInAddress": token_in_address,
                    "tokenOutChainId": self.chain_config.chain.chain_id,
                    "tokenOutAddress": token_out_address,
                    "amount": amount,
                    "type": tp,
                    "recipient": recipient,
                    "protocols": protocols,
                    "enableUniversalRouter": enable_universal_router,
                },
            )
            return RoutingResponse.parse_obj(resp.json())

        return _query_routing

    @property
    def async_tool_func(self) -> Optional[Callable[..., Awaitable[RoutingResponse]]]:
        async def _query_routing(
            token_in_address: str,
            token_out_address: str,
            amount: int,
            tp: str,
            recipient: str,
            protocols: str = "v3",
            enable_universal_router: bool = False,
        ) -> RoutingResponse:
            """Query routing information from the routing service."""
            async with AsyncClient() as client:
                resp = await client.get(
                    self.base_url,
                    params={
                        "tokenInChainId": self.chain_config.chain.chain_id,
                        "tokenInAddress": token_in_address,
                        "tokenOutChainId": self.chain_config.chain.chain_id,
                        "tokenOutAddress": token_out_address,
                        "amount": amount,
                        "type": tp,
                        "recipient": recipient,
                        "protocols": protocols,
                        "enableUniversalRouter": enable_universal_router,
                    },
                )
                return RoutingResponse.parse_obj(resp.json())

        return _query_routing
