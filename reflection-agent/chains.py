from typing import List, Tuple, Union
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


def create_reflection_prompt() -> ChatPromptTemplate:
    """Creates a prompt template for critiquing tweets.

    Returns:
        ChatPromptTemplate: A prompt template configured for tweet critique and recommendations.
    """
    messages: List[Union[Tuple[str, str], MessagesPlaceholder]] = [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet. "
            "Always provide detailed recommendations, including requests for length, virality, style, tone, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
    return ChatPromptTemplate.from_messages(messages)


def create_generation_prompt() -> ChatPromptTemplate:
    """Creates a prompt template for generating tweets.

    Returns:
        ChatPromptTemplate: A prompt template configured for tweet generation.
    """
    messages: List[Union[Tuple[str, str], MessagesPlaceholder]] = [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent posts. "
            "Generate the best twitter post for the user's request. "
            "If the user provides critique, respond with a revised version of your previous tweet.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
    return ChatPromptTemplate.from_messages(messages)


llm = ChatOpenAI()

generation_chain = create_generation_prompt() | llm
reflection_chain = create_reflection_prompt() | llm
