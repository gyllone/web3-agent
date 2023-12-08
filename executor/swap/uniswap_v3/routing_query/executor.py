from enum import Enum
from urllib.parse import urlunparse
from pydantic import BaseModel, Field

from executor.types import *
from executor.swap.uniswap_v3.routing_query.io import RoutingQueryInput, RoutingQueryOutput


class RoutingRequest(BaseModel):
    token_in_chain_id: int = Field(alias="tokenInChainId")
    token_in_address: str = Field(alias="tokenInAddress")
    token_out_chain_id: int = Field(alias="tokenOutChainId")
    token_out_address: str = Field(alias="tokenOutAddress")
    amount: int
    type: str
    recipient: str
    protocols: str = "v3"
    enable_universal_router: bool = Field(False, alias="enableUniversalRouter")


class RoutingResponse(BaseModel):
    block_number: str = Field(alias="blockNumber")
    amount_decimals: str = Field(alias="amountDecimals")
    quote_decimals: str = Field(alias="quoteDecimals")
    gas_estimate_usd: str = Field(alias="gasUseEstimateUSD")
    simulation_status: str = Field(alias="simulationStatus")
    simulation_error: bool = Field(alias="simulationError")
    routing: str = Field(alias="routeString")


class RoutingQuerier(Executor):
    """RoutingQuerier is an executor to query routing information from the routing service."""

    input: RoutingQueryInput
    output: RoutingQueryOutput

    base_url: str

    async def async_execute(self, _input: RoutingQueryInput, **kwargs) -> RoutingQueryOutput:
        pass




