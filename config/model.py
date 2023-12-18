from pydantic import BaseModel

from config.base import BaseConfig


class ModelArgs(BaseModel):
    model_name: str = "gpt-4"
    temperature: float = 0
    openai_api_key: str


class ModelConfig(BaseConfig):
    chat_model_args: ModelArgs
    agent_model_args: ModelArgs
