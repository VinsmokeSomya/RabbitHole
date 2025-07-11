<div align="center">
  🚩🧡🕉️ || जय श्री राम || 🕉️🧡🚩
</div>

---

# RabbitHole - Developer Guide

Welcome, contributor! We're thrilled that you're interested in improving RabbitHole. This guide provides all the information you need to get your development environment set up and start contributing.

## 1. Getting Started: Your Development Environment

### 1.1. Prerequisites
- Git
- Python 3.10+
- [Docker](https://www.docker.com/get-started) (for containerized testing)

### 1.2. Fork and Clone
1.  **Fork** the repository on GitHub.
2.  **Clone** your fork locally:
    ```bash
    git clone https://github.com/YOUR-USERNAME/RabbitHole.git
    cd RabbitHole
    ```

### 1.3. Set Up a Virtual Environment
We strongly recommend using a virtual environment to manage project dependencies. The `README.md` recommends `uv`, but if you don't have it, Python's built-in `venv` works perfectly.

```bash
# Using Python's built-in venv
python -m venv .venv
```

Activate the environment before proceeding:
```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 1.4. Install Dependencies
Install the project in **editable mode** (`-e`) with all development dependencies (`[dev]`). This setup links the installed package to your source code, so any changes you make are immediately reflected.

```bash
pip install -e ".[dev]"
```
This command installs all dependencies from `pyproject.toml`, including `pytest` for testing and `ruff` for linting/formatting.

## 2. Running and Testing

### 2.1. Running the Application
For detailed instructions on running the agent server, CLI, and Streamlit UI, please see the **[How to Run and Test Guide](./docs/howto.md)**.

### 2.2. Running the Test Suite
RabbitHole uses `pytest` for testing. To run the full test suite, simply execute:
```bash
pytest
```
Before submitting any changes, please ensure that all existing tests pass and that you've added new tests to cover your changes.

## 3. Code Quality and Conventions

### 3.1. Linting and Formatting
We use `ruff` to maintain a consistent code style and catch potential errors.

- **To check for linting errors:**
  ```bash
  ruff check .
  ```
- **To automatically format your code:**
  ```bash
  ruff format .
  ```

Please run both commands before committing your code to ensure it adheres to the project's standards.

## 4. Contribution Workflow
1.  **Create a New Branch:**
    ```bash
    git checkout -b your-feature-or-fix-name
    ```
2.  **Make Your Changes:** Implement your feature or bug fix.
3.  **Add Tests:** Add unit tests for any new functionality.
4.  **Run Checks:** Ensure your code is formatted and all tests pass.
    ```bash
    ruff format .
    ruff check .
    pytest
    ```
5.  **Commit Your Changes:** Use a clear and descriptive commit message.
    ```bash
    git add .
    git commit -m "feat: Add new agent framework for X"
    ```
6.  **Push to Your Fork:**
    ```bash
    git push origin your-feature-or-fix-name
    ```
7.  **Open a Pull Request:** Go to the original RabbitHole repository and open a pull request from your forked branch. Provide a detailed description of the changes you've made.

## 5. Architectural Deep Dive
To understand the core components, design patterns, and overall philosophy of the framework, please review the **[Software Architecture Description](./docs/architecture.md)**.

Thank you for contributing! 