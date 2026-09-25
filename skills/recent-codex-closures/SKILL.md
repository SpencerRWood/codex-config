---
name: recent-codex-closures
description: Identify Codex sessions that recently closed or terminated on this machine, including sessions absent from saved thread history. Use when a user asks which Codex sessions just disappeared after a terminal or Termius disconnect.
---

# Recent Codex Closures

Run `python3 scripts/recent_closures.py --minutes 90` from this skill directory. The helper reads local Codex SQLite shutdown logs across `CODEX_HOME`, `~/.codex`, and `~/.codex-secondary`, then joins saved thread metadata when available. It prints a compact list with local times, session IDs, titles, and whether work was saved. Increase `--minutes` only when the reported disconnect falls outside the initial window. Use `--codex-home PATH` to target another installation.

Treat shutdown time and last saved activity as different facts. A closed session may have no saved user prompt or rollout. State that clearly; do not substitute an older saved thread for a recently closed empty one. The helper reports logged Codex shutdowns; an abrupt process kill may leave no shutdown entry. These records describe only the local machine. If the user was connected to another host, identify that host before claiming to have found its sessions.

If the user needs the last task step, inspect only the matching saved rollout and summarize its final assistant message. Avoid printing raw prompts, tool output, environment variables, or secret values. The helper is read only and does not resume or stop sessions.
