# Release-branch governance change manifest

All proposals use isolated `docs/release-branch-methodology-20261011` worktrees.
The canonical definition is [branching-policy.md](branching-policy.md); the
[audit](release-branch-audit.md) records classifications, tests, limitations and
follow-up work. No runtime settings, secrets or application implementation change.
Application `main` PRs in this batch are governance migration proposals, not Story
integration. They require explicit migration/release-effects approval before merge.

| Repository | Changed files |
| --- | --- |
| `architecture-docs` | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `automerge-repair` | `.github/workflows/validate.yml`, `.gitignore`, `AGENTS.md`, `pyproject.toml` |
| `codex-config` | `AGENTS.md`, `README.md`, `docs/openproject-planning-increments.md`, `docs/wood-delivery-workflow.md`, `skills/openproject-development-workflow/SKILL.md`, `docs/branching-policy.md`, `docs/release-branch-audit.md` |
| `codex-runtime` | `AGENTS.md`, `pyproject.toml` |
| `events-service` | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `homelab` | `pyproject.toml`, `AGENTS.md` |
| `infrastructure` | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `openproject-reports` | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `pi-config` | `AGENTS.md`, `docs/pi-policy.md`, `pyproject.toml` |
| `portfolio-website` | `.github/workflows/validate.yml`, `.gitignore`, `backend/pyproject.toml`, `AGENTS.md` |
| `rag-service` | `.github/workflows/validate.yml`, `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `recovery-verification` | `.github/workflows/validate.yml`, `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `synthetic-website-analytics` | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `synthetic-website-analytics-platform` | `AGENTS.md` |
| `synthetic-website-data` | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `synthetic-website-dbt` | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `template-dbt` | `pyproject.toml`, `AGENTS.md` |
| `template-fastapi-react` | `backend/pyproject.toml`, `AGENTS.md` |
| `template-fastapi-service` | `pyproject.toml`, `AGENTS.md` |
| `template-python-analytics` | `pyproject.toml`, `AGENTS.md` |
| `template-python-api-client` | `pyproject.toml`, `AGENTS.md` |
| `template-python-cli` | `pyproject.toml`, `AGENTS.md` |
| `template-python-dagster` | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `template-python-library` | `pyproject.toml`, `AGENTS.md` |
| `template-synthetic-data` | `pyproject.toml`, `AGENTS.md` |
| `template-web-automation` | `pyproject.toml`, `AGENTS.md` |
| `website-marketing-simulation` | `AGENTS.md` |
| `wood-agents` | `AGENTS.md`, `pack/manifest.yaml`, `pack/skills/story-workflow/SKILL.md` |
| `wood-charts` | `pyproject.toml`, `AGENTS.md` |
| `wood-reports` | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `wood-tools` | `AGENTS.md`, `pyproject.toml` |
| `workflows` | `.github/workflows/release-container.yml`, `.github/workflows/release.yml`, `docs/branch-rules.md`, `scripts/release_head.py`, `tests/test_release_head.py`, `AGENTS.md` |

This manifest itself is an additional codex-config documentation file. Existing
Codex/Pi policy symlinks need no changes; the proposed source policy takes effect
only after adoption in the installed codex-config source checkout and new sessions.
