from typing import TypedDict, List, Union
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4o",temperature=0.7)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])

    print(f"\nAI: {response.content}\n")

    # Return a new state instead of mutating the existing one
    return {
        "messages": state["messages"] + [response]
    }


graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history: List[Union[HumanMessage, AIMessage]] = []

while True:
    user_input = input("You: ")
    if user_input.lower().strip() == "exit":
        break

    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"] #reset