---
name: audit-findings-log
description: Save the final findings of a completed audit to the user's Google Drive Logs folder. Use for repository, workflow, security, or operational audits with a substantive verdict or findings; skip when the current request forbids Drive writes.
---

# Audit findings log

The user has authorized automatic logging of completed audit findings across the `codex` and `codex2` profiles. The destination is the existing Google Drive `Logs/` folder: `https://drive.google.com/drive/folders/1vfexr_QKqKjYxambT1smWfLLts36olL5`.

After the audit findings are settled and before the final response:

1. Respect the current request. If it forbids Google Drive or external writes, do not upload; state that the audit was not logged. Do not treat this standing preference as permission for any other external change.
2. Prepare a Markdown copy of the actual final findings, including the subject, audit date, verdict, evidence, validation, remaining work, and disposition when applicable. Preserve material uncertainty and distinguish a fresh audit from a copy of older findings. Exclude credentials, tokens, private data, raw diagnostics, and unnecessary environment details.
3. Use the connected Google Drive capability to verify the destination folder, upload the Markdown file there with a descriptive, date-stamped name, and read back its metadata to verify its name and parent. Do not overwrite an existing log; add a time or revision suffix if the name is already used. Use a temporary local file only as needed for the upload.
4. Link the verified Drive file in the final response. If the connector is unavailable or the upload fails, report that plainly and give the completed audit findings in the response. Do not claim the log was saved without readback.

This skill logs audit findings only. It does not rerun an audit, change its verdict, or authorize edits to audited systems.
