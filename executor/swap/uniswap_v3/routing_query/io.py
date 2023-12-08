from enum import Enum
from pydantic import Field

from executor.types import *


class RoutingQueryInput(Input):
    token_in_chain_id: int = Field(description="Chain id of the token swapped in")
    token_in_symbol: str = Field(description="Symbol of the token swapped in")
    token_out_chain_id: int = Field(description="Chain id of the token swapped out")
    token_out_symbol: str = Field(description="Symbol of the token swapped out")
    amount: int = Field(description="Amount of token swapped in")
    type: str = Field(description="Type of swap")
    recipient: str = Field(description="Recipient of the swap")

    class Type(str, Enum):
        exact_in: str = "exactIn"
        exact_out: str = "exactOut"


class RoutingQueryOutput(Output):
    block_number: str = Field(description="Block number of the routing query")
    amount_decimals: str = Field(description="Decimals of the amount")
    quote_decimals: str = Field(description="Decimals of the quote")
    gas_estimate_usd: str = Field(description="Gas estimate in USD")
    simulation_status: str = Field(description="Status of the simulation")
    simulation_error: bool = Field(description="Whether the simulation has error")
    routing: str = Field(description="Routing string")
