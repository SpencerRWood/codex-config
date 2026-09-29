# Workbook operations

Run from the workbook's owning repository. Use the installed `wood` executable after checking that it exposes `project import-workbook`; in a Wood Tools checkout under review, use its checked-out implementation. Set `OPENPROJECT_URL` from verified configuration and inject `OPENPROJECT_API_TOKEN` with Infisical. Set `OPENPROJECT_PROJECT_ID` when available. For example:

```sh
OPENPROJECT_URL=https://projects.woodhost.cloud OPENPROJECT_PROJECT_ID=3 \
infisical run --env=dev --path=/openproject -- wood project import-workbook <workbook.xlsx> --json
```

The preview is read-only. `--project` and `--initiative` select a target when metadata is ambiguous; repeat them for apply. `--operation-offset` pages through plans longer than 50 operations. Save and inspect all pages before approval. Apply the reviewed plan with `--apply --plan-hash <reviewed-hash> --json`. A changed workbook or OpenProject context invalidates the hash and requires a new review.

The `Implementation` sheet models the project, R# planning version, Epic, Story, repository traceability, and predecessors. `Released In` stays blank during planning; R# is not an artifact version. The command reuses unambiguous matches, verifies writes, and records confirmed OpenProject IDs and root metadata in the workbook. Preserve those write-backs for idempotent reruns.

Keep credentials in Infisical. Save only JSON plans and apply results in the local run directory. Stop on ambiguous matches, stale IDs, or missing credentials. The `wood` v2 CLI has no workbook export or manual release-recording command; use the supported import and Story evidence workflow.
