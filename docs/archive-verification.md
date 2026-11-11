# D5BZ first-release archive verification

Edition **D5BZ-1** was sealed on 2026-11-11 (Australia/Sydney).
Publication remains **NOT READY / NOT CLEARED**.

The [external container manifest](archive-containers.json) has SHA-256
`2250f90eb90a691070b0a383b19bc58e57ede670b94e2ee9828c4ed3b422c4f6`.
It binds the two ZIPs, their adjacent indexes and READMEs, the build
method and the current source edition. The archive members carry no final
container or attestation hash.

| Archive and index | Members | SHA-256 |
| --- | ---: | --- |
| [Audits](audits/README.md) | 335 | `9f263e9a1676c2b79fba66bbf0aea0567aa02210a8a24998ef290a83cc4ab322` |
| [Implementation briefs](implementation-briefs/README.md) | 259 | `08987ed5f786da77085229e450ba02df0d6c7badd6c5532ffa46aed7de5d7433` |

The 594 members reconcile 588 intake files and six pre-seal records. The
originals of both replaced READMEs and the supplied governing brief are
members. The brief has 27,209 bytes and SHA-256
`ac9fc4e4e95d4c3fc2fa60d061062a7fc18c2df0bdf7375e10c17b8bb637c706`.
Each archive root has three files: its README for lookup and extraction
instructions, its machine-complete member CSV, and its ZIP. The external
manifest and this verification record hold container identities and review
outside the archives.

The CSVs record original path, byte size and SHA-256, intake Git blob where
applicable, classification, current authority and active destination. The
[current source edition](../research/evidence-data/README.md) records
relocated and changed source hashes. The pre-seal migration, evidence-access,
review, reading, journey and ledger records can be found by searching
the audit index for D5BZ. Their original paths are in the external manifest.

## Verification from the candidate

From the repository root, use Python 3.14.3 with zlib runtime
`1.3.1.zlib-ng` for the byte-for-byte compressor comparison. Give the
builder a fresh, caller-owned scratch directory. It verifies and extracts
both indexes and ZIPs, rebuilds, and compares both ZIPs, indexes and READMEs.

```text
python -B research/archival/archive.py rebuild docs NEW_DIRECTORY
python -B research/archival/verify_navigation.py
```

Final seal checks compared every member to the original or frozen pre-seal
source bytes, extracted both sets under exclusive roots, rebuilt the archives
deterministically, and reconciled the two actual archive directories.
Git HEAD, tree and the Git index match the intake receipt. The method
and asset validation paths remain in the current evidence source edition.
All eleven supplied evidence input identities used across the Workshop,
Cargo, N2 and D5BF batches matched before and after. Workshop and Cargo
matched their accepted historical receipts byte for byte. No game process
or native fixture ran. Local test inputs and outputs remain in private
custody. No release operation was performed.

## 7C and B6 handoff

- 7C needs the exact proposed checkout and refs, full reachable-history
  inventory, and exposure assessment of the two ZIPs and every member.
  Include private path metadata, embedded third-party material and
  game-derived data alongside the loose tree.
- Bind the seven candidate and two supplementary assets, member pins,
  exact lawful access route, named custodian, retention and transfer
  authority. Review the exact save, screenshot, projection, Workshop and
  Cargo disclosure surfaces under their existing decisions.
- B6 requires separately authorized isolation with the frozen source,
  approved supplied inputs and documented verification receipts. Check
  actual rendered diagrams, asset/member hashes, method scope and refusal
  cases, and the conditional D5AG host and lawful exact-file availability.
  Keep unselected and historically attributed routes at their stated tiers.
- The [publication run card](PUBLICATION_RUN_CARD.md) retains separate
  candidate freeze, independent preflight, hosting and final authorization
  checkpoints. A later authorized download check must bind actual served
  bytes, members, tag and final exposure to the approved candidate.

## Initial independent post-seal review

The independent reviewer returned REWORK for the index displaying the first
D5BZ pre-seal review disposition while the member also recorded the later
scoped ACCEPT. The reviewer independently checked all 594 source, ZIP and
extraction identities, the exact physical roots, the active source
identities, the Workshop and Cargo results, the tracked examples, graph
controls, navigation and both binary patch inventories. Q1 and Q2 were
COMPLETE. Q3 and Q4 remained INCOMPLETE. AC08 and AC10 failed on the stale
status. AC05 and AC12 awaited the external attestation and acceptance.
The reviewed container manifest was
`04cf1d441ab67f34064da29aa4e6460a1435a421cbe4c2034dfca05b8966d4cf`
and the reviewed delivery manifest was
`6952943b044dcf84990f44cb9e827635ac3f5b7edb8789a62b01d061811ffde2`.

The regenerated index surfaces the final explicit scoped disposition.
D5BZ lookup now returns ACCEPT for pre-seal review. D5BX retains its local
qualification scope and D5BY retains its final ACCEPT. Both ZIPs and both
READMEs matched the first sealed bytes. The regenerated indexes,
builder identity and updated external container manifest passed rebuild.
The first binary patch count matched a historical line containing the
diff header string. Restricting the check to actual line-start headers
resolved the count without changing the patch generator's payload.

## Independent post-seal attestation

**Disposition:** ACCEPT for the corrected substantive D5BZ migration.
The independent reviewer marked D5BZ-Q1 through Q4 COMPLETE and confirmed
scientific fidelity, engineering evidence and editorial conformance. The
review covers both ZIP identities above and the final container manifest
SHA-256 `2250f90eb90a691070b0a383b19bc58e57ede670b94e2ee9828c4ed3b422c4f6`.
The reviewed substantive delivery manifest SHA-256 was
`4fbdce15cc93c5656788a0638e22b55956072eca49611a55b882b9ff5e1cec17`.
The final export adds only this attestation to the reviewed candidate.
Its separate local delivery manifest binds the final patches without a
recursive digest in this document.

| Criterion | Independent result |
| --- | --- |
| AC01 | PASS. Applied controls, protected input receipts, Git identity and sequential reviews verified. |
| AC02 | PASS. Exact reconciliation of 588 intake files and six pre-seal records. |
| AC03 | PASS. Both physical roots contain exactly the named ZIP, README and index. |
| AC04 | PASS. All 594 member bytes, source identities, extraction receipts, adverse controls and rebuild outputs verified. |
| AC05 | PASS. The governing brief and six pre-seal records are exact. The nonrecursive container manifest and attestation bind the post-seal review. |
| AC06 | PASS. Active operand identities, isolated reader sources and Workshop and Cargo historical receipt equality verified. |
| AC07 | PASS. RC1, the selected reader journeys, negative findings and historical scientific limits retained. |
| AC08 | PASS. Exact historical paths, fragments, subject, ID and scoped final verdict lookup checked. |
| AC09 | PASS. D5BG, D5BR, D5BV, B3 and asset joins validated. Historical and technical catalogue editions retain their distinct pins. |
| AC10 | PASS. Current navigation passed across 671 pages, 8,365 links and 17 structurally checked flowcharts. Actual rendering remains a B6 check. |
| AC11 | PASS. Both local binary patches cover the same exact net tree across 1,275 paths. Forward and reverse byte reconstruction and actual-tree applicability were verified. The supplied brief has no loose final path and its exact bytes are in the brief ZIP. |
| AC12 | PASS. Separate independent pre-seal and post-seal ACCEPT dispositions and the 7C/B6 handoff are recorded. |

The final complete and task-only patches and their manifest are in ignored
local review storage. Publication remains **NOT READY / NOT CLEARED**.
