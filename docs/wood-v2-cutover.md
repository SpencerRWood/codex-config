# Wood Tools v2 cutover inventory (WP-401)

The installed `wood` CLI is the first-party execution contract. The old project,
resource, and template routers had no v2 callers and were removed from Wood Tools,
along with their private package logic, bundled template assets, and tests that only
exercised the retired routes. `wood_project.openproject`,
`wood_project.implementation`, and `wood_project.story` remain internal because the
public `wood` commands use them. The `resources.cli.audit` module remains for v2 audit
records; its retired command descriptions were removed.

| Migrated capability | Replacement | Caller migration | Validation and deletion |
| --- | --- | --- | --- |
| Secret readiness | `wood secret` and `wood doctor` with Infisical injection | Workbook skill and README | Wood Tools diagnostics tests and repository validation; old credential-file instructions removed |
| Project discovery and workbook import | `wood project list`, `status`, and `import-workbook` | Workbook skill, reference, Planning Increment guide | Plan-hash workflow retained; old workbook router and instructions removed |
| Story selection and lifecycle | `wood story next`, `get`, `start`, `complete` | Development workflow and README loop | Story tests and repository validation; old standalone selector references removed |
| Repository checks and delivery evidence | `wood repo validate`, `wood ci status`, `wood deploy status` | Development workflow and README loop | Repository validation and current-run checks; duplicate manual validation mechanics removed |
| Artifact release | Python semantic-release and the shared GitHub workflow | Planning Increment guide and Wood Tools migration procedure | Release workflow contract retained; manual release mutation routes absent |

The former project metadata, resource installation, and template generation commands
were v1-only capabilities outside the v2 command contract. Their code and bundled
assets were deleted rather than exposed under new aliases. The current v2 workflow
does not depend on them.

The workbook skill and its reference shrank from 1,145 to 391 whitespace-delimited
words (66% fewer). The compact loop in the README names the same review, CI, and
closure gates while deferring the detailed policy to the Story skill. This is an
instruction-size comparison, not a runtime token measurement.

Before review, scan both changed repositories for active calls to retired executable
names, resolved-token files, deprecated configuration keys, manual release mutation,
and removed Python modules. Historical changelog entries may retain names as records;
first-party instructions, imports, and tests must use only the v2 contract. The
Wood Tools architecture test also checks that removed modules and the extra console
entrypoints stay absent.
