---
name: openproject-development-workflow
description: "Execute an OpenProject Story through the shared development workflow: select, implement, validate, review, deliver, and close it. Use for Story-driven work, not one-off fixes."
---

# OpenProject development workflow

## Autonomous implementation and approval boundary

A request to implement a Story authorizes work within its defined scope through
Story/workflow inspection and dependency verification, repository and existing
implementation inspection, implementation, tests and required validation, fixing
validation failures, preparing OpenProject implementation evidence, and preparing
the proposed commit/PR summary. Proceed autonomously through these stages; do not
request intermediate approvals or permission to make in-scope implementation
changes. Preview/apply commands still require inspection of their previews, but
that inspection does not itself require another user approval for authorized work.

The first normal approval boundary is immediately before commit, push, or PR
creation. Present a concise review of changes made, repositories affected,
validation/test results (including unavailable checks), material implementation
decisions, and proposed commit(s) and PR(s). Then stop for explicit approval before
performing any of those actions. Approval covers the reviewed batch and its
existing standard delivery/closure workflow; continue that workflow without
repeating approval requests for already authorized actions.

This policy does not authorize scope expansion, destructive operations unrelated
to the Story, secret disclosure, bypassing safety controls, or actions for which
an underlying tool/runtime explicitly requires separate approval. Missing required
context or a material scope conflict still needs resolution; do not treat ordinary
implementation choices as approval gates or bypass execution permissions.

## Standard workflow

Work from the Story's repository. Run plain `wood` commands; in a Wood Tools
checkout under review, use `uv run --active --frozen wood`. Confirm the selected
executable exposes the needed commands with `wood contract --json` once, and
reuse that capability result. Wood Tools is the first control surface for supported
OpenProject, repository, CI, delivery, verification, and hierarchy operations.
Consume bounded JSON and retain returned IDs, revisions, hashes, and file paths;
do not reconstruct those facts with additional system queries. Run commands that
access external services with network permission from their first attempt. A
repository may provide `[tool.wood.openproject]` context; pass an Initiative
reference only when needed.
Never copy secret values into a checkout.

An installed executable can lag behind the Wood Tools checkout. If its contract
lacks a required capability, distinguish installation drift from a source capability
gap before selecting a fallback. Reuse the verified executable for the workflow;
do not guess flags or assume a command name proves that newer result fields exist.

1. Run `wood doctor --json` when readiness is uncertain. Select with
   `wood story next --json` (or an explicit Initiative), then read
   `wood story get <id> --json`. Read the goal, acceptance criteria, dependencies,
   repository, and Planning Increment. Stop on ambiguity, missing context, or
   ineligible work. Decompose a Story that is too broad before implementation.
2. The implementation request authorizes starting the eligible Story; preview and apply
   `wood story start <id> --json`. Verify In progress and the Story branch.
   Preserve unrelated changes; use an isolated clean worktree if another Story
   has unfinished work. Do not push merely to expose a branch.
3. Run `wood repo info --json` and `wood repo standards --json` once to read
   the repository contract. If authorized work needs hierarchy provisioning,
   use `wood hierarchy plan --project <project> --initiative <initiative>
   --release <release> --epic <epic> --json`. Review its operations, proposed
   mapping, and `plan_hash`; apply the same selectors with `wood hierarchy ensure
   --apply --plan-hash <reviewed-hash> --json`. Omitted selectors use repository
   mapping IDs. Retain the verified mapping; numeric misses, duplicate names,
   conflicting relationships, and stale plans require fresh inspection. See the
   [representative workflow](../../docs/wood-delivery-workflow.md) for scope and retries.
   Inspect the repository and existing implementation, then implement the Story's
   accepted scope without intermediate approval prompts. The CLI owns
   project selection, dependency and status checks, and branch preparation.
4. Run `wood repo validate --json` after edits. Retain its `data.validation_file`
   and log paths; the record binds passed checks to the validated file contents,
   including uncommitted implementation changes. Fix failures using its log paths.
   Use repository-specific checks only for an unsupported or unavailable check,
   or to diagnose a failure. Do not rerun passing checks without a relevant
   change or claim an unavailable check passed.
5. Prepare the OpenProject implementation evidence inputs using the saved
   validation record/logs, changes, and material decisions; prepare proposed
   commit(s) and PR title(s)/description(s). Final Wood-generated delivery evidence
   still requires verified merge/CI facts and is generated in step 7; do not
   fabricate those facts or post a completion claim during preparation.
   **Stop for review immediately before commit/push/PR creation.** Present the
   concise review defined above, including remaining material risks. Do not commit,
   push, open a PR, merge, or close until the user approves that reviewed batch.
6. After approval, commit and push the reviewed Story branch and open a PR to
   `main`. Wood Tools does not create or merge PRs; use `gh` for those operations.
   Use `wood ci status --json` for current centralized validation;
   use `wood ci failures --json` to diagnose failures. Verify PR checks on the
   Story commit and confirm the PR merged. If deployment applies, inspect
   `wood deploy status --json`. Never treat stale, pending, failed, or
   unavailable checks as passed. After merge, fast-forward local `main` and
   remove the merged Story branches; force-delete a local branch only after
   verifying a squash or rebase merge.
7. After merge, run `wood delivery status <id> --json` once from the Story checkout.
   Reuse its `fields`, `delivery_stage`, `blocker`, and `next_action` for the delivery
   briefing. A successful envelope means reconciliation completed, not that all
   stages passed. `not_applicable` is distinct from `unavailable`, `failed`, or
   pending delivery. Resolve applicable blockers before claiming delivery; refresh
   only after a relevant state change. Retain `observed_at`, the verified
   `fields.merged_revision`, and `fields.release_run` with its run ID, attempt,
   revision, conclusion, and authority link. `release_jobs` carries bounded
   unsuccessful/pending job diagnostics; `release_jobs_truncated` and each job's
   `steps_truncated` disclose omitted entries. Follow a returned diagnostic command
   using its exact run/attempt/job IDs and save full output with `brief-check`;
   do not recreate discovery or dump logs into context. A pending attempt calls
   for waiting on that run, then one refresh after completion. There is no delivery
   watch command. Successful release/promotion jobs do not establish the separate
   image digest, deployed revision, or runtime verification fields. Those fields
   remain unavailable until their own authority supplies verified evidence.
   If the repository declares `[tool.wood.verify]`, run `wood repo verify --json`
   against the implementation being delivered, with the required environment.
   Retain `data.verification_file`, source fingerprint, check states, and log paths.
   Required checks must pass; optional failures remain disclosed. Missing or
   malformed contracts fail clearly: do not invent verification, or report a
   verification requirement satisfied because no contract exists. Repositories
   with no applicable application verification can omit this step with the reason.
   Verification is separate from development validation; repository authors own
   retry-safe checks. Do not rerun a passing saved result unless source, contract,
   environment, or the observation's relevance has changed.
   Preview `wood story evidence <id> --validation <validation-file>
   --pr <number> --ci-run <run-id> --json`, then use `--apply` to generate the
   delivery files. When verification applies, pass `--verification <verification-file>`
   on both calls. Retain `data.evidence_file`, `data.update_file`, and the returned
   deterministic `delivery` snapshot; keep that evidence separate from narrative.
   The command
   requires a clean checkout containing the merge, a standard `feature/op-<id>-`
   PR branch, matching validated contents, all required logs, and passed validation
   CI on the source or merge revision. Use the explicit verified run ID from PR
   checks when `wood ci status` reports an unrelated latest run as stale.
8. Post the generated update using `wood story activity add <id>
   --evidence <evidence-file> --json` (preview, then `--apply`). Verify the returned
   activity ID. To inspect or repair an existing summary, use `wood story activity
   list <id> --json` and its `summary_activity_id`, `summary_count`, and activity
   `sha256`; page with `--offset` if needed. Multiple summaries require resolution.
   For an authorized summary update, preview `wood story activity summary <id>
   --evidence <evidence-file> --expected-sha256 <observed-hash> --json`, then apply.
   Creation uses `--expected-sha256 absent`; ordinary progress uses activity add
   with `--file` and a distinct heading. Do not overwrite unseen or changed content.
   Read the live Story, then preview and apply
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
The [representative workflow](../../docs/wood-delivery-workflow.md) specifies that
fallback format. Disclose its weaker source binding, retain the actual check logs,
and independently verify CI against the delivered revision before completion.

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

Before falling back to direct GitHub/OpenProject/infrastructure access or a custom
script, use the retained contract result or command help to establish the missing
capability, unsupported repository workflow, or focused diagnostic gap. Explain
that limitation once. Do not bypass ambiguity, stale plans, failed verification,
or credential errors by switching to a direct API. Do not add compatibility
wrappers or duplicate helpers for capabilities now owned by Wood Tools.
Edit repository code and tests directly with patch/edit tools;
do not write temporary Python scripts merely to generate or modify those files.
Existing checked-in scripts and skills remain appropriate for their supported
workflows.

At a repository or delivery boundary, brief from the latest verified Wood Tools
snapshot and saved records. Include observation time, Story/repository/branch,
source and merge revisions, PR/CI IDs, exact release-run ID/attempt, relevant job
IDs and truncation flags, validation and verification file/log paths, blockers,
and `next_action`. Use `none` or the reported unavailability reason for
missing facts; a handoff does not upgrade pending observations to passed evidence.

## Planning Increment loop

When the user explicitly authorizes a named Planning Increment loop, that
authorization covers the autonomous stages above for each dependency-ready Story,
including selection and start. Stop at the commit/push/PR approval boundary for
each Story. Approval of one review
authorizes delivery and closure of only that Story; after it closes, continue
to the next eligible Story using `wood story next --json`. Reuse the previous
closeout result until selection or the next mutation changes it; do not audit the
same delivery chain again. A successor in another repository uses that checkout
and its own contract/records. Approval of one Story never approves the next review.
Do not end a loop turn after partial implementation
or an initial check when useful work remains.
