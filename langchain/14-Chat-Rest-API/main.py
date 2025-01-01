import asyncio
import os
from dotenv import load_dotenv

from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain.chains.api.prompt import API_URL_PROMPT
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# NOTE: There are inherent risks in giving models discretion
# to execute real-world actions. We must "opt-in" to these
# risks by setting allow_dangerous_request=True to use these tools.
# This can be dangerous for calling unwanted requests. Please make
# sure your custom OpenAPI spec (yaml) is safe and that permissions
# associated with the tools are narrowly-scoped.
ALLOW_DANGEROUS_REQUESTS = True

# Subset of spec for https://jsonplaceholder.typicode.com
api_spec = """
openapi: 3.0.0
info:
  title: JSONPlaceholder API
  version: 1.0.0
servers:
  - url: https://jsonplaceholder.typicode.com
paths:
  /posts:
    get:
      summary: Get posts
      parameters: &id001
        - name: _limit
          in: query
          required: false
          schema:
            type: integer
          example: 2
          description: Limit the number of results
"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
toolkit = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),  # no auth required
    allow_dangerous_requests=ALLOW_DANGEROUS_REQUESTS,
)
tools = toolkit.get_tools()

api_request_chain = (
    API_URL_PROMPT.partial(api_docs=api_spec)
    | llm.bind_tools(tools, tool_choice="any")
)

class ChainState(TypedDict):
    """LangGraph state."""

    messages: Annotated[Sequence[BaseMessage], add_messages]


async def acall_request_chain(state: ChainState, config: RunnableConfig):
    last_message = state["messages"][-1]
    response = await api_request_chain.ainvoke(
        {"question": last_message.content}, config
    )
    return {"messages": [response]}

async def acall_model(state: ChainState, config: RunnableConfig):
    response = await llm.ainvoke(state["messages"], config)
    return {"messages": [response]}

graph_builder = StateGraph(ChainState)
graph_builder.add_node("call_tool", acall_request_chain)
graph_builder.add_node("execute_tool", ToolNode(tools))
graph_builder.add_node("call_model", acall_model)
graph_builder.set_entry_point("call_tool")
graph_builder.add_edge("call_tool", "execute_tool")
graph_builder.add_edge("execute_tool", "call_model")
graph_builder.add_edge("call_model", END)
chain = graph_builder.compile()


example_query = "Fetch the top two posts. What are their titles?"

events = chain.astream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
async def main():
    async for event in events:
        event["messages"][-1].pretty_print()

asyncio.run(main())