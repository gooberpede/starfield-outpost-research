# D5BT qualification and review

Independent review02 returned **ACCEPT**. D5BT-Q1 through Q4 are COMPLETE and
AC01 through AC12 are PASS. The original [brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BT_Save29_and_Display_Reader_Qualification.md),
[active ledger](investigation-ledger.md), [source and input crosswalk](provenance.md)
and [5B-2 handoff](README.md) govern this checkpoint.

## Executed checks

| Check | Result and scope |
| --- | --- |
| Selected original executions | Save29 and HIST-0021 each exited 0 from the workspace and a source-only copy. Source pins, staged inputs, archive digests, header and decoded digests agreed. |
| Save29 cross-check | Both counted-extra walks agreed on ends 1299173, 1300186, 1300688 and 1301351 and cursors 28, 7, 10 and 10 respectively. The third row has 11 queued references. The old subset refused beacon ExtraBC. |
| HIST-0021 closure | 215,649 typed R3 records and all 43 type-6 sections framed. Nested section ordinal 38 contains the two selected rows. Both fixtures had zero stock, and each item had seven counted extras and reciprocal joins. |
| Independent byte oracle | A separate local `struct` walker exhausts both typed R3 regions, checks the eight selected REFR spans and footer types, and rereads the electrical words, flags and reference queues. Its type-6 walk independently traverses CTName, all 43 component sections and five pending-dialogue rows. All 43 boundary and count triples match the product reader. It also rereads both Nested rows, zero counts and backlink fields. Both walks use the owned BCPS decoder. |
| Control tests | Thirty-three selected and synthetic checks passed. They cover malformed count, length, queue, header, type, order, flags, stock, pending-dialogue and other component data. The helmet checks include a well-formed extra list missing Extra36, a wrong Extra36 target and a well-formed tag outside the selected subset. Two clean-copy CLI cases refused a wrong input and output collision. In-memory mutations were discarded. |
| Existing suites | 18 Workshop population and six R3 framing tests passed with CPython `-I -B`. |

The initial Python alias failed to start. The existing installed executable
ran all tests. Two HIST-0021 failures are retained in separate output directories.
The first reader assumed item counted extras consumed the entire REFR. A second
run measured the failing helmet cursor at 5861628. The pinned historical SD1
receipt independently records that exact cursor and a REFR end of 5861629.
The corrected check preserved the one-byte tail distinction and passed for both
items. These were engineering failures with no original-byte changes.

## Independent review and preservation

Review01 returned **REWORK** on manifest SHA-256
`df0bb127b1d0baeca0b7096e2aae9eaa55e4b765d624306a6c4c1bf5b4aff96b`.
It verified the 11 file pins and patch inventories, and challenged the
independence of the type-6 and typed-footer checks, the missing backlink
control, the display extra subset, the protection receipt and a broken
D5BR table. The resubmission includes a separate typed-footer and component
walker, stricter extra admission and targeted controls. The first independent
component walk omitted the two leading scalar values in section 26 and
failed the bounds check. That failure was retained and the corrected walk
matched the full section map. The D5BR note now follows the complete table.

Review02 accepted the substantive manifest with SHA-256
`3e69b8452a7158e202ab8fa218700329093355528c35c356d77ae56662d21042`.
The reviewer verified the exact tree and patch identities, primary receipts
and output hashes, 43 contiguous oracle boundaries, clean-copy exit profile
and the changed prose. The reviewer inspected the test and reconstruction
receipts without rerunning experiments or opening original saves.

The final original-byte qualification binds the pre/post selected archives,
staged members, historical components, project source, HEAD, index and status
with invocation, exit and output hashes in one local preservation receipt.
It records identical workspace and source-only selected JSON. The intake
observations captured HEAD and status. The first reliable physical index
digest was recorded after the initial tests. The preservation bracket covers
the fresh complete execution and does not reconstruct an earlier digest.

The changed prose review covered the D5BT Markdown, the D5BR note in context,
and the authored source comments and docstrings. The screen checks changed
text for common formatting defects. Manual reading checked table continuity,
identity domains, evidence limits and consistency with primary receipts.
The package checker covers authored UTF-8/LF, added-line whitespace and local
link targets. The supplied brief is verified against its original bytes.

## Applied reading

- Standing orders, README, workflow, charter, research state and the evidence
  and completion standards guided the frozen questions, isolated read-only
  scope, explicit identity domains, retention of failures and distinction
  between saved evidence and historical runtime authority.
- D5BR Stage 0/A3/A5, D5BF package/member records, D5BG selected claim, edge and
  action rows and D5BQ define exact inputs, evidence tiers and held routes.
  The D5BR note is forward-looking. Frozen claim and action files remain
  untouched.
- The Save29 authority, review and test plan supplied the four saved row
  oracles, ordinary assumptions, attributed base values and historic
  observation boundary. SD1 methods, source ledger, report, review and
  selected saved/instance receipts supplied the pending-dialogue branch,
  stock cursor and token/ownership joins.
- B0 and publication policy separate rights and release authority from
  engineering qualification. B3 separates source availability from a runnable
  method. B4/F1 and save protection require the exact immutable selected members.
  B5's scratch lifecycle and the editorial standard govern disposable copies,
  packaging and exact-prose review. No outside code, private receipt or installed
  game data is required to run the selected reader.

## Acceptance matrix

| Criterion | Implementer assessment |
| --- | --- |
| AC01 | PASS proposed. Applied reading and authority controls documented above and verified in review02. |
| AC02 | PASS proposed. Exact ZIP and SFS hashes, framing and build pins agreed. |
| AC03 | PASS proposed. Source-only positive runs and collision/input refusals. |
| AC04 | PASS proposed. Four saved ranges, graph, base and word rows checked. |
| AC05 | PASS proposed. Two counted walks, legacy failure and separate fixed-offset and refusal controls. |
| AC06 | PASS proposed. Attributed definition values and swapped-order result. |
| AC07 | PASS proposed. Typed section closure, zero stock, two item joins and distinct ownership lanes. |
| AC08 | PASS proposed. Independent typed and section walks, targeted malformed controls and fail-closed extra subset. |
| AC09 | PASS proposed. Owned source and import closure documented with source-only replay. |
| AC10 | PASS proposed for the fully bracketed qualification. The intake digest limitation is documented above. |
| AC11 | PASS proposed. Screen, manual prose read, links, text encoding and complete/task-only exact reconstruction. |
| AC12 | PASS. Review01 returned REWORK. Review02 accepted the corrected substantive snapshot. |

Primary receipts are in the ignored D5BT working directory. The complete and
task-only patch manifests, status and exclusions are in the ignored review
delivery. The original brief is included byte-for-byte in the complete patch.
Scientific result is the existing saved-state tier with local reproduction.
Target survival is inapplicable. Publication remains NOT READY / NOT CLEARED.
