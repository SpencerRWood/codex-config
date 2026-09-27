# OpenProject implementation workbook operations

## Command surface

Run the commands from the repository that owns the workbook, using its resolved Wood
configuration. `wood-project` is installed centrally and is available on this machine
at `~/.local/bin/wood-project`.

```bash
wood-project implementation export <initiative-id> --output-dir <run-dir> --json
wood-project implementation plan <workbook.xlsx> --json
wood-project implementation apply <workbook.xlsx> --json
```

Use `export` to obtain a current workbook and JSON snapshot for an existing initiative.
It reads OpenProject without changing it. Use `plan` to evaluate a workbook without
changing OpenProject. Use `apply` only after explicit user approval.

## Per-repository environment

The workbook commands read `--env-file`, which defaults to `.env.resolved` in the
current repository. That file must contain these resolved values:

```dotenv
OPENPROJECT_URL=https://openproject.example.com
OPENPROJECT_API_TOKEN=<resolved token; never commit this>
```

Use these when the workbook does not supply an unambiguous value or when you want to
lock the target explicitly:

```dotenv
OPENPROJECT_PROJECT_ID=project-identifier
OPENPROJECT_INITIATIVE_ID=208
```

When creating a new OpenProject project, write its verified canonical identifier to the
new repository's uncommitted `.env` as `OPENPROJECT_PROJECT_ID`. This field accepts the
project identifier used by the OpenProject API; do not substitute a guessed name. Add
`OPENPROJECT_INITIATIVE_ID` only after the target root work package exists.

`OPENPROJECT_ROOT_WORK_PACKAGE_ID` or `OPENPROJECT_ROOT_ID` may be used instead of
`OPENPROJECT_INITIATIVE_ID`. Keep an untracked `.env` with a secret reference (rather
than a raw token), then generate the ignored `.env.resolved` through Wood Secrets:

```dotenv
OPENPROJECT_URL=https://openproject.example.com
OPENPROJECT_API_TOKEN=vaultwarden://openproject/wood-tools/api-token#OPENPROJECT_API_TOKEN
OPENPROJECT_PROJECT_ID=project-identifier
OPENPROJECT_INITIATIVE_ID=208
```

```bash
wood-secrets resolve-env --input .env --output .env.resolved --apply
```

Commit a `.env.example` containing only the variable names and non-sensitive examples.
Add `.env` and `.env.resolved` to the repository's `.gitignore`. If a repository uses
one explicit environment file outside its root, pass its absolute path with `--env-file`
instead of copying a token or resolved file into the repository.

## Current workbook behavior and V2 target

The frozen Wood Tools importer defaults to the `Implementation` sheet and requires
18 columns ending in `Notes`. It treats `Version` as an OpenProject Version name,
without enforcing R# Planning Increment syntax. It does not consume the newer
`Primary Repository`, `Affected Repositories`, or `Released In` columns if they
appear in a workbook. Planning and apply resolve the OpenProject project and root
work package from workbook metadata. Repeated runs reuse existing records where
their ID or an unambiguous deterministic match identifies them.

The Google Drive templates define the Wood Tools V2 target: `Version` holds an
R# Planning Increment such as `R1 — Codex Foundations`, ordered by its numeric R
identifier and independent of repository SemVer. Story rows require `Primary
Repository`; `Affected Repositories` may be blank; `Released In` stays blank
during planning and records an actual repository semantic-release version only
after shipment. The owning project follows the Domain/Platform outcome rule.
Do not apply a new 21-column template with the frozen importer or claim those
traceability fields will be persisted. The template/importer mismatch is
intentional technical debt for Wood Tools V2.

On successful apply, the CLI verifies writes before reporting them and writes confirmed
Story OpenProject IDs and root metadata back into the workbook. These write-backs are
part of idempotency and should be retained.

## Safety conditions

- An ambiguous match blocks planning; do not choose one manually.
- A supplied `OpenProject ID` must resolve to a Story below the intended root work
  package. IDs outside that tree block planning.
- Save the exact plan and apply JSON in the run directory. Store only operational
  records there; do not copy authentication material.
- Keep the workbook in its owning repository or its approved shared project location.
  Do not use `~/.wood` as the canonical store for every team's workbook.

## Per-repository onboarding

No repository-local pointer to the Codex skill is required: Codex discovers the shared
skill through `~/.codex/skills/openproject-implementation`. The implementation workbook
commands themselves do not require `project.json`; they use the workbook and
`--env-file`. Add `project.json` only when the repository also uses Wood Tools' broader
project/registry workflows.

Before an apply, confirm that the repository, workbook metadata, resolved environment,
and planned root work package all identify the same delivery backlog.
