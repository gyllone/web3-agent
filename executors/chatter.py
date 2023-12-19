from typing import Sequence, Optional, List, Tuple
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.tools.base import BaseTool
from langchain.prompts import MessagesPlaceholder
from langchain.schema import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain.schema.runnable import RunnableConfig


class Chatter:
    agent: AgentExecutor

    def __init__(
        self,
        *,
        model: ChatOpenAI,
        tools: Sequence[BaseTool],
        **kwargs,
    ):
        chat_history = MessagesPlaceholder(variable_name="chat_history")
        system_message = SystemMessage(
            content="You are an assistant of Gonswap, which is a DEX on the X1 network. Your "
                    "main job is to answer the user's question."
        )
        agent = OpenAIFunctionsAgent.from_llm_and_tools(
            model,
            tools,
            extra_prompt_messages=[chat_history],
            system_message=system_message,
        )
        self.agent = AgentExecutor.from_agent_and_tools(agent, tools, **kwargs)

    @staticmethod
    def _make_chat_history(chat_history: List[Tuple[str, str]]) -> List[BaseMessage]:
        messages = []
        for role, message in chat_history:
            if role in ("human", "user"):
                messages.append(HumanMessage(content=message))
            elif role in ("ai", "assistant"):
                messages.append(AIMessage(content=message))
            else:
                raise ValueError(f"Unexpected role: {role}")
        return messages

    async def chat(
        self,
        question: str,
        chat_history: List[Tuple[str, str]],
        config: Optional[RunnableConfig] = None,
    ) -> str:
        result = await self.agent.ainvoke(
            {
                "input": question,
                "chat_history": self._make_chat_history(chat_history),
            },
            config=config,
        )
        return result["output"]
