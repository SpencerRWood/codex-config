# Personal Codex configuration

This repository is the shared source for the `codex` and `codex2` CLI profiles on this Mac. It contains global guidance, personal skills, and their supporting scripts and references. It does not contain account credentials, Codex runtime state, or the old Wood Tools `AGENTS.md`.

Run `bash scripts/install.sh` after cloning to link `AGENTS.md` and every `skills/*/SKILL.md` folder into both Codex homes. The installer refuses to replace existing files or directories. Installation is limited to the Codex homes; it does not write guidance or Git configuration into a Wood Tools checkout.

Use `wood epic list/get` and `wood release list/get` with `--json` for live
OpenProject planning inspection (requires a Wood Tools version exposing these
commands). Both groups accept project context; get accepts an ID or exact name.
Edit repository code and tests directly instead of writing temporary Python
file generators. Check command help or `wood contract --json` before explaining
and using a fallback for an unsupported operation.

`brief-check` runs a command, saves its full combined output locally, and returns compact JSON. For example: `python3 scripts/brief-check.py -- sh -c 'printf "ok\\n"'`. `session-handoff` produces a concise fresh-session checkpoint. To measure local usage, run `python3 scripts/token-report.py --since YYYY-MM-DD`; it reads saved rollouts and reports totals and largest sessions. It does not monitor sessions in the background.

## Wood Tools v2 workflow

Use Wood Tools first for supported Story, repository, CI, delivery, verification,
and hierarchy operations. The adopted surface is Wood Tools **v0.19.2 or later**;
check the selected executable with `wood contract --json` once and retain that
result. Run plain `wood` commands and use the
[Story workflow](skills/openproject-development-workflow/SKILL.md) for review and
closure policy. Repositories with `[tool.wood.openproject]` context can omit the
Initiative reference. The [representative workflow](docs/wood-delivery-workflow.md)
includes previews, optional verification, summary repair, and hierarchy setup.

Use the globally installed `wood` from the current task repository. Install or
upgrade the released tool with:

```sh
uv tool install --force --python 3.14 --from 'git+https://github.com/SpencerRWood/wood-tools.git@v0.19.2' wood-tools
```

In a Wood Tools checkout under review, select `uv run --active --frozen wood`
instead. Installation does not select repository context: `project_id` and
`initiative_id` belong in the current Git root's `[tool.wood.openproject]` table
in `pyproject.toml`. Supported explicit CLI selectors take precedence over mapped
IDs. Agents must not use `OPENPROJECT_PROJECT_ID` or `OPENPROJECT_INITIATIVE_ID`
as overrides or fallbacks; configure missing required mappings or supply supported
explicit CLI selectors. These IDs are not global runtime prerequisites.
Wood Tools v0.19.2 removes environment-ID fallback from the implementation.

Only `OPENPROJECT_URL` and `OPENPROJECT_API_TOKEN` are globally required. The URL
is non-secret global configuration; the API token stays Infisical-backed and is
injected only into the command process. Never persist it in `.env`, `pyproject.toml`,
configuration files, logs, diagnostics, or generated artifacts. Project discovery
works with URL/token alone, without repository mappings.

The normal flow is:

```text
wood doctor --json                         # readiness when uncertain
wood story next --json
wood story get <id> --json
wood story start <id> --json
wood story start <id> --apply --json
# inspect existing implementation, implement, validate, and fix failures autonomously
wood repo validate --json
# prepare implementation evidence inputs and proposed commit/PR summary
# stop immediately before commit/push/PR creation for the Story skill's review
# approval permits the reviewed batch's standard delivery and closure workflow
wood ci status --json
# after the approved PR merges; retain data.validation_file from repo validate
wood delivery status <id> --json
wood repo verify --json                    # when repository-owned checks apply
# include --verification <verification-file> in both evidence calls when applicable
wood story evidence <id> --validation <validation-file> --pr <number> --ci-run <run-id> --json
wood story evidence <id> --validation <validation-file> --pr <number> --ci-run <run-id> --apply --json
wood story activity add <id> --evidence <evidence-file> --json
wood story activity add <id> --evidence <evidence-file> --apply --json
wood story complete <id> --evidence <evidence-file> --json
wood story complete <id> --evidence <evidence-file> --apply --json
```

The Story skill defines autonomous in-scope implementation through validation fixes,
evidence preparation, and proposed commit/PR summaries. It requires no intermediate
implementation approvals; the first normal approval boundary is immediately before
commit/push/PR creation. Review includes changes, repositories, validation/test
results, material decisions, and proposed commits/PRs. Separate tool/runtime
approvals and scope/safety limits still apply. The skill also owns status, branch,
CI, evidence, and closure safeguards. Workbook imports use `wood project
import-workbook` with a reviewed plan hash. Infisical supplies secret values;
Python semantic-release owns version, tag, and GitHub Release changes.

Reuse the generated evidence path returned by Wood Tools for activity posting and completion. Logs and generated files follow `[tool.wood.workflow] output_directory` in the current repository's `pyproject.toml`, defaulting to `/private/tmp`. The workflow skill explains regeneration and unsupported-workflow fallbacks.

Use one returned delivery snapshot for briefings and handoffs. Keep its observation
time, revisions, blockers, next action, and saved validation/verification/evidence
paths. Envelope success describes the query; it does not turn missing, pending,
or failed delivery into success. Direct GitHub/OpenProject/infrastructure access
requires an explained missing capability or diagnostic gap. Wood Tools does not
manage PR creation/merge, so those remain `gh` operations. Ambiguity, failed checks,
stale plans, and missing credentials do not justify bypassing its safeguards.

Enhanced delivery status also reports `observed_at`, `merged_revision`, the exact
revision-bound `release_run` and attempt, and bounded `release_jobs` diagnostics.
Use its returned diagnostic or wait action and retain truncation flags. Save full
diagnostic logs through `brief-check`. Release-job success does not establish an
image digest, deployment revision, or runtime health. The
[representative workflow](docs/wood-delivery-workflow.md) describes these fields
and installation-drift handling; older installed binaries may expose the command
without the enhanced fields.

The audit of this repository found no duplicated OpenProject control scripts to
remove. `brief-check`, token reporting, installation, and local session recovery
remain Codex-specific; see the [helper coverage record](docs/wood-delivery-workflow.md#helper-coverage).
Wood Tools already owns bounded output/logs for its supported checks, so do not
wrap those checks with `brief-check` or rerun them to prepare a handoff.

## Validation

This repository's normal suite is `python3 -m unittest discover -s tests -v`, as
declared in `.github/workflows/validate.yml`. It has no `.github/release.toml`,
so `wood repo validate` reports `CONTRACT_MISSING`; use the normal suite through
`brief-check` as the explicit fallback and retain its raw log. Do not claim that
unsupported Wood validation or generated evidence passed. Generated evidence is
unavailable for this repository's current contract; use the Story skill's documented
unsupported-workflow fallback after PR/CI verification.

The suite checks local document links, executable workflow examples, preview/apply
boundaries, and handoff routing. When Wood Tools is installed, it also verifies the
example commands and flags against that executable's contract and help output.
Set `CODEX_WOOD_EXECUTABLE=/path/to/wood` to test a selected installation. This
integration check is explicitly skipped when no Wood executable is available;
the repository's dependency-free helper tests still run. Skills can additionally
be checked with the skill-creator `quick_validate.py` helper.

Completed audit findings are saved to the shared Google Drive `Logs/` folder through the `audit-findings-log` skill, unless the specific audit request prohibits Drive writes. The installer links the skill into both Codex homes.

Codex reads global `AGENTS.md` at session start. Restart a session after changing global guidance. Skills can be discovered from their symlinked folders.

On this Mac, the default `codex` home is `~/.codex`; the `codex2` shell function sets `CODEX_HOME=~/.codex-secondary`. The installer links this repository's guidance and skills into both homes. Verify both links after installation, and start fresh sessions to load changed guidance.
