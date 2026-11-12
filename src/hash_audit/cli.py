import argparse
import json
from pathlib import Path

from .agents import audit
from .dataset import generate_accounts, generate_mutations, simulate_migration


def audit_batch(input_dir: str, output_file: str):
    directory = Path(input_dir)
    truth_file = directory / "ground_truth.json"

    if not truth_file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {truth_file}")

    ground_truth = json.loads(truth_file.read_text(encoding="utf-8"))

    aliases = {
        "md5": {"md5"},
        "sha1": {"sha1"},
        "fast_sha256": {"sha256_unsalted"},
        "constant_salt": {"constant_salt"},
        "timing_comparison": {"timing_comparison"},
        "truncated_hash": {"truncated_hash"},
        "bad_encoding": {"bad_encoding"},
        "argon2id": {"argon2id"},
    }

    results = []
    matched_count = 0
    audited_count = 0

    for entry in ground_truth:
        file_id = entry["id"]
        expected = entry["mutation"]
        filename = f"target_{file_id:02}.py"
        target = directory / filename

        if not target.exists():
            results.append({
                "file": filename,
                "expected": expected,
                "detected": False,
                "error": "Fichier absent",
                "findings": [],
            })
            continue

        state = audit(str(target), use_llm=False)
        audited_count += 1

        detected_schemes = sorted({
            finding.get("scheme", "")
            for finding in state.findings
        })

        expected_aliases = aliases.get(expected, {expected})
        matched = bool(expected_aliases.intersection(detected_schemes))

        if matched:
            matched_count += 1

        results.append({
            "file": filename,
            "expected": expected,
            "detected": matched,
            "detected_schemes": detected_schemes,
            "findings": state.findings,
            "trace": state.trace,
        })

    total = len(ground_truth)
    detection_rate = (
        round(100 * matched_count / total, 2)
        if total else 0
    )

    report = {
        "summary": {
            "total": total,
            "audited": audited_count,
            "matched": matched_count,
            "not_matched": total - matched_count,
            "detection_rate_percent": detection_rate,
            "evaluation": "Correspondance entre mutation attendue et détection statique",
            "llm_enabled": False,
        },
        "results": results,
    }

    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))
    print(f"\nRapport enregistré : {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Hash-Audit educational CLI"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    a = sub.add_parser("audit")
    a.add_argument("file")

    batch = sub.add_parser("audit-batch")
    batch.add_argument("--input", default="data/mutations")
    batch.add_argument("--out", default="results/mutation_audit.json")

    d = sub.add_parser("dataset")
    d.add_argument("--out", default="results/accounts.json")

    m = sub.add_parser("mutations")
    m.add_argument("--out", default="data/mutations")

    s = sub.add_parser("migration")
    s.add_argument("--out", default="results/migration.json")

    args = parser.parse_args()

    if args.command == "audit":
        state = audit(args.file)
        Path("traces").mkdir(exist_ok=True)

        with open("traces/latest.jsonl", "w", encoding="utf-8") as file:
            for item in state.trace:
                file.write(json.dumps(item, ensure_ascii=False) + "\n")

        print(json.dumps({
            "findings": state.findings,
            "trace": state.trace,
        }, indent=2, ensure_ascii=False))

    elif args.command == "audit-batch":
        audit_batch(args.input, args.out)

    else:
        if args.command == "dataset":
            result = generate_accounts()
        elif args.command == "mutations":
            result = generate_mutations()
        else:
            result = simulate_migration()

        output = Path(args.out)
        output.parent.mkdir(parents=True, exist_ok=True)

        if args.command == "mutations":
            output.mkdir(parents=True, exist_ok=True)

            for index, entry in enumerate(result):
                (output / f"target_{index:02}.py").write_text(
                    entry["code"],
                    encoding="utf-8",
                )

            truth = [
                {key: value for key, value in entry.items() if key != "code"}
                for entry in result
            ]

            (output / "ground_truth.json").write_text(
                json.dumps(truth, indent=2),
                encoding="utf-8",
            )
        else:
            output.write_text(
                json.dumps(result, indent=2),
                encoding="utf-8",
            )

        print(f"Generated {args.out}")


if __name__ == "__main__":
    main()
