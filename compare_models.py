import csv
import time
from datetime import datetime
from pathlib import Path

from hash_audit.llm import ask_ollama_detailed

MODELS = ["llama3.2:3b", "qwen3:4b"]

PROMPT = (
    "Une application stocke les mots de passe avec MD5. "
    "Explique le risque principal et recommande Argon2id. "
    "Reponds en francais en deux phrases."
)

RESULTS_FILE = Path("results/model_benchmark.csv")
RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

FIELDS = [
    "date",
    "model",
    "duration_seconds",
    "eval_count",
    "done_reason",
    "status",
    "prompt",
    "final_response",
    "raw_response",
]

def run_benchmark():
    file_exists = RESULTS_FILE.exists() and RESULTS_FILE.stat().st_size > 0

    with RESULTS_FILE.open("a", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, delimiter=";")

        if not file_exists:
            writer.writeheader()

        for model in MODELS:
            print(f"\n===== {model} =====", flush=True)
            start = time.perf_counter()

            row = {
                "date": datetime.now().isoformat(timespec="seconds"),
                "model": model,
                "duration_seconds": "",
                "eval_count": "",
                "done_reason": "",
                "status": "error",
                "prompt": PROMPT,
                "final_response": "",
                "raw_response": "",
            }

            try:
                result = ask_ollama_detailed(PROMPT, model=model)
                row.update({
                    "eval_count": result["eval_count"],
                    "done_reason": result["done_reason"],
                    "status": result["status"],
                    "final_response": result["final_response"],
                    "raw_response": result["raw_response"],
                })
            except Exception as exc:
                row["raw_response"] = f"{type(exc).__name__}: {exc}"

            row["duration_seconds"] = round(
                time.perf_counter() - start, 2
            )

            writer.writerow(row)
            file.flush()

            print("Statut :", row["status"])
            print("Duree :", row["duration_seconds"], "secondes")
            print("Tokens :", row["eval_count"])
            print("Fin :", row["done_reason"])
            print("Reponse finale :", row["final_response"])

    print("\nResultats enregistres dans :", RESULTS_FILE)


if __name__ == "__main__":
    run_benchmark()
