# Workbook operations

Run from the workbook's owning repository. Use the installed `wood` executable after checking that it exposes `project import-workbook`; in a Wood Tools checkout under review, use its checked-out implementation. Inject `OPENPROJECT_URL` and `OPENPROJECT_API_TOKEN` with Infisical. Discover project and initiative IDs through `wood project list --json`. For example:

```sh
infisical run --env=dev --path=/openproject -- wood project import-workbook <workbook.xlsx> --json
```

The preview is read-only. `--project` and `--initiative` select a target when metadata is ambiguous; repeat them for apply. `--operation-offset` pages through plans longer than 50 operations. Save and inspect all pages before approval. Apply the reviewed plan with `--apply --plan-hash <reviewed-hash> --json`. A changed workbook or OpenProject context invalidates the hash and requires a new review.

The `Implementation` sheet models the project, R# planning version, Epic, Story, repository traceability, and predecessors. `Released In` stays blank during planning; R# is not an artifact version. The command reuses unambiguous matches, verifies writes, and records confirmed OpenProject IDs and root metadata in the workbook. Preserve those write-backs for idempotent reruns.

When the import creates a project or initiative, reuse its canonical ID from the
verified apply result and preserved workbook write-back. A fresh `wood project list
--json` readback is needed only if the returned verification is missing or later
state invalidates it. Pass selectors explicitly when workbook metadata is ambiguous.

For repository hierarchy setup without Story/workbook changes, use `wood hierarchy
plan` and `wood hierarchy ensure --apply --plan-hash <reviewed-hash> --json`; that
command verifies relationships and persists repository context. It does not replace
workbook import or export functionality. See the [representative workflow](../../../docs/wood-delivery-workflow.md).

Keep credentials in Infisical. Save only JSON plans and apply results in the local run directory. Stop on ambiguous matches, stale IDs, or missing credentials. The `wood` v2 CLI has no workbook export or manual release-recording command; use the supported import and Story evidence workflow.
