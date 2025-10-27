import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from typing import Any


def count_lines(path: str) -> int:
    p = pathlib.Path(path)
    if not p.exists():
        return 0
    with p.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def read_state(state_path: str) -> dict[str, Any]:
    p = pathlib.Path(state_path)
    if not p.exists():
        return {"lines_processed": 0, "migrated_count": 0}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"lines_processed": 0, "migrated_count": 0}


def main() -> None:
    ap = argparse.ArgumentParser(description="Run NDJSON -> Firestore import in loops with sleeps between iterations")
    ap.add_argument("--in", dest="in_path", required=True)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--write-batch", type=int, default=75)
    ap.add_argument("--throttle", type=float, default=3.0)
    ap.add_argument("--iter-size", type=int, default=1000, help="Max rows per iteration (passed as --max-rows)")
    ap.add_argument("--sleep-sec", type=int, default=120, help="Seconds to sleep between iterations")
    ap.add_argument("--iter-timeout", type=int, default=900, help="Max seconds per iteration before retry")
    ap.add_argument("--state", default=None, help="Override state file path (default: <in>.state.json)")
    args = ap.parse_args()

    in_path = args.in_path
    state_path = args.state or (in_path + ".state.json")

    total = count_lines(in_path)
    print({"total_lines": total, "state_path": state_path})
    sys.stdout.flush()

    iter_no = 1
    while True:
        st = read_state(state_path)
        lines_processed = int(st.get("lines_processed") or 0)
        print(f"[Check] {lines_processed}/{total}")
        sys.stdout.flush()
        if total > 0 and lines_processed >= total:
            print("All lines processed. Exiting.")
            sys.stdout.flush()
            break
        print(f"=== Iteration {iter_no} ===")
        sys.stdout.flush()
        cmd = [
            sys.executable,
            "scripts/import_ndjson_to_firestore.py",
            "--in", in_path,
            "--collection", args.collection,
            "--id-field", args.id_field,
            "--write-batch", str(args.write_batch),
            "--throttle", str(args.throttle),
            "--max-rows", str(args.iter_size),
        ]
        try:
            print({"cmd": cmd, "iter_timeout": args.iter_timeout})
            sys.stdout.flush()
            res = subprocess.run(cmd, check=True, text=True, timeout=int(args.iter_timeout))
        except subprocess.CalledProcessError as e:
            print(f"[Error] Import iteration failed with exit code {e.returncode}. Will retry after sleep.")
            sys.stdout.flush()
        except subprocess.TimeoutExpired:
            print(f"[Timeout] Import iteration exceeded {args.iter_timeout}s. Will retry after sleep.")
            sys.stdout.flush()
        # Print state after iteration
        st = read_state(state_path)
        print({
            "lines_processed": st.get("lines_processed"),
            "migrated_total": st.get("migrated_count"),
            "iteration": iter_no,
        })
        sys.stdout.flush()
        iter_no += 1
        sleep_sec = int(args.sleep_sec)
        print(f"Sleeping {sleep_sec}s for quota...")
        sys.stdout.flush()
        time.sleep(sleep_sec)


if __name__ == "__main__":
    main()
