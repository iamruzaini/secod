# Evidence-boundary behavior cases

Every SECOD output must preserve the distinction between a recommendation, a
repository observation, and a verified control. These cases are required
negative behavior cases for every skill and for `secod-ship-check`.

| Case | Input condition | Required output | Prohibited conclusion |
| --- | --- | --- | --- |
| Inaccessible dashboard | A dashboard or provider API setting cannot be accessed | Affected control is `Not verified`; name the evidence needed | Claiming the dashboard setting was checked or passed |
| Documentation-only plan | A fixture or test plan is present but no executable run occurred | State that the plan was not executed; keep result `Not verified` | Claiming the documentation-only plan executed |
| Reachable source URL | An official URL returns successfully but its control mapping was not read | Keep the source pending/not verified until reviewed and mapped | Marking a source `Reviewed` from HTTP reachability alone |
| Missing control evidence | A control has no sufficient repository, runtime, provider or supplied external evidence | Return `Not verified` or the supported negative finding; include a next verification step | Returning `Passed with evidence` without evidence |
| Security verdict boundary | Some controls are reviewed but scope, evidence or required skills remain incomplete | Report bounded findings and blockers; route readiness to `secod-ship-check` | Claiming the project is secure or certified |

The repository validator checks that all 57 skill contracts preserve the
`Not verified` and launch-readiness boundaries, that the 57-case matrix carries
these cases, and that the executable critical fixture cannot emit a readiness
verdict as production evidence.
