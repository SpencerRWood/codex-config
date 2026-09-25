#!/usr/bin/env python3
"""Show recent local Codex shutdowns without loading whole session transcripts."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sqlite3
import sys


def connect_readonly(path: Path) -> sqlite3.Connection | None:
    if not path.is_file():
        return None
    try:
        return sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    except sqlite3.Error as exc:
        print(f"Could not read {path.name}: {exc}", file=sys.stderr)
        return None


def short_names(path: Path) -> dict[str, str]:
    names: dict[str, str] = {}
    if not path.is_file():
        return names
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item.get("id"), str) and isinstance(item.get("thread_name"), str):
                names[item["id"]] = item["thread_name"].replace("\n", " ")[:100]
    return names


def local_time(epoch: int) -> str:
    return dt.datetime.fromtimestamp(epoch).astimezone().strftime("%Y-%m-%d %I:%M:%S %p %Z")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minutes", type=int, default=90, help="Lookback window; default: 90")
    parser.add_argument("--limit", type=int, default=8, help="Maximum closures; default: 8")
    parser.add_argument("--codex-home", type=Path, action="append", help="Inspect only this Codex home; repeat for multiple homes")
    parser.add_argument("--json", action="store_true", help="Machine readable output")
    args = parser.parse_args()
    if args.minutes < 1 or args.limit < 1:
        parser.error("--minutes and --limit must be positive")

    candidates = args.codex_home or [
        Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        Path.home() / ".codex",
        Path.home() / ".codex-secondary",
    ]
    roots = list(dict.fromkeys(path.expanduser().resolve() for path in candidates))
    cutoff = int(dt.datetime.now().timestamp()) - args.minutes * 60
    results = []
    found_log = False
    for root in roots:
        logs = connect_readonly(root / "logs_2.sqlite")
        if logs is None:
            continue
        found_log = True
        try:
            rows = logs.execute(
                "SELECT MAX(ts), thread_id FROM logs "
                "WHERE ts >= ? AND thread_id IS NOT NULL "
                "AND feedback_log_body LIKE '%Shutting down Codex instance%' "
                "GROUP BY thread_id ORDER BY MAX(ts) DESC LIMIT ?",
                (cutoff, args.limit),
            ).fetchall()
        except sqlite3.Error as exc:
            print(f"Could not query {root}/logs_2.sqlite: {exc}", file=sys.stderr)
            continue
        finally:
            logs.close()

        state = connect_readonly(root / "state_5.sqlite")
        names = short_names(root / "session_index.jsonl")
        for timestamp, thread_id in rows:
            saved = None
            if state is not None:
                try:
                    saved = state.execute(
                        "SELECT source, rollout_path FROM threads WHERE id = ?", (thread_id,)
                    ).fetchone()
                except sqlite3.Error:
                    pass
            rollout = Path(saved[1]) if saved and saved[1] else None
            results.append({
                "closed_at": local_time(timestamp),
                "closed_epoch": timestamp,
                "codex_home": str(root),
                "session_id": thread_id,
                "name": names.get(thread_id, "(no saved title)"),
                "source": saved[0] if saved else None,
                "saved_rollout": bool(rollout and rollout.is_file()),
            })
        if state is not None:
            state.close()
    if not found_log:
        print("No local Codex shutdown log is available.", file=sys.stderr)
        return 1
    results.sort(key=lambda item: item["closed_epoch"], reverse=True)
    results = results[:args.limit]
    for item in results:
        del item["closed_epoch"]

    if args.json:
        print(json.dumps(results, indent=2))
    elif not results:
        print(f"No logged Codex shutdowns in the last {args.minutes} minutes on this machine.")
    else:
        for item in results:
            status = "saved" if item["saved_rollout"] else "no saved transcript"
            print(f'{item["closed_at"]} | {item["name"]} | {status}')
            print(f'  {item["session_id"]} | {item["codex_home"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
