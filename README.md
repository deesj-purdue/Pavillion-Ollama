# Pavillion-Ollama

Run [Ollama](https://ollama.com) in a Docker container with a lightweight Python/Flask chat UI — accessible from any device on your LAN.

## Features

- 🦙 **Ollama** runs entirely locally — no cloud, no telemetry
- 💬 **Streaming chat UI** with conversation history
- 🎨 Dark-themed, responsive interface
- 🔄 Automatic model discovery — switch models from the dropdown
- 📡 Accessible from any browser on your local network

## Requirements

- [Docker](https://docs.docker.com/get-docker/) with the Compose plugin (`docker compose`)
- ~4 GB+ RAM per model (more for larger models)

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/deesj-purdue/Pavillion-Ollama.git
cd Pavillion-Ollama

# 2. (Optional) Copy and edit environment variables
cp .env.example .env

# 3. Start the stack
docker compose up -d

# 4. Pull a model (first run only)
docker exec pavillion-ollama ollama pull llama3.2

# 5. Open the UI
#    Local:  http://localhost:5000
#    LAN:    http://<your-machine-ip>:5000
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `WEB_PORT` | `5000` | Host port for the web UI |
| `DEFAULT_MODEL` | `llama3.2` | Model pre-selected in the dropdown |

## Pulling Models

Any model from the [Ollama library](https://ollama.com/library) can be pulled and immediately used in the UI:

```bash
# Examples
docker exec pavillion-ollama ollama pull mistral
docker exec pavillion-ollama ollama pull gemma3:4b
docker exec pavillion-ollama ollama pull deepseek-r1:8b
```

## Project Structure

```
Pavillion-Ollama/
├── docker-compose.yml   # Ollama + web services
├── .env.example         # Environment variable template
└── app/
    ├── Dockerfile       # Python web service image
    ├── app.py           # Flask app (API + SSE streaming)
    ├── requirements.txt
    └── templates/
        └── index.html   # Chat UI
```

## Stopping / Updating

```bash
# Stop
docker compose down

# Update Ollama image and rebuild web image
docker compose pull
docker compose build --no-cache
docker compose up -d
```