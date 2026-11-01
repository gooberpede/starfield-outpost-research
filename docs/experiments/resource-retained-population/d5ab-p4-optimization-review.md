# P4 optimization correction review

2026-11-01, Australia/Sydney. **Final independent disposition ACCEPT. Corrected P4 COMPLETE;
READY for maintainer review only. B2 NOT AUTHORIZED.** The original P4 READY verdict
was superseded by the [dated correction](d5ab-p4-optimization-correction.md).
This record does not replace the [original review](d5ab-p4-review.md).

The independent reviewer authored none of the correction. It receives the original
D5AB/P4 contract, adopted maintainer instruction, original READY snapshot, source
and assertion audit, exact package/plan/card, primary old/new receipts, failed
controls, normal and optimized probes, protected equality and both review patches.
The specialist who authored the bounded legacy regression wrapper cannot accept
its own implementation.

## Preliminary independent challenge

Initial review confirms that optimization erases native API/cleanup calls as well
as validations. It traces the actual protection dependencies and distinguishes
direct B2 entry points from private imported historical helpers. No additional
uncovered B2 invocation edge is found after the early guards. The reviewer
explicitly challenges remaining native liveness queries inside assertions:
they remain supported-mode checks behind the guard, not pure expressions.
Historical generated `cutover.py` command metadata is not a child process executed
by this preservation path and is not silently relabeled optimization-safe.

The reviewer independently reruns 218 optimization controls across 24 modules and
28 admission controls. The primary exact receipt is
`.local-work/d5ab/p4-opt-independent-optimization01/receipt.json`, SHA-256
`d9a536ef45581782cfd175bfe47fae667a66770a5cd129acfdec1be953164677`.
The independent admission receipt is
`.local-work/d5ab/p4-opt-independent-admission01/receipt.json`.
These are actual disposable executions, without retail activity or source edits.

Independent inspection checks all 100 package member lengths/hashes, 99 plan
package pins and all 29 measured protection dependency-module hashes. Package
manifest SHA-256 is
`7ca5e79ac1ea0e761fe02df8fbf6640ab6453578e63ea1f5de9b28222fbbdc44`;
plan SHA-256 is
`2de7f60692af850c34cafa46de4fefb4679c33ac77f3944eeecf94f175dddc70`.
This preliminary result is not final acceptance of readiness or prose/delivery.

## Finalization requirements and evidence

The complete changed prose set includes the dated correction, history notice,
original-verdict snapshot, ledger/state/navigation, exact B2 commands, Python
guard comments/docstrings, assertion-audit qualifications and test/accounting
labels. All changed authored text receives automatic screening, full manual
reading/correction and independent exact-snapshot review. The supplied original
brief and existing raw evidence remain unchanged. No bulk historical cleanup.

The corrected exporter is
[d5ab_p4_opt_export.py](../../../research/resource-retained-population/d5ab_p4_opt_export.py).
It retains `d5ab-p4-opt-complete.diff` and `d5ab-p4-opt-task-only.diff` under
`.local-work/diffs/`, with frozen copies/status/inclusion/exclusion manifests in
`.local-work/d5ab/p4-opt-delivery/`. Admission was clean; both coverage patches
therefore contain the same task changes. Untracked authored text is included
without staging. Exact tracked/untracked inventory, forward/reverse application
and byte comparison, actual-tree reverse applicability, whitespace, UTF-8/LF,
local evidence links and unchanged HEAD/index are checked.

Final accounting explicitly uses `optimization-final02`, not the earlier fixed
`optimization-final01` input of the initial provenance verifier. The latter is
an intermediate historical receipt; its builder hash became stale after closure
expansion. No old receipt or source pin is rewritten. Current package/member,
all source/build/test hashes and full protection equality are verified by the
retained method `.local-work/d5ab/p4-opt-final-accounting01.py` and its receipt.

The final reviewer must assess every original AB question/twelve criteria and
P4 question/eight criteria, including the optimization failure mode and strongest
remaining avenue, rather than accepting test totals alone. Actual retail SFSE
admission and target scheduling remain untested future B2 outcomes. Independent
acceptance supplies neither integration, deployment, game nor publication authority.


## Final independent disposition

The implementation-independent reviewer returns ACCEPT for the exact review01
snapshot and all original AB/P4 questions and criteria. Its actual full return is
`.local-work/d5ab/p4-opt-independent-final-review01.md`. It additionally executes
41 procedure/archive/finalization controls; receipt SHA-256
`e13ca8f8ec3d0dcdb56d8dc8cad27d319e6471b26b9c5347a2a0403bbc0d3c82`.
It verifies all 41 source/prose hashes against review01 and manual01, both patch
hashes and reverse applicability, the exact current package/protection accounting,
and unchanged HEAD/index. Review01 delivery SHA-256 is
`814a68903e31dd8434d544605aba8025fe65ed55204617c2deb2c28381d5460d`;
both patches SHA-256
`cf1c7e5b8d857c96563eda31ec8ab82830bdf5df492b7531fea0b744e031f7a7`.

All twelve AB criteria, eight P4 criteria and both five-question sets are accepted
within original offline readiness. Strongest dependency-chain and side-effect
challenges are resolved with the explicit scoped limits retained in the correction.
Engineering, scientific-readiness, operational and editorial ACCEPT; publication
ON HOLD. Closing metadata alone receives a narrow exact-delta review recorded in
`.local-work/d5ab/p4-opt-delivery/final01/closing-review.md`. Final source/package,
plan, native bytes and test receipts are unchanged. Complete/task-only final
patches and inventory are in that directory and canonical `.local-work/diffs/`.
No acceptance grants integration, deployment, B2 or Git-write authority.
