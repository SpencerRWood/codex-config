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

The Wood Tools V2 next-Story selector will scan active R# Planning Increments
in numeric order and select a Story whose predecessors are closed. A Planning Increment is
complete when all included Stories are closed and shipped Stories have release
traceability where practical. Completion does not require a single repository
version or GitHub Release for the whole increment.

## Current runtime boundary

The clean OpenProject cutover retired the legacy backlog as `Rejected`, closed
legacy Versions, and left no active Story or Planning Increment. Historical work,
Version assignments, and predecessor relations remain intact. Wood Tools is frozen
until V2; do not retrofit its selector or importer now. The current importer still
uses its 18-column workbook contract and does not consume `Primary Repository`,
`Affected Repositories`, or `Released In`. It defaults to the `Implementation`
sheet, but it does not enforce R# Versions or the traceability lifecycle. Its
selector still uses legacy Version ordering and fallback behavior. The 21-column
Google Drive Planning Increment templates are the V2 target contract, not a
supported current import contract. Do not publish a new backlog with the frozen
importer solely because a template contains the target headers.

The installed `~/.wood/scripts/wood_openproject_env.py` is a temporary local
compatibility patch for the current `OpenProjectSettings` constructor. It is a
regular local file. The current codex-config installer leaves it alone; another
install that replaces `~/.wood/scripts` may overwrite it. Reproduce the
fix by removing unsupported `initiative_id` and `ca_file` constructor arguments
and supplying `project_id` as a string. Keep this patch local until V2 defines
the durable helper installation or generation path.
