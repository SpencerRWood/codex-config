# Branching and delivery policy

This is the canonical engineering policy for Codex and Pi. Repository AGENTS.md
files declare their strategy and justified exceptions, and reference this document
at `SpencerRWood/codex-config/docs/branching-policy.md`. Read it through the explicit
codex-config source path used by the installed global AGENTS.md; do not resolve
relative links against a Codex home. Preserve repository review, security, CI,
immutable artifact, rollback and approval requirements in addition to these gates.

## Repository strategy

Application repositories use **release-branch integration**:

```text
main
 └── release/vX.Y.Z
      ├── feat/op-123-description
      ├── feat/op-124-description
      └── fix/op-125-description
```

`main` is stable and releasable. An approved, bounded release scope has one
short-lived `release/vX.Y.Z` integration branch. Each Story is implemented and
validated on its own branch created from that release branch. Story PRs target
the release branch and merge only after review and required checks. Validate the
accumulated integration branch after merges. Keep `main` unchanged until the
release readiness gate passes. Never use a permanent `develop` branch.

Infrastructure, shared tooling/workflows, agent configuration, repository
templates and configuration-only repositories use **trunk-based development**:
create a short-lived Story/change branch from current `main`, validate it, then
review and merge its PR into `main`. Normal Story completion does not authorize
artifact publication or deployment. Release integration branches require an
explicit coordinated-change exception in these repositories.

Inspect purpose, repository metadata and existing conventions when classification
is unclear; a directory name or the presence of semantic-release is insufficient.
The [classification record](release-branch-audit.md) records the inspected fleet.
Templates themselves use trunk-based development. When instantiating a template,
replace its template-repository classification before application work starts.

## Discover before implementation

Follow **Discover → Branch → Implement → Validate → Review → PR → Merge → Update
OpenProject**. Discovery must finish before creating or mutating a Story worktree:

1. Identify the Git root, origin and applicable repository AGENTS.md strategy.
   Use `wood repo info --json` and `wood repo standards --json` for supported
   metadata, and the current root's `[tool.wood.openproject]` mapping.
2. Read the Story, predecessors and intended OpenProject release using
   `wood story get`, `wood release list/get` and, when needed, `wood epic get`,
   with `--json`. Prefer unfinished, dependency-ready Stories in the active scope
   over later releases. Verify selection returned by `wood story next`; its
   Planning Increment order alone does not select a Git integration branch.
3. Fetch origin and inspect remote branches. For applications, verify the exact
   `release/vX.Y.Z` branch against the approved release association, scope,
   lifecycle status and current remote revision. Multiple candidates, a closed
   or stale scope, or a missing association require resolution, never a guess.
4. OpenProject `R#` Planning Increments and repository SemVer remain distinct.
   Record the explicit mapping between project/version ID and intended repository
   version/branch in the approved release scope; do not derive SemVer from `R#`.
   If no branch exists, check whether a release is approved. Create its branch
   from verified current `main` only when existing conventions or an explicit
   release instruction authorizes creation. Otherwise report the missing gate.
   **Never silently fall back to `main` for an application Story.**
5. Confirm the base and PR target before implementation. For applications both
   are the verified release branch; for trunk repositories both are current
   `main`. Verify the selected Wood executable can honor that base, naming and
   evidence contract before applying `story start`. Unsupported tooling must
   fail closed; do not create a wrong-base claim and repair it behind Wood's back.
6. Use an isolated worktree or separate checkout for each concurrent execution,
   with a unique owner. Never concurrently mutate one working tree or implement
   directly on `main` or a shared integration branch. Application Stories use
   `feat/op-<id>-<slug>` for features and `fix/op-<id>-<slug>` for fixes once
   supported by the tool. Until then, report that naming/base capability gap
   rather than introducing aliases. Trunk repositories may retain their existing
   supported `feature/op-*` convention; it does not change their base or PR target.

Record strategy, selected base and target, fetched base revision, repository,
Story ID, OpenProject project/version ID and release name, planned SemVer,
approved scope reference, dependencies and branch creation authority in the
implementation evidence. For trunk work with no release association, record
`not applicable` and its reason. Preserve source/merge revisions, PR/check IDs,
review and approval evidence, validation records/logs and material limitations.
Supplement supported generated evidence through `wood story activity add --file`
when fields are absent; never fabricate a generated record or passed check.

## Story completion

Run applicable local checks, builds, integration/contract tests and declared
repository verification before PR creation. Review the implementation and retain
the existing commit/push/PR approval boundary. Confirm the explicit PR base and
revision-bound required CI before merge. Declare predecessor relationships and
integrate dependent Stories in order; revalidate affected integration contracts.

A Story completes after implementation, testing, review and integration into its
designated target succeed and required evidence and OpenProject status are
reconciled. Local builds (including unpublished images), local tests and CI
validation, approved PR operations and OpenProject updates are permitted.
Publishing images/packages, creating release tags or GitHub Releases, and
deploying to infrastructure dev or production are prohibited by default.

Story completion is independent of release publication and deployment. A delivery
report may include unavailable release/artifact/runtime fields; retain those
observations without treating them as failed Story integration or passed release
gates. Never follow a release/deployment next action as implicit authorization to
publish or deploy. Do not close a release when its Stories close. When the last
required Story completes, report a **candidate for release readiness validation**.

## Release readiness and approval

Open a release PR from `release/vX.Y.Z` into `main` after establishing:

- All required Stories are complete or explicitly deferred with approval.
- The integration branch contains the approved scope, with no unrelated work.
- Full repository validation and applicable integration/contract tests pass on
  the accumulated release revision; individual Story results are insufficient.
- Required documentation is current, OpenProject scope and implementation
  evidence are reconciled, and no blocking findings remain.
- The release PR has the required checks, review and explicit release approval.

Only then merge into `main`. Approval to integrate one Story does not authorize
this merge. Preserve commit history needed by semantic-release: the release PR's
merge strategy must retain the scope's conventional commit signals, or its reviewed
squash message must express the verified release impact. The planned branch
version is intent; semantic-release alone owns the actual version, tags and
GitHub Release. Reconcile a dry-run version mismatch before release approval.

## Publication and deployment gates

After the approved release merge, run the configured semantic-release process
from `main`, generate the actual version and immutable artifacts, publish required
images/packages, then deploy to infrastructure dev for release integration
verification. Verify deployed revision/digest, runtime health and rollback
readiness. Promote to production only with explicit authorization when applicable.
Trunk repositories still require separate publication/deployment authorization;
a normal merge is not that authorization.

Preserve a pipeline's necessary ordering for artifact identity and safe rollback,
and document its exact gate sequence. An explicitly approved early deployment
exception must record its reason, scope, target, artifacts, approval and recovery
requirements. Existing automatic publication/deployment is a technical gap until
separately gated; do not merge a change that would trigger it without the required
authorization or an approved narrowly scoped control change.

| Event | Validation | Release publication |
| --- | --- | --- |
| Feature PR → release branch | Required | Forbidden |
| Feature merge → release branch | Required | Forbidden |
| Release PR → main | Required | Forbidden |
| Approved release merge → main | Required | Eligible after release gate |
| Deployment promotion | Required | Separately controlled |

Agents must not invoke publishing workflows on feature branches, release branches
or PR events. Semantic-release publishes from `main` only unless a repository
has an explicitly approved exception. Branch names alone are not a safeguard:
inspect caller triggers, reusable job conditions, credentials and downstream jobs.
CI validation has no publishing authority. A semantic-release nonpublishing
verification/dry-run must use the installed tool's documented nonmutating mode
without publication credentials and must not invoke a publishing workflow.
Local image builds do not push images; tags/GitHub Releases, registry pushes and
image deployment are separate mutations requiring their own lifecycle gates.

## Cleanup

Retain Story worktrees and claims through evidence posting, verified closure and
recovery handoff. Release the claim only after execution stops. Delete completed
feature branches only after verifying their merge into the designated target,
clean state, no remaining dependency/recovery need and safe removal. Squash/rebase
merges need verified PR and content evidence before any force deletion.
Delete release branches only after the approved merge into `main`, retained
release/recovery evidence and confirmation they are no longer needed. Do not
delete a dirty worktree, a running execution's branch or another owner's claim.
