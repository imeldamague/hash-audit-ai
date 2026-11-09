import csv
import time
from datetime import datetime
from pathlib import Path

from hash_audit.llm import ask_ollama

MODELS = ["llama3.2:3b", "qwen3:4b"]
PROMPT = (
    "Une application stocke les mots de passe avec MD5. "
    "Explique le risque principal et recommande Argon2id. "
    "Reponds en francais en deux phrases."
)

RESULTS_FILE = Path("results/model_comparison.csv")
RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

with RESULTS_FILE.open("a", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";")

    if file.tell() == 0:
        writer.writerow([
            "date",
            "model",
            "duration_seconds",
            "status",
            "prompt",
            "response",
        ])

    for model in MODELS:
        print(f"\n===== {model} =====", flush=True)
        start = time.perf_counter()

        try:
            response = ask_ollama(PROMPT, model=model)
            status = "success"
        except Exception as exc:
            response = f"{type(exc).__name__}: {exc}"
            status = "error"

        duration = round(time.perf_counter() - start, 2)

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            model,
            duration,
            status,
            PROMPT,
            response,
        ])
        file.flush()

        print("Statut :", status)
        print("Duree :", duration, "secondes")
        print("Reponse :", response)

print("\nResultats enregistres dans :", RESULTS_FILE)
