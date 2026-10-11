# Release-branch rollout index — reduced scope

Only **codex-config, pi-config, wood-tools and workflows** remain in the active
rollout. The original 29 PRs are recorded below: three retained and 26 closed without
merge. Every closed PR was inspected live, matched to its exact preserved original
rollout diff and single governance commit, then rechecked for unchanged head before
closing. No mixed-purpose changes were found. Remote branch revisions and local
worktrees were verified afterward; no branch deletion, reset, force-push or merge
was performed. Pi had no original PR and preserves its review-before-commit gate.

The [historical audit](release-branch-audit.md) remains intact. Original diffs,
PR metadata, close logs, dispositions and pre-reduction documents are retained in
`/private/tmp/release-branch-reduction-20261011/`; original rollout validation remains
in `/private/tmp/release-branch-20261011/`. All proposal worktrees and remote branches
use `docs/release-branch-methodology-20261011` and remain available for recovery.

| Repository | Proposal and final disposition | Preserved proposal files |
| --- | --- | --- |
| `architecture-docs` | [PR #12](https://github.com/SpencerRWood/architecture-docs/pull/12) — **closed without merge; adoption deferred**  | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `automerge-repair` | [PR #5](https://github.com/SpencerRWood/automerge-repair/pull/5) — **closed without merge; adoption deferred**  | `.github/workflows/validate.yml`, `.gitignore`, `AGENTS.md`, `pyproject.toml` |
| `codex-config` | [PR #22](https://github.com/SpencerRWood/codex-config/pull/22) — **retained, open and unmerged**  | `AGENTS.md`, `README.md`, `docs/openproject-planning-increments.md`, `docs/wood-delivery-workflow.md`, `skills/openproject-development-workflow/SKILL.md`, `docs/branching-policy.md`, `docs/release-branch-audit.md`, `docs/release-branch-changes.md` |
| `codex-runtime` | [PR #3](https://github.com/SpencerRWood/codex-runtime/pull/3) — **closed without merge; adoption deferred**  | `AGENTS.md`, `pyproject.toml` |
| `events-service` | [PR #12](https://github.com/SpencerRWood/events-service/pull/12) — **closed without merge; adoption deferred**  | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `homelab` | [PR #65](https://github.com/SpencerRWood/homelab/pull/65) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `infrastructure` | [PR #125](https://github.com/SpencerRWood/infrastructure/pull/125) — **closed without merge; adoption deferred**  | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `openproject-reports` | [PR #12](https://github.com/SpencerRWood/openproject-reports/pull/12) — **closed without merge; adoption deferred**  | `.github/workflows/validate.yml`, `AGENTS.md`, `pyproject.toml` |
| `pi-config` | Pending mandatory review — **retained; two instruction files only, approval pending**  | `AGENTS.md`, `docs/pi-policy.md`, `pyproject.toml` |
| `portfolio-website` | [PR #24](https://github.com/SpencerRWood/portfolio-website/pull/24) — **closed without merge; adoption deferred**  | `.github/workflows/validate.yml`, `.gitignore`, `backend/pyproject.toml`, `AGENTS.md` |
| `rag-service` | [PR #10](https://github.com/SpencerRWood/rag-service/pull/10) — **closed without merge; adoption deferred**  | `.github/workflows/validate.yml`, `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `recovery-verification` | [PR #8](https://github.com/SpencerRWood/recovery-verification/pull/8) — **closed without merge; adoption deferred**  | `.github/workflows/validate.yml`, `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `synthetic-website-analytics` | [PR #6](https://github.com/SpencerRWood/synthetic-website-analytics/pull/6) — **closed without merge; adoption deferred**  | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `synthetic-website-analytics-platform` | [PR #2](https://github.com/SpencerRWood/synthetic-website-analytics-platform/pull/2) — **closed without merge; adoption deferred**  | `AGENTS.md` |
| `synthetic-website-data` | [PR #16](https://github.com/SpencerRWood/synthetic-website-data/pull/16) — **closed without merge; adoption deferred**  | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `synthetic-website-dbt` | [PR #10](https://github.com/SpencerRWood/synthetic-website-dbt/pull/10) — **closed without merge; adoption deferred**  | `.gitignore`, `pyproject.toml`, `.github/workflows/validate.yml`, `AGENTS.md` |
| `template-dbt` | [PR #2](https://github.com/SpencerRWood/template-dbt/pull/2) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `template-fastapi-react` | [PR #6](https://github.com/SpencerRWood/template-fastapi-react/pull/6) — **closed without merge; adoption deferred**  | `backend/pyproject.toml`, `AGENTS.md` |
| `template-fastapi-service` | [PR #5](https://github.com/SpencerRWood/template-fastapi-service/pull/5) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `template-python-analytics` | [PR #2](https://github.com/SpencerRWood/template-python-analytics/pull/2) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `template-python-api-client` | [PR #2](https://github.com/SpencerRWood/template-python-api-client/pull/2) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `template-python-cli` | [PR #2](https://github.com/SpencerRWood/template-python-cli/pull/2) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `template-python-dagster` | [PR #3](https://github.com/SpencerRWood/template-python-dagster/pull/3) — **closed without merge; adoption deferred**  | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `template-python-library` | [PR #4](https://github.com/SpencerRWood/template-python-library/pull/4) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `template-synthetic-data` | [PR #2](https://github.com/SpencerRWood/template-synthetic-data/pull/2) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `template-web-automation` | [PR #2](https://github.com/SpencerRWood/template-web-automation/pull/2) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `website-marketing-simulation` | Archived remote; local commit `8650138` — **deferred local proposal; no PR**  | `AGENTS.md` |
| `wood-agents` | Remote inaccessible; local proposal — **deferred local proposal; no PR**  | `AGENTS.md`, `pack/manifest.yaml`, `pack/skills/story-workflow/SKILL.md`, `pack/loops/story/SKILL.md` |
| `wood-charts` | [PR #7](https://github.com/SpencerRWood/wood-charts/pull/7) — **closed without merge; adoption deferred**  | `pyproject.toml`, `AGENTS.md` |
| `wood-reports` | [PR #27](https://github.com/SpencerRWood/wood-reports/pull/27) — **closed without merge; adoption deferred**  | `.gitignore`, `pyproject.toml`, `AGENTS.md` |
| `wood-tools` | [PR #61](https://github.com/SpencerRWood/wood-tools/pull/61) — **retained, open and unmerged**  | `AGENTS.md`, `pyproject.toml` |
| `workflows` | [PR #36](https://github.com/SpencerRWood/workflows/pull/36) — **retained, open and unmerged**  | `.github/workflows/release-container.yml`, `.github/workflows/release.yml`, `docs/branch-rules.md`, `scripts/release_head.py`, `tests/test_release_head.py`, `AGENTS.md` |

## Retained, deferred and duplicated work

- Required now: the canonical Codex/Pi policy, progressive adoption rules, Story
  discovery/lifecycle guidance, explicit Wood branch targets and mapped release
  validation, and centralized main-only publication guards.
- Useful later: application validation caller triggers for `release/v*`, repository
  semantic-release branch restrictions, approved release mappings and release-specific
  verification. Activate them only in a dedicated application adoption task.
- Unnecessary duplication: fleet AGENTS.md strategy sections, template classification
  instructions and `.gitignore` changes solely to track those instructions. Closed
  PRs preserve these proposals as evidence rather than maintaining them independently.
- Pi: only `AGENTS.md` and `docs/pi-policy.md` are retained. Its previous
  `pyproject.toml` proposal is deferred and preserved in `pi-original-proposal.patch`.
- Archived simulation and inaccessible Wood Agents proposals remain deferred locally.

Recovery Verification R1 is the first controlled application adoption. OP-499's
implementation, claim and worktree remain intact. Foundation fixture validation
cannot authorize changing its current branch arrangement or creating a live release.
No release, tag, image publication, deployment or merge into main is authorized here.

See [foundational implementation and validation](release-branch-foundation.md)
for the current tooling and CI contract, consumer activation dependencies and next steps.
