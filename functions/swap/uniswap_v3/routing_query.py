import httpx

from httpx import AsyncClient
from typing import LiteralString, Optional, Callable, Awaitable
from pydantic.v1 import BaseModel, Field

from functions.wrapper import FunctionWrapper


class RoutingQueryArgs(BaseModel):
    token_in_chain_id: int = Field(description="Chain ID of the token to swap in.")
    token_in_address: str = Field(description="Address of the token to swap in.")
    token_out_chain_id: int = Field(description="Chain ID of the token to swap out.")
    token_out_address: str = Field(description="Address of the token to swap out.")
    amount: int = Field(description="Amount of the token to swap in.")
    type: str = Field(description="Type of the swap.")
    recipient: str = Field(description="Recipient of the swap.")
    protocols: str = Field("v3", description="Protocols to use.")
    enable_universal_router: bool = Field(False, alias="enableUniversalRouter", description="Enable universal router.")


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

    base_url: str

    def __init__(self, *, base_url: str):
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
            token_in_chain_id: int,
            token_in_address: str,
            token_out_chain_id: int,
            token_out_address: str,
            amount: int,
            type: str,
            recipient: str,
            protocols: str = "v3",
            enable_universal_router: bool = False,
        ) -> RoutingResponse:
            """Query routing information from the routing service."""
            resp = httpx.get(
                self.base_url,
                params={
                    "tokenInChainId": token_in_chain_id,
                    "tokenInAddress": token_in_address,
                    "tokenOutChainId": token_out_chain_id,
                    "tokenOutAddress": token_out_address,
                    "amount": amount,
                    "type": type,
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
            token_in_chain_id: int,
            token_in_address: str,
            token_out_chain_id: int,
            token_out_address: str,
            amount: int,
            type: str,
            recipient: str,
            protocols: str = "v3",
            enable_universal_router: bool = False,
        ) -> RoutingResponse:
            """Query routing information from the routing service."""
            async with AsyncClient() as client:
                resp = await client.get(
                    self.base_url,
                    params={
                        "tokenInChainId": token_in_chain_id,
                        "tokenInAddress": token_in_address,
                        "tokenOutChainId": token_out_chain_id,
                        "tokenOutAddress": token_out_address,
                        "amount": amount,
                        "type": type,
                        "recipient": recipient,
                        "protocols": protocols,
                        "enableUniversalRouter": enable_universal_router,
                    },
                )
                return RoutingResponse.parse_obj(resp.json())

        return _query_routing
