from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

# we leverage langchain libraries as well as langgraph is built on top of langchain

load_dotenv()

class AgentState(TypedDict):
    messages : List[HumanMessage]

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

def process(state : AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print("LLM Response:", response.content)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

user_input = input("Enter your message: ")
agent.invoke({"messages": [HumanMessage(content=user_input)]})
