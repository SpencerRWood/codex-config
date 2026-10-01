# Wood Tools delivery workflow

Run from the Story's Primary Repository using an executable exposing the
v0.17.0 command contract. Use `wood contract --json` once per selected executable;
retain it when switching checkouts with that same executable. Inject credentials
through Infisical; `--project-config-dir <directory>` points at an existing
authorized context when the current repository has none. In a Wood Tools checkout,
use `uv run --active --frozen wood`. This document uses `wood` for either selection.

The [Story skill](../skills/openproject-development-workflow/SKILL.md) owns review
and delivery policy. The executable examples below are templates: replace bracketed
values with verified IDs and paths; never run placeholders literally. Lines beginning
with `#` describe authorization or applicability boundaries.

## Representative Story

```text
wood contract --json
wood story next <initiative> --json
wood story get <id> --json
wood story start <id> --json
wood story start <id> --apply --json
wood repo info --json
wood repo standards --json
# implement the packet's accepted scope
wood repo validate --json
# stop for review; approval permits commit/push and PR creation/merge through gh
wood ci status --json
# after CI passes on the Story revision and the PR merge is verified
wood delivery status <id> --pr <number> --json
# only when repository-owned verification applies and its contract is declared
wood repo verify --json
# reuse validation_file and applicable verification_file, without rerunning checks
wood story evidence <id> --validation <validation-file> --verification <verification-file> --pr <number> --ci-run <run-id> --json
wood story evidence <id> --validation <validation-file> --verification <verification-file> --pr <number> --ci-run <run-id> --apply --json
# when no application verification applies, omit --verification in both calls
wood story activity add <id> --evidence <evidence-file> --json
wood story activity add <id> --evidence <evidence-file> --apply --json
wood story complete <id> --evidence <evidence-file> --json
wood story complete <id> --evidence <evidence-file> --apply --json
```

Read the selected packet once for repository, acceptance criteria, Planning
Increment, and dependencies. `story start` verifies eligibility and prepares the
branch; do not separately recreate its dependency/branch logic. Keep the returned
validation record and log paths through delivery. CI must be completed and passed
on the source or merged revision; stale latest-run results cannot substitute for it.

`delivery status` returns one observation with `story_id`, normalized `fields`,
`observed_at`, `delivery_stage`, `blocker`, and `next_action`. For example, an available PR/CI with
an unavailable release can produce stage `release` and a next action to inspect
the release. A success envelope means the query succeeded, not that delivery is
complete. Follow the returned action; refresh after a relevant mutation or authority
state change, not in a long-lived watch loop. `--pr` disambiguates verified PR
linkage and `--environment` selects deployment context when necessary. When a stage
is not applicable, retain its reason rather than inventing release/deployment data.

Enhanced reports include `fields.merged_revision` and `fields.release_run`, whose
value identifies the revision-bound run ID, current attempt, status, and conclusion.
The query reads at most 100 jobs from that exact attempt once. `release_jobs`
returns up to five unsuccessful/pending jobs with authority links and at most three
failed step names each; names are capped at 160 characters. Preserve
`release_jobs_truncated` and each job's `steps_truncated`. Follow the supplied
publication/promotion/deployment diagnostic or wait action. For an exact
`gh run view` diagnostic, use `brief-check` to save its full output using the
returned run/attempt/job IDs. Do not repeat discovery or infer omitted entries.
PR and validation blockers take precedence over release diagnostics.

Actions success proves workflow execution only. It does not populate missing
image digest, infrastructure deployment, or runtime health evidence. A published
container with successful promotion can still lack a generic GitHub deployment
record; retain the unavailable fields and disclose that authority gap. The run
field is supplemental: absence of a discoverable run does not invalidate separately
verified delivery facts. `observed_at` timestamps this query, not a prior runtime
attestation. An older installed binary can expose the command without these fields;
check the selected result and distinguish installation drift from missing source
functionality before switching to direct tools.

`repo verify` executes declared retry-safe argument arrays from `[tool.wood.verify]`.
The repository owns application semantics; Wood Tools owns bounded results,
timeouts, source binding, and private full logs. Retain `data.verification_file` and
pass it to both evidence calls. Required failures block verified completion; optional
failures remain visible. A missing contract is an error, not a passed verification.
If application verification is required but its contract is missing, resolve that
gap before claiming delivery. Do not manufacture application checks for a repository
where they do not apply.

Evidence generation returns `data.evidence_file`, `data.update_file`, and the
deterministic `delivery` snapshot. Consumers reverify saved records and current
PR/CI state without rerunning application commands. Keep deterministic evidence
separate from explanatory narrative. A handoff can reuse this snapshot or the most
recent `delivery status` observation, with time, revisions, file/log paths, applicable
verification, blockers, and next action. No extra OpenProject/GitHub/infrastructure
queries are needed merely to restate those returned facts.

These outputs have different shapes: `delivery status` supplies `fields`,
`observed_at`, `release_jobs`, `delivery_stage`, `blocker`, and `next_action`;
evidence's `delivery` is a map of
field states, values, and sources without stage/action metadata. Preserve the
returned shape and mark absent metadata unavailable. Record the local observation
time when no timestamp is returned.

If validation/evidence is unsupported for the repository (as in this repository's
current contract), explain the limitation and use its existing normal checks with
full retained logs. After delivery approval and verified PR/CI, use the supported
activity `--file` input and the documented completion evidence format from the
Story skill, containing verified checks and revision-bound CI. Never fabricate a
Wood-generated record. Direct tools remain appropriate for unsupported PR management
or a focused diagnostic gap; failed checks, stale plans, and ambiguity are not gaps
to bypass. Keep the Story open if evidence cannot be verified or posted.

The unsupported-workflow completion file uses `repository_checks` entries with
`name` and `status: "passed"`, plus `ci` with a verified GitHub Actions run `url`
and `status: "passed"`. Retain the actual check logs, PR number, repository, and
source/merge revisions alongside it. Completion rechecks a successful CI run in
the Story's repository; the agent must independently establish its revision linkage
for this fallback. This is weaker than content-bound generated evidence and must
be disclosed. A Story without a Primary Repository uses `validation_summary`.

## Existing implementation summaries

```text
wood story activity list <id> --json
wood story activity summary <id> --evidence <evidence-file> --expected-sha256 <observed-hash> --json
wood story activity summary <id> --evidence <evidence-file> --expected-sha256 <observed-hash> --apply --json
```

Inspection distinguishes summary/progress/system activities and returns
`summary_activity_id`, `summary_count`, and per-activity `sha256`. Page with
`--offset` to find an off-page summary. An authorized edit uses the observed hash;
creation uses `absent`. Identical content is reused. Multiple summaries or changed
content require fresh inspection rather than an overwrite. Ordinary progress and
release follow-ups use `activity add --file` with distinct headings. OpenProject
cannot enforce an atomic content precondition across external concurrent editors;
avoid simultaneous summary writers.

## Authorized hierarchy setup

```text
wood hierarchy plan --project <project> --initiative <initiative> --release <release> --epic <epic> --json
wood hierarchy ensure --project <project> --initiative <initiative> --release <release> --epic <epic> --json
wood hierarchy ensure --project <project> --initiative <initiative> --release <release> --epic <epic> --apply --plan-hash <reviewed-hash> --json
```

Use this only for authorized repository setup. Retain exact operations, mapping,
`plan_hash`, and verified apply IDs. The Project must exist. Names propose missing
objects; numeric IDs must already exist. Ambiguous names, closed objects, and an
Epic with another Initiative/Release fail explicitly. Omitted selectors use saved
repository IDs. Apply verifies objects/relationships and preserves a standard
`[tool.wood.openproject]` mapping with `project_id`, `initiative_id`, `release_id`,
and `epic_id` in the repository's `pyproject.toml`.

After partial failure inspect a fresh plan; use returned `applied` IDs and verification
states instead of creating replacements blindly. Same-checkout writers are serialized;
external simultaneous creators can race because OpenProject lacks atomic name
uniqueness. The next discovery rejects duplicates. Hierarchy provisioning does not
create Stories, import workbooks, or publish semantic releases.

## Helper coverage

The Story 417 source audit found these helpers and no duplicated OpenProject
lifecycle, delivery reconciliation, verification, or hierarchy scripts:

| Source | Purpose and disposition |
| --- | --- |
| `scripts/brief-check.py` | Retain for Codex-specific or unsupported checks; Wood Tools already bounds its supported checks and retains their logs. |
| `scripts/token-report.py` | Retain local rollout usage accounting; no equivalent Wood Tools capability. |
| `skills/recent-codex-closures/scripts/recent_closures.py` | Retain local process/session recovery; no equivalent Wood Tools capability. |
| `scripts/install.sh` | Retain Codex profile skill/guidance links and safe existing-path refusal; Wood Tools does not install personal Codex configuration. |
| Workbook skill/references | Retain workbook import routing and write-back policy; standalone hierarchy setup now routes to `hierarchy`. |
| Story, handoff, briefing, and planning guidance | Updated to consume bounded Wood Tools results and returned records; manual reconstruction is limited to explained unsupported operations. |

These helpers are retained because replacement coverage is absent, not as compatibility
wrappers. No helper is removed merely for mentioning a related domain. The audit
does not claim that unavailable Wood validation or optional integration checks passed.
