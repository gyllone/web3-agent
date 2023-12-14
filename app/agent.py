from langchain.tools.render import format_tool_to_openai_function

from agents.swap.uniswap_v3.routing_query import RoutingQuerier


if __name__ == "__main__":
    agent = RoutingQuerier(base_url="https://routing-api.0x.org/swap/v1/quote")
    tool = agent.tool()
    description = format_tool_to_openai_function(tool)
    print(description)
