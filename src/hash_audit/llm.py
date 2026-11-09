
import json
import urllib.request


def ask_ollama(
    prompt: str,
    model: str = "llama3.2:3b",
) -> str:
    """Interroge un modèle Ollama local."""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0,
            "num_predict": 180,
            "num_ctx": 2048,
        },
    }

    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request, timeout=300
        ) as response:
            result = json.load(response)
    except TimeoutError as exc:
        raise RuntimeError(
            "Ollama a dépassé le délai de réponse."
        ) from exc

    return result.get("response", "").strip()
