# SD2 frozen offline plan

2026-10-19, Australia/Sydney. The [invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_SD2_shared_storage_crafting_access.md`)
and its eight mandatory criteria govern without amendment. SD3 Stored Resources
screen mapping is excluded. Results and acceptance remain separate.

Question: what gates and registers Shared Outpost Storage, where its items live,
and how ingredient counts differ from spending across actual consumers?
Competing models: global inventory, reference-owned distributed access, copying,
or virtual aggregation. Names alone discriminate none of these. Trace definitions
to producers and consumers, then test correspondence in historical originals.

Controls: ordinary chest, industrial store, Transfer Container, differently gated
COBJ recipes, player/ship/companion inventories, current versus remote Workshop.
Distinguish hidden/locked/buildable, visible/eligible/spent, present/registered,
default/override, and serialized/loaded. Search mature corpus beyond Save52;
no positive shared-storage witness is assumed. Unsupported parsers are gaps.

Allowed: installed definition/PEX/UI and executable file reads, existing Ghidra
readOnly/noanalysis exports, qualified project-owned save readers, temporary
derivatives and authored documentation. No native/PEX execution, game launch,
debugger, instrumentation, original-save/data/configuration/database edits,
network, deployment, staging, commit, push or publication.

Source identities are freshly checked against the protected SD1 baseline before
reuse; new add-on and save inputs receive pre/post hashes. Local receipts under
`.local-work/sd2-shared/` retain exact versions, offsets and failures. Helpers
must describe reads/writes and provenance. Raw inputs/exports remain LOCAL-ONLY;
authored summaries REVIEW-REQUIRED. No new third-party implementation is used.

Both C: and D: require 40,000,000,000 caller-available bytes. Stop affected work
on disk-query/guard failure, protected-input drift, unsafe output or integrity
failure; preserve receipts and continue unrelated safe work. No arbitrary
scientific timeout/sample cutoff. Clean decoding scratch and retire only the
owned offline worker through its stop sentinel; rehash protected state afterward.

Success requires supported causal branch chains, appropriate contrasts and the
original eight-criterion matrix, independent read-only review, exact complete
and task-only patch reconstruction and text/link checks. Absent witnesses permit
a qualified negative census and minimal proposed live test, never a gameplay
result. Failed necessary qualifications remain unfinished.
