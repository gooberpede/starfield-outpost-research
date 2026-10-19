# Saved counters and targeted construction contrasts

[Answer](report.md), [native model](native.md), [review](review.md).
All save offsets below are **decimal decompressed logical-stream offsets**.
Saved identities, current FormIDs, native handles and pointers remain distinct.
The saved build/header is not proof that every historical definition/setting
matches the present installation. No save was loaded or edited.

## Kreet controls

Fresh scans use all 17 hash-matched copies from the accepted
[manual S0-S7C corpus](../manual-save-corpus-S0-S7C.md), not similarly numbered
unrelated saves. [Prior root correspondence](../workshop-membership/report.md)
establishes the actual beacon/storage/extractor/solar actions and adjacent
controls. Source IDs are SOR-SAMPLE-0006 through 0022; the existing
[manifest](../manual-save-corpus/manifest.csv) supplies full original/copy hashes.
New `save-<label>.json` receipts independently verify those copy hashes and typed
record/extra framing. The historical active-save filenames are absent at their
old Saves paths; all 17 archived copies match the original manifest. Nothing
was silently replaced, and no new observation of those unavailable originals
is claimed.

The beacon `ff022c5d`, base `002c60e9`, has a closed ExtraBF base section with
AV **00000399** and one explicitly stored float in all 15 positive samples.
Its modifier section contains no entry for that AV in these records. The native
registry/loader, not the token's spelling, identifies WorkshopCurrentBudget.

| Sample(s) / sample ID | Supported action/state | Stored base U | Exact float offset, action / control |
|---|---|---:|---|
| S0/S0C / 0006-0007 | Before beacon | UNKNOWN / no beacon record | Not a serialized zero |
| S1/S1C / 0008-0009 | Beacon only | 7 / 7 | 1295916 / 1296522 |
| S2/S2C / 0010-0011 | Add solid storage | 8 / 8 | 1297992 / 1297602 |
| S3/S3C / 0012-0013 | Add Iron extractor and solar together | 10 / 10 | 1298279 / 1300997 |
| S4/S4C / 0014-0015 | Output link | 10 / 10 | 1299585 / 1298829 |
| S5/S5C / 0016-0017 | Rename, with incidental player movement | 10 / 10 | 1299971 / 1298332 |
| S6/S6C / 0018-0019 | Move solar | 10 / 10 | 1300071 / 1299654 |
| S7/S7C / 0020-0021 | Remove extractor, possible link cleanup | 9 / 9 | 1297629 / 1297586 |
| exit / 0022 | Incidental terminal snapshot | 9 | 1297614 |

These are saved values, not a screenshot meter measurement or runtime
effective-value query. No-action controls permit ongoing simulation; fauna
combat timing in this corpus remains qualified by the original report.
S3's +2 is a joint action, not independent experiments for each object.
The separate S7 -1 and direct storage +1 help discriminate the native model.

With the **conditional current-definition operands** baseCost=1, four GMST
surcharges=0, multiplier=1 and effective M=2500: ordinary storage predicts +1;
Iron/solar together predict +2; extractor deletion predicts -1; position/link
changes predict no added construction charge. These agree with the bytes.
Beacon-only U=7 is observed, rather than calculated from a guess that the one
PackIn root costs one. Native assembly summation explains multi-unit charge;
the sample's seven saved PackIn members plus foundation are not automatically
eight billable references. Exact loaded member/default eligibility was not
captured, so no missing member's cost is fabricated.

The native BF writer/loader persist the base section with one mask bit per AV
and nondefault float; the second section has three modifier bits per AV.
`1419aec20/1419aeff0` and base upsert `1419af7c0` give the independent wire
contract. Fresh primary float reads and queue/record bounds are checked by
[verify.py](../../../research/build-budget/verify.py). Equal serialized base
values do not prove identical effective loaded U or immediate HUD refresh.

## Direct object, assembly, hab and robot

| Witness | Actual definition/representation | Supported budget conclusion |
|---|---|---|
| Kreet solid storage | CONT `0023aed9` OutpostStorageSolid01Sm; direct single item | Reference/form lookup, base1 plus container term times installed0; observed +1 |
| Beacon assembly | PKIN `0029a8c6`, ACTI `002c60e9`; qualified dummy/constituents, not eight independent constructions | Member sum; observed total7. Root count1 differs from U7 |
| Ordinary furnishing | FURN `001ea29d` Chair_Generic01_Free; Save52 `ff01fa5b/5c/5d` are three separate accepted single roots | Same form/properties uses same charge inside/outside. Positions do not enter calculator; no hab trial or exact room join is claimed |
| Garden robot | NPC_ `0004297c`, COBJ `00042980`; real HIST-0255 actor `ff021b88`, owner `ff038542` | Direct actor representative enters single-item budget independently of robot JNAM quota; conditional default charge1 |
| Model A03 robot | NPC_ `001d924e`; real HIST-0255 `ff07258a`, owner `ff062012` | Same construction route; its power perk does not exempt it from the budget |

Furnishing provenance uses accepted [additional population roots](../workshop-population/report.md).
Robot identity/owner/assignment provenance uses the independent
[R1 instance ledger](../robots/instances.csv) and [lifecycle](../robots/lifecycle.md),
not proximity or robot names. The current definitions are reread as targeted
physical records. The form calculator has a literal type4b actor surcharge
branch, but effective-base resolution can supply an NPC_ form instead. Do not
call that branch an extra robot fee from its label; the installed surcharge
is0 in either case. A damaged/unassigned robot's operating contribution is
separate from construction ownership and its persisted budget history.

Fresh HIST-0255 beacon owner `ff038542` stores U=556 at6344232, and owner
`ff062012` stores U=249 at7831298. These are mixed mature outposts, **not**
before/after robot placements; no per-robot delta is extracted from them.
All 17 positive beacon records in that input and all19 in HIST-0267 have
explicit current-budget base values. Corpus receipt hashes pin the originals.

Hab interiors do not receive a position/occlusion discount in the traced
same-input cost function. Native operands include the actual selected effective
form, marker/model eligibility, collision-helper keywords and configured
properties. An assembled hab can cost more than a chair because it has several
eligible members. Its specialized interior collision primitives can be excluded
by their own marker/property route; that is not a discount for ordinary
furnishings located inside its room. The two retained ambiguous historical hab
groups in EXP0033 still lack construction-origin/ordinary-owner proof. They are
not promoted into a new budget inventory here.

## Persisted history is not a population oracle

Save52's historically disabled beacons `ff01b58f` and `ff0483f2` retain U=310
at3022948 and U=198 at5378142, despite zero surviving direct Workshop edges in
the accepted saved-owner ledger. This is an important counterexample to
equating the scalar with a fresh root census, to inferring zero from empty
links, and to treating a nonzero counter as proof of an active outpost.
It is not evidence of a budget bug or historical cause of disappearance.

The ordinary cost consumer reaches selected item members. It does not enumerate
surrounding procedural rocks/plants by spatial extent or subtract their
rendered occlusion when a hab is placed. If an environmental reference actually
enters that selected construction representation, the same eligibility/cost
contract applies; no universal exemption for every natural object is asserted.
Suppression, clipping, collision and later reappearance remain L3.

Current effective max/usage, actual historical load-order overrides and the
screenshot epoch remain UNKNOWN. A safe reconstruction uses the persisted
counter and native restoration, rather than inventing exhaustive membership or
declaring absence of a saved field because a search failed.
