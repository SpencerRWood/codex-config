#!/usr/bin/env python3
"""Run a command, save its complete output, and print bounded JSON."""

import argparse
from collections import deque
import json
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import time

MAX_LINE = 180
MAX_FAILURES = 3
FAILURE = re.compile(r"\b(error|failed|failure|exception|traceback|fatal)\b", re.I)


def summarize(path: Path) -> tuple[str, int]:
    tail: deque[str] = deque(maxlen=2)
    failures: deque[str] = deque(maxlen=MAX_FAILURES)
    lines = 0
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for raw in stream:
            lines += 1
            line = raw.strip().replace("\x00", "")[:MAX_LINE]
            if line:
                tail.append(line)
                if FAILURE.search(line):
                    failures.append(line)
    return " | ".join(failures or tail)[:540], lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", type=Path, help="Directory for the complete log")
    parser.add_argument("--timeout", type=float, help="Maximum command duration in seconds")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("provide a command after --")
    if args.timeout is not None and args.timeout <= 0:
        parser.error("--timeout must be positive")
    log_dir = (args.log_dir or Path(tempfile.gettempdir()) / "codex-brief-check").expanduser().resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix="check-", suffix=".log", dir=log_dir, delete=False) as log:
        log_path = Path(log.name)
        start = time.monotonic()
        timed_out = False
        try:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            exit_code = 124
        except OSError as exc:
            log.write(f"Could not start command: {exc}\n".encode())
            exit_code = 127
        duration = round(time.monotonic() - start, 3)
    summary, lines = summarize(log_path)
    success = exit_code == 0
    print(json.dumps({
        "command": shlex.join(command)[:300],
        "exit_code": exit_code,
        "duration_seconds": duration,
        "success": success,
        "failure_summary": "" if success else ("Timed out. " if timed_out else "") + (summary or f"Exited with code {exit_code}."),
        "line_count": lines,
        "raw_log_path": str(log_path),
    }, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
