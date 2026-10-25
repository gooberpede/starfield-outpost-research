# Completion contract, review and delivery

2026-10-25, Australia/Sydney. [Frozen brief](../../implementation-briefs/CODEX_BRIEF_SOR_preservation_audit_optimization.md),
[report](report.md), [methods](../../../research/preservation-verification/README.md).
No criterion is amended. **REWORK: AC4 FAIL.** A numerical conditional speedup
does not satisfy comparable protection. Suggested commit text is withheld under
the brief's explicit all-mandatory-criteria condition.

## Criterion matrix

| AC | Status | Primary evidence and limits |
|---|---|---|
| AC1 scope, authority, protection | PASS | Initial status only supplied brief; HEAD `30832aca68eee90c3af4941b454baaf245d3f2ed`. Existing protection helper before/after: zero changes; reuse confirms HEAD/index equality. Offline fixtures only, no original writes or policy activation. |
| AC2 baseline and accounting | PASS within disclosed measurement scope | `reconstruction.json`: exact 77,893/78,435/93,334 joins, equal within-task before/after bytes; current metadata/heuristic partitions; frozen run04 workloads; historical time/I/O UNKNOWN. Exact historical task-read coverage remains UNKNOWN. |
| AC3 risks and architectures | PASS for scoped design assessment | Three materially different approaches in designs/threat model; journal trust, immutable-store prerequisite and full-pass fallback costs are distinguished. No signed manifest or ordinary metadata is presented as an unread-byte oracle. |
| AC4 material efficiency | FAIL | Full-byte mode saves 33.33% hash bytes, 0% unique reads and 29.60% historical time, with increased enumeration. Conditional mode exceeds 80% numerically but lacks equal readable-byte detection. W2 retains full checks. No waiver is assumed. |
| AC5 scientific and critical protection | PASS for tested scope | All 17 scientific and eight critical fixture identities hashed twice in every W1 arm; paired backup bytes validated. Sixty-four actual source inputs rechecked at reuse, extra D5G ledger checked from HEAD before parsing; unchanged actual protection helper before/after passes. No old PASS supplies an expected input hash. |
| AC6 adversarial qualification | PASS for declared conditional/default coverage | run04: 50 declared outcomes match; supplement01: ten outcomes match, including baseline-construction race and global post-pass detection. The modeled unjournaled counterexample exposes, rather than passes, the stronger protection gap. Independent execution is recorded separately. |
| AC7 durable/editorial delivery | PASS | Independent substantive review returns editorial ACCEPT for review01. Changed-text screen, complete manual coverage, source/result identities and exact patch checks pass. The final closure/provenance delta is separately reviewed. |
| AC8 independent disposition and packaging | PASS for review execution and packaging | Independent review01 returns REWORK for AC4, with all other criteria PASS within stated scope. It independently checks all snapshot/source identities, arithmetic, representative execution and both complete/task-only patches. This is an independently reviewed failure, not accepted engineering. Final closure delta is bound separately. |

The acceptance status of the optimization remains FAIL/REWORK even if the
remaining verification/packaging criteria pass. Independent review must not
return ACCEPT for this unchanged contract while AC4 is failed. A narrow
maintainer decision about an alternative storage guarantee or amended detection
scope is the remaining decision boundary, not permission inferred from this report.

## Actual preservation and authority

The initial tool-observed status contained only the supplied brief. The later
durable start receipt includes the first task-created research scripts; its
time and status are not relabeled as an earlier capture. The export baseline
records how those observations are combined. HEAD/index are rechecked without
staging. Source/navigation outputs are distinguished from preserved source bytes.

`protected-before.json` checks the unchanged save/content policy: 12,974
historical rows, 173 qualified active-transient exclusions and zero protected
changes. These are neither all active saves nor all 93,334 historical pins.
The full broad historical audit was not repeated for timing. The final actual
source/protection receipt is `reuse.json` with separate cost/row receipts.
Before/after protection takes 154.2483605 and 112.9727065 measured seconds
respectively; those are actual assignment costs, not original D5G timings or
synthetic W1 costs. Both receipts preserve zero protected changes. Index SHA-256
remains `a6ab45d30477b4a51503944691dd6b33daa755a3c8a5d8652c4f42a9cd5aa3bd`.

Scientific result is a positive journaled-change detection and cost measurement
plus a scoped negative equal-protection result for the tested design. Engineering
qualification is synthetic and incomplete against AC4. Target survival and
restoration are not applicable; no target was operated. Original evidence and
saves were never fixtures. No new outside implementation, permission request,
publication, B6, RG2-D5H or Git-write authority is introduced.

## Failures and finalization record

Failed volume/journal access attempts remain in run01/run02 and the method
account. Run03's 50 passing declared outcomes did not expose the independently
identified baseline race or per-category pass-ordering weakness. The corrected
global before/after sequence and initial-cursor fence are qualified in run04 and
supplement01; earlier receipts remain unchanged. A rejected editorial/package
attempt, if any, is retained with diagnostics rather than silently replaced.

The independent reviewer separately executes ten representative frozen controls
under its own fresh `independent01/` subtree: unchanged negatives in both modes,
timestamp-preserving same-size mutation, unexpected additions, manifest tamper,
conditional journal failure and unchanged full fallback. All ten match their
predeclared outcomes. It independently recomputes the cost arithmetic and
historical receipt identities; this is distinct from merely reading our results.

The supplied brief retains original endings/spacing. Authored numeric tables
receive schema/count/hash review; opaque hashes and identifiers are not prose
rewriting targets. The final manual reading covers every new document, changed
navigation/credit/source paragraph, table label and Python comment/docstring.
Independent exact-text reading is separate from an automatic zero-diagnostic
screen. Final local editorial/manifest records bind the actual covered files.

Review packages use `.local-work/diffs/preservation-<label>-complete.diff` and
`preservation-<label>-task-only.diff`. Complete includes the unchanged supplied
brief; task-only excludes it. The existing owned exporter verifies path coverage,
UTF-8/newlines/whitespace and local links, exact forward/reverse content in fresh
scratch trees, and reverse applicability against the actual tree without staging.
Ignored fixtures, raw manifests and inherited proprietary/save/database material
are excluded and enumerated or referenced in the exclusion manifest. Those
exclusions are not publication clearance.

Exact final completion file/patch hashes and the actual reviewer return are
retained in `.local-work/preservation-verification/` and the associated
`.local-work/review-deliveries/` package. Local delivery records avoid embedding
a self-referential final hash in authored prose. No acceptance of this audit
would authorize activation, integration, staging, committing or pushing.

## Independent disposition and final delta

The actual independent return is retained as `independent-review01.md` locally:
**REWORK — AC4 FAIL; editorial ACCEPT for substantive review01**. Its reviewed
snapshot SHA-256 is `c1c66c1799668e23afec543dd2577edd926373dedb2cd2b23116ad60fc2929f0`.
The reviewer independently verifies all 26 changed files, 80 source identities,
the 26-path complete and 25-path task-only patches, original receipts and cost
arithmetic, and executes ten representative disposable controls. It finds no
other material defect in that bounded substantive snapshot.

The final delta closes this record and makes one provenance correction: the
actually imported tungsten save-policy helper/JSON paths are exact-byte aliases
of the initially pinned Carinae copies, verified against the existing expected
hashes and HEAD at finalization. Their path checks were late and are disclosed;
the intake helper now includes both actual paths for future reproduction. No
protection logic, measured prototype, workload, result or original receipt changes.
`review02/` and `independent-delta02.md` bind this final delta. Overall disposition
remains REWORK, with the same unresolved comparable-protection AC4 threshold.
