# Personal Codex configuration

This repository is the shared source for the `codex` and `codex2` CLI profiles on this Mac. It contains global guidance, personal skills, and their supporting scripts and references. It does not contain account credentials, Codex runtime state, or the old Wood Tools `AGENTS.md`.

Run `bash scripts/install.sh` after cloning to link `AGENTS.md` and every `skills/*/SKILL.md` folder into both Codex homes. The installer refuses to replace existing files or directories. The Wood Tools override is local to this Mac and excluded from that checkout's Git status.

`brief-check` runs a command, saves its full combined output locally, and returns compact JSON. For example: `python3 scripts/brief-check.py -- sh -c 'printf "ok\\n"'`. `session-handoff` produces a concise fresh-session checkpoint. To measure local usage, run `python3 scripts/token-report.py --since YYYY-MM-DD`; it reads saved rollouts and reports totals and largest sessions. It does not monitor sessions in the background.

## Wood Tools v2 workflow

The public execution contract is `wood`. Check `wood contract --json` for available commands. Set `OPENPROJECT_URL` from the repository, inject `OPENPROJECT_API_TOKEN` through Infisical, then use the [Story workflow](skills/openproject-development-workflow/SKILL.md) for its review and closure gates. The operational loop is:

```text
wood doctor --json                         # readiness when uncertain
wood project list --json                   # discover project and initiative
wood story next <initiative> --json        # select, then story get <id> --json
wood story start <id> --json               # preview, then --apply after start approval
implement; wood repo validate --json       # local evidence, then review
wood ci status --json                       # current commit after delivery
wood story complete <id> --evidence <file> --json  # preview, then --apply after merge and checks
```

The skill retains the status, branch, CI, implementation update, and review safeguards. Workbook imports use `wood project import-workbook` with a reviewed plan hash. Infisical supplies secret values; Python semantic-release owns version, tag, and GitHub Release changes. The former multi-command workbook and Story instructions have been reduced to this one public command path and two focused skills. See the [cutover inventory](docs/wood-v2-cutover.md) for removed components and instruction-size measurements.

Completed audit findings are saved to the shared Google Drive `Logs/` folder through the `audit-findings-log` skill, unless the specific audit request prohibits Drive writes. The installer links the skill into both Codex homes.

Codex reads global `AGENTS.md` at session start. Restart a session after changing global guidance. Skills can be discovered from their symlinked folders.
