# RabbitHole Framework: Feature Ideas

This document logs potential features and enhancements for the RabbitHole framework, categorized by theme. This is based on the initial project analysis and aligns with the official roadmap.

## Theme 1: Enhance Core Capabilities (The "What It Can Do")

These features expand the fundamental power of what an agent built with RabbitHole can achieve.

-   **Standardized Tool & Function Calling:**
    -   **What:** Create a formal, standardized way for an agent to declare it wants to use a tool (e.g., a web search, calculator, or database lookup). The framework would intercept this request, execute the tool's code, and inject the result back into the agent's context.
    -   **Why:** It makes tool-use a first-class citizen of the A2A protocol, decoupling agent logic from tool implementation and enabling a library of reusable tools.

-   **Pluggable Memory Architecture:**
    -   **What:** Introduce a `BaseMemory` abstract class and provide a few default implementations (e.g., `InMemoryMemory`, `FileMemory`, `VectorDBMemory`).
    -   **Why:** Makes the framework flexible, allowing developers to choose the right memory solution for their needs without rewriting agent logic.

## Theme 2: Improve the Developer Experience (The "How It Feels to Use")

These features make the framework easier and more pleasant to work with, which is critical for adoption.

-   **Project Scaffolding CLI:**
    -   **What:** Add a command like `rabbithole new agent --name my-agent` to automatically generate boilerplate for a new agent.
    -   **Why:** Dramatically lowers the barrier to entry and streamlines the development process, which is a hallmark of mature frameworks.

-   **Centralized Configuration Management:**
    -   **What:** Implement a central `config.toml` file for managing secrets, API keys, and other settings, using Pydantic's settings management.
    -   **Why:** Simplifies setup and deployment, making the system cleaner and more secure by avoiding scattered `.env` files.

## Theme 3: Increase Reliability & Trust (The "Can I Bet My Project On It?")

These features build confidence in the framework, making it suitable for more serious, production-oriented projects.

-   **Agent Evaluation & Testing Harness:**
    -   **What:** Create a dedicated testing suite to test agent compliance, functionality, and performance.
    -   **Why:** Provides developers with the tools to ensure their custom agents are robust and reliable, promoting a strong testing culture.

-   **Built-in Observability & Tracing:**
    -   **What:** Integrate structured logging and tracing (e.g., `trace_id`) throughout the `a2a/server` to provide a consolidated view of the entire lifecycle of a task.
    -   **Why:** Gives developers the visibility needed to debug complex agent behaviors, which is invaluable for fixing bugs in a distributed system. 