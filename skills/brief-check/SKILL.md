---
name: brief-check
description: Run a validation or diagnostic command while retaining its full local output and returning a bounded JSON result. Use when command output may be large.
---

# Brief Check

Run `python3 ../../scripts/brief-check.py -- COMMAND ARG...` from this skill directory. Pass a shell expression as `-- sh -c '...'` when needed. The helper writes complete combined stdout and stderr to a local log, then prints compact JSON with command, exit code, duration, success, failure summary, and log path. Set `--log-dir PATH` to choose a log location or `--timeout SECONDS` to bound execution time.

Read the raw log only when the summary does not explain a failure; use targeted searches or slices instead of loading it into context. The helper does not interpret whether a nonzero exit is acceptable for the task.
