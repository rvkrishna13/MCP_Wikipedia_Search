import asyncio
from mcp import ClientSession, StdioServerParameters
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI

server_params = StdioServerParameters(
	command = "python3",
	args = ["mcp_server.py"]
)

# LangGraph state definition
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


open_api_key = "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"

async def create_graph(session):
	tools = await load_mcp_tools(session)

	llm = ChatOpenAI(model='gpt-4', temperature=0, openai_api_key=open_api_key)
	llm_with_tools = llm.bind_tools(tools)

	prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that uses tools to search Wikipedia."),
        MessagesPlaceholder("messages")
    ])

	chat_llm = prompt_template | llm_with_tools

	def chat_node(state: State) -> State:
		state["messages"] = chat_llm.invoke({"messages":state["messages"]})
		return state

	graph = StateGraph(State)
	graph.add_node("chat_node", chat_node)
	graph.add_node("tool_node", ToolNode(tools=tools))
	graph.add_edge(START, "chat_node")
	graph.add_conditional_edges("chat_node", tools_condition, {
    	"tools": "tool_node",
    	"__end__": END
    })
	graph.add_edge("tool_node", "chat_node")

	return graph.compile(checkpointer=MemorySaver())

async def main():
	async with stdio_client(server_params) as (read,write):
		async with ClientSession(read, write) as session:
			await session.initialize()

			agent = await create_graph(session)
			print("Wikipedia MCP agent is ready.")

			while True:
				user_input = input("\nYou: ").strip()
				if user_input.lower() in {"exit", "quit", "q"}:
					break

				try:
					response = await agent.ainvoke(
						{"messages": user_input},
						config = {"configurable": {"thread_id": "wiki-session"}}
					)
					print("AI:", response["messages"][-1].content)
				except Exception as e:
					print("Error:", e)

if __name__=="__main__":
	asyncio.run(main())

