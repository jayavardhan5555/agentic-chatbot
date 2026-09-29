from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from typing import Annotated,TypedDict
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):

    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


checkpoint = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpoint)
