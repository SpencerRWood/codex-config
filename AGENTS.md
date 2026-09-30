# Shared Codex Guidance

- Prefer short, bounded execution phases over long-running sessions.
- At logical objective, repository, or deployment boundaries, create a concise handoff and start a fresh session when practical.
- Prefer deterministic helpers with bounded structured output over repeated exploratory commands or large raw logs.
- Keep full diagnostic output on disk and return only the summary, failures, relevant identifiers, and log path.
- Do not repeatedly rerun expensive validation unless a change or failure requires it.
- Read only the files and documentation needed for the current task.
- Prefer existing repository commands, scripts, and skills over recreating equivalent logic ad hoc.
- Use `wood epic list/get` and `wood release list/get` for supported live OpenProject inspection, with `--json` and project/status/offset options as needed. Release inspection refers to OpenProject planning versions.
- Edit repository code and tests directly with patch/edit tools. Do not create temporary Python file-writing helpers for routine changes. Check the supported command surface before using custom API scripts, and explain any unsupported-operation fallback.
- For OpenProject Story work, use the `openproject-development-workflow` skill. Prefer supported `wood` commands with `--json` and available filters. Use direct tools or custom scripts only for unsupported operations or focused diagnosis, and explain the fallback.
- Reuse the validation record and generated delivery inputs returned by Wood Tools. Use `wood story evidence` for supported repository workflows instead of manually assembling routine evidence JSON or implementation-update Markdown; follow the workflow skill for verification and posting.
- Keep project-specific workflows, architecture, and implementation guidance in repository-local AGENTS files or task-specific skills.
- Before external, destructive, production, or irreversible actions, require explicit confirmation unless the action is already covered by an approved workflow.
- After completing an audit, use the shared `audit-findings-log` skill to save its findings in Google Drive `Logs/`. This standing workflow is authorized by the user; a specific audit request that forbids Drive writes takes precedence.
- When finishing a task, report the verified state, validation performed, blockers, and the next exact action.
