# Story operations

Run these commands from the Story's repository. Set `OPENPROJECT_URL` from verified
repository configuration and use Infisical in `dev` at `/openproject` to inject
`OPENPROJECT_API_TOKEN`. Set `OPENPROJECT_PROJECT_ID` when available. The Story
commands use the single public `wood` executable.

Before a release updates the installed executable, run these examples from the
Wood Tools checkout with `uv run --active --frozen wood`. In another repository,
use the installed `wood` only after `wood story --help` confirms this command group.

```sh
OPENPROJECT_URL=https://projects.woodhost.cloud OPENPROJECT_PROJECT_ID=3 \
infisical run --env=dev --path=/openproject -- uv run --active --frozen wood story next 208 --json

OPENPROJECT_URL=https://projects.woodhost.cloud OPENPROJECT_PROJECT_ID=3 \
infisical run --env=dev --path=/openproject -- uv run --active --frozen wood story get 399 --json
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
update activity, then preview and apply `wood story complete <id> --evidence <file>
--json`. Verify the live closed status. Do not complete while checks are pending,
failed, or unavailable.
