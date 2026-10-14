# Review return and deliverable inventory

SOR-EXP-0025 / SOR-EV-0033, 2026-10-11. [Answer-first status](README.md),
[exact contracts](contract.md), [qualification/failures](qualification.md),
[prospective card](operator-card.md). Critical review is required before
integration, any live experiment or publication.

New source files under `debugger/event-oracle/`: adapter, original C++/MASM
fixture, qualification/build runner, local health controls, offline inspector,
inspector tests and source/effects README. New authored documents are the five
files in this review directory. Existing root/state/decision/provenance/source/
credit, experiment/evidence/brief indexes, function/state/subsystem records and
two historical acquisition contracts receive linked supplements. WORKFLOW gets
the requested standing review-diff convention. No rename/deletion. The supplied
brief was initially untracked and is included only in the complete patch.

Local review files:

- [Task-only patch](../../../.local-work/diffs/event-associated-oracle-instrumentation-task-only.diff).
- [Complete patch including supplied brief](../../../.local-work/diffs/event-associated-oracle-instrumentation-complete.diff).
- [Git status](../../../.local-work/event-instrumentation/review-01/status.txt).
- [Changed-file/exclusions/checks manifest](../../../.local-work/event-instrumentation/review-01/review.json).
- [Independent coverage/timing checks](../../../.local-work/event-instrumentation/review-01/coverage.json).
- [Versioned candidate/review ZIP](../../../.local-work/event-instrumentation/review-01/SorEventOracle-0.1.2.zip).
- [ZIP hash/member manifest](../../../.local-work/event-instrumentation/review-01/package.json).

Patches contain all current tracked edits and untracked text files with valid
Git-style new-file hunks; no staging is used. Review construction checks exact
path inventory, reverse applicability, and an independent forward application
to HEAD text in a new ignored scratch directory, then byte-compares the result
with the actual working tree. Whitespace/newline and changed Markdown local-file
links are checked. Link existence does not validate Markdown anchors or web
sources. Manifests identify new scripts/docs, tracked edits, supplied material,
renames/deletions and excluded ignored/binary/raw material separately.

The versioned ZIP contains the original external adapter, all changed/new
authored source/docs and supplied brief, GPL text and selected non-raw build/
qualification/preservation/provenance/check receipts. Its member list/hashes
are outside the archive in package.json. Proprietary executables/assets, raw
saves/decompressed saves, raw memory/fixture sections, Ghidra exports/databases,
Vortex content and compiler intermediate objects are excluded. This is an ignored
local review artifact, not cleared publication. Original game/SFSE package
ownership remains with Vortex; the external tool has no game payload and no
SFSE export/version change. The justified architecture/deliverable variation and
different smoke/preflight sequence explicitly await review under brief section 7.

Provenance remains mandatory despite maintainer-owned reuse permission. Existing
project readers preserve SOR-S-0132/SOR-P-0002 provenance; consulted sibling
repository paths/revisions/file hashes and Microsoft API consultation are recorded
in SOURCES/CREDITS and the local source receipt. No new third-party implementation,
licence acceptance, upstream contact, fork/PR, dependency download or disclosure.
No permission issue blocks this performed offline/disposable scope. Live work,
publication and integration remain independently gated. Frozen model and historical
evidence are preserved; no semantic finding is silently promoted.

Suggested commit subject only after review:

```text
research: implement event-associated workshop and terrain-grid oracles
```
