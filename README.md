# Python AI Agent with OpenAI Integration

This project implements a Python-based agent system that interacts with OpenAI's API. The agent runs in a loop of Thought, Action, PAUSE, and Observation, making it suitable for step-by-step reasoning and problem-solving tasks.

## Features

- Custom Agent implementation for OpenAI integration
- Docker containerization with uv package manager
- Environment variable management for secure API key handling

## Prerequisites

- Docker installed on your system
- OpenAI API key
- Python 3.8+ (for local development)

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
```

3. Build the Docker image:

```bash
docker build -t my-python-agent .
```

4. Run the container:

```bash
docker run --env-file .env my-python-agent
```

### Local Development

1. Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Set up the environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```

4. Run the application:

```bash
uv run python main.py
```

## Project Structure

```
.
├── Dockerfile           # Docker configuration
├── entrypoint.sh       # Docker entrypoint script
├── main.py             # Main application code
├── pyproject.toml      # Project dependencies and metadata
├── uv.lock             # Locked dependencies
└── .dockerignore       # Docker build exclusions
```

## Agent Capabilities

The agent supports the following actions:

1. `calculate`: Performs mathematical calculations

   ```python
   Action: calculate: 4 * 7 / 3
   ```

2. `planet_mass`: Retrieves planetary mass information
   ```python
   Action: planet_mass: Earth
   ```

## Docker Commands

Build the image:

```bash
docker build -t my-python-agent .
```

Run with environment variables:

```bash
docker run -e OPENAI_API_KEY=your_api_key_here my-python-agent
```

Run with .env file:

```bash
docker run --env-file .env my-python-agent
```
