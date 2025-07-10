# RabbitHole Documentation

Welcome to the official documentation for RabbitHole!

## 1. What is RabbitHole?
**RabbitHole** is a developer-friendly Python framework designed to simplify the creation and orchestration of AI agents. It wraps Google's core **A2A (Agent-to-Agent)** communication protocol, providing the structure to build, host, and interact with agents from various providers like Google (ADK) and OpenAI.

The primary goal of RabbitHole is to let you focus on your agent's unique logic, not the boilerplate of communication protocols and server setup.

### Key Features
- **Minimal Code:** Spin up a new A2A-compliant agent with very little code.
- **Extensible:** Designed as a plug-in architecture, allowing for the easy addition of new agent SDKs.
- **Interoperable:** Enables agents built on different platforms to communicate using a single, standardized protocol.
- **CLI Included:** Comes with a built-in command-line client for easy testing and interaction.
- **Dockerized:** Includes a Dockerfile for reproducible, containerized deployments.

---

## 2. Getting Started
Getting up and running with RabbitHole is simple. The recommended approach is to use `uv` for fast package management.

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/VinsmokeSomya/RabbitHole.git
    cd RabbitHole
    ```
2.  **Create a virtual environment and install dependencies:**
    ```bash
    # Create the virtual environment
    uv venv

    # Activate it
    # On Windows: .venv\Scripts\activate
    # On macOS/Linux: source .venv/bin/activate
    source .venv/bin/activate

    # Install the project in editable mode with dev dependencies
    uv pip install -e ".[dev]"
    ```

### Quick Start: Running the ADK Agent
1.  **Navigate to the ADK agent directory:**
    ```bash
    cd rabbithole/agent/adk
    ```
2.  **Set up your API Key:**
    Copy the `.env.template` file to a new file named `.env` and add your Google API Key.
    ```bash
    cp .env.template .env
    # Now edit .env with your key
    ```
3.  **Launch the Agent Server:**
    From the `rabbithole/agent/adk` directory, run:
    ```bash
    uv run .
    ```
    The server will start, typically on `http://localhost:10000`.

4.  **Talk to your Agent:**
    Open a **new terminal**, activate the virtual environment again, and navigate to the CLI directory:
    ```bash
    cd rabbithole/cli
    uv run . --agent http://localhost:10000
    ```
    You can now send messages to your agent!

---

## 3. Core Concepts

To effectively use RabbitHole, it's helpful to understand its core components.

- **A2A Server (`rabbithole/a2a/server`)**
  This is the heart of the framework. It's a web server (using FastAPI) that listens for incoming tasks, manages their execution, and sends back results. It handles all the complexities of the A2A protocol.

- **Agent (`rabbithole/agent/*`)**
  This is where you implement your specific logic. An "Agent" in RabbitHole is a Python module that defines how to handle a task. RabbitHole provides examples for Google's ADK and OpenAI's SDK, which you can use as templates for your own.

- **CLI Client (`rabbithole/cli`)**
  A command-line tool for sending tasks to a running A2A server. It's the primary way to interact with and debug your agents during development.

### 3.1. High-Level Workflow
Here is a diagram visualizing how the components interact when a user sends a message:

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

1.  **User Interaction**: A user sends a prompt through the `CLI Client`.
2.  **Request Forwarding**: The CLI packages the prompt into an A2A request and sends it to the `RabbitHole Agent Server`.
3.  **Server Processing**: The Agent Server receives the task, invokes the specific agent logic (e.g., the ADK agent), and communicates with an external `LLM` to get a response.
4.  **Response Delivery**: The Agent Server sends the LLM's response back to the CLI Client.
5.  **Push Notifications (Optional)**: For long-running tasks, the server can send asynchronous updates back to a listener running on the client side.

---

## 4. Next Steps

- **Explore the Project's Vision:**
  To understand the "why" behind the project, its strategic goals, and how it's different from other frameworks, read the **[Framework Vision & Strategy](./FRAMEWORK_VISION.md)**.

- **Understand the Architecture:**
  For a technical deep-dive into the design principles and system components, read the **[Software Architecture Description](./architecture.md)**.

- **Create Your Own Agent:**
  Follow the pattern in the `rabbithole/agent/adk` directory to create a new agent with a different LLM or custom tools.

- **See What's Next:**
  Check out the **[Official Roadmap](./roadmap.md)** for planned milestones and the **[Feature Ideas](./FEATURE_IDEAS.md)** log for what we're considering.

- **Contribute to the Project:**
  We welcome contributions! Check the `README.md` for guidelines on how to contribute. 