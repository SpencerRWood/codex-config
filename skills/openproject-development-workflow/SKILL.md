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
4. Run `wood repo validate --json` after edits. Retain its `data.validation_file`
   and log paths; the record binds passed checks to the validated file contents,
   including uncommitted implementation changes. Fix failures using its log paths.
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
7. After merge, preview `wood story evidence <id> --validation <validation-file>
   --pr <number> --ci-run <run-id> --json`, then use `--apply` to generate the
   delivery files. Retain `data.evidence_file` and `data.update_file`. The command
   requires a clean checkout containing the merge, a standard `feature/op-<id>-`
   PR branch, matching validated contents, all required logs, and passed validation
   CI on the source or merge revision. Use the explicit verified run ID from PR
   checks when `wood ci status` reports an unrelated latest run as stale.
8. Post the generated update using `wood story activity add <id>
   --evidence <evidence-file> --json` (preview, then `--apply`). Verify the returned
   activity ID. Read the live Story, then preview and apply
   `wood story complete <id> --evidence <evidence-file> --json`. Both consumers
   reverify the generated record and current PR/CI state. Verify Closed. Keep the
   Story open if evidence cannot be posted or verified. Closure does not create
   a release. Add a separate factual activity for material release or deployment
   details and limitations that the generated update does not capture.

Generated files and logs use the current repository's `[tool.wood.workflow]`
`output_directory` in `pyproject.toml`, defaulting to `/private/tmp`. Use returned
paths rather than inventing filenames or manually constructing routine evidence.
Files are temporary: retain them through delivery. If removed, regenerate them;
if the validation record or logs are missing, validate the exact implementation
contents again before generation. Never rerun passing validation solely because
the same contents were committed. Fetch a missing PR source revision if needed.
For unsupported repositories or evidence workflows, explain the limitation and
use the existing `--file` activity input and evidence format with verified facts.

`wood story` lifecycle commands preview by default and mutate only with
`--apply`. The completion evidence must include passed repository checks and a
passed GitHub Actions run for a repository Story. Keep secret values out of
comments and evidence. Infisical supplies credentials; semantic-release owns
version changes, tags, and GitHub Releases.

For live planning inspection, use `wood epic list --json`,
`wood epic get <id|exact-name> --json`, `wood release list --json`, and
`wood release get <id|exact-name> --json`. Project context comes from the
repository mapping; use `--project <id>` to override it. Lists accept `--status`
and `--offset`; Epic get pages child Stories with `--offset`. Epic get reports
current child statuses, completion readiness, and whether the Epic is already
complete. Rejected Stories do not block readiness. Release means an OpenProject
planning version, not a GitHub release. Use these reads when parent verification
or release selection is needed, rather than reproducing API queries in Python.

Before falling back to a custom script, check `wood contract --json` or command
help for the supported operation. Explain the missing capability or focused
diagnostic need. Edit repository code and tests directly with patch/edit tools;
do not write temporary Python scripts merely to generate or modify those files.
Existing checked-in scripts and skills remain appropriate for their supported
workflows.

## Planning Increment loop

When the user explicitly authorizes a named Planning Increment loop, that
authorization covers selection, start, implementation, and validation of each
dependency-ready Story. Stop at review for each Story. Approval of one review
authorizes delivery and closure of only that Story; after it closes, continue
to the next eligible Story. Do not end a loop turn after partial implementation
or an initial check when useful work remains.
