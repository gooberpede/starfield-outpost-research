# Local input and output topology

[Report](report.md), [native map](native.md), [E1 directional contract](../inorganic-extractors/links.md).
Proposed STRONG / STATIC plus scoped SAVE corroboration, REVIEW-REQUIRED.
This maps identity and reachability, without inventory counts or supply modeling.

The shared registry `145916580` maps **destination handles to incoming source
handle sets**, protected by lock `1459165d0`. Direct outgoing query `140f80af0`
finds every destination containing a given source handle; it is not an upstream
query. E1's add/remove/save/load consumers establish direction and remapping.
The organic input helper uses `140f881c0`, which starts with the consuming
producer handle, finds its incoming set, resolves source handles, deduplicates
resolved references and repeats upstream. This is transitive reverse traversal,
not a query limited to immediate input containers. Its temporary arrays and
retained references require native cleanup; handles/pointers are not stable save
identifiers or a qualified callable interface.

Supported descriptive operations are: resolve the facility's operational member;
identify selected IRES and FVPA inputs; list direct incoming sources from its
destination slot; list direct outgoing destinations using the shared query;
walk incoming local edges with visited identities and retain explicit paths;
join reached producer registrations to their selected IRES. Keep direct edges,
transitive reachability, Workshop owner edges and power connections separate.
For an offline saved graph, use save-era reference resolution and serializer
ordering; never splice live handles into saved FormIDs.

| Trace result | Meaning |
|---|---|
| LOCAL_PRODUCER_REACHED | A verified directed local path reaches a producer registered for the required resource; no supply/rate guarantee |
| STORAGE_OR_INCOMING_CARGO_BOUNDARY | A reached reference is independently identified as storage/incoming cargo; remote source remains unresolved, not absent |
| NO_STRUCTURAL_PATH_IDENTIFIED | No producer path in the inspected, qualified graph coverage; never universal resource absence |
| UNRESOLVED_EVIDENCE | Missing reference, unsupported framing, unknown endpoint type or incomplete graph; preserve the obstruction |

The native reverse-link walker does not interpret a remote cargo connection as
another local transfer edge. It can use resources physically present at a local
incoming container without identifying their remote origin. A Montara Luna path
ending at incoming Fiber cargo is therefore a valid boundary result; no new
Montara Luna husbandry observation was made in this task.

Fresh [saved.py](../../../research/e2-organic/saved.py) audit reads the protected
Save52 copy, reproduces the prior complete ordinary-beacon producer audit and
parses the unique framed transfer envelope into 246 endpoint occurrences. Those
are observed serialized edges in this representation, not a claim that all are
valid loaded links. Every one of the six identified greenhouse producers has
a saved upstream path through liquid storage to a saved Water producer.

For example, in save-era dynamic identities, direction of supply is:

`ff01a746` Water extractor → `ff01a752` liquid storage → `ff01a810` greenhouse.

The greenhouse is registered under Lubricant IRES `starfield.esm:0777f9` in
owner `ff01a75b`. Its saved producer-row body starts at decoded logical byte
2924711; operational member record starts at 2945505. Storage record starts at
2923918; the Water extractor record starts at 2921178 and registers Water IRES
`starfield.esm:0083ec`. The prior supported membership inventory independently
identifies their bases as `2965f7`, `2c5913` and `06ac92` respectively, with the
same explicit Workshop owner. These are SAVE identities, not native handles.
The local receipts retain all six paths, branch alternatives, offsets and
endpoint provenance. Their success does not establish current power, contents,
capacity, actual delivery or sufficient throughput.

Original Save52 SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`;
decoded SHA-256
`e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93`.
`saved02.json` and `saved-endpoints01.json` under `.local-work/e2-organic/`
retain detailed evidence. Existing membership inventory is pinned in derived01;
its 657-root baseline and later 848-root subset remain scoped historical results.
No full player population or live restoration is newly claimed.
