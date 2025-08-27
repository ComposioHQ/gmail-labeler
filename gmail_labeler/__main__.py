import argparse
import dotenv

from composio import Composio
from composio.types import TriggerEvent
from composio_langchain import LangchainProvider

from langchain.agents import AgentExecutor

from gmail_labeler.agent import create_agent
from gmail_labeler.connection import (
    create_connection,
    check_connected_account_exists,
)
from gmail_labeler.constants import GMAIL_NEW_GMAIL_MESSAGE_TRIGGER
from gmail_labeler.triggers import (
    check_trigger_exists,
    create_trigger,
)
from gmail_labeler.prompt import APPLY_NEW_LABEL


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=str, required=True)
    return parser.parse_args()


def run_agent(user_id: str):
    composio_client = Composio(provider=LangchainProvider())
    connected_account_id = check_connected_account_exists(composio_client, user_id)
    if connected_account_id is None:
        connection_request = create_connection(composio_client, user_id)
        print(
            f"Authenticate with the following link: {connection_request.redirect_url}"
        )
        connection_request.wait_for_connection()
        connected_account_id = connection_request.id

    # Check if trigger exists
    trigger_id = check_trigger_exists(
        composio_client=composio_client,
        connected_account_id=connected_account_id,
    )
    if trigger_id is None:
        trigger_id = create_trigger(
            composio_client=composio_client,
            connected_account_id=connected_account_id,
        )

    # Create agent
    agent = create_agent(user_id=user_id, composio_client=composio_client)

    # Create triggeer subscription
    trigger_subscription = composio_client.triggers.subscribe()

    # Register event handler
    @trigger_subscription.handle(
        # trigger_id=trigger_id,
        trigger_slug=GMAIL_NEW_GMAIL_MESSAGE_TRIGGER,
    )
    def handle_event(event: TriggerEvent):
        print("> Received email with subject: ", event["payload"]["subject"])
        result = agent.invoke(
            input={
                "input": APPLY_NEW_LABEL.format(
                    message_id=event["payload"]["id"],
                    message_subject=event["payload"]["subject"],
                    message_text=event["payload"]["message_text"],
                )
            }
        )
        print("> Result: ", result["output"])

    # Wait forever
    print("Waiting for events...")
    trigger_subscription.wait_forever()


def main():
    dotenv.load_dotenv()
    args = parse_args()
    run_agent(user_id=args.user_id)

if __name__ == "__main__":
    main()
