# Release-branch foundation — 2026-10-11

The rollout is limited to **codex-config, pi-config, wood-tools and workflows**.
The [canonical policy](branching-policy.md) is the single source of truth; repository
classification does not activate adoption. The [index](release-branch-changes.md)
records all original 29 PRs and their dispositions. The original fleet audit and
validation evidence are preserved; its prior tooling gaps are historical findings.

## Foundation retained

- codex-config PR #22: canonical policy, mandatory global references, shared Story
  skill and OpenProject guidance, progressive adoption and the retained audit/index.
- Pi: two instruction files reference the same policy through its installed source
  path; permission denials and review-before-commit remain intact. Its initial
  semantic-release configuration proposal is deferred and preserved as a patch.
- Wood Tools PR #61: `repo branching`, explicit `story start --base-branch` and
  `--target-branch`, three Story prefixes, approved OpenProject release mapping,
  exact remote release fetch, scope/status checks, revision-bound worktree claims,
  active-release Story selection and integration-target evidence. No release creation
  command exists. An absent branching section preserves trunk behavior. Active
  claims cannot silently migrate strategy or release scope.
- workflows PR #36: main/event guards on all three reusable publishers, main-only
  temporary semantic-release configuration and non-main head rejection. Legacy
  container preparation rejects nonpublishing contexts before Git/GitHub access.
  Candidate digest identity and required runtime validation order remain intact.

Story completion requires implementation, validation, review, integration, recorded
evidence and reconciled OpenProject status. Image publication and deployment are
independent. Release-target delivery reports identify `story_complete` without
querying publication/deployment providers. A ready Story never approves a release
PR into main. All foundational PRs remain unmerged; no release/tag/image/deployment
or destructive cleanup is authorized by this change.

## Controlled Recovery Verification R1 scenario

Read-only Wood inspection confirms OP-499 is In progress in project 3, Initiative
486 and open R1 planning version ID 20. Its existing `feature/op-499-*` worktree
and claim are preserved. No `release/v*` branch was found in the inspected origin.
R1 does not imply any repository SemVer. The fixture branch `release/v1.2.3` is
illustrative and is not an approved live Recovery Verification version.

Isolated Git/remote and OpenProject fixtures verify a release base containing an
earlier Story, all three Story prefixes, the explicit release PR target, unchanged
main, resumable ownership and recorded fetched revision. Missing scope, mismatched
planning release, wrong target, missing/stale remote branch and active-claim migration
fail closed. Evidence accepts a release-target merge and successful revision CI
without release/publication/deployment evidence; it rejects the same PR targeting
main. Active-release selection does not select unfinished later-release work.

OP-499 is not migrated or completed by this task. Next: review the foundation;
separately authorize its release/tool installation and caller activation, define
the actual R1 scope-to-SemVer mapping, then choose an explicitly approved safe
continuation arrangement for OP-499. Preserve its implementation throughout.

## CI compatibility and deferred consumer changes

The reusable validation workflow is branch agnostic and already supports release
PR/push events. Consumers must opt into release target/push triggers and configure
required release-branch checks/protections in a dedicated adoption task. The local
caller inventory contains 45 shared-workflow callers across 28 repositories; it
is a checkout observation, not a claim that every remote caller was inspected.
Pinned `@v1` and `@v3` consumers need a separately approved shared workflow
release/reference update; editing shared source alone does not update pinned refs.
No consumer configuration is changed in this reduced rollout.

Main-only eligibility does not supply release-readiness approval. Existing
automatic main-push release/deployment callers, including infrastructure/homelab,
still need separate authorization before a merge that triggers those effects.
Resolve caller approval controls at adoption rather than editing the fleet now.
The v3 ordering remains validation → version preparation → one candidate image →
exact digest/runtime validation → publication of that digest → VCS release.

Actionlint reports the same pre-existing `job.workflow_sha` expression diagnostic
in the three publishing workflows on both origin/main and the proposal. This
baseline gap is retained for focused follow-up; no new actionlint diagnostic was
introduced. Workflow contract tests pass; this is not a live GitHub runtime attestation.

## Validation and evidence

Pi passes all four checks: pre-commit, lint, typecheck and tests; record:
`/private/tmp/wood-repo-validate-bkvikfng/validation.json`.
Wood passes all six declared checks, 482 tests and 91.75% coverage (85% required);
final record: `/private/tmp/wood-repo-validate-1hzz1l9f/validation.json`, including
the current-root metadata selection regression. A focused 38-test branch/claim
check also passed before the final full validation.
Shared workflows pass 110 tests with the existing pinned python-semantic-release
10.6.2 dependency; log: `check-rs735ey8.log` in the retained evidence directory.
Codex passes 14 maintained documentation/helper tests against the reviewed Wood
executable; log: `check-u9j81edz.log`. The updated Story skill passes its validator.

Full logs and bounded records are retained in
`/private/tmp/release-branch-reduction-20261011/`; original rollout evidence remains
in `/private/tmp/release-branch-20261011/`. Withdrawn branches, worktrees, original
diffs, PR metadata and close-result verification remain available. Pi commit/push/PR
requires its pending review approval. Publishing workflows were never invoked.
