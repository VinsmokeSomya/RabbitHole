# RabbitHole Project Roadmap

This document outlines the planned features, enhancements, and milestones for the RabbitHole framework. Our goal is to evolve RabbitHole into a comprehensive, robust, and easy-to-use platform for building and orchestrating AI agents.

This roadmap is a living document and will be updated as the project evolves and receives community feedback.

---

## Phase 1: Core Framework & Extensibility (Current)

This phase focuses on building a solid foundation and ensuring the framework is stable, extensible, and developer-friendly.

-   [x] **Stable A2A Core:** A robust implementation of the Agent-to-Agent communication protocol.
-   [x] **Extensible Agent Architecture:** A plug-in model for integrating agents from different providers (e.g., Google ADK, OpenAI).
-   [x] **Comprehensive Documentation:** Clear guides for users, contributors, and architects (`documentation.md`, `DEV-README.md`, `architecture.md`).
-   [x] **Integrated Tooling:** Built-in CLI and Streamlit UI for easy interaction and testing.
-   [ ] **Full Test Coverage:** Increase unit and integration test coverage to ensure reliability.

---

## Phase 2: Enhanced Agent Capabilities

This phase is focused on making agents smarter and more capable by giving them access to tools and long-term memory.

-   **🎯 Goal: Standardized Tool & Function Calling**
    -   **Description:** Develop a universal interface within the framework for agents to declare and use external tools (e.g., APIs, databases, custom functions). This is crucial for building agents that can act on the world.
    -   **Key Features:**
        -   A standardized schema for defining tools.
        -   Automatic handling of tool-use requests and responses within the A2A protocol.
        -   Examples of agents using tools for tasks like web search or data retrieval.

-   **🎯 Goal: Long-Term Memory Management**
    -   **Description:** Provide built-in, pluggable solutions for agents to persist information across conversations.
    -   **Key Features:**
        -   Integrations with popular vector stores (e.g., ChromaDB, FAISS) for semantic memory.
        -   Simple key-value stores for short-term memory.
        -   An abstract `Memory` base class that developers can extend.

-   **🎯 Goal: Human-in-the-Loop (HITL)**
    -   **Description:** Implement checkpoints in agent execution where a human can review, approve, or redirect the agent's plan. This is essential for building safe and reliable autonomous systems.
    -   **Key Features:**
        -   An API hook to pause a task and await external validation.
        -   Integration with the Streamlit UI to display pending actions and accept user input.

---

## Phase 3: Multi-Agent Orchestration

This phase will elevate RabbitHole from a single-agent framework to a multi-agent system, enabling the creation of complex, collaborative agent workflows.

-   **🎯 Goal: Agent Orchestration Engine (RabbitHole Conductor)**
    -   **Description:** Introduce a new component, tentatively named the "Conductor," responsible for managing workflows between multiple agents. This is analogous to systems like LangGraph.
    -   **Key Features:**
        -   Define workflows as graphs where nodes are agents and edges represent the flow of information.
        -   A "supervisor" agent that can route tasks to specialized agents.
        -   Support for parallel, sequential, and conditional execution of agent tasks.

---

## Phase 4: Production & Ecosystem

This phase is focused on making RabbitHole production-ready and fostering a strong community ecosystem.

-   **🎯 Goal: Simplified Deployment & Monitoring**
    -   **Description:** Provide tools and documentation for deploying RabbitHole agents at scale.
    -   **Key Features:**
        -   One-click deployment templates for cloud services (e.g., Google Cloud Run, AWS Lambda).
        -   Integration with observability tools like LangSmith for tracing and debugging.

-   **🎯 Goal: Community Tool & Agent Hub**
    -   **Description:** Create a centralized repository or registry where the community can share and discover pre-built agents, tools, and prompts.
    -   **Key Features:**
        -   A command-line interface to easily download and use community-contributed components.
        -   A public website showcasing available agents and tools.

-   **🎯 Goal: Agent Evaluation & Benchmarking**
    -   **Description:** Create a robust suite for evaluating agent performance on standardized tasks and datasets. This allows developers to measure the impact of changes to prompts, models, or tools.
    -   **Key Features:**
        -   A library of common benchmarks (e.g., web browsing, code generation).
        -   Metrics for tracking cost, latency, accuracy, and tool usage.
        -   Integration with `wandb` or similar tools for logging and visualizing results.

---

## Phase 5: User Experience & Accessibility

This phase is dedicated to making RabbitHole more powerful and accessible to a wider range of developers and users.

-   **🎯 Goal: Advanced GUI / Playground**
    -   **Description:** Develop a rich, web-based graphical interface for visually building, debugging, and managing agentic workflows.
    -   **Key Features:**
        -   A drag-and-drop interface for composing multi-agent graphs.
        -   Real-time visualization of agent state and message flow.
        -   An integrated prompt engineering environment.

-   **🎯 Goal: Multi-Language Client SDKs**
    -   **Description:** Broaden the framework's reach by providing client SDKs for other popular programming languages.
    -   **Key Features:**
        -   A full-featured client SDK for JavaScript/TypeScript.
        -   Potentially a client SDK for Go or other languages based on community demand. 