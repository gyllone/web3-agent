from pydantic import BaseModel


class UniswapV3Deployment(BaseModel):
    Factory: str
    Multicall: str
    QuoterV2: str
    SwapRouter02: str
