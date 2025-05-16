import streamlit as st
from rabbithole.a2a.client.client import A2AClient
from rabbithole.a2a.types import Task, Message, TextPart, FilePart, TaskSendParams, TaskStatus, TaskState, SendTaskResponse
from uuid import uuid4
import asyncio
import json
import traceback
import httpx

def run_streamlit_app():
    st.set_page_config(page_title="🐇 The Rabbit Hole", layout="wide")
    st.title("🐇 Rabbit Hole")

    # Initialize session state for conversation history if it doesn't exist
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'agent_url' not in st.session_state:
        st.session_state.agent_url = "http://localhost:10000" # Default ADK agent port

    with st.sidebar:
        st.header("⚙️ Configuration")
        st.session_state.agent_url = st.text_input("Agent Server URL", value=st.session_state.agent_url)
        
        if st.button("Clear Conversation"):
            st.session_state.conversation = []
            st.rerun()

    st.header("💬 Chat with your Agent")

    # Display conversation history
    for author, message_content in st.session_state.conversation:
        with st.chat_message(author):
            if isinstance(message_content, str):
                st.markdown(message_content)
            elif isinstance(message_content, dict) and 'url' in message_content: # Basic image handling
                 st.image(message_content['url'])
            # Add more content type handlers as needed

    user_prompt = st.chat_input("Type your message here...")

    if user_prompt:
        st.session_state.conversation.append(("user", user_prompt))
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Placeholder for agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if not st.session_state.agent_url:
                        st.error("Agent Server URL is not set. Please configure it in the sidebar.")
                        st.stop()

                    client = A2AClient(url=st.session_state.agent_url)
                    
                    user_message = Message(
                        role="user",
                        parts=[TextPart(text=user_prompt)]
                    )
                    task_send_params = TaskSendParams(
                        id=f"streamlit-ui-{uuid4().hex}",
                        message=user_message
                    )
                    
                    send_task_response: SendTaskResponse = asyncio.run(
                        client.send_task(payload=task_send_params.model_dump())
                    )

                    agent_response_display = "No response from agent."
                    returned_task: Task | None = None

                    if send_task_response:
                        if send_task_response.result:
                            returned_task = send_task_response.result
                        elif send_task_response.error:
                            agent_response_display = f"Agent Error: {send_task_response.error.message} (Code: {send_task_response.error.code})\nDetails: {send_task_response.error.data}"
                    
                    if returned_task: # Only process if we have a valid task result
                        if returned_task.status and returned_task.status.message:
                            response_message = returned_task.status.message
                            for part in response_message.parts:
                                if isinstance(part, TextPart):
                                    agent_response_display = part.text
                                    break 
                                elif isinstance(part, FilePart) and part.file and part.file.uri:
                                    agent_response_display = {"url": part.file.uri}
                                    break
                        elif returned_task.artifacts:
                            found_artifact_content = False
                            for artifact_item in returned_task.artifacts:
                                for part in artifact_item.parts:
                                    if isinstance(part, TextPart) and part.text:
                                        agent_response_display = part.text
                                        found_artifact_content = True
                                        break 
                                if found_artifact_content:
                                    break 
                            if not found_artifact_content and returned_task.status: # If artifacts existed but no text content found
                                agent_response_display = f"Task status: {returned_task.status.state.value} (No displayable content in artifacts)"
                        elif returned_task.status: 
                            agent_response_display = f"Task status: {returned_task.status.state.value}"
                    
                    # If agent_response_display hasn't been updated by a successful task or a server error message, it keeps "No response from agent."
                    # Or if send_task_response was None (should not happen with current try/except but good for robustness)
                    elif not send_task_response:
                        agent_response_display = "Failed to get any response from server."

                    st.session_state.conversation.append(("assistant", agent_response_display))
                    
                    # Display the actual response (will be re-rendered on next cycle)
                    # Forcing a re-run to show the new message immediately
                    st.rerun()

                except httpx.HTTPStatusError as http_err:
                    error_message = f"HTTP error occurred: {http_err} - {http_err.request.url}"
                    try:
                        error_detail = http_err.response.json()
                        error_message += f"\nServer response: {json.dumps(error_detail, indent=2)}"
                    except json.JSONDecodeError:
                        error_message += f"\nServer response: {http_err.response.text}"
                    st.session_state.conversation.append(("assistant", error_message))
                    st.error(error_message)
                    st.rerun()
                except Exception as e:
                    error_message = f"An unexpected error occurred in Streamlit app: {type(e).__name__} - {e}"
                    st.session_state.conversation.append(("assistant", error_message))
                    st.error(error_message)
                    st.rerun()

if __name__ == "__main__":
    run_streamlit_app() 