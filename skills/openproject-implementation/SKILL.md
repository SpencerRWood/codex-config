---
name: openproject-implementation
description: "Plan or apply an Excel implementation workbook to OpenProject as versions, epics, stories, and predecessor relations. Use for backlog import or sync, not ordinary code implementation."
---

# OpenProject implementation workbook

Use the public `wood project import-workbook` command from the repository that owns the workbook. Read [workbook operations](references/workbook-operations.md) for selectors, environment, and write-back behavior.

1. Establish the workbook, owning repository, project, and initiative. Stop if the target is ambiguous.
2. Inject `OPENPROJECT_URL` and `OPENPROJECT_API_TOKEN` with Infisical. Discover the project and initiative IDs through `wood project list --json`. Save each JSON plan in a unique local run directory under `~/.wood/state/openproject-implementation/runs/`.
3. Preview `wood project import-workbook <workbook.xlsx> --json`. Review the plan hash, every page of operations, hierarchy, and predecessor changes.
4. After approval for that plan, run the same selectors with `--apply --plan-hash <reviewed-hash> --json`. Verify reported IDs and workbook write-back.

Keep the workbook as the desired state. Do not bypass the command's matching and stale-plan checks with manual API edits. Never store secret values in the workbook, run records, or response. For Story selection and delivery, use the [development workflow](../openproject-development-workflow/SKILL.md).
