from dotenv import load_dotenv
from typing import List, Sequence

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import generation_chain, reflection_chain

load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
    """
    Generates a response to the user's input.

    Args:
        state (Sequence[BaseMessage]): The user's input.

    Returns:
        List[BaseMessage]: The response to the user's input.
    """
    return generation_chain.invoke({"messages": state})


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    """
    Reflects on the user's input.

    Args:
        messages (Sequence[BaseMessage]): The user's input.

    Returns:
        List[BaseMessage]: The reflection on the user's input.
    """
    res = reflection_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]


builder = MessageGraph()

builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)


def should_continue(state: List[BaseMessage]) -> bool:
    """
    Determines whether the conversation should continue.

    Args:

        state (List[BaseMessage]): The conversation state.

    Returns:
        bool: Whether the conversation should continue.
    """
    if len(state) > 6:
        return END
    return REFLECT


builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()

# Visualize the graph
print(graph.get_graph().draw_mermaid())


if __name__ == "__main__":
    print("Welcome to the reflection agent!")
    inputs = HumanMessage(
        content="""
Make this tweet better: "I just got my new phone and I absolutely love it! The features are amazing, the design is sleek, and it works like a charm. Couldn't be happier with my purchase!"
"""
    )
    response = graph.invoke(inputs)
