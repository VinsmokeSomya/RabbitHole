import os
from typing import Any, Dict, AsyncIterable, Literal
from pydantic import BaseModel
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.runners import Runner


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal["input_required", "completed", "error"] = "input_required"
    message: str


class ADKAgent:
    def __init__(self):
        api_key_value = os.environ.get("GOOGLE_API_KEY")
        self.agent = Agent(
            name="Assistant",
            model=LiteLlm(model="gemini/gemini-1.5-flash", api_key=api_key_value),
            description=("Agent to answer any questions."),
            instruction=("You are a helpful assistant"),
            tools=[],
        )

        self.user_id = "adk_agent"
        self.runner = Runner(
            app_name=self.agent.name,
            agent=self.agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def invoke(self, query, session_id) -> AsyncIterable[Dict[str, Any]]:
        session = self.runner.session_service.get_session(
            app_name=self.agent.name, user_id=self.user_id, session_id=session_id
        )
        content = types.Content(role="user", parts=[types.Part.from_text(text=query)])
        if session is None:
            session = self.runner.session_service.create_session(
                app_name=self.agent.name,
                user_id=self.user_id,
                state={},
                session_id=session_id,
            )
        events = list(
            self.runner.run(
                user_id=self.user_id, session_id=session.id, new_message=content
            )
        )

        if not events or not events[-1].content or not events[-1].content.parts:
            yield {"is_task_complete": True, "require_user_input": False, "content": ""}
        else:
            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": "\n".join(
                    [p.text for p in events[-1].content.parts if p.text]
                ),
            }

    async def stream(self, query, session_id) -> AsyncIterable[Dict[str, Any]]:
        session = self.runner.session_service.get_session(
            app_name=self.agent.name, user_id=self.user_id, session_id=session_id
        )
        content = types.Content(role="user", parts=[types.Part.from_text(text=query)])
        if session is None:
            session = self.runner.session_service.create_session(
                app_name=self.agent.name,
                user_id=self.user_id,
                state={},
                session_id=session_id,
            )
        async for event in self.runner.run_async(
            user_id=self.user_id, session_id=session.id, new_message=content
        ):
            if event.is_final_response():
                response = ""
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    response = "\n".join(
                        [p.text for p in event.content.parts if p.text]
                    )
                elif (
                    event.content
                    and event.content.parts
                    and any([True for p in event.content.parts if p.function_response])
                ):
                    response = next(
                        (p.function_response.model_dump() for p in event.content.parts)
                    )
                yield {
                    "is_task_complete": True,
                    "require_user_input": False,
                    "content": response,
                }
            else:
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Processing the request...",
                }

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]
