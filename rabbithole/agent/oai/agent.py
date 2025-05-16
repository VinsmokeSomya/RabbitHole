from typing import Any, Dict, AsyncIterable, Literal
from pydantic import BaseModel
from openai.types.responses import (
    ResponseTextDeltaEvent,
    ResponseCompletedEvent,
    ResponseOutputText,
    ResponseOutputRefusal,
    ResponseOutputMessage,
    # If we want to handle tool calls specifically, they would be imported here too.
    # e.g., ResponseFileSearchToolCall, ResponseFunctionToolCall, etc.
)
from openai.types.beta.threads.runs import TextContentBlock

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
        # Assuming result.final_output gives a simple string directly
        # If it's structured like the streaming response, this might need adjustment
        content_to_return = "Agent invocation completed."
        if hasattr(result, 'final_output') and result.final_output:
            # This part is speculative based on typical agent runner patterns.
            # If final_output is already a string, this is fine.
            # If it's complex, needs specific handling.
            if isinstance(result.final_output, str):
                content_to_return = result.final_output
            else:
                # Attempt to extract text if final_output is like the streaming output parts
                try:
                    # This is a guess based on the streaming part. Adjust if invoke() has a different structure.
                    if isinstance(result.final_output, list) and len(result.final_output) > 0:
                        first_output_part = result.final_output[0]
                        if hasattr(first_output_part, 'content') and len(first_output_part.content) > 0:
                            if hasattr(first_output_part.content[0], 'text'):
                                content_to_return = first_output_part.content[0].text
                except Exception:
                    pass # Keep default content_to_return
       
        return {
            "is_task_complete": True,
            "require_user_input": False,
            "content": content_to_return
        }

    async def stream(self, query, sessionId) -> AsyncIterable[Dict[str, Any]]:
        result = Runner.run_streamed(self.agent, input=query)
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                if isinstance(event.data, ResponseTextDeltaEvent):
                    yield {
                        "is_task_complete": False,
                        "require_user_input": False,
                        "content": event.data.delta
                    }
                elif isinstance(event.data, ResponseCompletedEvent):
                    response_content = "Agent task completed."
                    is_complete = True
                    input_required = False

                    if isinstance(event.data.response, ResponseOutputText):
                        if event.data.response.output:
                            first_output_part = event.data.response.output[0]
                            if isinstance(first_output_part, ResponseOutputMessage):
                                if first_output_part.content:
                                    # Content is a list, usually of TextContentBlock for text
                                    first_content_block = first_output_part.content[0]
                                    if isinstance(first_content_block, TextContentBlock):
                                        response_content = first_content_block.text.value
                                    else:
                                        response_content = "[Non-text content received]"
                                else:
                                    response_content = "[Empty content in ResponseOutputMessage]"
                            else:
                                # Handle other output part types if necessary (e.g. tool calls)
                                response_content = f"[Unhandled output part type: {type(first_output_part).__name__}]"
                        else:
                            response_content = "[Empty output in ResponseOutputText]"
                    elif isinstance(event.data.response, ResponseOutputRefusal):
                        response_content = event.data.response.refusal or "[Agent refused request]"
                        # is_complete might depend on how refusals are handled, usually they are final.
                    else:
                        response_content = f"[Unhandled response type: {type(event.data.response).__name__}]"

                    yield {
                        "is_task_complete": is_complete,
                        "require_user_input": input_required,
                        "content": response_content
                    }

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]