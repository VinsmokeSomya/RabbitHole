# 1. Base Image - Use an official Python slim image
FROM python:3.10-slim

# 2. Set Environment Variables
#    - PYTHONUNBUFFERED: Ensures print statements and logs are sent straight to terminal
#    - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disc
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

#    - Set the default port the agent server will run on (matching ADK agent's default)
ENV AGENT_PORT=10000

# 3. Set Working Directory
WORKDIR /app

# 4. Install uv (Python package installer and resolver)
#    We use uv for consistency with the local setup described in README.md
RUN pip install uv

# 5. Copy Project Configuration and Lock Files
#    These are needed by uv to install dependencies
COPY pyproject.toml uv.lock ./

# 6. Install Dependencies using uv
#    This leverages your uv.lock for deterministic installs.
#    Installs project in editable mode with 'dev' extras.
#    --system: Install into the global site-packages (common in containers)
#    --no-cache: Reduce image size by not storing download cache for pip
RUN uv pip install --system --no-cache -e .[dev]

# 7. Copy the Application Code
#    The main 'rabbithole' package
COPY rabbithole/ ./rabbithole/
#    Copy assets (e.g., logo) - though likely not needed by the server itself,
#    it's included if any part of the copied code might reference it.
#    Adjust if your agent server specifically needs other top-level files/dirs.
COPY assets/ ./assets/

# 8. Expose the Agent Port (as defined by AGENT_PORT)
EXPOSE ${AGENT_PORT}

# 9. Define the Default Command to Run the ADK Agent Server
#    This runs the ADK agent's __main__.py.
#    It's crucial to use --host 0.0.0.0 so the server is accessible
#    from outside the container when a port is mapped.
CMD ["python", "rabbithole/agent/adk/__main__.py", "--host", "0.0.0.0", "--port", "10000"] 