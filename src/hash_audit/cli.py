import argparse
import json
from pathlib import Path
from .agents import audit
from .dataset import generate_accounts,generate_mutations,simulate_migration

def main():
    parser=argparse.ArgumentParser(description="Hash-Audit educational CLI")
    sub=parser.add_subparsers(dest="command",required=True)
    a=sub.add_parser("audit");a.add_argument("file")
    d=sub.add_parser("dataset");d.add_argument("--out",default="results/accounts.json")
    m=sub.add_parser("mutations");m.add_argument("--out",default="data/mutations")
    s=sub.add_parser("migration");s.add_argument("--out",default="results/migration.json")
    args=parser.parse_args()
    if args.command=="audit":
        state=audit(args.file)
        Path("traces").mkdir(exist_ok=True)
        with open("traces/latest.jsonl","w",encoding="utf-8") as f:
            for item in state.trace:f.write(json.dumps(item,ensure_ascii=False)+"\n")
        print(json.dumps({"findings":state.findings,"trace":state.trace},indent=2,ensure_ascii=False))
    else:
        result=generate_accounts() if args.command=="dataset" else generate_mutations() if args.command=="mutations" else simulate_migration()
        out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
        if args.command=="mutations":
            out.mkdir(parents=True,exist_ok=True)
            for i,entry in enumerate(result): (out/f"target_{i:02}.py").write_text(entry["code"],encoding="utf-8")
            (out/"ground_truth.json").write_text(json.dumps([{k:v for k,v in x.items() if k!="code"} for x in result],indent=2),encoding="utf-8")
        else:out.write_text(json.dumps(result,indent=2),encoding="utf-8")
        print(f"Generated {args.out}")
if __name__=="__main__":main()
