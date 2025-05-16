from typing import Any, Dict, AsyncIterable, Literal
from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent, ResponseCompletedEvent
from agents import Agent, Runner


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""
    status: Literal["input_required", "completed", "error"] = "input_required"
    message: str

class OAIAgent:
     
    def __init__(self):
        self.agent = Agent(name="Assistant", instructions="You are a helpful assistant")
        
    async def invoke(self, query, sessionId):
        result = await Runner.run(self.agent, query)
        return {
            "is_task_complete": True,
            "require_user_input": False,
            "content": result.final_output
        }

    async def stream(self, query, sessionId) -> AsyncIterable[Dict[str, Any]]:
        result = Runner.run_streamed(self.agent, input=query)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": event.data.delta
                }
            elif event.type == "raw_response_event" and isinstance(event.data, ResponseCompletedEvent):
                yield {
                    "is_task_complete": True,
                    "require_user_input": False,
                    "content": event.data.response.output[0].content[0].text
                }

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]