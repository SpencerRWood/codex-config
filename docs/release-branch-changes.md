# Release-branch governance change manifest and PR index

The [canonical policy](branching-policy.md) and [audit](release-branch-audit.md)
record the rules, classifications, validation results and enforcement follow-ups.
All proposals use isolated `docs/release-branch-methodology-20261011` worktrees.
No runtime settings, secrets or application implementation change. Application
`main` PRs are governance migration proposals and require explicit migration and
release-effects approval before merge. All created PRs are left unmerged.

| Repository | Proposal | Changed files |
| --- | --- | --- |
| `architecture-docs` | [PR #12](https://github.com/SpencerRWood/architecture-docs/pull/12) | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `automerge-repair` | [PR #5](https://github.com/SpencerRWood/automerge-repair/pull/5) | `.github/workflows/validate.yml`, `.gitignore`, `AGENTS.md`, `pyproject.toml` |
| `codex-config` | [PR #22](https://github.com/SpencerRWood/codex-config/pull/22) | `AGENTS.md`, `README.md`, `docs/openproject-planning-increments.md`, `docs/wood-delivery-workflow.md`, `skills/openproject-development-workflow/SKILL.md`, `docs/branching-policy.md`, `docs/release-branch-audit.md`, `docs/release-branch-changes.md` |
| `codex-runtime` | [PR #3](https://github.com/SpencerRWood/codex-runtime/pull/3) | `AGENTS.md`, `pyproject.toml` |
| `events-service` | [PR #12](https://github.com/SpencerRWood/events-service/pull/12) | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `homelab` | [PR #65](https://github.com/SpencerRWood/homelab/pull/65) | `pyproject.toml`, `AGENTS.md` |
| `infrastructure` | [PR #125](https://github.com/SpencerRWood/infrastructure/pull/125) | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `openproject-reports` | [PR #12](https://github.com/SpencerRWood/openproject-reports/pull/12) | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `pi-config` | Pending mandatory review | `AGENTS.md`, `docs/pi-policy.md`, `pyproject.toml` |
| `portfolio-website` | [PR #24](https://github.com/SpencerRWood/portfolio-website/pull/24) | `.github/workflows/validate.yml`, `.gitignore`, `backend/pyproject.toml`, `AGENTS.md` |
| `rag-service` | [PR #10](https://github.com/SpencerRWood/rag-service/pull/10) | `.github/workflows/validate.yml`, `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `recovery-verification` | [PR #8](https://github.com/SpencerRWood/recovery-verification/pull/8) | `.github/workflows/validate.yml`, `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `synthetic-website-analytics` | [PR #6](https://github.com/SpencerRWood/synthetic-website-analytics/pull/6) | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `synthetic-website-analytics-platform` | [PR #2](https://github.com/SpencerRWood/synthetic-website-analytics-platform/pull/2) | `AGENTS.md` |
| `synthetic-website-data` | [PR #16](https://github.com/SpencerRWood/synthetic-website-data/pull/16) | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `synthetic-website-dbt` | [PR #10](https://github.com/SpencerRWood/synthetic-website-dbt/pull/10) | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `template-dbt` | [PR #2](https://github.com/SpencerRWood/template-dbt/pull/2) | `pyproject.toml`, `AGENTS.md` |
| `template-fastapi-react` | [PR #6](https://github.com/SpencerRWood/template-fastapi-react/pull/6) | `backend/pyproject.toml`, `AGENTS.md` |
| `template-fastapi-service` | [PR #5](https://github.com/SpencerRWood/template-fastapi-service/pull/5) | `pyproject.toml`, `AGENTS.md` |
| `template-python-analytics` | [PR #2](https://github.com/SpencerRWood/template-python-analytics/pull/2) | `pyproject.toml`, `AGENTS.md` |
| `template-python-api-client` | [PR #2](https://github.com/SpencerRWood/template-python-api-client/pull/2) | `pyproject.toml`, `AGENTS.md` |
| `template-python-cli` | [PR #2](https://github.com/SpencerRWood/template-python-cli/pull/2) | `pyproject.toml`, `AGENTS.md` |
| `template-python-dagster` | [PR #3](https://github.com/SpencerRWood/template-python-dagster/pull/3) | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `template-python-library` | [PR #4](https://github.com/SpencerRWood/template-python-library/pull/4) | `pyproject.toml`, `AGENTS.md` |
| `template-synthetic-data` | [PR #2](https://github.com/SpencerRWood/template-synthetic-data/pull/2) | `pyproject.toml`, `AGENTS.md` |
| `template-web-automation` | [PR #2](https://github.com/SpencerRWood/template-web-automation/pull/2) | `pyproject.toml`, `AGENTS.md` |
| `website-marketing-simulation` | Archived remote; local commit `8650138` | `AGENTS.md` |
| `wood-agents` | Remote inaccessible; local proposal | `AGENTS.md`, `pack/manifest.yaml`, `pack/skills/story-workflow/SKILL.md`, `pack/loops/story/SKILL.md` |
| `wood-charts` | [PR #7](https://github.com/SpencerRWood/wood-charts/pull/7) | `pyproject.toml`, `AGENTS.md` |
| `wood-reports` | [PR #27](https://github.com/SpencerRWood/wood-reports/pull/27) | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `wood-tools` | [PR #61](https://github.com/SpencerRWood/wood-tools/pull/61) | `AGENTS.md`, `pyproject.toml` |
| `workflows` | [PR #36](https://github.com/SpencerRWood/workflows/pull/36) | `.github/workflows/release-container.yml`, `.github/workflows/release.yml`, `docs/branch-rules.md`, `scripts/release_head.py`, `tests/test_release_head.py`, `AGENTS.md` |

Pi's three-file proposal passes all four declared checks and awaits its existing
AGENTS.md commit/push/PR review. Wood Agents' inaccessible remote and the archived
simulation repository are not bypassed. The latter's staged-file hooks pass;
its push is rejected because GitHub is read-only.

Existing Codex/Pi policy symlinks need no changes. Adopt codex-config first in the
explicitly installed source checkout and start fresh sessions, then review the
repository adapters. Application Story execution remains blocked until Wood
supports the correct base/naming/evidence contract and approved release scopes
are provisioned. Review, security, CI, rollback and publication/deployment gates
remain in effect; none of these PRs authorizes a merge, release or deployment.
