# Workbook operations

Run plain `wood` commands from the workbook's owning repository. Use the installed executable after checking that it exposes `project import-workbook`; in a Wood Tools checkout under review, use its checked-out implementation. Discover project and initiative IDs through `wood project list --json`. For example:

```sh
wood project import-workbook <workbook.xlsx> --json
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

## Bounded import phases

1. **Source and preflight.** For a Drive workbook, read metadata and export once using the Drive skill. Import a local copy when the user requires the source to remain unchanged: the CLI writes IDs back to its input file. Preserve an untouched local export before apply. Validate the canonical Implementation rows and increment metadata together using the existing workbook parser. Read requirements only when requested or needed to resolve a contract. Check `wood contract --json` once and reuse its capability facts; do not search repository internals for a routine supported import.
2. **Discovery and plan.** Resolve project context once when it is not already verified. Save the import preview and inspect all operation pages. The importer matches roots project-wide but matches Stories within the selected root's descendants; a new root alone does not prove the Stories are absent elsewhere. When duplicate checks are required, list project Stories once, consume every returned page, and compare canonical IDs and subjects locally. Do not also list all R1 Stories unless that narrower query answers a separate unresolved question. Batch independent version and Story reads, retain full JSON on disk, and return only matches, counts, conflicts, and record paths.
3. **Apply.** Review every operation against the authorized workbook scope and reuse the reviewed hash. An explicit request to load the workbook covers faithful creation/reuse within that scope; it does not authorize overwriting unrelated work. Keep apply sequential after review. Do not combine preview and apply into an unattended mutation or automatically apply a changed hash.
4. **Verify and report.** The importer reads back and verifies its writes. Run one read-only post-apply preview and require zero create/update operations for convergence. Use one root-scoped Story list to verify the exact count and IDs, and reuse version evidence unless the import changed versions. The current apply envelope may omit created IDs even when it reports success; recover them from the local workbook write-back and post-apply preview rather than rediscovering the project. A converged preview does not prove there are no extra Stories or relations. When the requested verification requires exact packets or dependency equality, batch the necessary `wood story get` calls in one bounded credentials-injected execution, inspect all description/relation pages, and compare locally. Otherwise avoid redundant individual Story reads. Stop after the requested checks pass.

For network execution, reuse an applicable approved command prefix. If a sandbox request fails due to network restrictions, retry through the prescribed escalation once; use that established execution mode for subsequent calls to the same service instead of repeating sandbox failures. Batch independent authorized reads in a bounded execution to reduce approval round trips. Keep write approval separate when required; never weaken sandbox policy or request a broad arbitrary-shell approval to speed up imports.

Include phase-level timings when an import is slow so command execution, approval waiting, source retrieval, and verification are distinguishable. Reuse one saved verification snapshot in the completion report. Do not promise a fixed duration: network and approval latency remain external to the workflow.
