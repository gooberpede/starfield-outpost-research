# EXP0002 — primary manual checkpoint research path

SOR-D-0021: live outpost observation and differential saves are primary supported methods. Native save automation is optional and does not block this plan. This is the proposed first resumed outpost experiment, not a claim of new construction/captures or authorization to deploy an observer under the final debugger task.

Use a fresh run/session namespace and retain the existing EXP0002 aliases. User shorthand B0/B1/B1C maps to **A0/A1/A1C**; these do not overwrite review 14's historical A0/A0C or allocate new sample IDs before saves exist. Retain a fresh A0C no-action baseline if feasible to estimate baseline churn independently of beacon placement.

| New-run checkpoint | Controlled action | Evidence |
|---|---|---|
| A0 (B0) | Load pristine Save3; confirm no outpost; remain stationary | Live baseline, wall-clock timestamp, manual new-slot save |
| A0C | No deliberate change; matched short interval | Live control checkpoint and manual control save |
| A1 (B1) | Place exactly one outpost beacon | Immediate live state, timestamp, manual new-slot save |
| A1C (B1C) | No deliberate outpost change | Live control checkpoint, timestamp, manual control save |

Exit normally, complete Steam sync, inventory and copy all relevant saves into a fresh ignored archive, verify source/copy/source SHA-256 and sizes/times, and recheck protected Save3/backup. Correlate each checkpoint to its exact new filename; retain incidental exit saves separately. Do not overwrite or relabel old evidence.

Stay stationary where practical, avoid wait/rest/travel, retain already-disabled autosaves, log incidental movement/combat/time and every deliberate transition. A0→A1 alone does not isolate beacon bytes: compare A0/A0C and A1/A1C churn, use repetition for important transitions, and keep unknown differences unclassified. No-action controls are not claims that every background system was static.

Live priority: identify the beacon reference and cell/worldspace/position identities, then determine membership/GetWorkshop with a separately justified safe query mechanism. Prior AddTask thread variability remains a limit; do not make unqualified native calls or gate basic beacon/save evidence on solving native saving. Prefer the least complex appropriate SFSE observer/API, static Ghidra, xEdit or targeted debugger method for each concrete question. Observer 0.1.0 deployment/profile validation is separately reviewed; Vortex/SFSE rules apply to observer work, not the plain-Steam final save trace. Reuse only already-qualified non-invoking reads until native-query safety is established.

Offline priority: no-outpost→beacon-only; then beacon→one ordinary storage object; then extractor plus required power; then output link to storage. Later bounded transitions include rename, move, deletion, cargo links and resource/output state. One deliberate transition per comparison, appropriate no-action controls, consistent provenance. Live and save tracks remain independently useful even before their identities/fields can be correlated. No production parser/importer or generalized framework is implied.
