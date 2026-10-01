---
name: session-handoff
description: Create a compact, verified checkpoint for continuing an active objective in a fresh Codex session. Use at an objective, repository, or deployment boundary or when the user requests a handoff.
---

# Session Handoff

Create a concise checkpoint from verified work in the current session. Include these fields: Goal, Completed, Current State, Changed Files / PRs / Releases, Validation, Blockers, Next Exact Action, and References. Use `none` for empty fields and distinguish observed results from pending work. Include paths and links needed to resume, without copying transcripts, long logs, secrets, or speculative status. Target 500–800 words maximum; use less when the facts fit. Save it to a file only when the user requests an artifact; otherwise return it in the response.

For an OpenProject Story, consume the latest `wood delivery status <id> --json`
result or the `delivery` snapshot from `wood story evidence`. Reuse facts already
returned; query delivery once only if no relevant snapshot exists or a subsequent
mutation made it stale. Record the observation time, Story and repository, branch,
source/merge revisions, PR and CI identifiers, `delivery_stage`, `blocker`, and
`next_action`. Envelope success alone does not prove delivery complete.

For enhanced delivery reports, use `observed_at` as the query's observation time
and retain `fields.merged_revision`, `fields.release_run` (run ID, attempt,
revision, conclusion, authority link), relevant `release_jobs` IDs/failed steps,
and job/step truncation flags. Carry the exact returned diagnostic or wait action
forward; do not rediscover its identifiers. Release-job success does not establish
deployment or runtime health. Observation time does not refresh an older attestation.

The two snapshot shapes differ: `delivery status` supplies `fields` and stage/action
metadata, while evidence's `delivery` is a map of normalized field states, values,
and sources. Preserve the shape actually returned. Record the local observation time
if the result has no timestamp; mark missing stage/action metadata unavailable
rather than inferring it from an evidence snapshot.

Carry forward `data.validation_file`, applicable `data.verification_file`,
`data.evidence_file`, `data.update_file`, plan hashes, and full log paths exactly
as returned. Distinguish saved verification from a current environment observation;
do not rerun passing checks merely to prepare a handoff. Keep deterministic evidence
separate from the summary. Report absent, unavailable, pending, and not-applicable
facts as observed; never fill them in by guessing or additional API reconstruction.
Use direct system access only for an explained capability or diagnostic gap.
