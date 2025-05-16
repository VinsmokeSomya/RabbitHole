# Wormhole Agents 

The `wormhole.a2a` library allows you to build and run agents using various frameworks, including the Google Agent Development Kit (ADK) and OpenAI Agents SDK. We aim to support more agent frameworks in the future—community contributions are welcome!

## Getting Started

```bash
# Navigate to the agent sample directory
cd wormhole/agent/adk

# Create a .env file to store your API credentials
# You can also add other environment variables if required by your agent
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# specify a custom host and port
uv run . --host localhost --port 11011
# or by default
# uv run .
```

## Custom A2A Agent Development

Step 1: Initialize Files
```bash
cd wormhole/agent
# Create project
mkdir example && cd example
# Create required files
touch agent.py task_manager.py __init__.py __main__.py
```

Step 2: Create Custom Agent Class

Implement the following main functions:
```bash
# Non-streaming output
invoke()
# Streaming output
stream()
```

Step 3: Implement AgentTaskManager
```bash
# Non-streaming output
async on_send_task()
# Streaming output
async _run_streaming_agent()
```

Step 4: Define A2ACard

Refer to [A2A](https://github.com/google/A2A/blob/main/specification/json/a2a.json) for AgentCard definition
```python
class AgentCard(BaseModel):
    name: str
    description: str | None = None
    url: str
    provider: AgentProvider | None = None
    version: str
    documentationUrl: str | None = None
    capabilities: AgentCapabilities
    authentication: AgentAuthentication | None = None
    defaultInputModes: List[str] = ["text"]
    defaultOutputModes: List[str] = ["text"]
    skills: List[AgentSkill]
```