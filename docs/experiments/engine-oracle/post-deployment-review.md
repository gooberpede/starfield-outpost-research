# Observer 0.1.1 post-deployment / Phase 1 review package

2026-10-10; EXP0022 / EV0030. [Actual-file preflight](../../audits/observer-011-post-deployment-preflight.md),
[Phase 1 card](Phase1-Save25-Save26-operator-run-card.md),
[fixed-POI candidates](fixed-poi-validation-candidates.md),
[retained task scope](../../implementation-briefs/observer-011-post-deployment-phase1.md).
These are returned for critical review before the scientific live experiment.

Actual checks: installed/staged/all five approved ZIP member identities and
package CRC, directly parsed DLL SFSE export 0x00010001/version 0.1.1, installed
game/SFSE/loader versions/hashes, exact config identity, Vortex deployment source,
smoke startup READY/module identity and SFSE loader log, target-process absence,
path reparse attributes and exclusive write/fsync/readback/remove probe, isolated
helper accept/reject/STOP controls, caller-available disk guard, Save25/26 original/
archive hashes and 5298-file before/after byte/size/mtime preservation. No substantive
instrument defect found. Windows DLL version resource is absent; SFSE metadata
and startup/log corroboration provide plugin version identity.

Runtime instrument source, DLL, ZIP, config and scientific input/prediction files
are unchanged. Source hashes still match the approved build manifest. This task
changes authored Markdown only; no instrument rebuild/replacement or broad test
rerun is needed. Offline fixture qualification remains the original EXP0021
build receipt, not a newly executed scientific validation. No actual-session
requests, game launch/load, debugger, native query, save/config/profile mutation,
staging, commit, push or disclosure.

Original local preflight script/receipt and synthetic helper fixture remain under
`.local-work/beacon-observer-preflight/post-deploy-011-01/`. The receipt builder
`review.py` reads Git/authored docs/approved source hashes and writes a complete
tracked+new-file diff, status, SHA-256 file inventory and local review ZIP. It
checks UTF-8/no BOM/LF/trailing whitespace, `git diff --check`, relative Markdown
file destinations, unchanged HEAD, empty staged diff, ignored raw/build paths and
unchanged frozen inputs/predictions. Relative path checks exclude remote URLs and
do not validate Markdown anchor semantics. No network CI/upload or dependency.

Local delivery links:

- [Complete review ZIP](../../../.local-work/beacon-observer-preflight/post-deploy-011-01/review-package.zip)
- [Full actual-file preflight receipt](../../../.local-work/beacon-observer-preflight/post-deploy-011-01/preflight.json)
- [Changed-file/check receipt](../../../.local-work/beacon-observer-preflight/post-deploy-011-01/review.json)
- [Complete authored diff](../../../.local-work/beacon-observer-preflight/post-deploy-011-01/complete.diff)

Earlier failed preflight-script attempts (sandbox tasklist denial and incorrect
notice-member mapping assumption) are retained in separate console receipts.
Toolhelp metadata enumeration and actual Vortex data-folder mapping resolved
them without elevation or any installation change. Smoke readiness does not
establish scientific output freshness, active Workshop identity, frame equivalence,
independent grid validation or complete algorithm equivalence. No new scientific
finding, safe integration point or publication eligibility is promoted.

No permission issue blocks this offline handoff. Phase 1 remains review-required;
fixed POIs remain conditional candidates outside Phase 1, with no arbitrary
outpost-count requirement. A useful review can accept or revise the specific
condition matrix/association policy before authorizing live requests.

Optional future commit title, after review (none created):

```text
docs: verify observer 0.1.1 deployment and prepare Phase 1 validation
```
