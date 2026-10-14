# Offline interface and schema

The original stdlib/project library is
[workshop_inventory.py](../../../save-analysis/scripts/workshop_inventory.py);
[runner](../../../save-analysis/scripts/research_workshop_inventory.py),
[definition context](../../../save-analysis/scripts/workshop_definition_context.py),
[tests](../../../save-analysis/scripts/test_workshop_inventory.py).
Read-only inputs: existing qualified archives, existing decoded stream readers,
and optionally hash-pinned installed ESM identity/name context. Outputs: exclusively
new ignored run directory and temporary decoder scratch, removed by context exit.
No target, original save, database, Git or network writes. Both C:/D: free-space
guards retain 40,000,000,000 bytes. No scientific count/time/output quota.

Example, from repository root with installed CPython:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' save-analysis/scripts/research_workshop_inventory.py --run FRESH-NAME --save QUALIFIED.sfs --sha256 EXPECTED_SHA256 --context CONTEXT.json
```

Context is optional for detection; missing names do not remove instances. The
context generator scans headers of all supplied installed ESMs and reads all
record types for an exact identity request list. It retains definition type,
EditorID, keyword context, source hash and physical record offset; no assets.
Current definitions are not guaranteed equivalent to historical installed content.
See its `--help` for explicit file arguments. Its source pins are checked before
and after the inventory run.

`--manifest FILE` accepts a JSON list of `{label, series, pin}` inputs, where pin
is the existing project `identity()` object including absolute path, size, SHA256
and times. It excludes the default corpus, as does explicit `--save` mode. Without
either option the runner uses existing extractor run05 qualified corpus pins;
`--labels` selects named checkpoints. Never replace old receipts. The retained
27-label manifest is `.local-work/workshop-inventory/inputs27.json`.

Each `SERIES-LABEL.json` has schema `workshop-saved-membership/1` with root
representation `CLOSED_EXPLICIT_SAVED_WORKSHOP_NATIVE_ITEM_PROJECTION/1`:

| Field | Meaning |
|---|---|
| `instances` | All decoded explicit WorkshopItem-key member records, **not** constructed-instance rows. Competing edges and unresolved owners remain here. |
| `constructed_instances` | One row per supported unique native item root; single reference or compound dummy representative. |
| `member_roles` | Every direct member classified as single/compound root, generated member, foundation, or unresolved with reason. |
| `unresolved_population` | Every other framed R3 record, including unknown representation and unsupported extras; possible missed constructions, not a claim that they are constructions. |
| `owners` | All recognized ordinary beacon rows, including saved-disabled historical owners with zero recovered members. |
| `coverage` | Exact framing/role counts and independent completeness dimensions. Universal constructed and loaded populations remain false. |
| `source`, `plugins`, `decode` | Qualified archive identity, saved full/small/medium plugin tables, decoder provenance. |

Root fields include dynamic/saved qualified instance identity and raw token;
saved ordinary owner; raw base versus compound construction definition; kind;
optional EditorID and definition provenance; saved flags, disabled bit and deleted
bit; logical record offsets/type; optional raw position; qualified member identities
and their offsets. Unknown names/states remain null. A compound dummy's transform
is its raw representative transform, not a claim about every visible child or a
global coordinate. `member_population_complete=false` means the listed peers are
the qualified forward-edge subset, not the complete loaded reverse4D set.

Record rows retain raw reference/string queues, their logical queue/body offsets,
prefix fields, component-envelope references/strings, linked-entry queue indexes
and exact mode-byte offsets. Dynamic identities are `DYNAMIC:ff......`; file forms
are `plugin.esm:localid`. Runtime handles/pointers are never substituted for these.
ESM offsets are physical file offsets; save offsets are decoded logical offsets.

CSV companions preserve all roots and all member roles, plus one compact row per
other record. JSON preserves full competing/provenance evidence. Ordering is stable
by owner/root identity or saved identity/offset; unresolved records by ordinal.
No category, recipe, label, proximity or inventory-contents filter is applied.
`before.json`, `after.json`, `summary.json`, `reproduction.json` preserve inputs,
source/script hashes, repeated-primary-byte determinism and separate arithmetic
record-walker agreement. Repeated output is a mechanical check, not semantic proof.

Modern save build strings `1.16.244.0` and header/buffer version153 are qualified;
other versions fail rather than reusing layouts. Conditional dynamic reference
cases4/5/6/7 are inspected, with explicit types restricted to the previously
supported REFR-family range. Missing inline bases and unsupported extras remain
visible. The library consumes bytes only; it is a research interface, not an importer.
