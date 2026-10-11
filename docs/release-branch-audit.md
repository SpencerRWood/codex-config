# Release-branch governance audit — 2026-10-11

## Scope and disposition

Inspected global Codex/Pi policy links, codex-config Story skills and planning
references, local internal repository AGENTS.md files and purposes, repository
templates, `.github/release.toml`, semantic-release configuration, centralized
`SpencerRWood/workflows` release/validation contracts and Wood Tools source.
Changes are prepared in isolated `docs/release-branch-methodology-20261011`
worktrees. Existing dirty or divergent checkouts are preserved. Archived projects,
old Story worktrees, third-party plugins and employer-owned repositories are
outside this rollout; they do not override the canonical global policy for new work.

The [canonical policy](branching-policy.md) is the sole normative lifecycle
definition. Repository instructions contain classifications and references, not
copies. This task is a governance migration, not an application Story: its
application PRs are prepared against `main` for policy adoption and must not merge
until the user explicitly approves that migration exception and any automatic
release effects. No application release branch or release scope is invented.

## Existing guidance and conflicts

- Shared AGENTS.md preserves Wood-first operations, Infisical-only secret
  injection, repository-owned context, immutable evidence, review, validation,
  rollback and approval boundaries. No unrelated Codex settings are changed.
- The Story skill previously required local `main` as the worktree base,
  `main` as the PR target and local-main update on closure. Those directions now
  depend on the discovered strategy and explicitly reject unsupported selection.
- Existing `feature/op-*` examples describe the current Wood contract, not an
  alias for the required `feat/op-*` / `fix/op-*` naming. Application start is
  blocked until Wood supports the correct base and naming. Claims must not be
  silently rebased or renamed after creation.
- Delivery reporting and evidence combine Story integration with release and
  deployment observations. Instructions now distinguish the three lifecycles;
  absent artifacts/runtime observations are retained without triggering release.
- Existing `R#` Planning Increment hierarchy is preserved. R numbers do not imply
  SemVer; an approved repository release mapping is required before branch creation.
- Many repository AGENTS.md files were ignored/local-only. The rollout preserves
  their existing content, removes the root AGENTS.md ignore where present and
  makes their strategy available for normal review. Template descendants must
  replace the template-maintenance classification before application development.
- Historical Wood Agents pack commands/approval rules predate the current `wood`
  workflow. Its Story skill now references strategy discovery and lifecycle gates;
  comprehensive migration of the unavailable remote pack is separate work.

## Repository classifications

Classification is based on inspected purpose/README, AGENTS.md and capability
metadata, not the folder name or OpenProject ownership domain.

| Strategy | Repositories | Reason |
| --- | --- | --- |
| Release-branch integration | `architecture-docs`, `automerge-repair`, `events-service`, `portfolio-website`, `rag-service`, `recovery-verification` | Deployable applications, services and scheduled workload providers, even when their outcome belongs to Platform/Engineering. |
| Release-branch integration | `openproject-reports` | Scheduled reporting application with its own package/image lifecycle. |
| Release-branch integration | `synthetic-website-analytics`, `synthetic-website-data`, `synthetic-website-dbt`, `website-marketing-simulation` | Product analysis, generation, transformations and simulation implementations. |
| Trunk-based | `infrastructure`, `homelab`, `workflows` | Infrastructure topology/host configuration and shared CI/CD contracts. |
| Trunk-based | `codex-config`, `pi-config`, `wood-agents` | Shared agent configuration, policy and tooling packs. |
| Trunk-based | `codex-runtime`, `wood-tools`, `wood-charts`, `wood-reports` | Reusable shared capacity, operations, chart and publication tooling/libraries. |
| Trunk-based | `synthetic-website-analytics-platform` | Cross-repository architecture/roadmap documentation; no application package. |
| Trunk-based | `template-dbt`, `template-fastapi-react`, `template-fastapi-service`, `template-python-analytics`, `template-python-api-client`, `template-python-cli`, `template-python-dagster`, `template-python-library`, `template-synthetic-data`, `template-web-automation` | Template maintenance; created applications must be reclassified. |

Total: 11 application repositories and 21 trunk repositories inspected. The
simulation repository is archived on GitHub: its instruction commit is retained
locally, but the server rejects its push as read-only. Do not unarchive it as part
of this task. `wood-agents`
remote fetch returns Repository not found; its local proposal is based on cached
`origin/main`, not a verified current remote. Remote access must be restored
before publishing that PR. No active application release was selected or created
by this governance task.

Fetched remote branch inventories contain no `origin/release/*` branches in
any of the eleven application repositories. This is a missing release-provisioning
gate, not authorization to start their next application Story from `main`.

Read-only `wood release list --json` from the events-service mapping confirmed
Wood Platform project 3 has open planning versions `R1` (ID 20) and
`R1 — Wood Pi Harness` (ID 24), alongside closed historical V# versions.
Neither observation defines an approved repository SemVer integration branch;
no OpenProject mutation was performed.

## Codex/Pi alignment

Both `~/.codex/AGENTS.md` and `~/.codex-secondary/AGENTS.md` link to the same
codex-config source. Installed Pi agent directories also link that shared AGENTS.md
and reference Pi's own appended policy. Pi's appended policy now routes release
discovery to `docs/branching-policy.md` through the explicit shared source path.
Existing Pi hard denials, separate operator release path and per-call permission
requirements remain intact. No installer, runtime settings, extension selection,
secret or account configuration changes are necessary.

The proposed policy is in review worktrees, not installed over the user's main
checkouts. Merge codex-config first, update the explicitly installed source
checkout and start fresh sessions to load it. Then deliver repository adapters;
do not point active installations at an unmerged temporary worktree.

## CI and semantic-release compatibility

- Existing application `validate.yml` callers restricted PRs to `main`.
  They now validate PRs into `main` and `release/v*`, and integration pushes to
  `release/v*`. Three synthetic application repositories that had only a main
  release caller gain a read-only validation caller using the same shared contract
  and existing dbt secret bindings. `website-marketing-simulation` has neither
  the release contract nor CI; its checks remain local and CI adoption is follow-up.
- Existing semantic-release consumers omit explicit branch configuration.
  Their configuration now explicitly selects `^main$` with prerelease disabled.
  Release capability tables and version ownership remain unchanged.
- Shared `release.yml` and `release-container.yml` publishing jobs now require
  `refs/heads/main` on `push` or `workflow_dispatch`. Their validation job remains
  separate. The publication freshness helper rejects non-main refs before Git
  access. These guards do not attest release approval or deploy authorization.
- The integrated v3 container path calculates/prepares version metadata, builds
  or reuses one commit/version candidate, verifies its digest and applicable
  runtime checks, then publishes tags/GitHub Release and immutable image references.
  Preserve this ordering after the approved main merge; rebuilding a different
  image after approval would break identity. No candidate push belongs to a Story.
- Legacy `container-release.yml` accepts an existing release tag and validates its
  authority; branch/event restrictions there and consumer adoption of revised
  major workflow references remain technical follow-ups. No existing major tag
  is moved and no workflow is dispatched in this task.
- Infrastructure/homelab main pushes automatically publish and deploy; several
  shared libraries/templates automatically publish on main. Agents must obtain
  separate authorization before a merge that triggers those paths. Separating
  those triggers and promotions requires focused follow-up, not a centralized
  pipeline redesign here. Application main release eligibility still follows
  the release-readiness gate. Existing dev promotion PR/digest controls remain.
- `workflows/docs/branch-rules.md` on fetched main records active main protections
  for workflows/infrastructure/homelab and a disabled portfolio ruleset. Those
  documented protections are preserved; live rulesets were not independently
  re-attested. Release-branch protection/required-check rollout is still needed.
- Actionlint reports undefined `job.workflow_sha` in both shared release callers.
  The exact same two diagnostics occur on their unchanged fetched-main versions;
  the new branch/event conditions add no diagnostic. Repairing that implementation
  checkout authority is a separate existing CI compatibility finding.

## Technical enforcement follow-up

1. Extend Wood's supported contract for strategy/base/target/release discovery,
   approved branch creation, `feat/` and `fix/` naming, and source-bound claim
   recovery. Current `wood story start` has no base selector and starts from
   local `main` (`wood_project/story/session.py`). Validate fetched base freshness.
2. Extend `wood/evidence.py` and `wood/delivery_status.py`: both currently require
   `main` and `feature/op-*`. Accept the verified designated target and explicit
   release mapping, and make Story closure independent of publication/deployment.
   Extend selection to prefer the mapped active release; do not equate R# ordering
   with Git branch discovery. Until supported, application start fails closed.
3. Declare each application's approved OpenProject-to-SemVer release scope and
   provisioning authority. Do not invent active releases or close planning versions.
4. Protect release branches with required review and revision-bound validation;
   reconcile dependency-bot PR targets with application release scopes.
5. Adopt reviewed centralized publishing guards in the consumer workflow versions,
   enforce separately approved trunk publication/deployment, cover legacy tagged
   image callers, and add CI to the simulation application.
6. Restore Wood Agents remote access and migrate its historical command surface
   in a separate scoped change. Retain operator controls and recovery invariants.

## Validation and delivery status

Validation records are retained under `/private/tmp/release-branch-20261011/`;
the [change manifest](release-branch-changes.md) enumerates every instruction and
configuration edit. The codex-config suite passes all 14 tests. All 104 shared
workflow contract tests pass with CI's pinned python-semantic-release 10.6.2.
Pi's pre-commit, lint, typecheck and test checks pass with saved record
`/private/tmp/wood-repo-validate-t0ttg634/validation.json`. The updated Story skill
passes skill-creator validation. Semantic-release's own configuration model accepts
all 27 changed configurations with `^main$` as the sole publishing match.
All ten changed/new application validation callers pass Actionlint.

Of the other 26 repositories declaring Wood validation, 23 pass the full declared
checks. Remaining failures are recorded without bypass:

- `events-service`: pytest and coverage fail in the unchanged disposable
  PostgreSQL fixture at `docker port`; log
  `/private/tmp/wood-repo-validate-e0hgzjzx/04-pytest.log`.
- `template-dbt`: its example Postgres profile has no installed Postgres adapter
  and sqlfluff lacks a configured profile; record
  `/private/tmp/wood-repo-validate-pd64mjoi/validation.json`.
- `wood-charts`: existing 684 KB `uv.lock` exceeds the 500 KB pre-commit large-file
  limit; log `/private/tmp/wood-repo-validate-cmphw0bc/04-pre-commit.log`.

Wood Agents passes 26 scaffold tests after updating its changed content
checksums; one test still expects a missing sibling Wood Tools legacy skill
baseline. Its remote remains unavailable. The documentation-only platform and
simulation changes receive static classification/reference/whitespace checks;
they have no supported Wood validation/CI contract. No unavailable check is marked
passed. Full-stack checks passed after selecting their installed backend environment;
synthetic dbt passed with a temporary example profile. Passing suites are reused.

Static policy
review covers application and infrastructure targeting, missing/stale release
handling, Story completion without publishing/deployment, accumulated release
validation/approval and safe cleanup. Technical limitations above mean the full
automatic Story-selection success criterion is **not yet technically enforced**.
This governance update makes unsupported application execution stop clearly.

No deployments, tags, releases, registry pushes, workflow dispatches, branch
protection changes or application feature edits are authorized by this task.
Normal PR creation is requested; Pi repository instructions still require a
concrete review before commit/push/PR creation. Review and delivery must preserve
that boundary, and no prepared application migration PR should be merged as a
side effect of preparing the policy.

The [PR index](release-branch-changes.md) contains 29 normal, open, unmerged
PRs targeting `main` for this governance rollout. Pi remains a validated local
three-file proposal awaiting its existing review boundary. Wood Agents remains
local pending remote access; the archived simulation's local instruction commit
cannot be pushed. No protection, hook or archival restriction was bypassed.

A single GitHub observation at `2026-10-11T11:05:29.920274+00:00` inspected all
29 PRs and their exact governance-branch workflow runs. It found no publishing,
release, promotion or deployment runs and no truncated run lists. The saved
authority snapshot is `/private/tmp/release-branch-20261011/pr-observation.json`.
This attests to that observation, not to release approval or runtime health.
Wood's shared-workflow CI status returned `CI_EVIDENCE_UNAVAILABLE` because it
looks for validation workflows and does not select the `test-contracts.yml`
authority; the focused GitHub branch/PR read is the explained diagnostic fallback.
