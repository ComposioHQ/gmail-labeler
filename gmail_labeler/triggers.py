import typing as t

from composio import Composio
from composio_langchain import LangchainProvider

from .constants import GMAIL_NEW_GMAIL_MESSAGE_TRIGGER


def check_trigger_exists(
    composio_client: Composio[LangchainProvider],
    connected_account_id: str,
) -> t.Optional[str]:
    """
    Check if a trigger exists.
    """
    triggers = composio_client.triggers.list_active(
        trigger_names=[GMAIL_NEW_GMAIL_MESSAGE_TRIGGER],
        connected_account_ids=[connected_account_id],
    )
    for trigger in triggers.items:
        return trigger.id
    return None


def create_trigger(
    composio_client: Composio[LangchainProvider],
    connected_account_id: str,
) -> str:
    """
    Create a trigger.
    """
    response = composio_client.triggers.create(
        slug=GMAIL_NEW_GMAIL_MESSAGE_TRIGGER,
        connected_account_id=connected_account_id,
        trigger_config={},
    )
    return response.trigger_id
 