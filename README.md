<div align="center">
  <h1 style="border-bottom: none;">
    🐇 RabbitHole 🕳️
  </h1>
</div>
<p align="center" width="100%">
  <img src="assets/logo.png" alt="RabbitHole Logo" width="200"/>
</p>

**RabbitHole** 🌀 wraps Google's official [A2A](https://github.com/google/A2A) repository with a developer-friendly layer that:

📦 Minimal code to spin up an **A2A Agent**  
⚡ Keeps in lock-step with upstream **Google A2A** releases  
🌱 Adds plug-ins for **Google ADK**, **OpenAI Agents SDK**, **MCP**, and more on the way!

## 📜 Table of Contents

- [🛠️ Installation](#installation)
  - [💡 What is UV?](#what-is-uv)
- [⚡ A2A Agents Unleashed](#a2a-agents-unleashed)
  - [Prerequisites 📋](#prerequisites)
  - [🚀 Quick Start Guide](#quick-start-guide)
- [🐳 Running with Docker](#running-with-docker)
  - [Prerequisites](#prerequisites-1)
  - [Building the Docker Image](#building-the-docker-image)
  - [Running the Docker Container](#running-the-docker-container)
- [🗺️ Project Structure](#project-structure)
- [🔄 Project Workflow Diagram](#project-workflow-diagram)
- [🤝 Contributing](#contributing)
- [📝 License](#license)

## 🛠️ Installation

```bash
# 1. Clone the RabbitHole repository 🐾
git clone https://github.com/VinsmokeSomya/RabbitHole.git
cd RabbitHole
```

```bash
# 2. Create a virtual environment and install dependencies ➕🐍
# (Using uv, a fast Python package installer and resolver)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"  # Editable install + development extras
```

### 💡 What is UV?
UV is a modern Python package management tool that's significantly faster than pip and pip-tools. Learn more and install it from [astral.sh/uv](https://astral.sh/uv).
If you don't have `uv` installed:

```bash
# For Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
# For Windows, check https://astral.sh/uv/install for instructions.
```

```bash
# Verify installation
uv --version
```

## ⚡ A2A Agents Unleashed

The ```rabbithole.a2a``` library allows you to build and run agents using various frameworks, including:
- Google Agent Development Kit (ADK) 🤖
- OpenAI Agents SDK 🧠

We aim to support more agent frameworks in the future—community contributions are welcome! 🤝

### Prerequisites 📋

*   Python 3.9+ 🐍
*   UV Package Manager (or pip, see alternative setup)
*   Access to a compatible LLM and a valid API key (e.g., Google API key for Gemini) 🔑

### 🚀 Quick Start Guide

#### Step 1: Navigate to an Agent Sample Directory 📁
Let's pick the Google ADK agent for this example:
```bash
cd rabbithole/agent/adk
```

#### Step 2: Set Up Your Environment 🔑
Create a `.env` file in the chosen agent directory (`rabbithole/agent/adk/`) to store your API credentials:
```bash
# Replace 'your_api_key_here' with your actual Google API Key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```
You can also add other environment variables if required by your agent (e.g., for other LLM providers).

#### Step 3: Launch the Agent Server 📡
From the agent directory (e.g., `rabbithole/agent/adk`):
```bash
# Default host (localhost) and port (e.g., 10000 for ADK agent)
uv run . 
# Or python __main__.py if not using uv
```

To specify a custom host and port:
```bash
uv run . --host localhost --port 11011
# Or python __main__.py --host localhost --port 11011
```
📝 *Make sure to note the port if you override it—it will be needed by the A2A client.*

#### Step 4: Start the A2A CLI Client in a New Terminal 💻
Navigate to the CLI directory:
```bash
cd rabbithole/cli
```
Run the client, connecting to the agent server's port:
```bash
# Replace YOUR_PORT with the correct agent server port (e.g., 10000 or 11011)
uv run . --agent http://localhost:YOUR_PORT
```
Or

```bash
python __main__.py --agent http://localhost:YOUR_PORT
```
Example:
```bash
uv run . --agent http://localhost:10000
```
🎉 You should now be able to interact with your agent!

## 🐳 Running with Docker

You can also run the RabbitHole agent server (specifically the ADK agent for this example) using Docker. This provides a containerized environment for your application.

### Prerequisites

*   **Docker Installed**: Ensure Docker Desktop (for Windows/Mac) or Docker Engine (for Linux) is installed and running on your system. You can find installation instructions at [docker.com](https://www.docker.com/get-started).

### Building the Docker Image

A `Dockerfile` is provided in the project root to build an image for the ADK agent server.

1.  **Navigate to the project root directory** (where the `Dockerfile` is located) in your terminal.
2.  **Build the image** by running:
    ```bash
    docker build -t rabbithole-adk-agent .
    ```
    *   `-t rabbithole-adk-agent`: Tags the image with the name `rabbithole-adk-agent` for easy reference.
    *   `.`: Specifies the current directory as the build context (where Docker looks for the `Dockerfile` and project files).

### Running the Docker Container

Once the image is built, you can run a container from it:

```bash
docker run --rm -it -e GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_API_KEY" -p 10000:10000 rabbithole-adk-agent
```

Let's break down this command:
*   `docker run`: The command to start a new container.
*   `--rm`: Automatically removes the container when it stops. This is useful for cleanup.
*   `-it`: Runs the container in interactive mode and allocates a pseudo-TTY, allowing you to see the server logs and stop it with `Ctrl+C`.
*   `-e GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_API_KEY"`: This is **crucial**. It sets the `GOOGLE_API_KEY` environment variable inside the container. Replace `"YOUR_ACTUAL_GOOGLE_API_KEY"` with your real Google API key. The agent server running inside the container will use this key.
*   `-p 10000:10000`: Maps port `10000` on your host machine to port `10000` inside the container. The ADK agent server in the Docker image is configured to run on port `10000` and listen on `0.0.0.0`.
*   `rabbithole-adk-agent`: The name of the Docker image to run.

After running this command, the ADK agent server should be running inside the Docker container, and you should see its logs in your terminal.

**Connecting the CLI Client to the Dockerized Server:**

Your local CLI client (from `rabbithole/cli/`) can then connect to this Dockerized agent server using the address `http://localhost:10000` (since port 10000 on your host is mapped to the container's port 10000).

```bash
# From your local rabbithole/cli directory, after activating your local venv
python __main__.py --agent http://localhost:10000
# Or using uv, if you prefer:
# uv run . --agent http://localhost:10000
```

## 🗺️ Project Structure

Here's a glimpse into the RabbitHole 🐇🕳️:
```ascii
RabbitHole/
├── .git/               # Git version control files
├── .venv/              # Python virtual environment (e.g., created by `uv venv`)
├── assets/             # Logos, images, etc.
│   └── logo.png
├── rabbithole/         # <--- Your main Python package!
│   ├── __init__.py
│   ├── a2a/            # Core Agent-to-Agent (A2A) protocol implementation
│   │   ├── __init__.py
│   │   ├── client/     # A2A client logic (connecting to agents)
│   │   │   ├── __init__.py
│   │   │   ├── card_resolver.py
│   │   │   └── client.py
│   │   ├── server/     # A2A server logic (hosting agents)
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   ├── task_manager.py
│   │   │   └── utils.py
│   │   ├── types.py    # A2A data types, Pydantic models, and schemas
│   │   └── utils/      # Shared utilities for A2A (e.g., auth)
│   │       ├── __init__.py
│   │       └── push_notification_auth.py
│   ├── agent/          # Specific agent implementations
│   │   ├── __init__.py
│   │   ├── adk/        # Google ADK based agent example
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py  (Runnable ADK agent server 🚀)
│   │   │   ├── agent.py     (ADK agent core logic)
│   │   │   └── task_manager.py
│   │   └── oai/        # OpenAI based agent example
│   │       ├── __init__.py
│   │       ├── __main__.py  (Runnable OpenAI agent server 🚀)
│   │       ├── agent.py     (OpenAI agent core logic)
│   │       └── task_manager.py
│   └── cli/            # Command Line Interface (CLI) to interact with agents
│       ├── __init__.py
│       ├── __main__.py      (Runnable CLI client 💻)
│       └── push_notification_listener.py
├── .gitignore          # Files and directories ignored by Git
├── pyproject.toml      # Project metadata, dependencies, build config (PEP 518)
├── README.md           # You are here! 👋
└── uv.lock             # Lock file for deterministic dependencies (uv)
```

## 🔄 Project Workflow Diagram

Visualizing the Agent Interaction Flow:

```ascii

  +----------------------+      +--------------------------------+      +-----------------------+
  | 👤 User via CLI      | ---> | 🐇 RabbitHole Agent Server    | ---> | 🧠 LLM (e.g., Gemini) | 
  | (rabbithole/cli)     | <--- | (rabbithole/agent/adk or /oai) | <--- | (generative AI)       |
  +----------------------+      +--------------------------------+      +-----------------------+
          ^        \                                 ^
          |         \ (Optional Push Notifications)  | (A2A Protocol)
          |          \                               |
          |           V                              |
          |  +----------------------------+          |
          |  | Push Notification Listener |          |
          |  | (within CLI client)        |          |
          |  +----------------------------+          |
          |                                          |
          +---- Task Responses & Updates <-----------+ 

```
**Key Workflow Steps:**

1.  ▶️ **User Interaction**: User sends a prompt or command through the `CLI Client`.
2.  ↪️ **Request Forwarding**: The `CLI Client` packages this as an A2A request and sends it to the active `RabbitHole Agent Server` (e.g., ADK agent).
3.  ⚙️ **Server Processing**: The `Agent Server`:
    *   Receives the task.
    *   Interacts with the configured `LLM` (like Google Gemini) for language understanding and generation.
    *   Manages the task lifecycle (e.g., using its `task_manager.py`).
    *   May use specific agent logic from its `agent.py`.
4.  ↩️ **Response Delivery**: The `Agent Server` sends the LLM's response (or streams updates) back to the `CLI Client` via the A2A protocol.
5.  🔔 **Push Notifications (Optional)**: If configured:
    *   The `Agent Server` can send asynchronous updates (push notifications) to a URL provided by the client.
    *   The `Push Notification Listener` (running as part of the CLI or a separate client-side service) receives these updates.

## 🤝 Contributing

We're actively expanding support for other agent frameworks and cool features! If you're interested in contributing 🧑‍💻, adding custom tools 🛠️, or have ideas 💡, feel free to:
*   Open a Pull Request
*   Start a Discussion

Your contributions are highly welcome!

## 📝 License

This project is licensed under the [MIT License](LICENSE).
