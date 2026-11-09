import json
import urllib.request


def extract_final_response(content: str) -> str:
    """Extrait la réponse finale si une balise de raisonnement existe."""
    if "</think>" in content:
        content = content.rsplit("</think>", 1)[-1]
    return content.strip()


def ask_ollama(
    prompt: str,
    model: str = "llama3.2:3b",
) -> str:
    """Interroge un modèle Ollama local."""

    max_tokens = 1024 if model.startswith("qwen3:") else 256

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0,
            "num_predict": max_tokens,
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
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.load(response)
    except TimeoutError as exc:
        raise RuntimeError(
            "Ollama a depasse le delai de reponse."
        ) from exc

    if result.get("done_reason") == "length":
        raise RuntimeError(
            f"Reponse tronquee pour {model} : limite de tokens atteinte."
        )

    content = result.get("response", "")
    final_response = extract_final_response(content)

    if not final_response:
        raise RuntimeError(
            f"Aucune reponse finale exploitable pour {model}."
        )

    return final_response
