---
title: Getting Started
description: How to install and run RabbitHole.
---

## What is RabbitHole?
**RabbitHole** is a developer-friendly Python framework designed to simplify the creation and orchestration of AI agents. It wraps Google's core **A2A (Agent-to-Agent)** communication protocol, providing the structure to build, host, and interact with agents from various providers like Google (ADK) and OpenAI.

The primary goal of RabbitHole is to let you focus on your agent's unique logic, not the boilerplate of communication protocols and server setup.

### Key Features
- **Minimal Code:** Spin up a new A2A-compliant agent with very little code.
- **Extensible:** Designed as a plug-in architecture, allowing for the easy addition of new agent SDKs.
- **Interoperable:** Enables agents built on different platforms to communicate using a single, standardized protocol.
- **CLI Included:** Comes with a built-in command-line client for easy testing and interaction.
- **Dockerized:** Includes a Dockerfile for reproducible, containerized deployments.

---

## Installation
Getting up and running with RabbitHole is simple. The recommended approach is to use `uv` for fast package management.

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

## Quick Start: Running the ADK Agent
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