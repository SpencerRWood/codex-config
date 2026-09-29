---
name: session-handoff
description: Create a compact, verified checkpoint for continuing an active objective in a fresh Codex session. Use at an objective, repository, or deployment boundary or when the user requests a handoff.
---

# Session Handoff

Create a concise checkpoint from verified work in the current session. Include these fields: Goal, Completed, Current State, Changed Files / PRs / Releases, Validation, Blockers, Next Exact Action, and References. Use `none` for empty fields and distinguish observed results from pending work. Include paths and links needed to resume, without copying transcripts, long logs, secrets, or speculative status. Target 500–800 words maximum; use less when the facts fit. Save it to a file only when the user requests an artifact; otherwise return it in the response.
