<div align="center">
  🚩🧡🕉️ || जय श्री राम || 🕉️🧡🚩
</div>

---

<div align="center">
  <h1 style="border-bottom: none;">
    🐇 RabbitHole 🕳️
  </h1>
  <p>Build, host, and orchestrate AI agents with ease.</p>
</div>

<p align="center" width="100%">
  <img src="assets/logo.png" alt="RabbitHole Logo" width="300"/>
</p>

<!-- Badges -->
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/VinsmokeSomya/RabbitHole?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/VinsmokeSomya/RabbitHole/stargazers"><img src="https://img.shields.io/github/stars/VinsmokeSomya/RabbitHole?style=for-the-badge&logo=github" alt="Stars"></a>
  <a href="https://github.com/VinsmokeSomya/RabbitHole/issues"><img src="https://img.shields.io/github/issues/VinsmokeSomya/RabbitHole?style=for-the-badge" alt="Issues"></a>
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python" alt="Python Version">
</p>

**RabbitHole** is a Python framework for building and orchestrating LLM-powered agents. It acts as a universal translator, providing a standardized **Agent-to-Agent (A2A) communication protocol** that allows agents from different providers (Google, OpenAI, etc.) to work together seamlessly.

While inspired by tools like LangChain that help build powerful individual agents, RabbitHole focuses on a higher level of abstraction: **multi-agent orchestration**. It provides the backbone for a *society* of agents to collaborate on complex tasks.

## 🤔 Why RabbitHole?

Building AI agents involves more than just writing prompts. You need to handle server setup, communication protocols, and task management. RabbitHole abstracts away this boilerplate, providing a robust foundation for your agent applications.

Use RabbitHole for:
*   **Standardized Communication**: Built on Google's A2A protocol, RabbitHole ensures your agents speak a common language, making them interoperable by design.
*   **Rapid Development**: Get an agent server running with minimal code. Our framework provides the structure, so you can focus on your agent's unique logic.
*   **Extensible by Design**: With a plug-in architecture, RabbitHole makes it easy to integrate agents from different providers. We currently support Google's ADK and OpenAI's Agent SDK, with more on the way.
*   **Integrated Tooling**: Comes with a built-in CLI and a Streamlit UI for easy testing and interaction with your agents right out of the box.

## 🚀 Getting Started

### Installation

Get started by installing RabbitHole directly from the source. We recommend using a virtual environment.

```bash
# 1. Clone the repo
git clone https://github.com/VinsmokeSomya/RabbitHole.git

cd RabbitHole

# 2. Create a virtual environment and activate it
# We recommend `uv`, but Python's venv works great too.
python -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install in editable mode with all dev dependencies
pip install -e ".[dev]"
```

### Run Your First Agent

Let's run the pre-built Google ADK agent.

**1. Set up your API Key:**
Navigate to `rabbithole/agent/adk/`, copy `.env.template` to `.env`, and add your Google API key.

```bash
cd rabbithole/agent/adk

cp .env.template .env
# Now, edit .env to add your key
```

**2. Launch the Agent Server:**
From the `rabbithole/agent/adk` directory, run:
```bash
python __main__.py
```
The agent is now live on `http://localhost:10000`.

**3. Talk to Your Agent (from a new terminal):**
Navigate to the CLI directory and start the client.
```bash
# In a new terminal, from the project root
cd ../../cli

python __main__.py --agent http://localhost:10000
```
You're now chatting with your first agent! For more detailed instructions, check out **[How to Run and Test](./docs/howto.md)**.

## 📚 Documentation

Our documentation provides a deep dive into the framework's architecture, vision, and usage.

- **[Live Documentation Website](https://vinsmokesomya.github.io/RabbitHole/)**: The best place to start, with full search and navigation.
- **[Getting Started](./docs/documentation.md)**: Your main guide to installation, core concepts, and contributing.
- **[Framework Vision](./docs/FRAMEWORK_VISION.md)**: Understand the "why" behind RabbitHole and its strategic direction.
- **[Software Architecture](./docs/architecture.md)**: A technical deep-dive into the system's design.
- **[Feature Ideas](./docs/FEATURE_IDEAS.md)**: See the list of potential upcoming features.
- **[Official Roadmap](./docs/roadmap.md)**: The planned milestones for the project.
- **[Developer Guide](./DEV-README.md)**: Everything you need to know to contribute code.

## 🗺️ Vision & Roadmap

Our vision is to build the premier open-source framework for creating and orchestrating multi-agent systems. To understand our goals and where the project is headed, please see our detailed documents:

- **[Framework Vision & Strategy](./docs/FRAMEWORK_VISION.md)**
- **[Project Roadmap](./docs/roadmap.md)**
- **[Feature Ideas](./docs/FEATURE_IDEAS.md)**

## 🤝 Contributing

RabbitHole is an open-source project, and we welcome contributions from the community! Whether it's adding a new agent integration, improving documentation, or fixing a bug, your help is valued.

Please read our **[Developer Guide](./DEV-README.md)** to get started.

## 📝 License

This project is licensed under the [MIT License](./LICENSE).
