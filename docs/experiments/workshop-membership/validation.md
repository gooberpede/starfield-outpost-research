# Validation and actual evidence receipts

2026-10-14. Final extraction: `.local-work/workshop-inventory/final05/`.
Final validator: `validation04/receipt.json` and `owner-context.json` in the same
evidence root. Earlier runs remain retained; only final05 is the final detector
snapshot. [Schema/commands](schema.md), [scientific limits](report.md).

| Check | Actual result and limit |
|---|---|
| Qualified corpus | 27 labels, 26 unique archive hashes; manual 17,link 7,mature 1,two-outpost2. L0 reuses S4C. |
| Primary record walks |755,559 R3 records across labels, 205,557 in Save52; exact region closure and separate arithmetic framing agreement for every save. Shared decompression/directory readers are not an independent whole save parser. |
| Determinism | Detection repeated against primary decoded bytes for each label; identical result objects before metadata attachment. Source/script/input pins retained in final05/reproduction.json. |
| Controlled construction counts | S0/S0C0;S1/S1C1 beacon;S2/S2C2 with storage;S3–S6 and controls 4 with extractor/solar;S7/S7C/manual exit 3 after extractor removal. Root identities/base/owner/kind stable across manual controls. |
| Link controls | All seven labels 4 roots; L1/L1C and L2/L2C identities/owners stable. L0→L0C crosses reload, so raw token equality is not imposed. |
| Two outposts | Save25/26 each 2 roots, 2 owners, 8 direct members per owner; no nearest-beacon assignment in the reported continuous landing area. |
| Synthetic/adversarial tests |61 PASS across inventory 35, extractor 11, record framing 6 and membership 9. Includes mixed explicit non-REFR decoy through audit, truncations, duplicate types/bases/owner records, conflicting/null/missing owner, identity-domain collisions, unknown names, historical flags, trailing DA/80/9C, opaque 57, BC/CA/DE/30/96 branches, missing foundation target and 80 foundation ambiguity. |
| ESM context | All 38 installed ESM header censuses; initial 245 identities replay exactly, expanded 278 includes compound PKIN definitions. Every final root has uniquely resolved optional EditorID/type; detection is independent of names. |
| Prior extractor comparison | All 63 recognized prior extractor references match the current decoded ordinary owner and single-root role. These selected objects are not a full construction oracle. |
|17 outside-base leads | All 17 are recognized ordinary beacon records with self-owner edges and saved-disabled clear, not extra extractor/fabricator rows. Native BC resource queues explain why they mention extractor definitions. |
| Comparative network |17 saved-active beacon context names match the previously maintained JSON; earlier cargo count/topology checks remain attributed EXP0006 evidence. No new all-furniture/category or full construction count is asserted from that JSON. |
| Preservation | All 26 qualified archive hashes checked before/after; 38 ESM sources before/after; 16 database/executable pins match baseline; 60 sealed 050 evidence files and 3 frozen input/prediction/model hashes match prior seals. Validation rehashes its input pins after checks. |

Expected construction actions come from the independently authored
[manual brief](../../implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md),
not detector-generated expectations. Native representative selection and ESM
templates supply another evidence path. The selected prior resource/network
comparison is independent context with explicitly limited coverage.

## Save52 accounting

| Population | Count |
|---|---:|
| Direct WorkshopItem member records |8,628|
| Assigned to ordinary saved owners |8,627|
| Supported construction roots |657|
| Single roots |462|
| Compound PackIn roots |195|
| Qualified generated PackIn members |5,496|
| Generated foundations |2,282|
| Unresolved direct-member roles |193|
| All other R3 records, retained as possible-missed |196,929|
| Ordinary beacon owners |19|
| Saved-disabled clear owners |17|
| Saved-disabled set historical owners |2|

The five root/member roles sum exactly 8,628. Unresolved roles: 191 omitted
ExtraFlags/default-unknown references; one alternate 80 beacon context; one
nonordinary owner target (`81fdaa`→`DYNAMIC:ff028246`, definition context ship
decoration terminal). It is retained, not reassigned to a nearby outpost. All
8,628 member extra lists close after adding the native four-byte 57 branch.
Root construction definitions are 224 CONT, 215 ACTI, 195 PKIN, 23 FURN; no final root
has an observed WEAP/ARMO/MISC/AMMO definition. This is an observation, not a
class whitelist. Containers and display fixtures are neither filtered by empty
contents nor collapsed by base. 657 names resolve; null-name behavior is tested.

All 657 root representatives have saved-disabled/deleted bits clear. The complete
member ledger still retains 118 disabled-set and 695 omitted-state references;
these are not silently discarded or described as proved deleted constructions.
The two historical owners (`81b58f`,`8483f2`) have zero recovered explicit direct
members, which is not proof they never had or no longer retain any constructions.
`owners.csv` includes all 19 owner/state/count rows; every owner completeness field
remains NOT_ESTABLISHED for the universal population.

Other-record ledger contains 15,526 other representations and 2,341 prefix errors;
these are retained diagnostic bounds, not evidence that their objects are absent.
Decoded alternate 80 contexts occur in 10,477 full-R3 rows; additional unsupported
leading-extra paths can conceal more. No observed queued WorkshopItem keyword
remains without a decoded explicit edge, but metadata/defaults can supply that
keyword without queueing it. Hence zero queued misses does not prove zero misses.

## Reproduction and failure history

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' save-analysis/scripts/research_workshop_inventory.py --run FRESH-INVENTORY --manifest .local-work/workshop-inventory/inputs27.json --context .local-work/workshop-inventory/definition-complete.json
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' save-analysis/scripts/verify_workshop_inventory.py --run FRESH-INVENTORY --receipt FRESH-VALIDATION
```

Run the four named unittest modules from `save-analysis/scripts/`.
`tests-final.txt`, `context-replay.json`, final05 before/after/reproduction,
validation04 receipt, package.json/status and source hashes retain actual checks.
The validator reads completed output and primary hashes, writes exclusive local
receipts, and verifies original action expectations, selected previous objects,
names and earlier seals. It never loads a save into the game.

Preserved failures/corrections: initial Java-launch settings write failed; direct
installed JVM launch corrected it. Native 03 numeric-address coercion and native13
absent-function lookup left partial exports; preceding complete functions remain
evidence with explicit partial status. Solar/component and first 4C-only
interpretations were superseded. A probe read attempted unfinished JSON and was
repeated after output closure. One interim source-edit-during-run snapshot
(`final01`) is excluded from script-hash reproduction claims. Closed/root probes,
final01/02/03/04 and validation 01 remain retained. A prematurely invoked validation 03 found no completion receipt and stopped; validation04 ran only after final05 closed. Validation 01's63-single-root check
failed because two extractors had trailing 57; the native dispatcher proved its
four-byte width, a regression test was added and final05/validation04 passed.
The six newly closed 57 references comprise four roots and two generated peers;
the intermediate projected 659 count is superseded by 657, not concealed.

Historical gameplay original paths in the manual/link manifests are unavailable
at their former locations; no fresh original hash claim is made for those paths.
Immutable research archives remain present and match frozen pins. No action in
this assignment moved, deleted or wrote originals. Frozen 23 and 60-file seals,
database/executable and current source pins are freshly verified. Publication
eligibility remains separate; full raw/private/bulk evidence is ignored/local.
