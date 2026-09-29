# Story operations

Run these commands from the Story's repository. Use Infisical in `dev` at
`/openproject` to inject `OPENPROJECT_URL` and `OPENPROJECT_API_TOKEN`.
Discover the project and initiative IDs through `wood project list --json`. The Story
commands use the single public `wood` executable.

In the Wood Tools checkout under review, use `uv run --active --frozen wood`.
In another repository, use the installed `wood` after `wood story --help` confirms
this command group. Keep the command's working directory in the Story repository;
`story start` checks its repository name and working tree.

```sh
infisical run --env=dev --path=/openproject -- wood story next 208 --json

infisical run --env=dev --path=/openproject -- wood story get <id> --json
```

`next` selects an eligible Story in the earliest active R# release. Closed and Rejected
Stories are terminal; a Rejected predecessor does not satisfy a dependency. Blocked
and unversioned Stories are ineligible. If no Story is returned, report that condition.
Use `get --offset N` if the packet includes more than 50 description chunks.

After authorization to start, preview then apply `wood story start <id> --json` with
`--apply`. `start` checks the live Story, open planning version, predecessors, and
repository before updating status and preparing the standard local branch. Verify the
returned status and branch. It does not commit or push.

After a merged PR and required checks, prepare a JSON evidence file with passed
`repository_checks` entries and a passed `ci` run URL. Post and verify the implementation
update activity with the released `wood story activity add <id> --file <comment-file> --json`
command (preview, then `--apply`), then preview and apply `wood story complete <id> --evidence <file>
--json`. Verify the live closed status. Do not complete while checks are pending,
failed, or unavailable.

For a repository with the WP-400 commands, use the passed entries from
`wood repo validate --json` as local `repository_checks` evidence and keep its returned
log paths rather than pasting logs. `wood ci status --json` supplies the run URL only
when its commit is current and the run succeeded. Use `wood ci failures --json` only
to diagnose a failed current run. When `ci status` is stale because another commit has
the latest repository run, use the PR's authoritative checks. `wood deploy status --json`
supplies deployment evidence when `repo info` marks deployment applicable; specify
`--environment` when several environments exist. `not_applicable` is expected for
libraries without a deployment workflow. These read-only inspections do not authorize
a Story status change or replace the live CI verification in `wood story complete`.
