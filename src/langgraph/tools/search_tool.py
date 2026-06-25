from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

def get_tool():

    tools = [TavilySearch(max_results=2)]
    return tools

def create_tool_node(tools):
    return ToolNode(tools=tools)

