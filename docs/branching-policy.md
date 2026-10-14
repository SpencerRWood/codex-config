# Branching and delivery policy

This is the single canonical engineering policy for Codex and Pi. Repository metadata
declares an adopted strategy and justified exceptions; instruction files reference this document
at `SpencerRWood/codex-config/docs/branching-policy.md`. Read it through the explicit
codex-config source path used by the installed global AGENTS.md; do not resolve
relative links against a Codex home. Preserve repository review, security, CI,
immutable artifact, rollback and approval requirements in addition to these gates.

## Repository strategy

All active repositories progressively adopt the same **configuration-driven integration**:

```text
working branch → development → protected main → automatic pinned release workflow
```

This target applies to applications, CLI tools, libraries, infrastructure,
templates, shared workflows and agent configuration. Repository purpose determines
publication outputs, not branching strategy. Do not infer strategy from type/name.

`main` is stable and releasable. Adopted Stories start from the fetched,
explicitly configured integration branch, normally `development`, and target that
same branch. Validate each Story and the accumulated integration branch. Keep main
unchanged until the separately approved release integration gate passes. Branch
names do not select a strategy: root `pyproject.toml` does.

| Declared strategy | Story base and PR target | Scope |
| --- | --- | --- |
| `integration` | Configured `integration_branch`, normally `development` | Open planning release and approved scope |
| `release` | Configured `release_branch`, `release/vX.Y.Z` | Existing approved bounded release scope |
| `trunk` or absent section | `main` | Existing trunk behavior; absence is not application adoption |

Existing approved release mappings remain supported. Do not rename or migrate
their branches/claims while executing unrelated work. A later change from release
to integration requires an explicit adoption scope and safe release boundary.

Existing declared trunk, undeclared trunk defaults, and bounded release strategies
remain compatible until deliberately migrated. They are transitional behavior,
not permanent exceptions based on repository purpose. The historical
[classification record](release-branch-audit.md) is evidence of the inspected fleet,
not the current architectural decision or permission to migrate it.

## Progressive adoption and rollout scope

BR-01 code/policy changes are limited to wood-tools, codex-config and pi-config.
No repository's adopted strategy, live branch arrangement, publishing workflow
or GitHub enforcement is migrated by BR-01.
Do not edit application, infrastructure or template AGENTS.md files as a fleet migration.
Repository-specific references or configuration changes require a specific adoption task.
Nonadopters continue their existing conventions without blocking unrelated development.
An existing in-progress Story may finish its existing branch arrangement when safe
and explicitly approved; record that approval and retain its worktree and implementation.

Repositories adopt integration only after the approved release
scope, explicit OpenProject-to-Git mapping, compatible Wood executable and validation
callers are available. Record adoption in `[tool.wood.branching]` with
`strategy = "integration"`, `release_id`, `integration_branch` and `scope_reference`.
Existing `strategy = "release"` uses `release_branch` instead. For example:

```toml
[tool.wood.branching]
strategy = "integration"
release_id = 123 # actual approved OpenProject planning version ID
integration_branch = "development"
scope_reference = "<actual scope approval reference>"
```
The release ID is the OpenProject planning version ID; the scope reference identifies
the actual approval, not an approval inferred from a branch name. Wood verifies an
open matching release and an existing remote branch; it never creates an integration branch.
An absent branching section preserves existing trunk behavior; it does not certify a
repository's purpose or authorize migration. Use `strategy = "trunk"` where explicit
metadata is useful. Both adopted nontrunk strategies fail closed on missing gates.

An approved planning-scope rollover may retain the long-lived development branch.
Finish or explicitly resolve old-scope Stories, retain their evidence, and release
claims only after execution stops. Do not close a planning release while its active
Stories still require it. Approve the next open version and scope, then review the
root mapping update as a separate change. A closed planning version or changed
mapping blocks start/resume without deleting claims or unfinished work. Resolve
the planning conflict before resuming with the recorded owner/worktree; never
rewrite a live claim to bypass it. Rollover grants no publication/deployment authority.

Wood Design System is the approved development pilot; reference existing Stories
547 and 551 without duplicating their scope or claims. Recovery Verification retains
its approved release mapping until a separately authorized transition boundary.
Preserve existing implementations, claims and worktrees. A fixture
validation of this scenario does not approve a SemVer, create a live branch, migrate
OP-499 or authorize a release. Deferred caller trigger and publication controls must
be resolved at that adoption boundary. See the [rollout index](release-branch-changes.md).

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
3. Fetch origin and inspect remote branches. For adopted repositories, verify the exact
   configured integration or release branch against the approved release association, scope,
   lifecycle status and current remote revision. Multiple candidates, a closed
   or stale scope, or a missing association require resolution, never a guess.
4. OpenProject `R#` Planning Increments and repository SemVer remain distinct.
   Record the explicit mapping between project/version ID and intended repository
   version/branch in the approved release scope; do not derive SemVer from `R#`.
   If no branch exists, check whether a release is approved. Create its branch
   from verified current `main` only when existing conventions or an explicit
   release instruction authorizes creation. Otherwise report the missing gate.
   **Never silently fall back to `main` for an adopted integration/release Story.**
5. Confirm the base and PR target before implementation. For adopted repositories both
   are the configured integration/release branch; for trunk repositories both are current
   `main`. Read `wood contract --json` once: require branching contract version 1
   with all three strategies and feature/feat/fix prefixes, then read
   `wood repo branching --json`. Confirm supported `story start --base-branch`
   and `--target-branch` selectors. Inspect the preview's strategy, base/target,
   scope, resolved revision, branch, owner and worktree before applying start.
   Discovery's observed local revision is not live remote verification. Unsupported tooling must
   fail closed; do not create a wrong-base claim and repair it behind Wood's back.
6. Use an isolated worktree or separate checkout for each concurrent execution,
   with a unique owner. Never concurrently mutate one working tree or implement
   directly on `main` or a shared integration branch. Adopted Stories use
   `feature/op-<id>-<slug>` by default for integration and `feat/op-*` for release;
   `feature`, `feat` and `fix` are supported prefixes using `--branch-prefix`.
   Trunk repositories may retain their existing
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

Run `wood repo release-readiness --json` for adopted integration repositories
before preparing the development → main release PR and again after relevant
remote changes. It fetches exact main/integration refs, requires complete history,
and blocks with exit 3 if main is not an ancestor of integration. Retain its
revision-bound `readiness_file`. This conservatively requires all main-only
commits, including emergency fixes and release metadata, to be back-integrated.
Equivalent cherry-picks alone do not satisfy this ancestry gate. Missing branch,
incomplete history or unavailable evidence fails closed. This is a local gate;
required GitHub CI wiring belongs to BR-02/BR-03, not an enforcement claim here.

Open a release PR from the configured integration branch (`development` or the
existing approved `release/vX.Y.Z`) into `main` after establishing:

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

After explicit approval and successful validation of the protected development →
main release integration, main triggers the repository's pinned release workflow
automatically. That reviewed integration is distinct from ordinary Story approval.
Outputs are repository-specific: packages, images, configuration releases or other
declared artifacts. Semantic-release owns version calculation where configured;
planning R# identifiers are never SemVer. Publication outputs and workflow changes
are outside BR-01. Deployment/promotion remains subject to its own approved
repository lifecycle, immutable artifact, runtime-health and rollback gates.
Existing automatic publishers do not make a legacy Story merge authorized to
publish; inspect and resolve those side effects before delivery.

## Authorized emergency hotfix

Normal work always uses the declared integration path. For an urgent production
incident in an adopted integration repository, explicitly select the existing
Story and supply both `--hotfix-incident <incident-or-emergency-justification>` and
`--hotfix-approval <authorization-evidence-reference>` to `wood story start`.
Wood verifies repository identity, open matching planning scope and supported
prefix, fetches main, and creates only the isolated working branch from main.
The returned plan records mode `hotfix`, original integration branch, incident,
approval reference and base revision. Existing feature/feat/fix prefixes remain
supported; emergency start defaults to fix. Never enable hotfix by repository
name/type, leave it as a default, or change the persistent branching strategy.

These references record the operator's explicit authorization; they do not
independently prove human approval or replace protected-main controls. Review the
actual incident/approval evidence, require the applicable CI and protected-main
approval, and integrate only through a PR. No command permits direct main pushes,
merges, bypass grants, publication or deployment. Pi requires an explicit Story
and the same references, validates the preview before apply, and retains the
claim if any check fails. Resume with the same owner, worktree and references.

Use the same incident/approval selectors for `wood story evidence` and
`wood delivery status`. Generated evidence verifies the actual merged main PR
and revision-bound validation CI and records the references. Story completion
still does not confer release or deployment authority.

After the hotfix integrates, reconcile main back into development through a
reviewed, validated PR. Record its PR, revision and incident association. Run
`wood repo release-readiness --json` and retain the exact main/integration SHAs
and result as reconciliation evidence before any subsequent release integration.
An unresolved main-only hotfix blocks preparation. Do not rewrite claims or
history, accept a stale record, or mark reconciliation passed from a branch name.

Preserve a pipeline's necessary ordering for artifact identity and safe rollback,
and document its exact gate sequence. An explicitly approved early deployment
exception must record its reason, scope, target, artifacts, approval and recovery
requirements. Existing automatic publication/deployment is a technical gap until
separately gated; do not merge a change that would trigger it without the required
authorization or an approved narrowly scoped control change.

| Event | Validation | Release publication |
| --- | --- | --- |
| Feature PR → configured integration/release branch | Required | Forbidden |
| Feature merge → configured integration/release branch | Required | Forbidden |
| Release PR → main | Required | Forbidden |
| Approved release merge → main | Required | Eligible after release gate |
| Deployment promotion | Required | Separately controlled |

Agents must not invoke publishing workflows on feature branches, development/integration or release branches
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
Retain a long-lived development branch across releases. Delete bounded release branches only after the approved merge into `main`, retained
release/recovery evidence and confirmation they are no longer needed. Do not
delete a dirty worktree, a running execution's branch or another owner's claim.
