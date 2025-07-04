# How to Run and Test RabbitHole

This guide provides a focused, step-by-step walkthrough for running the RabbitHole agent, clients, and test suite.

## 1. Prerequisites
- Python 3.11+
- Git
- Docker (Optional, for containerized deployment)

---

## 2. Running the Agent (Local Development)

This method uses a local Python virtual environment and is ideal for development and testing.

### Step 1: Clone and Install
```bash
# Clone the repository
git clone https://github.com/VinsmokeSomya/RabbitHole.git
cd RabbitHole

# Create and activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
source .venv/bin/activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Step 2: Set Up Your API Key
The agent needs a Large Language Model (LLM) to function.
1.  Navigate to the agent directory: `cd rabbithole/agent/adk`
2.  Copy the template environment file: `cp .env.template .env`
3.  Open the new `.env` file and add your `GOOGLE_API_KEY`.

### Step 3: Run the Agent Server
From the `rabbithole/agent/adk` directory, start the server:
```bash
# This will run the __main__.py in the current directory
python .
```
The server will start on `http://localhost:10000`. Leave this terminal window running.

### Step 4: Run the CLI Client
Open a **new terminal window**, activate the virtual environment again, and run the following:
```bash
# Navigate to the CLI directory
cd rabbithole/cli

# Run the client, pointing to the agent server
python . --agent http://localhost:10000
```
You can now chat with your agent via the command line.

### Step 5: Run the Streamlit UI
To use the web interface, open a **new terminal window**, activate the virtual environment, and run the following from the project's **root directory**:
```bash
streamlit run rabbithole/ui/streamlit_app.py
```
Open the URL provided (usually `http://localhost:8501`) in your browser.

---

## 3. Running the Agent (Docker)

This method runs the agent in a container, which is great for production-like environments.

### Step 1: Build the Docker Image
From the project's **root directory**, run:
```bash
docker build -t rabbithole-adk-agent .
```

### Step 2: Run the Docker Container
Run the image and inject your API key as an environment variable.
```bash
# Replace "YOUR_API_KEY" with your actual Google API key
docker run --rm -it -e GOOGLE_API_KEY="YOUR_API_KEY" -p 10000:10000 rabbithole-adk-agent
```
The agent server is now running inside the container and is accessible on `localhost:10000`.

### Step 3: Connect with the CLI Client
You can use the same local CLI client from Step 4 of the local development section to connect to the Dockerized agent.

---

## 4. Running the Test Suite

This is crucial for contributors to ensure that no changes have broken existing functionality.

### Step 1: Ensure Dev Dependencies are Installed
Make sure you have installed the project using the `[dev]` extra, as shown in the local development setup.

### Step 2: Run Pytest
From the project's **root directory**, simply run:
```bash
pytest
```
This will discover and run all the tests in the `tests/` directory. 