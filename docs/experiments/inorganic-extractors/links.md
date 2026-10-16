# Outgoing transfer links and destination references

[Report](report.md), [native register](../native-availability-map/functions.csv),
[source inventory](sources.csv). Addresses use the pinned static domain in
[native.md](native.md). This is an output-relationship map, not cargo modeling or
an account of current stored quantities.

**STATIC result:** transfer state is destination-keyed, with a set of incoming
source handles for each destination. A source query scans those sets and returns
the matching destination handles. This supplies actual target identities, not
merely a linked Boolean. Source and destination are proven by the native callback's
diagnostic strings, its argument movement and the insertion/removal consumers;
serialized byte order alone was not used to infer direction.

| Route | Exact local evidence | Native contract |
|---|---|---|
| Named operation binding | e1-07 `14208556c..142085584`, `142089ff2..14208a00a` | ObjectReference AddTransferLink binds callback 142068a10; RemoveTransferLink binds 14207eb00. Binding is not general invocation/lifetime qualification. |
| Source/destination interpretation | e1-08 `142068a10..142068b48` | R8 reference is source, R9 reference is destination. Null destination emits No destination specified; source validation emits not a valid Transfer Source. Passes source as RCX and destination as RDX to 140f85760. |
| Add edge | e1-09 `140f85760..140f858fd`; e1-10 `140f81200..140f8165a` | After validation, calls 140f81200 with source RDX and destination R8. Under lock 1459165d0, destination handle indexes global map 145916580; source handle is inserted in the nested set. Map mutation and graph/cache refresh follow; never invoked here. |
| Find outgoing destinations | e1-09 `140f80af0..140f80d6f` | RDX source reference; R8 caller output vector. Iterates occupied destination slots, resolves destination handle, matches source handle against each nested set, appends destination handle. All occupied slots are considered; multiple destinations are representable. Failed destinations are skipped; exact runtime handle resolution/lifetime is still necessary. |
| Remove edge | e1-08 `14207eb00..14207eb3c`; e1-09 `140f81a90..140f81cbc` | Callback moves source R8→RDX and destination R9→R8. Removal selects destination-keyed slot and removes source from its nested set, then refreshes derived graph/cache. This corroborates insertion direction independently. |
| Graph versus direct edges | e1-08 `140f82820..140f82c2a`; e1-05 `140f82c30..140f82e56`; e1-11 `140f881c0` | The cached traversal can include source/self and further connected targets subject to classification filters. It is not interchangeable with the direct outgoing edge query. Production's candidate source traversal can walk incoming links. Never label every connected reference an immediate output destination. |
| Save and restoration | e1-11 `140f7e6f0..140f7ea07`, `140f7ea10..140f7ee31` | Saver writes registered Workshop references, then destination count; each destination reference precedes its incoming-source count/list. Source handles resolve to FormIDs through helper 141868de0; destination uses reference writer 1402cedd0. Loader reads references through 1402cef80, converts to current handles and rebuilds the same destination-keyed nested sets, then schedules cache rebuilding. Save identities are not raw runtime handles. |

Map layout, STATIC on the pinned executable: outer storage 1459165b0, capacity
1459165b8, lock 1459165d0; outer stride 38, destination u32 at slot+00,
nested container at+08 (data+10, capacity+18, free count+20), occupancy/link dword
at+30. Nested source slots stride 0c, source u32 at+00 and occupancy/link at+04.
Unused occupancy is ffffffff. These are hash capacities and occupied-slot rules,
not stable contiguous arrays of exactly capacity active edges. No link keyword
is consumed in this direct map; WorkshopItem 054ba6 owner links and power
connections are different relationships.

The [controlled saved-link experiment](../output-link-validation-L0-L2C.md)
originally retained direction UNKNOWN. It establishes endpoint persistence and
reversible 19→12→19-byte payloads, with linked L0C at decoded offset 425510,
unlinked L1/L1C at 425510 and relinked L2/L2C at 426830/426826. The changing group
is storage token 81a7a3 followed by count 04 and extractor token 81a947. The newly
mapped writer/loader order supports storage as destination and extractor as
incoming source within that qualified framing. This is a new STATIC explanation
of the old SAVE association; the historical report remains unchanged.

The broad [mature-save collection](../mature-save-outpost-validation.md) includes
zero keys and non-extractor relationships. This work does not relabel all 246
endpoint occurrences as valid extractor output links. A null/dead reference,
missing destination, unsupported save representation or failed load resolution
must remain distinct from a qualified currently live destination.

Persistence classification is MIXED: direct relationships are PERSISTED and
restored with identity conversion; handle objects and connected-component caches
are RECONSTRUCTED/TRANSIENT. The static load path does not prove that a particular
historical pair was restored unchanged in a current session. No actual loaded
extractor or destination was sampled, and delivery of new units is not guaranteed
merely by an existing edge.
