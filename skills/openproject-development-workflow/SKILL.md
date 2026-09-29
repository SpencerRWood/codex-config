---
name: openproject-development-workflow
description: "Execute an OpenProject Story through the shared development workflow: select the next Story, prepare a branch, implement and validate it, stop for review, then commit and open a GitHub pull request. Use for Story-driven work, not one-off or hot-fix changes."
---

# OpenProject development workflow

Apply this workflow from the repository that owns the Story. Set `OPENPROJECT_URL`
from repository configuration and use Infisical to inject `OPENPROJECT_API_TOKEN`.
Resolve the project and initiative IDs from repository context or
`wood project list --json`. Use the public `wood story` commands as described in
[Story operations](references/story-operations.md). Before use, verify the selected
`wood` executable exposes `story`. In a Wood Tools checkout under review, use
`uv run --active --frozen wood` so commands invoke the checked-out implementation.

1. Run `wood story next <initiative-ref> --json`, then `wood story get <id> --json`.
   Read the goal, acceptance criteria, dependencies, and target release before editing.
2. With explicit approval to start that Story, preview then apply
   `wood story start <id> --json`. Verify the returned In progress status and local
   `feature/op-<id>-<slug>` branch when the Story names a repository. Do not push it
   merely to make a GitHub branch visible.
3. Implement only the selected Story and its acceptance criteria. Preserve unrelated
   worktree changes.
4. Run the repository's declared checks. Use its documented commands and
   `.pre-commit-config.yaml`; typical configured checks include Ruff, mypy, SQLFluff,
   tests, and `pre-commit run --all-files`. Do not claim a check ran when its tool or
   dependencies are unavailable.
5. **STOP FOR REVIEW.** Present the diff summary, changed files, validation results,
   and remaining risks. Do not commit, push, open a PR, merge, or close the Story until
   the user explicitly approves that post-review batch.
6. After approval, commit the reviewed scope to the Story branch, push it, and open a
   GitHub pull request targeting `main`. Report the commit and PR URLs. After confirming
   the PR merged, switch to `main`, fast-forward it from `origin/main`, delete the
   merged local Story branch with `git branch -d <branch>`, and delete its remote branch
   with `git push origin --delete <branch>`. When the PR used squash or rebase merging,
   `git branch -d` may reject the equivalent local commit; force-delete only that exact
   local branch after verifying its merged PR or patch equivalence. The post-review
   approval also authorizes closure of that Story after the PR is confirmed merged and
   all applicable required checks have passed, including post-merge validation when
   configured. Post and verify the implementation update described below. Read the
   live OpenProject status, preview `wood story complete <id> --evidence <file>`, then
   apply it and verify the configured closed status. Do not close while a required
   check is pending, failed, or unavailable.

## Implementation update at closure

After the merge and required checks pass, post one concise OpenProject activity comment
to the Story before setting it to `Closed`. Include what shipped, the PR and merge commit,
validation evidence, the published release tag when applicable, and any remaining
limitations. Link to the authoritative GitHub run instead of pasting logs; exclude
secret values. Use a stable heading such as `Implementation update (WP-<id>)` and check
existing Story activities for that heading before posting, so retries do not duplicate
the comment. Use the first-party Story command when it supports comments; otherwise
OpenProject API v3 accepts `POST /api/v3/work_packages/<id>/activities` with
`{"comment":{"raw":"..."}}`. Verify the created activity by readback. If the comment
cannot be posted and verified, leave the Story open and report the failure.

## Planning Increment loop authorization

The selector uses active R# planning releases in numeric order and respects
predecessor readiness. Start the loop when an active backlog has eligible work.

When the user explicitly asks to continue a named Planning Increment loop, that authorization covers
selection, status changes, branching, implementation, and validation for each next
dependency-ready Story in that Planning Increment. Stop at the review gate for every Story. Approval
of a review authorizes delivery and closure of only that reviewed Story; after it is
complete, resume the loop with the next Story automatically. Do not treat loop
authorization as approval to commit, push, open or merge a PR, or close a Story before its
individual review approval.

An active Planning Increment loop must not end an agent turn after partial implementation, an initial
test pass, or a progress update. Continue until the Story reaches its review gate, a
genuine blocker requires user direction, or no dependency-ready Story remains. After a
review-approved Story is delivered, continue directly to the next Story rather than
returning a terminal response between loop iterations.

## Guards

- The selector uses active R# planning releases in numeric order.
- `wood story next` and `wood story get` are read-only. Story lifecycle commands
  preview by default; `--apply` mutates OpenProject and may prepare a local branch.
- Delete Story branches only after confirming their PR merged and after switching away
  from the local branch. Start with `git branch -d`. Use `git branch -D` only when a
  squash or rebase merge has been verified through the merged PR or patch equivalence.
- Stop if the next-Story lookup is ambiguous, no Story is available, the repository has
  uncommitted work outside the requested scope, or the OpenProject environment is not
  resolved.
- Do not create a branch, commit, push, PR, or close a Story as an implicit consequence
  of selecting it. Closure follows only the individual post-review approval and the
  verified merge and checks described above.
