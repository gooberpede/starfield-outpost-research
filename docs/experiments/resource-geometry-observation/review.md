# C1 acceptance accounting and delivery

[Original frozen AC1–AC8](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_C1_native_region_observation_feasibility.md`).
This is an offline feasibility assessment; live qualification/native equality
are NOT TESTED and are not requirements silently relabelled PASS.

| Criterion | Implementer status / primary evidence |
|---|---|
| AC1 | PASS: start.json HEAD/index/status, installed EXE and26 protected file pins; postflight verifies equality and disk guards. Offline read/write scope only. |
| AC2 | PASS: acquisition.md bounded named families and exact gaps; evidence.json native/raw source hashes; inherited ledgers and point-of-use links. No new external material. |
| AC3 | PASS: native-contract.md producer/consumer/static address domains, minimal typed schema, coordinate conversions and explicitly named ownership/placement gaps. |
| AC4 | PASS: native-contract.md coherence/ABA/per-use/epoch requirements and stability.md causal controls. No invented native epoch counter. |
| AC5 | PASS: cases.md positive saved joins and exact witnesses for four distinct cases; cards.md comparison order/optional stability design. |
| AC6 | PASS for bounded negative feasibility: acquisition.md actual prior failures/alternatives and missing qualification; cards.md prospective actions, preservation/STOP and replay. No live readiness asserted. |
| AC7 | PASS: report/native-contract/stability/cases/acquisition/cards, source metadata and historical backlinks; frozen predictions preserved. |
| AC8 | Independent substantive ACCEPT; exact-final accounting confirmation required in the local final review receipt. Package verification covers all12 complete/11 task-only paths, exact forward/reverse application and actual-tree reverse. |

Local evidence root: `.local-work/resource-geometry-observation/`.
`start.json` captures initial HEAD `16a7b439d084f244f26c4936a97274a85cab32a2`,
index hash, only the supplied untracked brief, both disk guards and protected pins.
`evidence.json` records197 hash pin occurrences/161 unique paths plus seven
literal native locator assertions. These are integrity/locator checks, not197
semantic tests. No new synthetic or native runtime tests were run: this task
changes documentation and runs read-only preservation/source/package checks.

Local original helpers `rg2c1-start.py` and `rg2c1-evidence.py` read named
repository records, source/raw receipt inputs and installed EXE, hash via stdlib,
and write ignored JSON receipts only. They do not decode saves, execute native
tools or contact a network. Existing project-owned `research/review_package.py`
reads HEAD/current text and the start receipt, writes ignored diffs/manifests and
forward/reverse scratch trees under `.local-work/review-patches/`; its scoped
scratch cleanup and Git ceiling follow WORKFLOW. No staging/index/ref mutation.

Complete patch includes the supplied untracked brief unchanged; task-only
excludes that input. Both include every authored changed/new text file.
Exact paths, hashes, changed-file/status inventory and forward/reverse verification
are in `.local-work/review-deliveries/rg2c1-final02.json` and adjacent status file;
patches `.local-work/diffs/rg2c1-final02-complete.diff` and
`rg2c1-final02-task-only.diff`. Later reviewed revisions, if needed, use new labels
and preserve earlier attempts. These are local paths, not publication links.

Exclusions: all `.local-work` raw/private data, saved source/decoded payloads,
native TSVs, installed EXE/ESM, databases, prior observer artifacts and scratch
are excluded from authored patches. Exact selected source locations/hashes are
in evidence.json; no binary/proprietary payload is promoted. Local helper/check
outputs and review receipts are excluded as operational evidence and listed in
the local package receipt; the supplied brief is separately identified as input.
No claim that every ignored file in the repository was newly audited.

Scientific outcome: completed bounded design with no currently qualified coherent
capture route in inspected evidence; IL/Iron unresolved, Copper conditional
positive. Engineering: design only, observer/lifetime/retirement unqualified.
Target survival/rollback: not applicable, zero target operations. Authority:
offline only, no commit/push/publication or installed-file change. Independent
review and maintainer integration remain distinct.

Preserved attempts: an initial `rg --files` call used unsupported wildcard
directory arguments and returned a locator error; explicit inventory corrected
it. Several combined tool outputs were truncated, followed by focused reads.
Neither was used as scientific absence evidence. No failed live or synthetic
experiment was performed in C1.

Independent substantive disposition: **ACCEPT**, original AC1–AC7 PASS; AC8
final accounting remained NOT TESTED at that return. The actual return is retained
in independent-review01-message.md under the local evidence root. Reviewer
independently checked197 evidence pins/161 paths,26 protected pins,12 package
file hashes,2 patch hashes,4 tracked diff sections and all new-file payloads,
12/11 complete/task inventories,2 actual-tree reverse checks,39 local links,
three named receipt structures, critical native consumer/provider/gate/destructor
windows and one raw manager header. No substantive defect was found.

Exact-final disposition in independent-review-final.md under the same root
controls acceptance of this accounting update and final02 manifest, including AC8.
The final response reports it only after it exists. A final rejection requires
REWORK/repackaging, never a presumed PASS. Subsequent authored changes require
re-review; no integration, C2, staging or publication permission is supplied.

Actual postflight01.json records223 unchanged hash comparisons (26 protected plus
197 source occurrences), unchanged HEAD/index, both disk guards PASS and whitespace
PASS. operations01.json additionally verifies Save51/52 against the D1 ledger and
lists local operational files/exclusions; tools01.json pins Python3.14.3 and the
owned exporter with Git2.53.0.windows.1. The local postflight helper reads those
protected paths/HEAD/index and checks hashes/space/whitespace, writing only its
ignored JSON. Inventory/version one-liners likewise write ignored metadata only.
No live, native-runtime or new synthetic tests were executed.

Final01 confirmation found one encoding defect in this accounting file: a UTF-8
en dash was read through the Windows default code page. Explicit UTF-8 corrected
it before final02; the failed confirmation is retained in encoding-rework01.md.
The primary design and all frozen inputs were unaffected.
