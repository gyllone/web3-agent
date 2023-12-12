import json
from langchain.tools.render import render_text_description_and_args, format_tool_to_openai_function

from executor.swap.uniswap_v3.routing_query.func import RoutingQuerier


if __name__ == "__main__":
    querier = RoutingQuerier(base_url="https://routing-api.sushiswapclassic.org/v1/route")
    print(json.dumps(format_tool_to_openai_function(querier.make_tool()), indent=2))
