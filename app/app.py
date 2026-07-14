from flask import Flask, render_template, request, Response, stream_with_context
import requests
import json
import os

app = Flask(__name__)

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "llama3.2")
SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    "You are a helpful assistant. Keep your answers short and concise. Avoid unnecessary elaboration.",
)


def get_models():
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return [m["name"] for m in data.get("models", [])]
    except requests.RequestException:
        return []


@app.route("/")
def index():
    models = get_models()
    return render_template("index.html", models=models, default_model=DEFAULT_MODEL)


@app.route("/api/models")
def api_models():
    return {"models": get_models()}


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(force=True)
    model = body.get("model", DEFAULT_MODEL)
    messages = body.get("messages", [])

    if SYSTEM_PROMPT.strip() and not any(m.get("role") == "system" for m in messages):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
    }

    def generate():
        try:
            with requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
                stream=True,
                timeout=120,
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        done = chunk.get("done", False)
                        yield f"data: {json.dumps({'content': content, 'done': done})}\n\n"
                        if done:
                            break
        except requests.RequestException as e:
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
