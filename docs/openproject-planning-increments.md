# OpenProject Planning Increments

## Ownership and hierarchy

Place work in the OpenProject project that owns its outcome. Domain projects own a
specific product or repository result. Durable Platform projects own shared CI/CD,
infrastructure, secrets, authentication, migrations, and cross-repository
engineering. A code edit in a Domain repository does not by itself move a shared
outcome out of Platform. Resolve ownership before publishing Stories. Do not use
a generic Ad Hoc project or create a project for each migration.

Use `Project → R# Planning Increment → Epic → Story`, with pull requests and
repository releases providing separate delivery traceability. An OpenProject
Version represents exactly one Planning Increment.
Name it `R1`, `R2`, etc., optionally adding a description such as `R1 — Codex
Foundations`. Order by the numeric R value, so R10 follows R9. The R identifier
has no relationship to repository SemVer. A Planning Increment may include
multiple semantic-release versions and GitHub Releases.

Each Story records its owning project, Planning Increment, Primary Repository,
other Affected Repositories where needed, and genuine Predecessors. Keep the
workbook `Version` header for OpenProject compatibility and put the R# name
there. Keep `Released In` blank at planning and publication. After a shipped
Story's actual repository semantic-release version is known, enter that version
without changing its Planning Increment. A GitHub Release is the published
repository artifact record, separate from both fields.

`wood story next --json` uses repository context when available and scans active R# Planning Increments
in numeric order and selects a Story whose predecessors are closed. A Planning Increment is
complete when all included Stories are closed and shipped Stories have release
traceability where practical. Completion does not require a single repository
version or GitHub Release for the whole increment.

## Current command path

Use `wood project import-workbook` to preview and apply the 21-column workbook,
`wood story next` to select eligible work, and `wood story get` to read its packet.
The [development workflow](../skills/openproject-development-workflow/SKILL.md)
governs Story status, branch preparation, review, and closure. Inject OpenProject
credentials with Infisical. Python semantic-release owns artifact versions, tags,
and GitHub Releases; the planning increment remains independent of those releases.

For authorized hierarchy setup without workbook Story changes, use
`wood hierarchy plan --json` followed by `wood hierarchy ensure --apply --plan-hash
<reviewed-hash> --json` with the same project/Initiative/Release/Epic selectors.
Reuse the verified mapping rather than manually matching or creating those objects.

After an approved Story merges, use `wood delivery status <id> --json` for one
delivery-chain briefing, `wood repo verify --json` for applicable repository-owned
checks, and `wood story evidence` with the saved validation/verification records.
Keep this deterministic evidence separate from implementation narrative. Reuse the
returned fields in the next Story briefing or handoff; a new repository requires
its own context and validation. The [representative workflow](wood-delivery-workflow.md)
shows the finalized command shapes and explicit unsupported-workflow fallbacks.
