# Branching and delivery policy

This is the canonical development methodology for every active repository:
`feature/* → development → main`. Repository purpose selects applicable release
artifacts and deployment behavior; it does not select a different branch strategy.

## Ordinary development

Every active repository has long-lived main and development branches. Main is
stable and releasable; development integrates accumulated release work. Ordinary
Story branches originate from fetched development and their PRs target development.
Merge completed Story PRs after repository-appropriate CI passes. Story completion
does not require publication or deployment.

Root `[tool.wood.branching]` declares integration and development. Existing Wood
planning release and scope mappings remain local planning context. Verify the
repository, fetched base, PR target and Story association before activating a
claim. OpenProject remains the planning/evidence system, accessed by Wood/Codex
using existing local Infisical credentials. GitHub Actions needs no OpenProject
credential or hosted planning-readiness gate for branch standardization.

## Effective protections

Apply the same policy to main and development:

- Require pull requests and passing repository-appropriate validation.
- Prevent direct pushes, force pushes and branch deletion.
- Require resolved review conversations.
- Require zero independent approving reviewers for the approved single-maintainer model.
- Configure no bypass actors.

Inspect all effective rulesets and classic protections. Explicitly report a
security-relevant reduction of stronger existing controls before applying it;
material security downgrades require user approval. Do not bypass existing security
checks to obtain canonical readback. Reuse BR-03 migration and protection tooling:
review a fresh plan, apply its exact hash, and verify effective readback. An API
write alone does not establish protection or passing CI.

## Validation and release isolation

Development pushes and PR merges perform validation only: no semantic-release,
GitHub Release, package/GHCR publication or deployment. Inspect caller triggers,
job conditions, reusable workflow pins and downstream jobs; branch naming alone
does not prove isolation.

At release completion, review a development-to-main PR with successful accumulated
validation. Protected-main integration requires explicit user approval because it
triggers publication or deployment. Preserve conventional commit history needed
by the existing semantic-release engine, or use an explicitly reviewed squash
message representing the release impact.

The approved main integration invokes the repository's existing appropriate
centralized release machinery. Keep immutable workflow/helper pins and existing
artifact identity, deployment, runtime-health and rollback controls. CLI, library
and configuration repositories publish only applicable artifacts. Container
applications publish their required images. Infrastructure and Homelab retain
relevant deployment behavior under the same development/main integration model.
Do not add a publishing engine, release-authorization protocol, OAuth initiative
or hosted OpenProject authentication requirement to implement this methodology.

## Urgent hotfixes

Urgent fixes originate from main and PR into main with existing required validation
and explicit approval for any resulting publication/deployment. Preserve existing
incident/approval evidence references where required by Wood's hotfix interface.
Reconcile main into development through a validated PR before the next normal
release. The release candidate must include current main ancestry; equivalent
cherry-picks alone do not establish reconciliation. Wood's local
`repo release-readiness` ancestry result may support operator review; hosted
OpenProject release readiness is not a branch-standardization blocker.

## Fleet migration and active work

BR-05 authorizes deliberate standardization across the existing 31 active
repositories in bounded batches. Exclude the two archived repositories. Record
inaccessible wood-agents explicitly and request disposition only if it prevents
completion. Legacy branching, workflow or protection differences are not permanent
exceptions merely because they exist.

Assess branches, PRs, CI, effective protections, release/deployment behavior, active
claims and worktrees. Reconcile histories and active work before safely initializing
development where absent. Preserve existing production/runtime state, release
history and other owners' work. Never rewrite a live claim to bypass its scope;
retain a handoff and use supported session release/start when a stopped session
needs a new verified scope. Parallel work requires isolated worktrees and owners.

Record original/target strategy, baselines, migration status, effective protections,
exact CI revisions/runs, release isolation, preserved main publisher, hotfix
reconciliation contract, PRs and evidence in one consolidated matrix. Close Story
558 only after all accessible in-scope repositories meet acceptance; identify
approved exceptions explicitly. Pending evidence is not passed verification.

## Authorization and cleanup

The user's BR-05 authorization covers local implementation, routine commits/pushes,
development PR creation, passing development merges, CI fixes, reviewed protection
application without material security weakening, and evidence recording. Stop for
material downgrades, protected-main publication/deployment merges, destructive
operations or material deviations. Do not add routine approval gates.

Retain Story claims/worktrees through evidence posting and verified closure.
Retain development across releases. Remove only clean, verified merged working
branches/worktrees after checking dependency and recovery needs; preserve dirty
work and other owners' claims. Keep deterministic evidence separate from narrative.
