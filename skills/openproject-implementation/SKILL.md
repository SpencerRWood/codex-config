---
name: openproject-implementation
description: "Plan or apply a shared Excel implementation workbook to OpenProject as versions, epics, stories, and predecessor relations. Use when a user asks to import, sync, review, or update an OpenProject delivery backlog from a workbook; do not use for ordinary code implementation."
---

# OpenProject implementation workbook

Use the centrally installed `wood-project` CLI as the only importer. Its maintained
implementation lives in the Wood Tools repository; do not revive or adapt the legacy
scripts in `~/Downloads`.

This skill is shared across repositories. Treat the repository containing the workbook
as the project context, while shared run artifacts belong under `~/.wood/state`.
Never place credentials, workbooks, or project-specific data in this skill folder.

## Workflow

1. Establish the target repository, workbook path, OpenProject project, and intended
   root work package. Do not infer a target when the workbook metadata is ambiguous.
2. Read [workbook operations](references/workbook-operations.md) before working with a
   workbook. It describes the supported command surface and its invariants.
3. Create a unique run directory at
   `~/.wood/state/openproject-implementation/runs/<timestamp-or-run-id>/`. Preserve the
   exported snapshot and the JSON result of every plan there. This directory is local
   operational state, not source-controlled project content.
4. Check the workbook contract before invoking the importer. The current Wood Tools importer
   requires 18 columns and ignores the three traceability columns in the new Google
   Drive templates. Treat the 21-column Planning Increment templates as the Wood
   Tools V2 target; do not plan or publish them through the frozen importer.
5. For a workbook supported by the current importer, run
   `wood-project implementation plan <workbook.xlsx> --json` before proposing any
   OpenProject change. Planning is read-only. Review planned creations, updates,
   reused records, ambiguity, and failures. Present the plan's Versions, Epics,
   Stories, hierarchy, and predecessors, then obtain approval for the specific apply.
6. Only after approval, run `wood-project implementation apply <workbook.xlsx> --json`.
   Record its output in the run directory. Verify its reported IDs and the workbook
   write-back before claiming success.

## New-project handoff

When a workflow creates a new OpenProject project, verify the created project's canonical
identifier and update the owning repository's uncommitted `.env` immediately:

```dotenv
OPENPROJECT_PROJECT_ID=<created-project-identifier>
```

Do this only after the project creation succeeded and the identifier was read back from
OpenProject. Preserve the repository's existing `.env` values and never put the resolved
token in source control. Do not set `OPENPROJECT_INITIATIVE_ID` until the root work
package has actually been created or selected.

## Boundaries

- Do not change the frozen Wood Tools importer or use its current 18-column behavior
  as evidence that `Primary Repository`, `Affected Repositories`, or `Released In`
  will be persisted. Those fields and strict R# enforcement are V2 work.
- `implementation apply` is the sole operation here that may mutate OpenProject.
  Never run it merely because a user asked to inspect, prepare, export, or plan.
- Stop on ambiguous matches, stale IDs, missing credentials, or an unresolved project
  context; do not create replacements or guess mappings.
- Preserve the workbook as the desired state. Do not manually call OpenProject APIs or
  make one-off changes that bypass the CLI's idempotency checks.
- Use the existing Wood configuration and secrets mechanisms. Never read a token into
  an artifact, workbook, plan, or response.

## Shared locations

- Skill source and references: `~/.wood/agent-skills/openproject-implementation/`
- Codex discovery link: `~/.codex/skills/openproject-implementation`
- Shared Wood runtime and secrets: `~/.wood/`
- Local plans and apply records: `~/.wood/state/openproject-implementation/runs/`

For a read-only next-Story lookup, use `wood-next-story --json`. The installed
wrapper reads `.env` in the current directory by default; use `--env-file` for
another path. It uses `OPENPROJECT_INITIATIVE_ID` by default and remains subject
to the frozen selector behavior described above.

For workbook sheets, required environment, and exact CLI behavior, read
[workbook operations](references/workbook-operations.md).
