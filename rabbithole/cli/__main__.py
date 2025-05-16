import asyncclick as click
import asyncio
import base64
import os
import urllib
from uuid import uuid4
from dotenv import load_dotenv
from typing import Optional, Union, cast, List, Any

from rabbithole.a2a.client import A2AClient, A2ACardResolver
from rabbithole.a2a.types import (
    TaskState,
    Task,
    TextPart,
    FilePart,
    FileContent,
    Message,
    TaskSendParams,
    PushNotificationConfig,
    AuthenticationScheme,
    GetTaskResponse,
    SendTaskResponse,
    TaskQueryParams,
)
from rabbithole.a2a.utils.push_notification_auth import PushNotificationReceiverAuth


@click.command()
@click.option("--agent", default="http://localhost:10000")
@click.option("--session", default="0")
@click.option("--history", default=False, is_flag=True)
@click.option("--use_push_notifications", default=False, is_flag=True)
@click.option("--push_notification_receiver", default="http://localhost:5000")
async def cli(agent: str, session: str, history: bool, use_push_notifications: bool, push_notification_receiver: str):
    card_resolver = A2ACardResolver(agent_url=agent)
    card = await card_resolver.get_agent_card()

    if not card:
        print(f"Could not resolve agent card from {agent}")
        return

    print("======= Agent Card ========")
    print(card.model_dump_json(exclude_none=True))

    notif_receiver_parsed = urllib.parse.urlparse(push_notification_receiver)
    notification_receiver_host: Optional[str] = notif_receiver_parsed.hostname
    notification_receiver_port: Optional[int] = notif_receiver_parsed.port

    if use_push_notifications:
        if not card.capabilities.pushNotifications:
            print("Agent does not support push notifications. Ignoring --use_push_notifications.")
            use_push_notifications = False
        elif not notification_receiver_host or not notification_receiver_port:
            print("Push notification receiver host or port is missing. Ignoring --use_push_notifications.")
            use_push_notifications = False
        else:
            from .push_notification_listener import PushNotificationListener
            agent_base_url = card.url
            parsed_agent_url = urllib.parse.urlparse(agent_base_url)
            well_known_jwks_url = urllib.parse.urlunparse(
                (parsed_agent_url.scheme, parsed_agent_url.netloc, "/.well-known/jwks.json", "", "", "")
            )
            jwks_uri_from_card = None
            if card.authentication:
                for auth_method in card.authentication:
                    if auth_method.scheme == AuthenticationScheme.BEARER_TOKEN and auth_method.jwksUrl:
                        jwks_uri_from_card = auth_method.jwksUrl
                        break
            
            jwks_url_to_use = jwks_uri_from_card or well_known_jwks_url

            print(f"Attempting to load JWKS from: {jwks_url_to_use}")

            notification_receiver_auth = PushNotificationReceiverAuth()
            try:
                print(f"JWKS loading from {jwks_url_to_use} needs to be implemented if not handled by PushNotificationReceiverAuth.")

            except Exception as e:
                print(f"Failed to load JWKS: {e}. Push notifications might not be authenticated correctly.")


            push_notification_listener = PushNotificationListener(
                host=cast(str, notification_receiver_host),
                port=cast(int, notification_receiver_port),
                notification_receiver_auth=notification_receiver_auth,
            )
            push_notification_listener.start()
        
    client = A2AClient(agent_card=card)
    current_sessionId: str
    if session == "0":
        current_sessionId = uuid4().hex
    else:
        current_sessionId = session

    continue_loop = True
    streaming_supported = card.capabilities.streaming

    while continue_loop:
        taskId = uuid4().hex
        print("=========  starting a new task ======== ")
        continue_loop = await completeTask(
            client, 
            streaming_supported, 
            use_push_notifications, 
            notification_receiver_host, 
            notification_receiver_port, 
            taskId, 
            current_sessionId
        )

        if history and continue_loop:
            print("========= history ======== ")
            task_query_params = TaskQueryParams(id=taskId, historyLength=10)
            task_response = await client.get_task(task_query_params)
            if task_response.result:
                 print(task_response.model_dump_json(include={"result": {"history"}}))
            elif task_response.error:
                print(f"Error getting task history: {task_response.error.message}")


async def completeTask(
    client: A2AClient, 
    streaming_supported: bool, 
    use_push_notifications: bool, 
    notification_receiver_host: Optional[str], 
    notification_receiver_port: Optional[int], 
    taskId: str, 
    sessionId: str
) -> bool:
    prompt_text = click.prompt(
        "\nWhat do you want to send to the agent? (:q or quit to exit)"
    )
    if prompt_text.lower() in [":q", "quit"]:
        return False
    
    message_parts: List[Union[TextPart, FilePart]] = [TextPart(type="text", text=prompt_text)]
    
    file_path = click.prompt(
        "Select a file path to attach? (press enter to skip)",
        default="",
        show_default=False,
    )
    if file_path and file_path.strip() != "":
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
                file_content_b64 = base64.b64encode(file_bytes).decode('utf-8')
                file_name = os.path.basename(file_path)
            
            message_parts.append(
                FilePart(
                    type="file",
                    file=FileContent(
                        name=file_name,
                        bytes=file_content_b64,
                    )
                )
            )
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping attachment.")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}. Skipping attachment.")

    current_message = Message(role="user", parts=message_parts)
 
    task_send_params = TaskSendParams(
        id=taskId,
        sessionId=sessionId,
        acceptedOutputModes=["text"],
        message=current_message,
    )

    if use_push_notifications and notification_receiver_host and notification_receiver_port:
        task_send_params.pushNotification = PushNotificationConfig(
            url=f"http://{notification_receiver_host}:{notification_receiver_port}/notify",            
            authentication=[AuthenticationScheme.BEARER_TOKEN],
        )

    taskResult: Union[GetTaskResponse, SendTaskResponse, None] = None
    
    actual_streaming_to_use = streaming_supported
    if streaming_supported and card.capabilities.streamingHttpV1alpha is False:
        print("Agent supports general streaming but not streamingHttpV1alpha. Falling back to non-streaming.")
        actual_streaming_to_use = False


    if actual_streaming_to_use:
        try:
            response_stream = client.send_task_streaming(task_send_params)
            async for result_item in response_stream:
                print(f"stream event => {result_item.model_dump_json(exclude_none=True)}")
                if result_item.result and result_item.result.final:
                    pass 
            taskResult = await client.get_task(TaskQueryParams(id=taskId))
        except Exception as e:
            print(f"Error during streaming: {e}")
            taskResult = await client.get_task(TaskQueryParams(id=taskId))

    else:
        taskResult = await client.send_task(task_send_params)
        if taskResult:
            print(f"\n{taskResult.model_dump_json(exclude_none=True)}")

    if taskResult and taskResult.result and taskResult.result.status:
        final_task_details = cast(Task, taskResult.result)
        current_state_val = final_task_details.status.state
        
        if current_state_val == TaskState.INPUT_REQUIRED:
            return await completeTask(
                client,
                streaming_supported,
                use_push_notifications,
                notification_receiver_host,
                notification_receiver_port,
                taskId,
                sessionId
            )
        else:
            print(f"Task {taskId} finished with state: {current_state_val.value}")
            return True
    elif taskResult and taskResult.error:
        print(f"Task {taskId} resulted in an error: {taskResult.error.message}")
        return True
    else:
        print(f"Task {taskId} did not return a valid result or status. Ending interaction.")
        return False


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(cli())
