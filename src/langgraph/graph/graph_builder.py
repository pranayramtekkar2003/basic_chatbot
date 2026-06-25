from langgraph.graph import StateGraph, START, END
from src.langgraph.state.state import State
from src.langgraph.nodes.chatbot import BasicChatbotNode
from src.langgraph.tools.search_tool import get_tool, create_tool_node
from langgraph.prebuilt import ToolNode, tools_condition
from src.langgraph.nodes.chatbot_tool import ChatbotTool

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_graph(self):

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)

        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def chatbot_with_tool_graph(self):
        tools = get_tool()
        tool_node = create_tool_node(tools)

        llm = self.llm

        chatbotNodetool = ChatbotTool(llm)
        chatbotNode = chatbotNodetool.create_chatbot(tools)

        self.graph_builder.add_node("chatbot",chatbotNode)
        self.graph_builder.add_node("tools",tool_node)

        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot", END)
    
    def setup_graph(self, usecase:str):
        
        if usecase == "Basic Chatbot":
            self.basic_chatbot_graph()
        elif usecase == "Chatbot With Web":
            self.chatbot_with_tool_graph()

        return self.graph_builder.compile()