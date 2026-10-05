---
name: openproject-implementation
description: "Plan or apply an Excel implementation workbook to OpenProject as versions, epics, stories, and predecessor relations. Use for backlog import or sync, not ordinary code implementation."
---

# OpenProject implementation workbook

Use the public `wood project import-workbook` command from the repository that owns the workbook. Read [workbook operations](references/workbook-operations.md) for selectors, environment, and write-back behavior.

1. Establish the workbook, owning repository, project, and initiative. Stop if the target is ambiguous.
2. Run plain `wood` commands. Reuse verified repository mappings and earlier returned IDs; use `wood project list --json` only when discovery is needed. Save each JSON plan in a unique local run directory under `~/.wood/state/openproject-implementation/runs/`.
3. Preview `wood project import-workbook <workbook.xlsx> --json`. Review the plan hash, every page of operations, hierarchy, and predecessor changes.
4. After reviewing the plan, apply it with the same selectors and `--apply --plan-hash <reviewed-hash> --json` when the user's existing authorization covers its operations. Ask for confirmation only for uncovered scope or a material conflict. Verify reported IDs and workbook write-back.

Use the bounded import phases in [workbook operations](references/workbook-operations.md). Batch independent reads and reuse saved results instead of rediscovering IDs or fetching every Story individually by default. Existing task authorization does not replace sandbox execution approval.

Keep the workbook as the desired state. Do not bypass the command's matching and stale-plan checks with manual API edits. Never store secret values in the workbook, run records, or response. For Story selection and delivery, use the [development workflow](../openproject-development-workflow/SKILL.md).

When the authorized task is repository hierarchy setup without a workbook, use
`wood hierarchy plan --json` and `wood hierarchy ensure --apply --plan-hash
<reviewed-hash> --json` with the same selectors. Read the returned operations and
proposed mapping before apply; retain verified IDs and the saved repository mapping.
Do not create a workbook or manual API helper solely to provision an Initiative,
Release, and Epic. Workbook imports remain the supported path for desired Stories
and predecessor relations.
