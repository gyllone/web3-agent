import httpx

from httpx import AsyncClient
from typing import LiteralString, Dict
from pydantic import BaseModel, Field
from langchain.agents import Tool

from tools.maker import ToolMaker


class RoutingQueryArguments(BaseModel):
    token_in_chain_id: int = Field(description="Chain ID of the token to swap in.")
    token_in_address: str = Field(description="Address of the token to swap in.")
    token_out_chain_id: int = Field(description="Chain ID of the token to swap out.")
    token_out_address: str = Field(description="Address of the token to swap out.")
    amount: int = Field(description="Amount of the token to swap in.")
    type: str = Field(description="Type of the swap.")
    recipient: str = Field(description="Recipient of the swap.")
    protocols: str = Field("v3", description="Protocols to use.")
    enable_universal_router: bool = Field(False, alias="enableUniversalRouter", description="Enable universal router.")

    def to_params(self) -> Dict:
        return {
            "tokenInChainId": self.token_in_chain_id,
            "tokenInAddress": self.token_in_address,
            "tokenOutChainId": self.token_out_chain_id,
            "tokenOutAddress": self.token_out_address,
            "amount": self.amount,
            "type": self.type,
            "recipient": self.recipient,
            "protocols": self.protocols,
            "enableUniversalRouter": self.enable_universal_router,
        }


class RoutingResponse(BaseModel):
    block_number: str = Field(alias="blockNumber", description="Block number of the routing transaction.")
    amount_decimals: str = Field(alias="amountDecimals", description="Decimals of the amount.")
    quote_decimals: str = Field(alias="quoteDecimals", description="Decimals of the quote.")
    gas_estimate_usd: str = Field(alias="gasUseEstimateUSD", description="Gas estimate in USD.")
    simulation_status: str = Field(alias="simulationStatus", description="Simulation status.")
    simulation_error: bool = Field(alias="simulationError", description="Simulation error.")
    routing: str = Field(alias="routeString", description="Routing string.")


class RoutingQuerier(ToolMaker):

    base_url: str

    @classmethod
    def name(cls) -> LiteralString:
        return "routing_querier"

    @classmethod
    def description(cls) -> LiteralString:
        return "Query routing information from the routing service"

    def query(self, req: RoutingQueryArguments) -> RoutingResponse:
        """Query routing information from the routing service."""
        resp = httpx.get(self.base_url, params=req.to_params())
        return RoutingResponse.parse_obj(resp.json())

    async def async_query(self, req: RoutingQueryArguments) -> RoutingResponse:
        """Query routing information from the routing service."""
        async with AsyncClient() as client:
            resp = await client.get(self.base_url, params=req.dict())
        return RoutingResponse.parse_obj(resp.json())

    def make_tool(self, **kwargs) -> Tool:
        """Create a tool for querying routing information."""
        return Tool.from_function(
            self.query,
            self.name(),
            self.description(),
            args_schema=RoutingQueryArguments,
            coroutine=self.async_query,
            **kwargs,
        )
