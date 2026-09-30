---
name: brief-check
description: Run a validation or diagnostic command while retaining its full local output and returning a bounded JSON result. Use when command output may be large.
---

# Brief Check

Run `python3 ../../scripts/brief-check.py -- COMMAND ARG...` from this skill directory. Pass a shell expression as `-- sh -c '...'` when needed. The helper writes complete combined stdout and stderr to a local log, then prints compact JSON with command, exit code, duration, success, failure summary, and log path. Set `--log-dir PATH` to choose a log location or `--timeout SECONDS` to bound execution time.

Read the raw log only when the summary does not explain a failure; use targeted searches or slices instead of loading it into context. The helper does not interpret whether a nonzero exit is acceptable for the task.

Wood Tools already returns bounded JSON and retains full logs for supported
repository validation and verification. Use `wood repo validate --json`,
`wood repo verify --json`, or `wood ci failures --json` directly for those operations;
reuse their structured result and returned log paths instead of wrapping them or
running a second check. For a Story delivery briefing, consume an existing
`wood delivery status <id> --json` snapshot and its stage, blocker, and next action.
Use this helper for an explained unsupported repository check or a Codex-specific
diagnostic whose raw output would otherwise be large. Its `success` describes
the command exit, not Story delivery completion.
