# OpenProject Planning Increments

## Ownership and hierarchy

Place work in the OpenProject project that owns its outcome. Domain projects own a
specific product or repository result. Durable Platform projects own shared CI/CD,
infrastructure, secrets, authentication, migrations, and cross-repository
engineering. A code edit in a Domain repository does not by itself move a shared
outcome out of Platform. Resolve ownership before publishing Stories. Do not use
a generic Ad Hoc project or create a project for each migration.

Use `Project → R# Planning Increment → Epic → Story → pull request → repository
artifact`. An OpenProject Version represents exactly one Planning Increment.
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

The next-Story selector scans active R# Planning Increments in numeric order
and selects a Story whose predecessors are closed. A Planning Increment is
complete when all included Stories are closed and shipped Stories have release
traceability where practical. Completion does not require a single repository
version or GitHub Release for the whole increment.

## Existing OpenProject data: migration notes

Do not rename historical Versions or rewrite repository release history
automatically. Inventory each existing OpenProject project, Version, Story,
predecessor relation, repository, and known artifact version first. Decide the
durable Domain or Platform owner from the outcome; group migrations within
Platform increments and Epics. Map future planned work to new R# Versions.
For active legacy Versions, draft an explicit Story-by-Story mapping and review
whether renaming or moving would change historical meaning or external links.
Preserve old names when necessary and document the mapping rather than inferring
SemVer from a Version name. Populate `Released In` only from verified repository
release evidence. Preview all intended OpenProject writes and run the separate
live migration only after its own approval. This task makes no live changes to
existing OpenProject projects or Versions.
