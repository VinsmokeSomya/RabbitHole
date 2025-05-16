from rabbithole.a2a.server import A2AServer
from rabbithole.a2a.types import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from rabbithole.a2a.utils.push_notification_auth import PushNotificationSenderAuth
from rabbithole.agent.adk.task_manager import AgentTaskManager
from rabbithole.agent.adk.agent import ADKAgent
import click
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from the same directory as __main__.py
dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=dotenv_path, override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=10000)
def main(host, port):
    """Chat with Google ADK Agent server."""
    try:
        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="adk_chat",
            name="ADK Chat Tool",
            description="Chat with ADK Agent",
            tags=["adk chat"],
            examples=["What is exchange rate between USD and GBP?"],
        )
        agent_card = AgentCard(
            name="ADK Agent",
            description="Chat with ADK",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=ADKAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=ADKAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        notification_sender_auth = PushNotificationSenderAuth()
        notification_sender_auth.generate_jwk()
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=ADKAgent(), notification_sender_auth=notification_sender_auth),
            host=host,
            port=port,
        )

        server.app.add_route(
            "/.well-known/adk.json", notification_sender_auth.handle_jwks_endpoint, methods=["GET"]
        )

        logger.info(f"Starting server on {host}:{port}")
        server.start()
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()
