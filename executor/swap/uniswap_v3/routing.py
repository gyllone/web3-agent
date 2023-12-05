from enum import Enum
from urllib.parse import urlunparse
from pydantic import BaseModel, Field


class RoutingRequest(BaseModel):
    token_in: "TokenInfo"
    amount: int
    type: str
    recipient: str

    class TokenInfo:
        chain_id: int = Field(description="")
        symbol: str = Field(description="")

    class Type(str, Enum):
        exact_in: str = "exactIn"
        exact_out: str = "exactOut"




class RoutingResponse(BaseModel):
    block_number: str = Field(alias="blockNumber")
    amount_decimals: str = Field(alias="amountDecimals")
    quote_decimals: str = Field(alias="quoteDecimals")
    gas_estimate_usd: str = Field(alias="gasUseEstimateUSD")
    simulation_status: str = Field(alias="simulationStatus")
    simulation_error: bool = Field(alias="simulationError")
    routing: str = Field(alias="routeString")

    def format(self) -> str:
        return """"""


class RoutingQuerier:
    base_url: str

    async def quote(self, ):
        pass


