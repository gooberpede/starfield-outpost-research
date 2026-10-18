# Historical saved instances and the missing crew control

**2026-10-18 corrective continuation:** [Current saved assignments](current-assignments.md)
now demonstrates reciprocal actor4C/outpostE2 relationships in HIST-0021/22/24/0255 and three positive saved available-roster actors.
[Rework review and exact package](current-review.md) controls this continuation.
The initial CR1 observations and review below are retained as the earlier snapshot;
its missing-positive-assignment boundary is superseded for the new positive subset.
Real saved unassigned-roster inputs are now qualified; universal post-load authority remains OPEN.

Primary fresh receipts: `.local-work/cr1-crew/{Save52,HIST-0036,HIST-0077}-crew03.json`,
save-joins01.json and placed-definitions01.json. All offsets below are **decimal
decoded logical-stream offsets**, unless explicitly called original ESM offsets.
No offset is a runtime VA. Authored REVIEW-REQUIRED; raw saves/decoded bytes LOCAL-ONLY.

| Input | SHA-256 | Closed ordinary beacon extras | E2 extra in those beacons |
|---|---|---:|---:|
| Archived Save52 | See source pin in save-joins01.json and sources.csv | 19 | 0 |
| HIST-0036 | `7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37` | 19 | 0 |
| HIST-0077 | `3830eb374f086bece85ca3e92ff2d13a3d5aa811193f0c2e583c4564000551bc` | 16 | 0 |

These are different existing observational saves, not three independent controlled
assignment trials. Every listed beacon's declared counted extra list closes after
the Workshop payload, using the existing owned grammar extended to E2. There are
also zero queued CrewAssignment-key mentions in these selected R3 scans. This is
useful scoped negative evidence. It is not proof of zero ship crew, zero recruited
crew, no default/alternate links or universal absence of assignment state.

## Positive station and owner joins

Fresh bytes reproduce 17 ordinary station roots in Save52. Each positively joined
root has physical base `starfield.esm:015804`, ExtraDA construction identity
`starfield.esm:299f59`, and exact Extra4C keyword `starfield.esm:054ba6` pointing
to the owner's ordinary beacon record. [stations.csv](stations.csv) records all
17 roots, exact owner-link offsets, historical disabled/deleted bits and the
owner's saved slot value. Prior Workshop population results supplied leads only;
the new joins reread the protected original.

| Example | Saved identity and offset | Positive association |
|---|---|---|
| First station root | `DYNAMIC:ff01fa66`, record 3164543; owner-link mode byte 3164683 | Construction 299f59; owner `DYNAMIC:ff01a75b`; disabled/deleted clear. |
| Contributing sibling | `DYNAMIC:ff01fa65`, record 3164394 | Same construction and owner; BF base CrewSlots 1 at 3164515. |
| Root stamped property | `DYNAMIC:ff01fa66`, BF 3164658 | Base CrewSlots 1, with separate CrewRating and dummy/event properties. |
| Exact owner | `DYNAMIC:ff01a75b`, BF 2924887 | Saved base CrewSlots 2. Its closed extras have no E2 list. |

All 19 ordinary Save52 beacon base-slot observations are 2. Seventeen explicit
station roots do not prove exactly 17 stations, nor explain every beacon's
construction history. The separate two-beacon root gap is retained. A station
base value, a historical constructed root and a current effective capacity are
three different evidence claims. No power/arrival/current-bonus observation follows.

## Named and generic identity evidence

Fresh installed ACHR NAME records join Lin `00005639` to NPC `00005638`, and
Heller `0000563c` to `0000563a`. Their original ESM record offsets are respectively
203652488 and 203652354. Historical R3 records with those exact ACHR identities
exist in both HIST-0036 and HIST-0077; the named-base NPC change records also occur.

The original reference-prefix attempt is **not a qualified actor decoder**. It
could even consume an ACHR prefix and pass a self-token check while reporting
`01054c` as a spurious base and implausible saved flags. Receipt03 excludes all
such actor/NPC interpretations. Keep receipts01/02 as failed method history.
Exact record identity plus installed NAME establishes the named actor/base join;
the rejected decoded base/flags/XYZ establish no actor semantics.

A created `DYNAMIC:ff03c141` record queues generic base/template leads
`0026f937` and `0002e91c` in Save52. This is a positive queued association to an
Engineering Specialist definition, **not** a qualified actor-reference/assignment
join. No Management Specialist instance or saved active skill rank was qualified.
The initial generic record prefix result is likewise excluded. A queue hit is not
a current hire state, owner link or proof that a specialist contributes.

Consequently actual historical recruitment availability, assigned ship/unassigned
roster, persisted added perks/ranks, pending aliases and post-load physical presence
remain unqualified for these actors. Missing ordinary change records must not be
converted to false/empty fields. The [runtime/save matrix](lifecycle.md#persistence-classes)
states exactly which paths are definition-derived, persisted-capable or reconstructed.

## Narrow missing control; proposal only

The bounded corpus gap is an actor with an independently recorded crew identity
and a known assignment transition, paired with the exact owner and save provenance.
The smallest later acquisition is a protected-copy baseline/no-action save plus
one same-session successor after assigning one identified named recruit to an
identified ordinary station-bearing outpost. Record the Crew row and owner IDs,
current slots, actor identity and loaded/pending conditions, then make a no-action
successor if timer/script churn matters. A named actor avoids generic unload deletion.

To distinguish generic retention from assignment, a separate generic actor control
would compare hired-unassigned before and after unload; it is not interchangeable
with the named assignment pair. Reload authority and physical arrival would need
their own observations. This proposal creates no gameplay save, launches no game
and grants no live/observer/save-writer authority under CR1.
