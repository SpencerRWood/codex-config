# Personal Codex configuration

This repository is the shared source for the `codex` and `codex2` CLI profiles on this Mac. It contains global guidance, personal skills, and their supporting scripts and references. It does not contain account credentials, Codex runtime state, or the old Wood Tools `AGENTS.md`.

Run `bash scripts/install.sh` after cloning to link `AGENTS.md` and every `skills/*/SKILL.md` folder into both Codex homes. The installer refuses to replace existing files or directories. The Wood Tools override is local to this Mac and excluded from that checkout's Git status.

Use `wood epic list/get` and `wood release list/get` with `--json` for live
OpenProject planning inspection (requires a Wood Tools version exposing these
commands). Both groups accept project context; get accepts an ID or exact name.
Edit repository code and tests directly instead of writing temporary Python
file generators. Check command help or `wood contract --json` before explaining
and using a fallback for an unsupported operation.

`brief-check` runs a command, saves its full combined output locally, and returns compact JSON. For example: `python3 scripts/brief-check.py -- sh -c 'printf "ok\\n"'`. `session-handoff` produces a concise fresh-session checkpoint. To measure local usage, run `python3 scripts/token-report.py --since YYYY-MM-DD`; it reads saved rollouts and reports totals and largest sessions. It does not monitor sessions in the background.

## Wood Tools v2 workflow

The public execution contract is `wood`. Check `wood contract --json` for available commands. Inject OpenProject credentials through Infisical and use the [Story workflow](skills/openproject-development-workflow/SKILL.md) for review and closure policy. Repositories with `[tool.wood.openproject]` context can omit the Initiative reference:

```text
wood doctor --json                         # readiness when uncertain
wood story next --json
wood story get <id> --json
wood story start <id> --apply --json
# implement and review
wood repo validate --json
wood ci status --json
# after the approved PR merges; retain data.validation_file from repo validate
wood story evidence <id> --validation <validation-file> --pr <number> --ci-run <run-id> --json
wood story evidence <id> --validation <validation-file> --pr <number> --ci-run <run-id> --apply --json
wood story activity add <id> --evidence <evidence-file> --apply --json
wood story complete <id> --evidence <evidence-file> --apply --json
```

The Story skill defines status, branch, CI, review, and evidence safeguards. Workbook imports use `wood project import-workbook` with a reviewed plan hash. Infisical supplies secret values; Python semantic-release owns version, tag, and GitHub Release changes.

Reuse the generated evidence path returned by Wood Tools for activity posting and completion. Logs and generated files follow `[tool.wood.workflow] output_directory` in the current repository's `pyproject.toml`, defaulting to `/private/tmp`. The workflow skill explains regeneration and unsupported-workflow fallbacks.

Completed audit findings are saved to the shared Google Drive `Logs/` folder through the `audit-findings-log` skill, unless the specific audit request prohibits Drive writes. The installer links the skill into both Codex homes.

Codex reads global `AGENTS.md` at session start. Restart a session after changing global guidance. Skills can be discovered from their symlinked folders.

On this Mac, the default `codex` home is `~/.codex`; the `codex2` shell function sets `CODEX_HOME=~/.codex-secondary`. The installer links this repository's guidance and skills into both homes. Verify both links after installation, and start fresh sessions to load changed guidance.
