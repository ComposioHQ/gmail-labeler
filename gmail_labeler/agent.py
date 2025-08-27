"""
Langchain demo.
"""

from composio import Composio
from composio_langchain import LangchainProvider

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI


def create_agent(user_id: str, composio_client: Composio[LangchainProvider]):
    """
    Create an agent for a given user id.
    """
    # Step 1: Get all the tools
    tools = composio_client.tools.get(
        user_id=user_id,
        tools=[
            "GMAIL_LIST_LABELS",
            "GMAIL_ADD_LABEL_TO_EMAIL",
        ],
    )

    # Step 2: Pull relevant agent prompt.
    prompt = hub.pull("hwchase17/openai-functions-agent")

    # Step 3: Initialize chat model.
    openai_client = ChatOpenAI(model="gpt-4-turbo")

    # Step 4: Define agent
    return AgentExecutor(
        agent=create_openai_functions_agent(
            openai_client,
            tools,
            prompt,
        ),
        tools=tools,
        verbose=False,
    )
