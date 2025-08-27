from composio import after_execute
from composio.types import ToolExecutionResponse


@after_execute(tools=["SLACK_FETCH_CONVERSATION_HISTORY"])
def clean_conversation_history(
    tool: str,
    toolkit: str,
    response: ToolExecutionResponse,
) -> ToolExecutionResponse:
    """
    Clean the conversation history.
    """
    if not response["data"]["ok"]:
        return response

    try:
        response["data"]["messages"] = [
            {"user": message["user"], "text": message["text"]}
            for message in response["data"]["messages"]
            if message["type"] == "message"
        ]
    except KeyError:
        pass

    return response
