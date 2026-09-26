#!/usr/bin/env python3
"""Report local Codex rollout token usage without loading transcript content."""

import argparse
from datetime import date
import json
import os
from pathlib import Path

FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens")


def session_usage(path: Path) -> dict | None:
    usage: dict = {}
    session_id = path.stem
    requests = 0
    tool_results = 0
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = item.get("payload") or {}
            if item.get("type") == "session_meta":
                session_id = payload.get("id") or payload.get("session_id") or session_id
            elif item.get("type") == "event_msg" and payload.get("type") == "token_count":
                info = payload.get("info") or {}
                total = info.get("total_token_usage")
                if isinstance(total, dict):
                    usage = total
                    if info.get("last_token_usage"):
                        requests += 1
            elif item.get("type") == "response_item" and payload.get("type") in ("function_call_output", "custom_tool_call_output"):
                tool_results += 1
    if not usage and not tool_results:
        return None
    return {"session_id": session_id, "path": str(path), **{field: int(usage.get(field, 0)) for field in FIELDS}, "request_count": requests, "tool_result_count": tool_results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, action="append", help="Codex home to inspect; repeatable")
    parser.add_argument("--since", type=date.fromisoformat, help="Session directory date, YYYY-MM-DD")
    parser.add_argument("--top", type=int, default=5, help="Largest sessions to show")
    args = parser.parse_args()
    if args.top < 0:
        parser.error("--top must be nonnegative")
    homes = args.codex_home or [Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")), Path.home() / ".codex", Path.home() / ".codex-secondary"]
    sessions = []
    paths = set()
    for home in dict.fromkeys(path.expanduser().resolve() for path in homes):
        for path in (home / "sessions").glob("*/*/*/*.jsonl"):
            if path in paths:
                continue
            paths.add(path)
            if args.since:
                try:
                    day = date.fromisoformat("-".join(path.parts[-4:-1]))
                except ValueError:
                    continue
                if day < args.since:
                    continue
            try:
                record = session_usage(path)
            except OSError:
                continue
            if record:
                sessions.append(record)
    totals = {field: sum(row[field] for row in sessions) for field in (*FIELDS, "request_count", "tool_result_count")}
    print(json.dumps({
        "session_count": len(sessions),
        "totals": totals,
        "largest_sessions": sorted(sessions, key=lambda row: row["input_tokens"] + row["output_tokens"], reverse=True)[:args.top],
        "measurement": "Latest cumulative token_count per rollout; request count uses records with last_token_usage; tool results count response_item outputs.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
