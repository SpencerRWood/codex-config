# Personal Codex configuration

This repository is the shared source for the `codex` and `codex2` CLI profiles on this Mac. It contains global guidance, personal skills, and their supporting scripts and references. It does not contain account credentials, Codex runtime state, or the old Wood Tools `AGENTS.md`.

Run `bash scripts/install.sh` after cloning to link `AGENTS.md` and every `skills/*/SKILL.md` folder into both Codex homes. The installer also links the tracked OpenProject environment helper into `~/.wood/scripts`. It converts an existing identical helper file into the managed link, and refuses to replace differing files. The Wood Tools override is local to this Mac and excluded from that checkout's Git status.

`brief-check` runs a command, saves its full combined output locally, and returns compact JSON. For example: `python3 scripts/brief-check.py -- sh -c 'printf "ok\\n"'`. `session-handoff` produces a concise fresh-session checkpoint. To measure local usage, run `python3 scripts/token-report.py --since YYYY-MM-DD`; it reads saved rollouts and reports totals and largest sessions. It does not monitor sessions in the background.

Codex reads global `AGENTS.md` at session start. Restart a session after changing global guidance. Skills can be discovered from their symlinked folders.
