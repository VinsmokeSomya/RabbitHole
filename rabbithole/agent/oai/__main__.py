from rabbithole.a2a.server import A2AServer
from rabbithole.a2a.types import AgentCard, AgentCapabilities, AgentSkill, MissingAPIKeyError
from rabbithole.a2a.utils.push_notification_auth import PushNotificationSenderAuth
from rabbithole.agent.oai.task_manager import AgentTaskManager
from rabbithole.agent.oai.agent import OAIAgent
import click
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=10000)
def main(host, port):
    """Chat with OpenAI Agent server."""
    try:
        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="oai_chat",
            name="OpenAI Chat Tool",
            description="Chat with OpenAI",
            tags=["openai chat"],
            examples=["What is exchange rate between USD and GBP?"],
        )
        agent_card = AgentCard(
            name="OpenAI Agent",
            description="Chat with OpenAI",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=OAIAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=OAIAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        notification_sender_auth = PushNotificationSenderAuth()
        notification_sender_auth.generate_jwk()
        server = A2AServer(
            agent_card=agent_card,
            task_manager=AgentTaskManager(agent=OAIAgent(), notification_sender_auth=notification_sender_auth),
            host=host,
            port=port,
        )

        server.app.add_route(
            "/.well-known/oai.json", notification_sender_auth.handle_jwks_endpoint, methods=["GET"]
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
