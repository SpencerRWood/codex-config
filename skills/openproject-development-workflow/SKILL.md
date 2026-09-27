---
name: openproject-development-workflow
description: "Execute an OpenProject Story through the shared development workflow: select the next Story, prepare a branch, implement and validate it, stop for review, then commit and open a GitHub pull request. Use for Story-driven work, not one-off or hot-fix changes."
---

# OpenProject development workflow

Apply this workflow from the repository that owns the Story. It assumes the repository's
`.env` provides the repository's OpenProject URL and initiative ID. The shared
credential is read from `~/.wood/runtime/openproject.env`.

1. Run `wood-next-story --json` to select the next dependency-ready Story. Read its
   goal, acceptance criteria, predecessors, and Planning Increment before editing.
   The command selects a ready Story from the earliest active R# Planning Increment,
   ordered numerically (R9 before R10). OpenProject Version is that increment, not
   a repository artifact version.
2. With explicit approval to start that Story, preview then apply its status update:
   `wood-set-story-status <id> --status "In progress" --json`, followed by the same
   command with `--apply`. When requesting execution approval, use the reusable command
   prefix `wood-set-story-status`, not a Story-ID-specific prefix.
3. If the current directory is an initialized, clean Git repository, create a local
   branch named `feature/op-<id>-<slug>`. This is a local branch; do not push it merely
   to make a GitHub branch visible.
4. Implement only the selected Story and its acceptance criteria. Preserve unrelated
   worktree changes.
5. Run the repository's declared checks. Use its documented commands and
   `.pre-commit-config.yaml`; typical configured checks include Ruff, mypy, SQLFluff,
   tests, and `pre-commit run --all-files`. Do not claim a check ran when its tool or
   dependencies are unavailable.
6. **STOP FOR REVIEW.** Present the diff summary, changed files, validation results,
   and remaining risks. Do not commit, push, open a PR, merge, or close the Story until
   the user explicitly approves that post-review batch.
7. After approval, commit the reviewed scope to the Story branch, push it, and open a
   GitHub pull request targeting `main`. Report the commit and PR URLs. After confirming
   the PR merged, switch to `main`, fast-forward it from `origin/main`, delete the
   merged local Story branch with `git branch -d <branch>`, and delete its remote branch
   with `git push origin --delete <branch>`. When the PR used squash or rebase merging,
   `git branch -d` may reject the equivalent local commit; force-delete only that exact
   local branch after verifying its merged PR or patch equivalence. Story closure is
   separate: after the PR is merged and the user approves closure, preview then run
   `wood-set-story-status <id> --status "Closed" --apply`. When requesting execution
   approval, use the reusable command prefix `wood-set-story-status`, not a
   Story-ID-specific prefix.

## Planning Increment loop authorization

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

- Leave `Released In` blank during planning and implementation. After the actual
  repository semantic-release version is known, record it on the shipped Story;
  a Planning Increment may contain multiple such versions and GitHub Releases.

- `wood-next-story` is read-only. `wood-set-story-status --apply` mutates OpenProject.
- Delete Story branches only after confirming their PR merged and after switching away
  from the local branch. Start with `git branch -d`. Use `git branch -D` only when a
  squash or rebase merge has been verified through the merged PR or patch equivalence.
- Stop if the next-Story lookup is ambiguous, no Story is available, the repository has
  uncommitted work outside the requested scope, or the OpenProject environment is not
  resolved.
- Do not create a branch, commit, push, PR, or close a Story as an implicit consequence
  of selecting it. Each occurs only at the approval point above.
