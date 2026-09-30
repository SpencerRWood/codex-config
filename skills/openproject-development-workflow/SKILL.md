---
name: openproject-development-workflow
description: "Execute an OpenProject Story through the shared development workflow: select, implement, validate, review, deliver, and close it. Use for Story-driven work, not one-off fixes."
---

# OpenProject development workflow

Work from the Story's repository. Use the supported `wood` CLI; in a Wood Tools
checkout under review, use `uv run --active --frozen wood`. Confirm the selected
executable exposes the needed commands. Inject OpenProject credentials with
`infisical run --env=dev --path=/openproject --`. Run Infisical-backed commands
with network permission from their first attempt. A repository may provide
`[tool.wood.openproject]` context; pass an Initiative reference only when needed.

1. Run `wood doctor --json` when readiness is uncertain. Select with
   `wood story next --json` (or an explicit Initiative), then read
   `wood story get <id> --json`. Read the goal, acceptance criteria, dependencies,
   repository, and Planning Increment. Stop on ambiguity, missing context, or
   ineligible work. Decompose a Story that is too broad before implementation.
2. Once starting that Story is authorized, preview and apply
   `wood story start <id> --json`. Verify In progress and the Story branch.
   Preserve unrelated changes; use an isolated clean worktree if another Story
   has unfinished work. Do not push merely to expose a branch.
3. Run `wood repo info --json` and `wood repo standards --json` once to read
   the repository contract. Implement the Story's accepted scope. The CLI owns
   project selection, dependency and status checks, and branch preparation.
4. Run `wood repo validate --json` after edits. Fix failures using its log paths.
   Use repository-specific checks only for an unsupported or unavailable check,
   or to diagnose a failure. Do not rerun passing checks without a relevant
   change or claim an unavailable check passed.
5. **Stop for review.** Present the diff, validation, and remaining risks.
   Do not commit, push, open a PR, merge, or close until the user approves
   that reviewed batch.
6. After approval, commit and push the reviewed Story branch and open a PR to
   `main`. Use `wood ci status --json` for current centralized validation;
   use `wood ci failures --json` to diagnose failures. Verify PR checks on the
   Story commit and confirm the PR merged. If deployment applies, inspect
   `wood deploy status --json`. Never treat stale, pending, failed, or
   unavailable checks as passed. After merge, fast-forward local `main` and
   remove the merged Story branches; force-delete a local branch only after
   verifying a squash or rebase merge.
7. Post one concise implementation update using
   `wood story activity add <id> --file <comment-file> --json` (preview, then
   `--apply`). Start it with `Implementation update (WP-<id>)`; include what
   shipped, PR and merge commit, validation and CI links, release tag when
   applicable, and limitations. Verify the returned activity ID. Read the live
   Story, then preview and apply
   `wood story complete <id> --evidence <evidence-file> --json` only after
   required checks pass. Verify Closed. Keep it open if evidence cannot be
   posted or verified. Closure does not create a release.

`wood story` lifecycle commands preview by default and mutate only with
`--apply`. The completion evidence must include passed repository checks and a
passed GitHub Actions run for a repository Story. Keep secret values out of
comments and evidence. Infisical supplies credentials; semantic-release owns
version changes, tags, and GitHub Releases.

## Planning Increment loop

When the user explicitly authorizes a named Planning Increment loop, that
authorization covers selection, start, implementation, and validation of each
dependency-ready Story. Stop at review for each Story. Approval of one review
authorizes delivery and closure of only that Story; after it closes, continue
to the next eligible Story. Do not end a loop turn after partial implementation
or an initial check when useful work remains.
