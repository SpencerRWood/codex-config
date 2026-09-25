# Personal Codex configuration

This repository is the shared source for the `codex` and `codex2` CLI profiles on this Mac. It contains global guidance, three personal skills, and their supporting scripts and references. It does not contain account credentials, Codex runtime state, or the old Wood Tools `AGENTS.md`.

Run `bash scripts/install.sh` after cloning to link `AGENTS.md` and the skill folders into both Codex homes. The installer refuses to replace existing files or directories. The Wood Tools override is local to this Mac and excluded from that checkout's Git status.

Codex reads global `AGENTS.md` at session start. Restart a session after changing global guidance. Skills can be discovered from their symlinked folders.
