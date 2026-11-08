# Native functions by RVA

`Starfield.exe` 1.16.244.0. Preferred VAs use base `0x140000000`.
See the [build pin and ABI limits](README.md).

| RVA | Preferred VA | Function | Purpose | Level |
| --- | --- | --- | --- | --- |
| `0x0000f770` | `0x14000f770` | [Inline LensFlare registration-name source](geography.md#rva-0x0000f770) | Inline LensFlare registration-name source | C |
| `0x00018340` | `0x140018340` | [Initialize the maximum display slot item limit](inventory.md#rva-0x00018340) | Initialize the maximum display slot item limit | C |
| `0x000183b0` | `0x1400183b0` | [Install display-case defaults](inventory.md#rva-0x000183b0) | Install display-case defaults | C |
| `0x0001e340` | `0x14001e340` | [Initialize biome extension or path string](geography.md#rva-0x0001e340) | Initialize biome extension or path string | C |
| `0x0001e370` | `0x14001e370` | [Initialize paired biome extension or path string](geography.md#rva-0x0001e370) | Initialize paired biome extension or path string | C |
| `0x000255c0` | `0x1400255c0` | [Initialize the easy StarMap level threshold](interfaces.md#rva-0x000255c0) | Initialize the easy StarMap level threshold | C |
| `0x00030f50` | `0x140030f50` | [OpenCloseFormState string initializer](power.md#rva-0x00030f50) | OpenCloseFormState string initializer | B |
| `0x000391d0` | `0x1400391d0` | [Open animation variable initializer](power.md#rva-0x000391d0) | Open animation variable initializer | B |
| `0x00039200` | `0x140039200` | [Close animation variable initializer](power.md#rva-0x00039200) | Close animation variable initializer | B |
| `0x0003e540` | `0x14003e540` | [Initialize the queue-selection default](power.md#rva-0x0003e540) | Initialize the queue-selection default | C |
| `0x0003e570` | `0x14003e570` | [Initialize a Workshop power default object](power.md#rva-0x0003e570) | Initialize a Workshop power default object | C |
| `0x00051240` | `0x140051240` | [Initialize the inactive common-resource chance setting](geography.md#rva-0x00051240) | Initialize the inactive common-resource chance setting | C |
| `0x00051270` | `0x140051270` | [Initialize the inactive uncommon-resource chance setting](geography.md#rva-0x00051270) | Initialize the inactive uncommon-resource chance setting | C |
| `0x000512a0` | `0x1400512a0` | [Initialize the inactive rare-resource chance setting](geography.md#rva-0x000512a0) | Initialize the inactive rare-resource chance setting | C |
| `0x000512d0` | `0x1400512d0` | [Initialize the inactive exotic-resource chance setting](geography.md#rva-0x000512d0) | Initialize the inactive exotic-resource chance setting | C |
| `0x00051300` | `0x140051300` | [Initialize the inactive unique-resource chance setting](geography.md#rva-0x00051300) | Initialize the inactive unique-resource chance setting | C |
| `0x00051330` | `0x140051330` | [Initialize the inactive special-resource chance setting](geography.md#rva-0x00051330) | Initialize the inactive special-resource chance setting | C |
| `0x00055360` | `0x140055360` | [Initialize the native block orientation default](geography.md#rva-0x00055360) | Initialize the native block orientation default | C |
| `0x0008a340` | `0x14008a340` | [Initialize the ship fast travel marker default object](workshop.md#rva-0x0008a340) | Initialize the ship fast travel marker default object | C |
| `0x0008cb90` | `0x14008cb90` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0008cb90) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0008cc50` | `0x14008cc50` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0008cc50) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0008d130` | `0x14008d130` | [Participate in surface-pattern default initialization](geography.md#rva-0x0008d130) | Participate in surface-pattern default initialization | C |
| `0x0008d160` | `0x14008d160` | [Participate in surface-pattern default initialization](geography.md#rva-0x0008d160) | Participate in surface-pattern default initialization | C |
| `0x0008d1c0` | `0x14008d1c0` | [Initialize the surface-tree generation save setting](geography.md#rva-0x0008d1c0) | Initialize the surface-tree generation save setting | C |
| `0x00092260` | `0x140092260` | [Read the resource's base production interval](production.md#rva-0x00092260) | Read the resource's base production interval | C |
| `0x000977a0` | `0x1400977a0` | [Initialize the grouped-item dummy base](workshop.md#rva-0x000977a0) | Initialize the grouped-item dummy base | C |
| `0x0009bc60` | `0x14009bc60` | [Initialize the power route keyword default object](power.md#rva-0x0009bc60) | Initialize the power route keyword default object | C |
| `0x000a97a0` | `0x1400a97a0` | [Participate in effective harvester interval multiplier lookup](production.md#rva-0x000a97a0) | Participate in effective harvester interval multiplier lookup | C |
| `0x000e5200` | `0x1400e5200` | [entry-point metadata initialization](population.md#rva-0x000e5200) | entry-point metadata initialization | B |
| `0x000f81e0` | `0x1400f81e0` | [sleep update setting initializer](production.md#rva-0x000f81e0) | sleep update setting initializer | B |
| `0x00126ca0` | `0x140126ca0` | [Transfer Container keyword binding](inventory.md#rva-0x00126ca0) | Transfer Container keyword binding | C |
| `0x00126ce0` | `0x140126ce0` | [Footer gaps investigated · entry](workshop.md#rva-0x00126ce0) | Original report discusses this roster entry under Footer gaps investigated. | C |
| `0x00126d20` | `0x140126d20` | [Footer gaps investigated · entry](workshop.md#rva-0x00126d20) | Original report discusses this roster entry under Footer gaps investigated. | C |
| `0x00127cc0` | `0x140127cc0` | [actor scanner info list binding](production.md#rva-0x00127cc0) | actor scanner info list binding | B |
| `0x00127d00` | `0x140127d00` | [flora scanner info list binding](production.md#rva-0x00127d00) | flora scanner info list binding | B |
| `0x00127e80` | `0x140127e80` | [knowledge default keyword binding](production.md#rva-0x00127e80) | knowledge default keyword binding | B |
| `0x0012a8d0` | `0x14012a8d0` | [local-to-UT cap initializer](production.md#rva-0x0012a8d0) | local-to-UT cap initializer | B |
| `0x001366a0` | `0x1401366a0` | [Initialize the Freestar faction default object](interfaces.md#rva-0x001366a0) | Initialize the Freestar faction default object | C |
| `0x00156980` | `0x140156980` | [Initialize the harvester transfer-link default object](inventory.md#rva-0x00156980) | Initialize the harvester transfer-link default object | C |
| `0x00156a40` | `0x140156a40` | [Initialize the organic facility input default object](production.md#rva-0x00156a40) | Initialize the organic facility input default object | C |
| `0x00156bc0` | `0x140156bc0` | [Initialize the placement keyword default object](workshop.md#rva-0x00156bc0) | Initialize the placement keyword default object | C |
| `0x00156d00` | `0x140156d00` | [domesticability default keyword binding](production.md#rva-0x00156d00) | domesticability default keyword binding | B |
| `0x00156f40` | `0x140156f40` | [OutpostBuildContainer default binding](inventory.md#rva-0x00156f40) | OutpostBuildContainer default binding | C |
| `0x00156f80` | `0x140156f80` | [incoming prohibition default binding](inventory.md#rva-0x00156f80) | incoming prohibition default binding | C |
| `0x00156fc0` | `0x140156fc0` | [outgoing prohibition default binding](inventory.md#rva-0x00156fc0) | outgoing prohibition default binding | C |
| `0x001571c0` | `0x1401571c0` | [Construct the quest quota default-object registration](workshop.md#rva-0x001571c0) | Construct the quest quota default-object registration | C |
| `0x00157280` | `0x140157280` | [Initialize the production halt keyword default](production.md#rva-0x00157280) | Initialize the production halt keyword default | C |
| `0x00157480` | `0x140157480` | [Initialize the Workshop production interval override](production.md#rva-0x00157480) | Initialize the Workshop production interval override | C |
| `0x00157700` | `0x140157700` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00157700) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00157730` | `0x140157730` | [Initialize the Workshop transfer-link default object](inventory.md#rva-0x00157730) | Initialize the Workshop transfer-link default object | C |
| `0x00157770` | `0x140157770` | [Initialize the Workshop keyword default object](workshop.md#rva-0x00157770) | Initialize the Workshop keyword default object | C |
| `0x00157cc0` | `0x140157cc0` | [Territory and POI context · entry](geography.md#rva-0x00157cc0) | Original report discusses this roster entry under Territory and POI context. | C |
| `0x00158670` | `0x140158670` | [Initialize a budget actor-value default object](workshop.md#rva-0x00158670) | Initialize a budget actor-value default object | C |
| `0x001586b0` | `0x1401586b0` | [Initialize the WorkshopBudgetBaseline default object](workshop.md#rva-0x001586b0) | Initialize the WorkshopBudgetBaseline default object | C |
| `0x001594f0` | `0x1401594f0` | [Construct the deployment limit default-object registration](workshop.md#rva-0x001594f0) | Construct the deployment limit default-object registration | C |
| `0x001595f0` | `0x1401595f0` | [Construct the outpost panel exclusion default object](interfaces.md#rva-0x001595f0) | Construct the outpost panel exclusion default object | C |
| `0x0015a0d0` | `0x14015a0d0` | [Initialize the native budget base cost](workshop.md#rva-0x0015a0d0) | Initialize the native budget base cost | C |
| `0x0015a100` | `0x14015a100` | [Initialize the native budget baseline fallback](workshop.md#rva-0x0015a100) | Initialize the native budget baseline fallback | C |
| `0x002036f0` | `0x1402036f0` | [QPC clock initialization](production.md#rva-0x002036f0) | QPC clock initialization | B |
| `0x002b56d0` | `0x1402b56d0` | [No-op density or layer rank callback](geography.md#rva-0x002b56d0) | No-op density or layer rank callback | C |
| `0x002b5fa0` | `0x1402b5fa0` | [function data getter](population.md#rva-0x002b5fa0) | function data getter | B |
| `0x002b6280` | `0x1402b6280` | [Allocation-size candidate census · entry](geography.md#rva-0x002b6280) | Original report discusses this roster entry under Allocation-size candidate census. | C |
| `0x002b6c70` | `0x1402b6c70` | [Remap TESFile form identities by namespace](geography.md#rva-0x002b6c70) | Remap TESFile form identities by namespace | C |
| `0x002b7070` | `0x1402b7070` | [Check identity and install a reference-counted value](workshop.md#rva-0x002b7070) | Check identity and install a reference-counted value | C |
| `0x002b75d0` | `0x1402b75d0` | [Grid, terrain and density preparation · entry](workshop.md#rva-0x002b75d0) | Original report discusses this roster entry under Grid, terrain and density preparation. | C |
| `0x002b76b0` | `0x1402b76b0` | [Handle the MISC interface identity check](inventory.md#rva-0x002b76b0) | Handle the MISC interface identity check | C |
| `0x002b7740` | `0x1402b7740` | [Direct serialization edges recovered (exports 36–40) · entry](geography.md#rva-0x002b7740) | Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40). | C |
| `0x002b9480` | `0x1402b9480` | [Resolve the location link field in fixup](interfaces.md#rva-0x002b9480) | Resolve the location link field in fixup | C |
| `0x002b9ea0` | `0x1402b9ea0` | [Preparation and the two service pumps · entry](geography.md#rva-0x002b9ea0) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x002ba260` | `0x1402ba260` | [Native facts and alternatives examined · entry](geography.md#rva-0x002ba260) | Original report discusses this roster entry under Native facts and alternatives examined. | C |
| `0x002ba340` | `0x1402ba340` | [Native facts and alternatives examined · entry](geography.md#rva-0x002ba340) | Original report discusses this roster entry under Native facts and alternatives examined. | C |
| `0x002ba430` | `0x1402ba430` | [Support the typed uint16 save wire route](workshop.md#rva-0x002ba430) | Support the typed uint16 save wire route | C |
| `0x002c45a0` | `0x1402c45a0` | [Release exclusive owner-wide lock](geography.md#rva-0x002c45a0) | Release exclusive owner-wide lock | C |
| `0x002c5b40` | `0x1402c5b40` | [Allocation-size candidate census · entry](geography.md#rva-0x002c5b40) | Original report discusses this roster entry under Allocation-size candidate census. | C |
| `0x002c5b80` | `0x1402c5b80` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x002c5b80) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x002c5bd0` | `0x1402c5bd0` | [Wrap heap-array growth for source storage](geography.md#rva-0x002c5bd0) | Wrap heap-array growth for source storage | C |
| `0x002c5be0` | `0x1402c5be0` | [Support the executed atmosphere-list allocation control](geography.md#rva-0x002c5be0) | Support the executed atmosphere-list allocation control | C |
| `0x002cb870` | `0x1402cb870` | [Find an interned name in the SFTR factory map](interfaces.md#rva-0x002cb870) | Looks up the exact name through the matching key and hash namespace. | B |
| `0x002cb9f0` | `0x1402cb9f0` | [Release keys and clear the name registry](interfaces.md#rva-0x002cb9f0) | Clears backing storage on the mapped shutdown path. | B |
| `0x002cd1b0` | `0x1402cd1b0` | [Participate in current-cell and location eligibility](workshop.md#rva-0x002cd1b0) | Participate in current-cell and location eligibility | C |
| `0x002cedd0` | `0x1402cedd0` | [UI, save framing and lifecycle native entry](interfaces.md#rva-0x002cedd0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x002cee60` | `0x1402cee60` | [saved reference to current validated handle restoration](power.md#rva-0x002cee60) | saved reference to current validated handle restoration | B |
| `0x002cef80` | `0x1402cef80` | [saved FormID remap and reference lookup](power.md#rva-0x002cef80) | saved FormID remap and reference lookup | B |
| `0x002cf060` | `0x1402cf060` | [validated reference handle callback](power.md#rva-0x002cf060) | validated reference handle callback | B |
| `0x002d26d0` | `0x1402d26d0` | [Insert an interned name and factory in the map](interfaces.md#rva-0x002d26d0) | Hashes and compares the name in the exact-name namespace. | B |
| `0x002d4ce0` | `0x1402d4ce0` | [Return the GridFillFile dependency result](geography.md#rva-0x002d4ce0) | Return the GridFillFile dependency result | C |
| `0x002d65e0` | `0x1402d65e0` | [Initialize the native float-setting object](geography.md#rva-0x002d65e0) | Writes the initial setting and its shadow value. | B |
| `0x002d66a0` | `0x1402d66a0` | [Set the StarMap level thresholds](interfaces.md#rva-0x002d66a0) | Set the StarMap level thresholds | C |
| `0x002faea0` | `0x1402faea0` | [Construct the game setting collection](geography.md#rva-0x002faea0) | Construct the game setting collection | C |
| `0x00306090` | `0x140306090` | [Register or store the Workshop budget INI setting](workshop.md#rva-0x00306090) | Register or store the Workshop budget INI setting | C |
| `0x00306db0` | `0x140306db0` | [Encode a saved reference identity](population.md#rva-0x00306db0) | Encode a saved reference identity | C |
| `0x00306e40` | `0x140306e40` | [report · entry](population.md#rva-0x00306e40) | Original report discusses this roster entry under report. | C |
| `0x00315190` | `0x140315190` | [L01–L21 accounting · entry](geography.md#rva-0x00315190) | Original report discusses this roster entry under L01–L21 accounting. | C |
| `0x003499f0` | `0x1403499f0` | [Eight-byte pointer hash; full u64 equality; collision links; capacity sentinel](geography.md#rva-0x003499f0) | Eight-byte pointer hash; full u64 equality; collision links; capacity sentinel | C |
| `0x0035d380` | `0x14035d380` | [Append references during terrain relocation enumeration](workshop.md#rva-0x0035d380) | Append references during terrain relocation enumeration | C |
| `0x00360120` | `0x140360120` | [Checkpoint: ordinary-movement lifetime witness and final branch dispositions · entry](geography.md#rva-0x00360120) | Original report discusses this roster entry under Checkpoint: ordinary-movement lifetime witness and final branch dispositions. | C |
| `0x00360310` | `0x140360310` | [Register the playable center-cell key](geography.md#rva-0x00360310) | Register the playable center-cell key | C |
| `0x003605e0` | `0x1403605e0` | [Register the neighboring cell key](geography.md#rva-0x003605e0) | Register the neighboring cell key | C |
| `0x003615d0` | `0x1403615d0` | [Checkpoint: ordinary-movement lifetime witness and final branch dispositions · entry](geography.md#rva-0x003615d0) | Original report discusses this roster entry under Checkpoint: ordinary-movement lifetime witness and final branch dispositions. | C |
| `0x00362140` | `0x140362140` | [Register resource task dependency edges](geography.md#rva-0x00362140) | Register resource task dependency edges | C |
| `0x00362300` | `0x140362300` | [Register the paired resource task dependency path](geography.md#rva-0x00362300) | Register the paired resource task dependency path | C |
| `0x003623a0` | `0x1403623a0` | [Dependency completion and effective ordering · entry](geography.md#rva-0x003623a0) | Original report discusses this roster entry under Dependency completion and effective ordering. | C |
| `0x003623b0` | `0x1403623b0` | [Dependency completion and effective ordering · entry](geography.md#rva-0x003623b0) | Original report discusses this roster entry under Dependency completion and effective ordering. | C |
| `0x003623f0` | `0x1403623f0` | [Construct resource dependency node](geography.md#rva-0x003623f0) | Construct resource dependency node | C |
| `0x00362510` | `0x140362510` | [Forward the task-completion callback](geography.md#rva-0x00362510) | Forward the task-completion callback | C |
| `0x00362520` | `0x140362520` | [Preparation and the two service pumps · entry](geography.md#rva-0x00362520) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x003625e0` | `0x1403625e0` | [dependent resource request](geography.md#rva-0x003625e0) | dependent resource request | B |
| `0x00362fa0` | `0x140362fa0` | [Acquire keyed coordinate object](geography.md#rva-0x00362fa0) | Acquire keyed coordinate object | C |
| `0x003635f0` | `0x1403635f0` | [Checkpoint 3 — incremental claims and upstream dependencies · entry](geography.md#rva-0x003635f0) | Original report discusses this roster entry under Checkpoint 3 — incremental claims and upstream dependencies. | C |
| `0x00363b80` | `0x140363b80` | [Dispatch neighbor coordinate demand](geography.md#rva-0x00363b80) | Dispatch neighbor coordinate demand | C |
| `0x00364280` | `0x140364280` | [Alternative producers and coverage boundary · entry](geography.md#rva-0x00364280) | Original report discusses this roster entry under Alternative producers and coverage boundary. | C |
| `0x003643e0` | `0x1403643e0` | [Alternative producers and coverage boundary · entry](geography.md#rva-0x003643e0) | Original report discusses this roster entry under Alternative producers and coverage boundary. | C |
| `0x00364980` | `0x140364980` | [Acquire the scoped manager reader](geography.md#rva-0x00364980) | Acquire the scoped manager reader | C |
| `0x00365780` | `0x140365780` | [Checkpoint 3 — incremental claims and upstream dependencies · entry](geography.md#rva-0x00365780) | Original report discusses this roster entry under Checkpoint 3 — incremental claims and upstream dependencies. | C |
| `0x00365be0` | `0x140365be0` | [Ordinary initialization and ingress · entry](geography.md#rva-0x00365be0) | Original report discusses this roster entry under Ordinary initialization and ingress. | C |
| `0x00365c90` | `0x140365c90` | [Ordinary initialization and ingress · entry](geography.md#rva-0x00365c90) | Original report discusses this roster entry under Ordinary initialization and ingress. | C |
| `0x0036b9a0` | `0x14036b9a0` | [Preparation and the two service pumps · entry](geography.md#rva-0x0036b9a0) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x00384600` | `0x140384600` | [Current outpost and area branch · entry](geography.md#rva-0x00384600) | Original report discusses this roster entry under Current outpost and area branch. | C |
| `0x0038a050` | `0x14038a050` | [Return the bound member at receiver offset 0x28](inventory.md#rva-0x0038a050) | Return the bound member at receiver offset 0x28 | C |
| `0x0038a200` | `0x14038a200` | [forward value assignment to AV base setter](power.md#rva-0x0038a200) | forward value assignment to AV base setter | B |
| `0x0039ff30` | `0x14039ff30` | [Free the provider's temporary source-list chunks](geography.md#rva-0x0039ff30) | Releases the caller-owned list storage on the mapped provider cleanup path. | B |
| `0x003a4250` | `0x1403a4250` | [Traverse the owner store in native key order](geography.md#rva-0x003a4250) | Traverse the owner store in native key order | C |
| `0x003a5130` | `0x1403a5130` | [Serialize the generated-world descriptor array](workshop.md#rva-0x003a5130) | Serialize the generated-world descriptor array | C |
| `0x003a53b0` | `0x1403a53b0` | [Copy packed descriptor key to world](geography.md#rva-0x003a53b0) | Copy packed descriptor key to world | C |
| `0x003a5560` | `0x1403a5560` | [Decode and remap descriptor fields](geography.md#rva-0x003a5560) | Decode and remap descriptor fields | C |
| `0x003a5770` | `0x1403a5770` | [Typed restoration and packed origin (exports 42–49) · entry](workshop.md#rva-0x003a5770) | Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49). | C |
| `0x003a5e00` | `0x1403a5e00` | [Resolve or create reconstructed world](geography.md#rva-0x003a5e00) | Resolve or create reconstructed world | C |
| `0x003a69e0` | `0x1403a69e0` | [Return the stored game-day value](geography.md#rva-0x003a69e0) | Return the stored game-day value | C |
| `0x003a6ae0` | `0x1403a6ae0` | [Persistence and load · entry](geography.md#rva-0x003a6ae0) | Original report discusses this roster entry under Persistence and load. | C |
| `0x003a6dd0` | `0x1403a6dd0` | [Copy PlanetWorldSpaceData game-day fields](geography.md#rva-0x003a6dd0) | Copy PlanetWorldSpaceData game-day fields | C |
| `0x003a70a0` | `0x1403a70a0` | [Write the typed world component rows](geography.md#rva-0x003a70a0) | Write the typed world component rows | C |
| `0x003a74e0` | `0x1403a74e0` | [Persistence and load · entry](geography.md#rva-0x003a74e0) | Original report discusses this roster entry under Persistence and load. | C |
| `0x003a75e0` | `0x1403a75e0` | [Apply the queued game-day value](geography.md#rva-0x003a75e0) | Apply the queued game-day value | C |
| `0x003a7910` | `0x1403a7910` | [Initialize a world component with a zero-value branch](geography.md#rva-0x003a7910) | Initialize a world component with a zero-value branch | C |
| `0x003a7cc0` | `0x1403a7cc0` | [Restore a 32-bit descriptor field](workshop.md#rva-0x003a7cc0) | Restore a 32-bit descriptor field | C |
| `0x003a7eb0` | `0x1403a7eb0` | [Persistence and load · entry](geography.md#rva-0x003a7eb0) | Original report discusses this roster entry under Persistence and load. | C |
| `0x003a7ee0` | `0x1403a7ee0` | [Queue a current game-day component update](geography.md#rva-0x003a7ee0) | Queue a current game-day component update | C |
| `0x003e0080` | `0x1403e0080` | [Route bounded LOD locality demand](geography.md#rva-0x003e0080) | Route bounded LOD locality demand | C |
| `0x00404a10` | `0x140404a10` | [Read the Extra33 mod-instance list](interfaces.md#rva-0x00404a10) | Reads a mod-instance list from ExtraData loader case 0x33. | B |
| `0x00404cf0` | `0x140404cf0` | [Write the Extra33 mod-instance list](interfaces.md#rva-0x00404cf0) | Writes the mod-instance list selected by ExtraData writer case 0x33. | B |
| `0x00406e80` | `0x140406e80` | [Specific ship representation gap resolved · entry](inventory.md#rva-0x00406e80) | Original report discusses this roster entry under Specific ship representation gap resolved. | C |
| `0x004073c0` | `0x1404073c0` | [Charged slots and the player clamp · entry](population.md#rva-0x004073c0) | Original report discusses this roster entry under Charged slots and the player clamp. | C |
| `0x004074a0` | `0x1404074a0` | [Clamp destination crew capacity by player command slots](population.md#rva-0x004074a0) | Takes the lesser of effective destination capacity and player command capacity. | B |
| `0x004074f0` | `0x1404074f0` | [Check ordinary crew admission](population.md#rva-0x004074f0) | Evaluates destination slots and assignment restrictions before ordinary insertion. | A |
| `0x004076b0` | `0x1404076b0` | [Insert an actor into Workshop crew membership](population.md#rva-0x004076b0) | Transfers crew membership and writes the actor's keyed assignment. | A |
| `0x00407a10` | `0x140407a10` | [Remove crew](population.md#rva-0x00407a10) | Remove crew | C |
| `0x00407cb0` | `0x140407cb0` | [Migrate selected groups of crew handles](production.md#rva-0x00407cb0) | Migrate selected groups of crew handles | C |
| `0x004088c0` | `0x1404088c0` | [Sum charged slot costs](population.md#rva-0x004088c0) | Sum charged slot costs | C |
| `0x004089e0` | `0x1404089e0` | [report · entry](workshop.md#rva-0x004089e0) | Original report discusses this roster entry under report. | C |
| `0x00408a50` | `0x140408a50` | [get/create CrewExtraData](population.md#rva-0x00408a50) | get/create CrewExtraData | B |
| `0x00408bb0` | `0x140408bb0` | [assignment perk notification](population.md#rva-0x00408bb0) | assignment perk notification | B |
| `0x004094b0` | `0x1404094b0` | [Reverse the destination ability path during assignment removal](population.md#rva-0x004094b0) | Reverse the destination ability path during assignment removal | C |
| `0x004095c0` | `0x1404095c0` | [highest qualifying crew rank dispatcher](population.md#rva-0x004095c0) | highest qualifying crew rank dispatcher | B |
| `0x00409f10` | `0x140409f10` | [Participate in selected-actor perk entry dispatch](production.md#rva-0x00409f10) | Participate in selected-actor perk entry dispatch | C |
| `0x00409f60` | `0x140409f60` | [AA: ship capacity, not a CONT CarryWeight aura · entry](inventory.md#rva-0x00409f60) | Original report discusses this roster entry under AA: ship capacity, not a CONT CarryWeight aura. | C |
| `0x00409f80` | `0x140409f80` | [Combat and non-effect role metadata · entry](population.md#rva-0x00409f80) | Original report discusses this roster entry under Combat and non-effect role metadata. | C |
| `0x0040a0d0` | `0x14040a0d0` | [Prune unresolved entries during E2 serialization](population.md#rva-0x0040a0d0) | Prune unresolved entries during E2 serialization | C |
| `0x0040a230` | `0x14040a230` | [crew perk traversal](population.md#rva-0x0040a230) | crew perk traversal | B |
| `0x0040a360` | `0x14040a360` | [Assignment to a real query · entry](population.md#rva-0x0040a360) | Original report discusses this roster entry under Assignment to a real query. | C |
| `0x0040a840` | `0x14040a840` | [Type1 abilities: ship Fusion and destination state · entry](population.md#rva-0x0040a840) | Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state. | C |
| `0x0040a9d0` | `0x14040a9d0` | [type-one crew effect competition](population.md#rva-0x0040a9d0) | type-one crew effect competition | B |
| `0x0041e7f0` | `0x14041e7f0` | [Initialize the missing readiness entry](geography.md#rva-0x0041e7f0) | Initialize the missing readiness entry | C |
| `0x00422e10` | `0x140422e10` | [Dispatch the Reschedule command updater](geography.md#rva-0x00422e10) | Dispatch the Reschedule command updater | C |
| `0x0042e250` | `0x14042e250` | [Append a resource identity on the special path](geography.md#rva-0x0042e250) | Append a resource identity on the special path | C |
| `0x00431a00` | `0x140431a00` | [Register the display-case native form type](inventory.md#rva-0x00431a00) | Register the display-case native form type | C |
| `0x00431b50` | `0x140431b50` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x00431b50) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x004321f0` | `0x1404321f0` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x004321f0) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x0044b590` | `0x14044b590` | [property-sheet component descriptor](production.md#rva-0x0044b590) | property-sheet component descriptor | B |
| `0x0044b610` | `0x14044b610` | [Test property presence](production.md#rva-0x0044b610) | Test property presence | C |
| `0x0044b670` | `0x14044b670` | [extra property value lookup](production.md#rva-0x0044b670) | extra property value lookup | B |
| `0x00452e20` | `0x140452e20` | [raw property-sheet loading](production.md#rva-0x00452e20) | raw property-sheet loading | B |
| `0x004536c0` | `0x1404536c0` | [property-row insertion](production.md#rva-0x004536c0) | property-row insertion | B |
| `0x00453740` | `0x140453740` | [property-sheet copy](production.md#rva-0x00453740) | property-sheet copy | B |
| `0x004595c0` | `0x1404595c0` | [BGSWorldSpaceOverlay_Component key/name](workshop.md#rva-0x004595c0) | BGSWorldSpaceOverlay_Component key/name | C |
| `0x004597a0` | `0x1404597a0` | [BNAM PNAM SNAM loader](workshop.md#rva-0x004597a0) | BNAM PNAM SNAM loader | C |
| `0x00459a30` | `0x140459a30` | [resolve Block bounds](workshop.md#rva-0x00459a30) | resolve Block bounds | C |
| `0x0045a2d0` | `0x14045a2d0` | [plugin-aware form resolution](workshop.md#rva-0x0045a2d0) | plugin-aware form resolution | C |
| `0x00461370` | `0x140461370` | [Concrete factory loader construction](geography.md#rva-0x00461370) | Concrete factory loader construction | C |
| `0x004613d0` | `0x1404613d0` | [Register an SFTR factory by interned name](interfaces.md#rva-0x004613d0) | Stores a name key and supplied factory in the name registry. | B |
| `0x00461f10` | `0x140461f10` | [Look up the current body-name component](interfaces.md#rva-0x00461f10) | Look up the current body-name component | C |
| `0x004628b0` | `0x1404628b0` | [Look up an SFTR factory by interned name](interfaces.md#rva-0x004628b0) | Returns a matching factory or null in the qualified lookup. | B |
| `0x004639f0` | `0x1404639f0` | [Obtain the SFTR name-factory registry](interfaces.md#rva-0x004639f0) | Supplies the shared registry to registration and loader lookup. | B |
| `0x00463ed0` | `0x140463ed0` | [Dispatch a component block by exact name](interfaces.md#rva-0x00463ed0) | Routes the named component lookup into the factory registry. | B |
| `0x00475740` | `0x140475740` | [Queue satellite metadata by body identity](geography.md#rva-0x00475740) | Queue satellite metadata by body identity | C |
| `0x00475810` | `0x140475810` | [Queue body-index metadata by body identity](geography.md#rva-0x00475810) | Queue body-index metadata by body identity | C |
| `0x00477bd0` | `0x140477bd0` | [Initialize without retaining the incidental owner-field argument](geography.md#rva-0x00477bd0) | Initialize without retaining the incidental owner-field argument | C |
| `0x00478030` | `0x140478030` | [map load and default replacement](geography.md#rva-0x00478030) | map load and default replacement | C |
| `0x00478350` | `0x140478350` | [body-keyed biome map resource path](geography.md#rva-0x00478350) | body-keyed biome map resource path | C |
| `0x00478820` | `0x140478820` | [Native writer and alias graph · entry](geography.md#rva-0x00478820) | Original report discusses this roster entry under Native writer and alias graph. | C |
| `0x00478a30` | `0x140478a30` | [BiomeMapDB entry acquisition](geography.md#rva-0x00478a30) | BiomeMapDB entry acquisition | B |
| `0x0047a2b0` | `0x14047a2b0` | [map file header/version loader](geography.md#rva-0x0047a2b0) | map file header/version loader | C |
| `0x0047a930` | `0x14047a930` | [face arrays and identity remapping](geography.md#rva-0x0047a930) | face arrays and identity remapping | C |
| `0x0047fce0` | `0x14047fce0` | [Workshop keyword recognition](interfaces.md#rva-0x0047fce0) | Workshop keyword recognition | C |
| `0x0048eba0` | `0x14048eba0` | [Get facility base property sheet](production.md#rva-0x0048eba0) | Get facility base property sheet | C |
| `0x0049a430` | `0x14049a430` | [actor-value singleton accessor](production.md#rva-0x0049a430) | actor-value singleton accessor | B |
| `0x004a7da0` | `0x1404a7da0` | [Build the inverse matrix for body-oriented map selection](workshop.md#rva-0x004a7da0) | Build the inverse matrix for body-oriented map selection | C |
| `0x004a7f90` | `0x1404a7f90` | [native sin cosine helper](geography.md#rva-0x004a7f90) | native sin cosine helper | B |
| `0x004bcc80` | `0x1404bcc80` | [UI float copy and dirty setter](production.md#rva-0x004bcc80) | UI float copy and dirty setter | B |
| `0x00500ba0` | `0x140500ba0` | [Consult cached quest alias and bound target metadata](workshop.md#rva-0x00500ba0) | Consult cached quest alias and bound target metadata | C |
| `0x00500fd0` | `0x140500fd0` | [Insert ExtraData with type-specific ordering](workshop.md#rva-0x00500fd0) | Insert ExtraData with type-specific ordering | C |
| `0x00504b40` | `0x140504b40` | [Handle the materialized display reference](inventory.md#rva-0x00504b40) | Handle the materialized display reference | C |
| `0x0050aa30` | `0x14050aa30` | [Ownership and player action · entry](inventory.md#rva-0x0050aa30) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x0050aad0` | `0x14050aad0` | [Ownership and player action · entry](inventory.md#rva-0x0050aad0) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x0050b150` | `0x14050b150` | [Inventory instance to displayed reference · entry](inventory.md#rva-0x0050b150) | Original report discusses this roster entry under Inventory instance to displayed reference. | C |
| `0x0050ced0` | `0x14050ced0` | [Apply ownership to the copied item](inventory.md#rva-0x0050ced0) | Apply ownership to the copied item | C |
| `0x0050f400` | `0x14050f400` | [Preparation and the two service pumps · entry](geography.md#rva-0x0050f400) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x0050f5b0` | `0x14050f5b0` | [Support stored extra-location transform selection](workshop.md#rva-0x0050f5b0) | Support stored extra-location transform selection | C |
| `0x0050f750` | `0x14050f750` | [Select stored reference position for save framing](workshop.md#rva-0x0050f750) | Select stored reference position for save framing | C |
| `0x0050feb0` | `0x14050feb0` | [ExtraAction bit clearing](power.md#rva-0x0050feb0) | ExtraAction bit clearing | B |
| `0x0050ffe0` | `0x14050ffe0` | [default-open saved-difference restore](power.md#rva-0x0050ffe0) | default-open saved-difference restore | B |
| `0x00511680` | `0x140511680` | [Store the first original base for later reversion](workshop.md#rva-0x00511680) | Store the first original base for later reversion | C |
| `0x00511950` | `0x140511950` | [Resolve the original base on the saved override route](workshop.md#rva-0x00511950) | Resolve the original base on the saved override route | C |
| `0x00515090` | `0x140515090` | [Resolve the ExtraItemDropper relation](inventory.md#rva-0x00515090) | Resolve the ExtraItemDropper relation | C |
| `0x00515ee0` | `0x140515ee0` | [Resolve extra data for display attachment](inventory.md#rva-0x00515ee0) | Resolve extra data for display attachment | C |
| `0x00517c00` | `0x140517c00` | [Resolve the quest alias target for linked references](workshop.md#rva-0x00517c00) | Resolve the quest alias target for linked references | C |
| `0x00517d60` | `0x140517d60` | [Resolve a keyed reference](workshop.md#rva-0x00517d60) | Looks up a keyed reference on the path reached by the GetWorkshop callback. | B |
| `0x00518750` | `0x140518750` | [reverse4D deduplicating append](power.md#rva-0x00518750) | reverse4D deduplicating append | B |
| `0x0051b2b0` | `0x14051b2b0` | [Support native current-location resolution](workshop.md#rva-0x0051b2b0) | Support native current-location resolution | C |
| `0x0051c5d0` | `0x14051c5d0` | [Participate in CrewExtraData E2 access](production.md#rva-0x0051c5d0) | Participate in CrewExtraData E2 access | C |
| `0x0051c800` | `0x14051c800` | [Participate in CrewExtraData E2 access](production.md#rva-0x0051c800) | Participate in CrewExtraData E2 access | C |
| `0x0051ea30` | `0x14051ea30` | [Serialize typed ExtraData cases](interfaces.md#rva-0x0051ea30) | Dispatches type-specific saved framing for native ExtraData lists. | A |
| `0x00521620` | `0x140521620` | [Load typed ExtraData cases](interfaces.md#rva-0x00521620) | Dispatches type-specific ExtraData readers under the containing load framing. | B |
| `0x00526bb0` | `0x140526bb0` | [post-load forward to reverse ownership rebuilding](power.md#rva-0x00526bb0) | post-load forward to reverse ownership rebuilding | B |
| `0x00528450` | `0x140528450` | [Install ExtraModelSwap for the selected stage](workshop.md#rva-0x00528450) | Install ExtraModelSwap for the selected stage | C |
| `0x005315c0` | `0x1405315c0` | [Enter the alternate association insertion route](power.md#rva-0x005315c0) | Enter the alternate association insertion route | C |
| `0x00531b10` | `0x140531b10` | [extra flags mask reader](production.md#rva-0x00531b10) | extra flags mask reader | B |
| `0x005335c0` | `0x1405335c0` | [Merge the ExtraMaterialSwap material array](workshop.md#rva-0x005335c0) | Merge the ExtraMaterialSwap material array | C |
| `0x005366a0` | `0x1405366a0` | [Participate in native selected-template restoration](population.md#rva-0x005366a0) | Participate in native selected-template restoration | C |
| `0x0053a2d0` | `0x14053a2d0` | [Type 9 destination generic form token reader](geography.md#rva-0x0053a2d0) | Type 9 destination generic form token reader | C |
| `0x0053dd30` | `0x14053dd30` | [Allocate Workshop ExtraData storage](workshop.md#rva-0x0053dd30) | Requests the documented 0xa0-byte object allocation. | B |
| `0x005407b0` | `0x1405407b0` | [Dispatch direct or queued association insertion](power.md#rva-0x005407b0) | Dispatch direct or queued association insertion | C |
| `0x00540a90` | `0x140540a90` | [Forward the alternate association route](power.md#rva-0x00540a90) | Forward the alternate association route | C |
| `0x005431d0` | `0x1405431d0` | [ExtraPowerLinks obtain or create](power.md#rva-0x005431d0) | ExtraPowerLinks obtain or create | B |
| `0x00543370` | `0x140543370` | [Participate in native selected-template restoration](population.md#rva-0x00543370) | Participate in native selected-template restoration | C |
| `0x00543c80` | `0x140543c80` | [Process queued association insertion](power.md#rva-0x00543c80) | Process queued association insertion | C |
| `0x00545e40` | `0x140545e40` | [Extra9C flag restoration](power.md#rva-0x00545e40) | Extra9C flag restoration | B |
| `0x00546580` | `0x140546580` | [Further resolved branches (exports 23–28) · entry](workshop.md#rva-0x00546580) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x00547c90` | `0x140547c90` | [Dispatch saved linked-reference restoration](population.md#rva-0x00547c90) | Dispatch saved linked-reference restoration | C |
| `0x00547d80` | `0x140547d80` | [Resolve linked reference from FormID or handle](workshop.md#rva-0x00547d80) | Resolve linked reference from FormID or handle | C |
| `0x0054b1e0` | `0x14054b1e0` | [Read alternate extra identity and group object ID](workshop.md#rva-0x0054b1e0) | Read alternate extra identity and group object ID | C |
| `0x0054c2f0` | `0x14054c2f0` | [UI, save framing and lifecycle native entry](interfaces.md#rva-0x0054c2f0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00554bd0` | `0x140554bd0` | [Load the ExtraData E6 counted representation](population.md#rva-0x00554bd0) | Load the ExtraData E6 counted representation | C |
| `0x00562ef0` | `0x140562ef0` | [Refresh, caches and persistence · entry](inventory.md#rva-0x00562ef0) | Original report discusses this roster entry under Refresh, caches and persistence. | C |
| `0x00573090` | `0x140573090` | [Definition loading and postlink readiness · entry](geography.md#rva-0x00573090) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x00575020` | `0x140575020` | [Save loading and interior residency · entry](geography.md#rva-0x00575020) | Original report discusses this roster entry under Save loading and interior residency. | C |
| `0x005754c0` | `0x1405754c0` | [Save loading and interior residency · entry](geography.md#rva-0x005754c0) | Original report discusses this roster entry under Save loading and interior residency. | C |
| `0x00579cc0` | `0x140579cc0` | [Reset causality and lifecycle purpose · entry](geography.md#rva-0x00579cc0) | Original report discusses this roster entry under Reset causality and lifecycle purpose. | C |
| `0x0057a3d0` | `0x14057a3d0` | [Reset causality and lifecycle purpose · entry](geography.md#rva-0x0057a3d0) | Original report discusses this roster entry under Reset causality and lifecycle purpose. | C |
| `0x0057abc0` | `0x14057abc0` | [Confirmation and transition ingress · entry](geography.md#rva-0x0057abc0) | Original report discusses this roster entry under Confirmation and transition ingress. | C |
| `0x0057fc40` | `0x14057fc40` | [Clear the separate TES runtime member](geography.md#rva-0x0057fc40) | Clear the separate TES runtime member | C |
| `0x0057fce0` | `0x14057fce0` | [Reset causality and lifecycle purpose · entry](geography.md#rva-0x0057fce0) | Original report discusses this roster entry under Reset causality and lifecycle purpose. | C |
| `0x00580d20` | `0x140580d20` | [global0A saved notification list restoration](power.md#rva-0x00580d20) | global0A saved notification list restoration | B |
| `0x005810b0` | `0x1405810b0` | [global0A finish object-loaded notifications](power.md#rva-0x005810b0) | global0A finish object-loaded notifications | B |
| `0x00582d60` | `0x140582d60` | [Read native condition command descriptors](geography.md#rva-0x00582d60) | Read native condition command descriptors | C |
| `0x005883b0` | `0x1405883b0` | [Elapsed producer and staged consumers · entry](inventory.md#rva-0x005883b0) | Original report discusses this roster entry under Elapsed producer and staged consumers. | C |
| `0x005893c0` | `0x1405893c0` | [Visit the cell-finish notification path](power.md#rva-0x005893c0) | Visit the cell-finish notification path | C |
| `0x0058ccf0` | `0x14058ccf0` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x0058ccf0) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x0058d470` | `0x14058d470` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x0058d470) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x0058e9d0` | `0x14058e9d0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x0058e9d0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x00591d40` | `0x140591d40` | [Append an SFPT entry to the typed registry](geography.md#rva-0x00591d40) | Append an SFPT entry to the typed registry | C |
| `0x00593280` | `0x140593280` | [Enumerate actor-value definitions](production.md#rva-0x00593280) | Enumerate actor-value definitions | C |
| `0x00594980` | `0x140594980` | [d5ad input provenance · entry](geography.md#rva-0x00594980) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x00594ad0` | `0x140594ad0` | [Select the typed surface-pattern registry](geography.md#rva-0x00594ad0) | Select the typed surface-pattern registry | C |
| `0x00596dd0` | `0x140596dd0` | [Unload the LoadedCellDB entry](geography.md#rva-0x00596dd0) | Unload the LoadedCellDB entry | C |
| `0x005972b0` | `0x1405972b0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005972b0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x00597a70` | `0x140597a70` | [Definition loading and postlink readiness · entry](geography.md#rva-0x00597a70) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x005994a0` | `0x1405994a0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005994a0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x0059ac20` | `0x14059ac20` | [Calendar singleton/GLOB 0x00000039 binding and initialization](geography.md#rva-0x0059ac20) | Calendar singleton/GLOB 0x00000039 binding and initialization | C |
| `0x0059d7c0` | `0x14059d7c0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x0059d7c0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x0059e000` | `0x14059e000` | [d5ad input provenance · entry](geography.md#rva-0x0059e000) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x005a0520` | `0x1405a0520` | [Enter a forward-derived reconstruction path](power.md#rva-0x005a0520) | Enter a forward-derived reconstruction path | C |
| `0x005a3cc0` | `0x1405a3cc0` | [Create the player backing reference](inventory.md#rva-0x005a3cc0) | Create the player backing reference | C |
| `0x005afc70` | `0x1405afc70` | [Append a style-matched surface-pattern candidate](geography.md#rva-0x005afc70) | Append a style-matched surface-pattern candidate | C |
| `0x005afea0` | `0x1405afea0` | [Process association during reconstruction](power.md#rva-0x005afea0) | Process association during reconstruction | C |
| `0x005b5bb0` | `0x1405b5bb0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005b5bb0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x005b5be0` | `0x1405b5be0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005b5be0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x005b68d0` | `0x1405b68d0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005b68d0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x005b7310` | `0x1405b7310` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005b7310) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x005b9750` | `0x1405b9750` | [Construct the packed plugin-file object](geography.md#rva-0x005b9750) | Installs the TESPackedFile table after base construction. | B |
| `0x005b9950` | `0x1405b9950` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005b9950) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x005bb020` | `0x1405bb020` | [Definition loading and postlink readiness · entry](geography.md#rva-0x005bb020) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x005bf6d0` | `0x1405bf6d0` | [Register BGSDestructibleObject_Component](population.md#rva-0x005bf6d0) | Register BGSDestructibleObject_Component | C |
| `0x005bfe60` | `0x1405bfe60` | [Damage and operational consequences · entry](population.md#rva-0x005bfe60) | Original report discusses this roster entry under Damage and operational consequences. | C |
| `0x005c02a0` | `0x1405c02a0` | [Damage and operational consequences · entry](population.md#rva-0x005c02a0) | Original report discusses this roster entry under Damage and operational consequences. | C |
| `0x005c0530` | `0x1405c0530` | [Damage and operational consequences · entry](workshop.md#rva-0x005c0530) | Original report discusses this roster entry under Damage and operational consequences. | C |
| `0x005c1a40` | `0x1405c1a40` | [Resolve a model variant for a damage stage](workshop.md#rva-0x005c1a40) | Resolve a model variant for a damage stage | C |
| `0x005c2e10` | `0x1405c2e10` | [Derive the current damage-stage model](workshop.md#rva-0x005c2e10) | Derive the current damage-stage model | C |
| `0x005c42d0` | `0x1405c42d0` | [Restore Health damage through modifier index 2](population.md#rva-0x005c42d0) | Restore Health damage through modifier index 2 | C |
| `0x005ccd00` | `0x1405ccd00` | [settled open-close action completion](power.md#rva-0x005ccd00) | settled open-close action completion | B |
| `0x005cd370` | `0x1405cd370` | [reference open-close state setter](power.md#rva-0x005cd370) | reference open-close state setter | B |
| `0x005cd7a0` | `0x1405cd7a0` | [open-close action animation dispatch](power.md#rva-0x005cd7a0) | open-close action animation dispatch | B |
| `0x005cdc70` | `0x1405cdc70` | [Read supported open-close state](power.md#rva-0x005cdc70) | Read supported open-close state | C |
| `0x005d2590` | `0x1405d2590` | [Load the NPC template parts array](population.md#rva-0x005d2590) | Load the NPC template parts array | C |
| `0x005d2d90` | `0x1405d2d90` | [Resolve enabled NPC template parts](population.md#rva-0x005d2d90) | Resolve enabled NPC template parts | C |
| `0x005d3ad0` | `0x1405d3ad0` | [Resolve enabled NPC template parts](population.md#rva-0x005d3ad0) | Resolve enabled NPC template parts | C |
| `0x005d4a00` | `0x1405d4a00` | [Selected rank and load reconstruction · entry](population.md#rva-0x005d4a00) | Original report discusses this roster entry under Selected rank and load reconstruction. | C |
| `0x005d4b20` | `0x1405d4b20` | [generic template selected-source recursion; not alone proof of scripts](population.md#rva-0x005d4b20) | generic template selected-source recursion; not alone proof of scripts | C |
| `0x005da040` | `0x1405da040` | [TESContainer component name identity](inventory.md#rva-0x005da040) | TESContainer component name identity | C |
| `0x005daca0` | `0x1405daca0` | [Select budget fallback by form type](workshop.md#rva-0x005daca0) | Select budget fallback by form type | C |
| `0x005ddbd0` | `0x1405ddbd0` | [Resolve the object component for budget properties](workshop.md#rva-0x005ddbd0) | Resolve the object component for budget properties | C |
| `0x005de3b0` | `0x1405de3b0` | [Resolve the FormID for the object-loaded event](inventory.md#rva-0x005de3b0) | Resolve the FormID for the object-loaded event | C |
| `0x005df510` | `0x1405df510` | [Support retention of the shared-storage reference](inventory.md#rva-0x005df510) | Support retention of the shared-storage reference | C |
| `0x005df980` | `0x1405df980` | [SFTR vtable inherited SaveGame flags](geography.md#rva-0x005df980) | SFTR vtable inherited SaveGame flags | C |
| `0x005dfa40` | `0x1405dfa40` | [Restore saved form flags](workshop.md#rva-0x005dfa40) | Restore saved form flags | C |
| `0x005e0230` | `0x1405e0230` | [installed VMAD loader forwards parser](population.md#rva-0x005e0230) | installed VMAD loader forwards parser | C |
| `0x005e0930` | `0x1405e0930` | [Load an SFTR BFCB component block](interfaces.md#rva-0x005e0930) | Resolves a named factory and skips bounded data if none exists. | B |
| `0x005e10b0` | `0x1405e10b0` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x005e10b0) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x005e18a0` | `0x1405e18a0` | [Actual causal chain · entry](inventory.md#rva-0x005e18a0) | Original report discusses this roster entry under Actual causal chain. | C |
| `0x005e1f40` | `0x1405e1f40` | [DATA component scalar distribution](inventory.md#rva-0x005e1f40) | DATA component scalar distribution | C |
| `0x005e3fb0` | `0x1405e3fb0` | [Look up the planet subtitle name](interfaces.md#rva-0x005e3fb0) | Look up the planet subtitle name | C |
| `0x005e40a0` | `0x1405e40a0` | [Resolve a name for the outpost body context](interfaces.md#rva-0x005e40a0) | Resolve a name for the outpost body context | C |
| `0x005e68e0` | `0x1405e68e0` | [reference resource/biome condition consumer](geography.md#rva-0x005e68e0) | reference resource/biome condition consumer | C |
| `0x005e9000` | `0x1405e9000` | [Expand special product](production.md#rva-0x005e9000) | Expand special product | C |
| `0x005ed1b0` | `0x1405ed1b0` | [Look up or insert a selected-root map entry](geography.md#rva-0x005ed1b0) | Look up or insert a selected-root map entry | C |
| `0x005f7280` | `0x1405f7280` | [Participate in a production event branch](production.md#rva-0x005f7280) | Participate in a production event branch | C |
| `0x005f7a80` | `0x1405f7a80` | [planet subordinate range](production.md#rva-0x005f7a80) | planet subordinate range | B |
| `0x005fc440` | `0x1405fc440` | [Resolve item mass from the applicable provider](inventory.md#rva-0x005fc440) | Resolve item mass from the applicable provider | C |
| `0x00609320` | `0x140609320` | [Register placed reference](workshop.md#rva-0x00609320) | Register placed reference | C |
| `0x00609d20` | `0x140609d20` | [Definition loading and postlink readiness · entry](geography.md#rva-0x00609d20) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x0060d920` | `0x14060d920` | [Definition loading and postlink readiness · entry](geography.md#rva-0x0060d920) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x0060dbe0` | `0x14060dbe0` | [Definition loading and postlink readiness · entry](geography.md#rva-0x0060dbe0) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x00626a90` | `0x140626a90` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x00626a90) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x0063e4e0` | `0x14063e4e0` | [Receive the prepared default inventory count](interfaces.md#rva-0x0063e4e0) | Receive the prepared default inventory count | C |
| `0x00640030` | `0x140640030` | [Ownership and player action · entry](inventory.md#rva-0x00640030) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x00640c90` | `0x140640c90` | [Visit item data for display admission](inventory.md#rva-0x00640c90) | Visit item data for display admission | C |
| `0x00640eb0` | `0x140640eb0` | [Ownership and player action · entry](inventory.md#rva-0x00640eb0) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x00641180` | `0x140641180` | [item identity stacks quantity bookkeeping save](inventory.md#rva-0x00641180) | item identity stacks quantity bookkeeping save | C |
| `0x00641320` | `0x140641320` | [item identity and stack load](inventory.md#rva-0x00641320) | item identity and stack load | C |
| `0x006416f0` | `0x1406416f0` | [Normalize inventory extras before state inspection](inventory.md#rva-0x006416f0) | Normalize inventory extras before state inspection | C |
| `0x006425a0` | `0x1406425a0` | [Remove the represented display inventory quantity](inventory.md#rva-0x006425a0) | Remove the represented display inventory quantity | C |
| `0x00642a00` | `0x140642a00` | [stack extra list and signed quantity load](inventory.md#rva-0x00642a00) | stack extra list and signed quantity load | C |
| `0x00643240` | `0x140643240` | [Dispatch inventory list insertion](inventory.md#rva-0x00643240) | Dispatch inventory list insertion | C |
| `0x00643360` | `0x140643360` | [Inventory instance to displayed reference · entry](inventory.md#rva-0x00643360) | Original report discusses this roster entry under Inventory instance to displayed reference. | C |
| `0x00644210` | `0x140644210` | [Destroy existing stack extras on inventory reset](inventory.md#rva-0x00644210) | Destroy existing stack extras on inventory reset | C |
| `0x006447c0` | `0x1406447c0` | [inventory item count and row serialization](inventory.md#rva-0x006447c0) | inventory item count and row serialization | C |
| `0x006448b0` | `0x1406448b0` | [reference inventory list restoration](inventory.md#rva-0x006448b0) | reference inventory list restoration | C |
| `0x006450e0` | `0x1406450e0` | [Clear the inventory row array](inventory.md#rva-0x006450e0) | Clear the inventory row array | C |
| `0x00645ca0` | `0x140645ca0` | [mutation invalidates cached weight](inventory.md#rva-0x00645ca0) | mutation invalidates cached weight | C |
| `0x0064a770` | `0x14064a770` | [localized symbol resolution](interfaces.md#rva-0x0064a770) | localized symbol resolution | C |
| `0x0065bc30` | `0x14065bc30` | [Load linked refs from definition](power.md#rva-0x0065bc30) | Load linked refs from definition | C |
| `0x0065be30` | `0x14065be30` | [load saved electrical entries](power.md#rva-0x0065be30) | load saved electrical entries | B |
| `0x0065bf00` | `0x14065bf00` | [Insert linked-ref pair under protection](power.md#rva-0x0065bf00) | Insert linked-ref pair under protection | C |
| `0x0065bfc0` | `0x14065bfc0` | [Remove linked-ref membership](power.md#rva-0x0065bfc0) | Remove linked-ref membership | C |
| `0x0065c1b0` | `0x14065c1b0` | [copy restored electrical array](power.md#rva-0x0065c1b0) | copy restored electrical array | B |
| `0x0065c2f0` | `0x14065c2f0` | [insert electrical membership](power.md#rva-0x0065c2f0) | insert electrical membership | B |
| `0x00668130` | `0x140668130` | [Interpolate wire cable geometry](power.md#rva-0x00668130) | Interpolate wire cable geometry | C |
| `0x00668380` | `0x140668380` | [Resolve spline endpoint](power.md#rva-0x00668380) | Resolve spline endpoint | C |
| `0x00668560` | `0x140668560` | [Interpolate cable sag](power.md#rva-0x00668560) | Interpolate cable sag | C |
| `0x00668fa0` | `0x140668fa0` | [Test simple relationship words](power.md#rva-0x00668fa0) | Test simple relationship words | C |
| `0x00669090` | `0x140669090` | [Look up existing wire connection](power.md#rva-0x00669090) | Look up existing wire connection | C |
| `0x006695c0` | `0x1406695c0` | [power applicability predicate](production.md#rva-0x006695c0) | power applicability predicate | B |
| `0x00669670` | `0x140669670` | [connection-and-receiver predicate](power.md#rva-0x00669670) | connection-and-receiver predicate | B |
| `0x00669700` | `0x140669700` | [electrical endpoint predicate](power.md#rva-0x00669700) | electrical endpoint predicate | B |
| `0x006697f0` | `0x1406697f0` | [nominal generator predicate](power.md#rva-0x006697f0) | nominal generator predicate | B |
| `0x00669880` | `0x140669880` | [conditional generator contribution](power.md#rva-0x00669880) | conditional generator contribution | B |
| `0x006699b0` | `0x1406699b0` | [radiation predicate](power.md#rva-0x006699b0) | radiation predicate | B |
| `0x00669a10` | `0x140669a10` | [Classify snap power propagation](power.md#rva-0x00669a10) | Classify snap power propagation | C |
| `0x00669a60` | `0x140669a60` | [Classify demand-side candidate](power.md#rva-0x00669a60) | Classify demand-side candidate | C |
| `0x00669ac0` | `0x140669ac0` | [allocation node exclusion](power.md#rva-0x00669ac0) | allocation node exclusion | B |
| `0x00669c60` | `0x140669c60` | [electrical partition gate](power.md#rva-0x00669c60) | electrical partition gate | B |
| `0x00669d60` | `0x140669d60` | [Create reciprocal simple power memberships](power.md#rva-0x00669d60) | Create reciprocal simple power memberships | C |
| `0x00669ff0` | `0x140669ff0` | [Gather simple or snap power candidates](power.md#rva-0x00669ff0) | Gather simple or snap power candidates | C |
| `0x0066abc0` | `0x14066abc0` | [apply inverse unpowered flag](power.md#rva-0x0066abc0) | apply inverse unpowered flag | B |
| `0x0066b100` | `0x14066b100` | [electrical cumulative allocator](power.md#rva-0x0066b100) | electrical cumulative allocator | B |
| `0x0066bad0` | `0x14066bad0` | [simple radiating connector exclusion](power.md#rva-0x0066bad0) | simple radiating connector exclusion | B |
| `0x0066bcb0` | `0x14066bcb0` | [Accumulate generation during traversal](power.md#rva-0x0066bcb0) | Accumulate generation during traversal | C |
| `0x0066bd50` | `0x14066bd50` | [wire pair admission predicate](power.md#rva-0x0066bd50) | wire pair admission predicate | B |
| `0x0066bec0` | `0x14066bec0` | [Test explicit word-3 relationship](power.md#rva-0x0066bec0) | Test explicit word-3 relationship | C |
| `0x0066bfc0` | `0x14066bfc0` | [connect electrical graph and reallocate](power.md#rva-0x0066bfc0) | connect electrical graph and reallocate | B |
| `0x0066c4f0` | `0x14066c4f0` | [Participate in the power AV modifier caller set](power.md#rva-0x0066c4f0) | Participate in the power AV modifier caller set | C |
| `0x0066ccd0` | `0x14066ccd0` | [Participate in the power AV modifier caller set](power.md#rva-0x0066ccd0) | Participate in the power AV modifier caller set | C |
| `0x0066d4b0` | `0x14066d4b0` | [Refresh owner-linked power components](power.md#rva-0x0066d4b0) | Refresh owner-linked power components | C |
| `0x0066d890` | `0x14066d890` | [Participate in the power AV modifier caller set](power.md#rva-0x0066d890) | Participate in the power AV modifier caller set | C |
| `0x0066e9b0` | `0x14066e9b0` | [remove electrical connection and reallocate](power.md#rva-0x0066e9b0) | remove electrical connection and reallocate | B |
| `0x0066f3e0` | `0x14066f3e0` | [Create automatic graph relationships](power.md#rva-0x0066f3e0) | Create automatic graph relationships | C |
| `0x0066f880` | `0x14066f880` | [schedule power recomputation](power.md#rva-0x0066f880) | schedule power recomputation | B |
| `0x0066fa50` | `0x14066fa50` | [recompute powered set differences](power.md#rva-0x0066fa50) | recompute powered set differences | B |
| `0x006700f0` | `0x1406700f0` | [Resolve paired spline endpoint](power.md#rva-0x006700f0) | Resolve paired spline endpoint | C |
| `0x00671f70` | `0x140671f70` | [generation traversal dispatcher](power.md#rva-0x00671f70) | generation traversal dispatcher | B |
| `0x006722f0` | `0x1406722f0` | [Append eligible allocation neighbors](power.md#rva-0x006722f0) | Append eligible allocation neighbors | C |
| `0x006728e0` | `0x1406728e0` | [owner reverse-link generator root collector](power.md#rva-0x006728e0) | owner reverse-link generator root collector | B |
| `0x00675c50` | `0x140675c50` | [queue generation traversal](power.md#rva-0x00675c50) | queue generation traversal | B |
| `0x00676350` | `0x140676350` | [Traverse generation graph recursively](power.md#rva-0x00676350) | Traverse generation graph recursively | C |
| `0x006779e0` | `0x1406779e0` | [enumerate electrical neighbors](power.md#rva-0x006779e0) | enumerate electrical neighbors | B |
| `0x00677c50` | `0x140677c50` | [Handle pending and unseen electrical neighbor identities](power.md#rva-0x00677c50) | Promotes an already queued neighbor or evaluates an unseen neighbor's edge. | B |
| `0x00678f60` | `0x140678f60` | [Resolve recursive graph neighbors](power.md#rva-0x00678f60) | Resolve recursive graph neighbors | C |
| `0x006791d0` | `0x1406791d0` | [Recurse to eligible graph neighbor](power.md#rva-0x006791d0) | Recurse to eligible graph neighbor | C |
| `0x006797c0` | `0x1406797c0` | [generation pending front insertion](power.md#rva-0x006797c0) | generation pending front insertion | B |
| `0x00679890` | `0x140679890` | [pending range rotation](power.md#rva-0x00679890) | pending range rotation | B |
| `0x00684160` | `0x140684160` | [Read the float setting from loaded DATA](geography.md#rva-0x00684160) | Passes the mapped float from the definition record to the native setter. | B |
| `0x006843d0` | `0x1406843d0` | [Dispatch loaded setting data](geography.md#rva-0x006843d0) | Feeds the typed DATA reader on the mapped setting-load path. | B |
| `0x006846f0` | `0x1406846f0` | [Resolve the setting by collection and name](geography.md#rva-0x006846f0) | Supplies the setting to the native loaded-data dispatch. | B |
| `0x00684b30` | `0x140684b30` | [Write the current float-setting value](geography.md#rva-0x00684b30) | Can replace the value supplied by the initializer. | B |
| `0x00689180` | `0x140689180` | [Movement selection and admission · constructor](inventory.md#rva-0x00689180) | Original report discusses this roster entry under Movement selection and admission. | C |
| `0x0068a750` | `0x14068a750` | [Movement selection and admission · entry](inventory.md#rva-0x0068a750) | Original report discusses this roster entry under Movement selection and admission. | C |
| `0x00694f80` | `0x140694f80` | [Further resolved branches (exports 23–28) · entry](workshop.md#rva-0x00694f80) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x006db950` | `0x1406db950` | [Compare ready-tree keys in the paired bound helper](geography.md#rva-0x006db950) | Orders ready keys using unsigned rank followed by unsigned insertion serial. | B |
| `0x006dd4f0` | `0x1406dd4f0` | [Compare ready-tree keys in the mapped bound helper](geography.md#rva-0x006dd4f0) | Orders ready keys using unsigned rank followed by unsigned insertion serial. | B |
| `0x00769e90` | `0x140769e90` | [Support coarse candidate enumeration before reference creation](workshop.md#rva-0x00769e90) | Support coarse candidate enumeration before reference creation | C |
| `0x0076a340` | `0x14076a340` | [Floor local offsets in the bounded candidate route](workshop.md#rva-0x0076a340) | Floor local offsets in the bounded candidate route | C |
| `0x0076a5c0` | `0x14076a5c0` | [Preparation and the two service pumps · entry](geography.md#rva-0x0076a5c0) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x0076b110` | `0x14076b110` | [Checkpoint: completion callbacks and the preparation antecedent · entry](geography.md#rva-0x0076b110) | Original report discusses this roster entry under Checkpoint: completion callbacks and the preparation antecedent. | C |
| `0x0076b3e0` | `0x14076b3e0` | [Reset callers and predicates · entry](geography.md#rva-0x0076b3e0) | Original report discusses this roster entry under Reset callers and predicates. | C |
| `0x0076b950` | `0x14076b950` | [atmosphere population copy](geography.md#rva-0x0076b950) | atmosphere population copy | B |
| `0x0076bd20` | `0x14076bd20` | [effective atmosphere resolver](geography.md#rva-0x0076bd20) | effective atmosphere resolver | B |
| `0x0076c560` | `0x14076c560` | [four-level resource task producer](geography.md#rva-0x0076c560) | four-level resource task producer | B |
| `0x0076cd40` | `0x14076cd40` | [resource task registration](geography.md#rva-0x0076cd40) | resource task registration | B |
| `0x0076d140` | `0x14076d140` | [resource task dispatch wrapper](geography.md#rva-0x0076d140) | resource task dispatch wrapper | B |
| `0x0076d1c0` | `0x14076d1c0` | [dependency resource task construction](geography.md#rva-0x0076d1c0) | dependency resource task construction | B |
| `0x0076d500` | `0x14076d500` | [Fractional position producers and consumers · entry](geography.md#rva-0x0076d500) | Original report discusses this roster entry under Fractional position producers and consumers. | C |
| `0x0076db70` | `0x14076db70` | [Initialization and successful-construction obligations · entry](geography.md#rva-0x0076db70) | Original report discusses this roster entry under Initialization and successful-construction obligations. | C |
| `0x0076de40` | `0x14076de40` | [Further resolved branches (exports 23–28) · entry](geography.md#rva-0x0076de40) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x0076e720` | `0x14076e720` | [Positive typed alternatives · entry](geography.md#rva-0x0076e720) | Original report discusses this roster entry under Positive typed alternatives. | C |
| `0x0076e810` | `0x14076e810` | [Copy resource generator component](geography.md#rva-0x0076e810) | Copy resource generator component | C |
| `0x0076ec00` | `0x14076ec00` | [planet record tag loader](geography.md#rva-0x0076ec00) | planet record tag loader | C |
| `0x00770eb0` | `0x140770eb0` | [Resolve typed surface-tree reference](geography.md#rva-0x00770eb0) | Resolve typed surface-tree reference | C |
| `0x00771ac0` | `0x140771ac0` | [Queue planetary overlay component](workshop.md#rva-0x00771ac0) | Queue planetary overlay component | C |
| `0x00771f30` | `0x140771f30` | [per-biome component lookup](geography.md#rva-0x00771f30) | per-biome component lookup | B |
| `0x00773090` | `0x140773090` | [Queue fixed-world overlay component](workshop.md#rva-0x00773090) | Queue fixed-world overlay component | C |
| `0x00773180` | `0x140773180` | [Queue typed resource component creation](geography.md#rva-0x00773180) | Queue typed resource component creation | C |
| `0x00773910` | `0x140773910` | [planet component materialization](geography.md#rva-0x00773910) | planet component materialization | C |
| `0x00773be0` | `0x140773be0` | [Participate in typed resource component creation and copy](geography.md#rva-0x00773be0) | Participate in typed resource component creation and copy | C |
| `0x00773d80` | `0x140773d80` | [Initialize surface-tree owner fields](geography.md#rva-0x00773d80) | Initialize surface-tree owner fields | C |
| `0x00774970` | `0x140774970` | [Remove a typed resource component edge](geography.md#rva-0x00774970) | Remove a typed resource component edge | C |
| `0x00774ee0` | `0x140774ee0` | [Forward planetary overlay update](workshop.md#rva-0x00774ee0) | Forward planetary overlay update | C |
| `0x007772c0` | `0x1407772c0` | [Dispatch planetary overlay callback](workshop.md#rva-0x007772c0) | Dispatch planetary overlay callback | C |
| `0x00777560` | `0x140777560` | [Store planetary overlay tuple](workshop.md#rva-0x00777560) | Store planetary overlay tuple | C |
| `0x007791d0` | `0x1407791d0` | [Typed PNDT lookup validates form-type byte 0xba](geography.md#rva-0x007791d0) | Typed PNDT lookup validates form-type byte 0xba | C |
| `0x00779300` | `0x140779300` | [Register planetary overlay context](workshop.md#rva-0x00779300) | Register planetary overlay context | C |
| `0x00779610` | `0x140779610` | [Route PNDT resource component update](geography.md#rva-0x00779610) | Route PNDT resource component update | C |
| `0x00779760` | `0x140779760` | [PNDT RSCS and per-biome fallback MT initializer; distinct earlier seed](geography.md#rva-0x00779760) | PNDT RSCS and per-biome fallback MT initializer; distinct earlier seed | C |
| `0x0077bce0` | `0x14077bce0` | [Enumerate resource runtime pointers into scratch storage](geography.md#rva-0x0077bce0) | Enumerate resource runtime pointers into scratch storage | C |
| `0x0077c470` | `0x14077c470` | [Dispatch PNDT resource component update](geography.md#rva-0x0077c470) | Dispatch PNDT resource component update | C |
| `0x0077d090` | `0x14077d090` | [Participate in the PlanetData resource input route](geography.md#rva-0x0077d090) | Participate in the PlanetData resource input route | C |
| `0x0077d960` | `0x14077d960` | [Filter and sort linked worlds](geography.md#rva-0x0077d960) | Filter and sort linked worlds | C |
| `0x0077def0` | `0x14077def0` | [Producer-to-consumer closure · entry](workshop.md#rva-0x0077def0) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x0077e350` | `0x14077e350` | [Producer-to-consumer closure · entry](workshop.md#rva-0x0077e350) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x0077f6e0` | `0x14077f6e0` | [Producer-to-consumer closure · entry](workshop.md#rva-0x0077f6e0) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x0077f900` | `0x14077f900` | [Producer-to-consumer closure · entry](workshop.md#rva-0x0077f900) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x0077fbc0` | `0x14077fbc0` | [Dispatch residual frame handling to the integer-grid route](workshop.md#rva-0x0077fbc0) | Dispatch residual frame handling to the integer-grid route | C |
| `0x0077fc20` | `0x14077fc20` | [Split local placement into indexed pair and residual](workshop.md#rva-0x0077fc20) | Combines the indexed displacement with reference XYZ and retains the fractional residual separately. | A |
| `0x00780710` | `0x140780710` | [Producer-to-consumer closure · entry](workshop.md#rva-0x00780710) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x00780a50` | `0x140780a50` | [Producer-to-consumer closure · entry](workshop.md#rva-0x00780a50) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x00780aa0` | `0x140780aa0` | [Producer-to-consumer closure · entry](workshop.md#rva-0x00780aa0) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x00781390` | `0x140781390` | [Producer-to-consumer closure · entry](workshop.md#rva-0x00781390) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x00781c80` | `0x140781c80` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00781c80) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x00781cc0` | `0x140781cc0` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00781cc0) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x00782070` | `0x140782070` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00782070) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x007823d0` | `0x1407823d0` | [Active branch checkpoints · entry](geography.md#rva-0x007823d0) | Original report discusses this roster entry under Active branch checkpoints. | C |
| `0x007824b0` | `0x1407824b0` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x007824b0) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x00782690` | `0x140782690` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x00782690) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x00782910` | `0x140782910` | [Checkpoint 3 — incremental claims and upstream dependencies · entry](geography.md#rva-0x00782910) | Original report discusses this roster entry under Checkpoint 3 — incremental claims and upstream dependencies. | C |
| `0x00783080` | `0x140783080` | [d5ad input provenance · entry](geography.md#rva-0x00783080) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x00783480` | `0x140783480` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x00783480) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x00783600` | `0x140783600` | [Checkpoint 3 — incremental claims and upstream dependencies · entry](geography.md#rva-0x00783600) | Original report discusses this roster entry under Checkpoint 3 — incremental claims and upstream dependencies. | C |
| `0x007836f0` | `0x1407836f0` | [Checkpoint 3 — incremental claims and upstream dependencies · entry](geography.md#rva-0x007836f0) | Original report discusses this roster entry under Checkpoint 3 — incremental claims and upstream dependencies. | C |
| `0x00784530` | `0x140784530` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00784530) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x00784680` | `0x140784680` | [Install Landscape module body context](geography.md#rva-0x00784680) | Install Landscape module body context | C |
| `0x007846d0` | `0x1407846d0` | [Release landscape Grid owners on reset](geography.md#rva-0x007846d0) | Release landscape Grid owners on reset | C |
| `0x00784730` | `0x140784730` | [Release the Landscape Grid reference](geography.md#rva-0x00784730) | Decrements the retained Grid reference and dispatches destruction on final release. | B |
| `0x007847b0` | `0x1407847b0` | [Construct Landscape Grids](geography.md#rva-0x007847b0) | Construct Landscape Grids | C |
| `0x00784c30` | `0x140784c30` | [Do the enclosing scopes poison ordinary new source births? · entry](geography.md#rva-0x00784c30) | Original report discusses this roster entry under Do the enclosing scopes poison ordinary new source births?. | C |
| `0x00784c40` | `0x140784c40` | [d5ad input provenance · entry](geography.md#rva-0x00784c40) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x00785190` | `0x140785190` | [Finalize Landscape Grid preparation](geography.md#rva-0x00785190) | Finalize Landscape Grid preparation | C |
| `0x00785490` | `0x140785490` | [Construct overlay Grid source](geography.md#rva-0x00785490) | Construct overlay Grid source | C |
| `0x00785610` | `0x140785610` | [Update Landscape file origin](geography.md#rva-0x00785610) | Update Landscape file origin | C |
| `0x007856b0` | `0x1407856b0` | [Dispatch Landscape Grid shift](geography.md#rva-0x007856b0) | Dispatch Landscape Grid shift | C |
| `0x00786230` | `0x140786230` | [Starting-input and initialization challenge: active positive route · entry](geography.md#rva-0x00786230) | Original report discusses this roster entry under Starting-input and initialization challenge: active positive route. | C |
| `0x007862a0` | `0x1407862a0` | [Construct base Grid source](geography.md#rva-0x007862a0) | Construct base Grid source | C |
| `0x00786690` | `0x140786690` | [Look up the primary Locations body context](interfaces.md#rva-0x00786690) | Look up the primary Locations body context | C |
| `0x007873d0` | `0x1407873d0` | [D5AD handoff and contrary cases · entry](geography.md#rva-0x007873d0) | Original report discusses this roster entry under D5AD handoff and contrary cases. | C |
| `0x00787830` | `0x140787830` | [Construct and register the manager's ProcGen owner](geography.md#rva-0x00787830) | Stores the manager's ProcGen pointer and registers it for module dispatch. | B |
| `0x00788b60` | `0x140788b60` | [Delete the ProcGen manager owner](geography.md#rva-0x00788b60) | Delete the ProcGen manager owner | C |
| `0x00788bc0` | `0x140788bc0` | [Destroy context manager](geography.md#rva-0x00788bc0) | Destroy context manager | C |
| `0x00788e70` | `0x140788e70` | [Reset current resource owner](geography.md#rva-0x00788e70) | Reset current resource owner | C |
| `0x007895a0` | `0x1407895a0` | [Wrap the ordinary full-load ProcGen reset](geography.md#rva-0x007895a0) | Wrap the ordinary full-load ProcGen reset | C |
| `0x007896d0` | `0x1407896d0` | [Save loading and interior residency · entry](geography.md#rva-0x007896d0) | Original report discusses this roster entry under Save loading and interior residency. | C |
| `0x00789850` | `0x140789850` | [Reset resource descriptors without owner replacement](geography.md#rva-0x00789850) | Reset resource descriptors without owner replacement | C |
| `0x00789ce0` | `0x140789ce0` | [Install a runtime manager owner and descriptor](geography.md#rva-0x00789ce0) | Selects reset or reinitialization behavior from actual owner and component inputs. | B |
| `0x0078a120` | `0x14078a120` | [Bind runtime owner PNDT](geography.md#rva-0x0078a120) | Bind runtime owner PNDT | C |
| `0x0078a5b0` | `0x14078a5b0` | [Typed scalar producer and queued update after descriptor success](geography.md#rva-0x0078a5b0) | Typed scalar producer and queued update after descriptor success | C |
| `0x0078abc0` | `0x14078abc0` | [Select biome input with world or encounter overrides](geography.md#rva-0x0078abc0) | Select biome input with world or encounter overrides | C |
| `0x0078af30` | `0x14078af30` | [Focus-invalid initialization refinement · entry](geography.md#rva-0x0078af30) | Original report discusses this roster entry under Focus-invalid initialization refinement. | C |
| `0x0078b030` | `0x14078b030` | [Install current resource context](geography.md#rva-0x0078b030) | Install current resource context | C |
| `0x0078bc30` | `0x14078bc30` | [Complete resource context transition](geography.md#rva-0x0078bc30) | Complete resource context transition | C |
| `0x0078c060` | `0x14078c060` | [Checkpoint: verified inputs and first five export passes · entry](geography.md#rva-0x0078c060) | Original report discusses this roster entry under Checkpoint: verified inputs and first five export passes. | C |
| `0x0078c190` | `0x14078c190` | [Dispatch ordered manager shift callbacks](geography.md#rva-0x0078c190) | Dispatch ordered manager shift callbacks | C |
| `0x0078c290` | `0x14078c290` | [Update context at shift boundary](geography.md#rva-0x0078c290) | Update context at shift boundary | C |
| `0x0078c3a0` | `0x14078c3a0` | [Positive native chain and writer closure · entry](geography.md#rva-0x0078c3a0) | Original report discusses this roster entry under Positive native chain and writer closure. | C |
| `0x0078c4e0` | `0x14078c4e0` | [current manager context resolution](geography.md#rva-0x0078c4e0) | current manager context resolution | B |
| `0x0078c570` | `0x14078c570` | [Checkpoint: verified inputs and first five export passes · entry](geography.md#rva-0x0078c570) | Original report discusses this roster entry under Checkpoint: verified inputs and first five export passes. | C |
| `0x0078c5f0` | `0x14078c5f0` | [Evaluate the focus movement and shift threshold](geography.md#rva-0x0078c5f0) | Evaluate the focus movement and shift threshold | C |
| `0x0078c940` | `0x14078c940` | [Initialization and successful-construction obligations · entry](geography.md#rva-0x0078c940) | Original report discusses this roster entry under Initialization and successful-construction obligations. | C |
| `0x0078ce00` | `0x14078ce00` | [Run the manager-exclusive terrain shift](geography.md#rva-0x0078ce00) | Run the manager-exclusive terrain shift | C |
| `0x0078cf00` | `0x14078cf00` | [Action-to-transition table · entry](geography.md#rva-0x0078cf00) | Original report discusses this roster entry under Action-to-transition table. | C |
| `0x0078d090` | `0x14078d090` | [Clear retained world handles during cleanup](workshop.md#rva-0x0078d090) | Clear retained world handles during cleanup | C |
| `0x0078d1f0` | `0x14078d1f0` | [Fractional position producers and consumers · entry](workshop.md#rva-0x0078d1f0) | Original report discusses this roster entry under Fractional position producers and consumers. | C |
| `0x0078d2c0` | `0x14078d2c0` | [Producer-to-consumer closure · entry](workshop.md#rva-0x0078d2c0) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x0078d370` | `0x14078d370` | [Further resolved branches (exports 23–28) · entry](geography.md#rva-0x0078d370) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x0078d4b0` | `0x14078d4b0` | [Exact common prefix and the attempt to falsify it · entry](geography.md#rva-0x0078d4b0) | Original report discusses this roster entry under Exact common prefix and the attempt to falsify it. | C |
| `0x0078d660` | `0x14078d660` | [half-step grid-to-square path](workshop.md#rva-0x0078d660) | half-step grid-to-square path | C |
| `0x0078d7b0` | `0x14078d7b0` | [Pack generation cell key](geography.md#rva-0x0078d7b0) | Pack generation cell key | C |
| `0x0078d930` | `0x14078d930` | [Typed restoration and packed origin (exports 42–49) · entry](workshop.md#rva-0x0078d930) | Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49). | C |
| `0x0078e900` | `0x14078e900` | [ABI, loss and capability comparison · entry](geography.md#rva-0x0078e900) | Original report discusses this roster entry under ABI, loss and capability comparison. | C |
| `0x0078ee90` | `0x14078ee90` | [spatial biome resolver](geography.md#rva-0x0078ee90) | spatial biome resolver | B |
| `0x0078efa0` | `0x14078efa0` | [numeric base BIOM lookup](geography.md#rva-0x0078efa0) | numeric base BIOM lookup | C |
| `0x0078f0b0` | `0x14078f0b0` | [Drain tracked resource generation](geography.md#rva-0x0078f0b0) | Drain tracked resource generation | C |
| `0x0078f480` | `0x14078f480` | [Checkpoint: complete first-resource destinations and phase boundaries · entry](geography.md#rva-0x0078f480) | Original report discusses this roster entry under Checkpoint: complete first-resource destinations and phase boundaries. | C |
| `0x0078f670` | `0x14078f670` | [owned ProcGen pointer cleanup](geography.md#rva-0x0078f670) | owned ProcGen pointer cleanup | B |
| `0x0078f810` | `0x14078f810` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x0078f810) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x0078faa0` | `0x14078faa0` | [Release the retained Grid reference](geography.md#rva-0x0078faa0) | Release the retained Grid reference | C |
| `0x0078fc90` | `0x14078fc90` | [deleting ProcGen destructor](geography.md#rva-0x0078fc90) | deleting ProcGen destructor | B |
| `0x007906e0` | `0x1407906e0` | [Send resource generation completion command](geography.md#rva-0x007906e0) | Send resource generation completion command | C |
| `0x00797dc0` | `0x140797dc0` | [terrain+1ec/+1f0 rebase caller](workshop.md#rva-0x00797dc0) | terrain+1ec/+1f0 rebase caller | C |
| `0x00797e90` | `0x140797e90` | [Handle alternate shift path](geography.md#rva-0x00797e90) | Handle alternate shift path | C |
| `0x00798030` | `0x140798030` | [Select active or requested frame before overlay activation](workshop.md#rva-0x00798030) | Select active or requested frame before overlay activation | C |
| `0x00798130` | `0x140798130` | [State classification and its limits · entry](geography.md#rva-0x00798130) | Original report discusses this roster entry under State classification and its limits. | C |
| `0x007986d0` | `0x1407986d0` | [active/requested pair differences and activation](workshop.md#rva-0x007986d0) | active/requested pair differences and activation | C |
| `0x0079a310` | `0x14079a310` | [Forward into the nonlocal ProcGen route](geography.md#rva-0x0079a310) | Forward into the nonlocal ProcGen route | C |
| `0x0079a330` | `0x14079a330` | [Attempt a per-cell generated resource region](geography.md#rva-0x0079a330) | Performs a bounded resource-region attempt and can append into the holder's resource collection. | B |
| `0x0079b020` | `0x14079b020` | [generation overlap geometry test](geography.md#rva-0x0079b020) | generation overlap geometry test | B |
| `0x0079b520` | `0x14079b520` | [Generate regions into a source holder](geography.md#rva-0x0079b520) | Uses source-local and geographic query inputs to populate a resource holder. | A |
| `0x0079c470` | `0x14079c470` | [generation cell traversal](geography.md#rva-0x0079c470) | generation cell traversal | B |
| `0x0079c540` | `0x14079c540` | [resource descriptor selection](geography.md#rva-0x0079c540) | resource descriptor selection | B |
| `0x0079c5e0` | `0x14079c5e0` | [alternate biome descriptor selection](geography.md#rva-0x0079c5e0) | alternate biome descriptor selection | B |
| `0x0079c900` | `0x14079c900` | [Producer to provider · entry](geography.md#rva-0x0079c900) | Original report discusses this roster entry under Producer to provider. | C |
| `0x0079cd50` | `0x14079cd50` | [Validate task descriptor](geography.md#rva-0x0079cd50) | Validate task descriptor | C |
| `0x0079ce00` | `0x14079ce00` | [Admit and transfer a manager reader to nested work](geography.md#rva-0x0079ce00) | Admit and transfer a manager reader to nested work | C |
| `0x0079d080` | `0x14079d080` | [Handle region task payload](geography.md#rva-0x0079d080) | Handle region task payload | C |
| `0x0079d660` | `0x14079d660` | [ProcGen initialization](geography.md#rva-0x0079d660) | ProcGen initialization | B |
| `0x0079d910` | `0x14079d910` | [ProcGen destruction](geography.md#rva-0x0079d910) | ProcGen destruction | B |
| `0x0079da80` | `0x14079da80` | [PCM persisted placement span into ProcGen preparation record collection](geography.md#rva-0x0079da80) | PCM persisted placement span into ProcGen preparation record collection | C |
| `0x0079ddf0` | `0x14079ddf0` | [ProcGen broad reset](geography.md#rva-0x0079ddf0) | ProcGen broad reset | B |
| `0x0079df60` | `0x14079df60` | [Transition matrix · entry](geography.md#rva-0x0079df60) | Original report discusses this roster entry under Transition matrix. | C |
| `0x0079df70` | `0x14079df70` | [resident region point-query traversal](geography.md#rva-0x0079df70) | resident region point-query traversal | B |
| `0x0079e060` | `0x14079e060` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x0079e060) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x0079e220` | `0x14079e220` | [Preparation, terrain work and conditional protection · entry](geography.md#rva-0x0079e220) | Original report discusses this roster entry under Preparation, terrain work and conditional protection. | C |
| `0x0079e3b0` | `0x14079e3b0` | [PCM/content preparation has a different mutable map · entry](geography.md#rva-0x0079e3b0) | Original report discusses this roster entry under PCM/content preparation has a different mutable map. | C |
| `0x0079e6d0` | `0x14079e6d0` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x0079e6d0) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x0079ea40` | `0x14079ea40` | [Selected placement local range preparation helper](geography.md#rva-0x0079ea40) | Selected placement local range preparation helper | C |
| `0x0079ebe0` | `0x14079ebe0` | [Supply geographic phase to prepared density selection](geography.md#rva-0x0079ebe0) | Supply geographic phase to prepared density selection | C |
| `0x0079ee50` | `0x14079ee50` | [PCM/content preparation has a different mutable map · entry](geography.md#rva-0x0079ee50) | Original report discusses this roster entry under PCM/content preparation has a different mutable map. | C |
| `0x0079f860` | `0x14079f860` | [Provide source population for a terrain query](geography.md#rva-0x0079f860) | Selects source contributors and conditionally reuses or constructs a ProcGen population. | A |
| `0x007a0820` | `0x1407a0820` | [source raster cache path](geography.md#rva-0x007a0820) | source raster cache path | B |
| `0x007a0bf0` | `0x1407a0bf0` | [resource entry processing iterator](geography.md#rva-0x007a0bf0) | resource entry processing iterator | B |
| `0x007a0cc0` | `0x1407a0cc0` | [resource definition aggregate processing](geography.md#rva-0x007a0cc0) | resource definition aggregate processing | B |
| `0x007a0fa0` | `0x1407a0fa0` | [neighbor resource preparation](geography.md#rva-0x007a0fa0) | neighbor resource preparation | B |
| `0x007a1260` | `0x1407a1260` | [neighbor resource task request](geography.md#rva-0x007a1260) | neighbor resource task request | B |
| `0x007a1580` | `0x1407a1580` | [Bounded rectangular demand reaches coordinate dependency request; task-mediated ancestry is…](geography.md#rva-0x007a1580) | Bounded rectangular demand reaches coordinate dependency request; task-mediated ancestry is documented by D5D. | C |
| `0x007a1940` | `0x1407a1940` | [alternate provider consumer](geography.md#rva-0x007a1940) | alternate provider consumer | B |
| `0x007a1f80` | `0x1407a1f80` | [Active branch checkpoints · entry](geography.md#rva-0x007a1f80) | Original report discusses this roster entry under Active branch checkpoints. | C |
| `0x007a38c0` | `0x1407a38c0` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007a38c0) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007a3b00` | `0x1407a3b00` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007a3b00) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007a4730` | `0x1407a4730` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007a4730) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007a4b90` | `0x1407a4b90` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007a4b90) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007a4cc0` | `0x1407a4cc0` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007a4cc0) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007a50d0` | `0x1407a50d0` | [ProcGen activation state change](workshop.md#rva-0x007a50d0) | ProcGen activation state change | C |
| `0x007a5210` | `0x1407a5210` | [ProcGen active update](workshop.md#rva-0x007a5210) | ProcGen active update | C |
| `0x007a5790` | `0x1407a5790` | [Consume and release a retained population holder](geography.md#rva-0x007a5790) | Consume and release a retained population holder | C |
| `0x007a59f0` | `0x1407a59f0` | [Mutation and backing-allocation coverage · entry](geography.md#rva-0x007a59f0) | Original report discusses this roster entry under Mutation and backing-allocation coverage. | C |
| `0x007a6150` | `0x1407a6150` | [Bounds consumer installer](workshop.md#rva-0x007a6150) | Bounds consumer installer | C |
| `0x007a6540` | `0x1407a6540` | [Typed decal bounds predicate](workshop.md#rva-0x007a6540) | Typed decal bounds predicate | C |
| `0x007a6690` | `0x1407a6690` | [ProcGen radius reset](workshop.md#rva-0x007a6690) | ProcGen radius reset | C |
| `0x007a6700` | `0x1407a6700` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007a6700) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007a7060` | `0x1407a7060` | [Create reference with world context](workshop.md#rva-0x007a7060) | Create reference with world context | C |
| `0x007a8d30` | `0x1407a8d30` | [density dependency gathering](geography.md#rva-0x007a8d30) | density dependency gathering | B |
| `0x007a9690` | `0x1407a9690` | [Release a holder reference on cleanup](geography.md#rva-0x007a9690) | Release a holder reference on cleanup | C |
| `0x007a97c0` | `0x1407a97c0` | [Resource u32 lookup and assignment to caller output holder; not cached-entry replacement](geography.md#rva-0x007a97c0) | Resource u32 lookup and assignment to caller output holder; not cached-entry replacement | C |
| `0x007a98b0` | `0x1407a98b0` | [Release the resource collection reference](geography.md#rva-0x007a98b0) | Release the resource collection reference | C |
| `0x007aa5f0` | `0x1407aa5f0` | [Source-key insertion; existing/new result; grow helper; provider assigns retained holder](geography.md#rva-0x007aa5f0) | Source-key insertion; existing/new result; grow helper; provider assigns retained holder | C |
| `0x007aa8a0` | `0x1407aa8a0` | [source map entry release](geography.md#rva-0x007aa8a0) | source map entry release | B |
| `0x007aa9b0` | `0x1407aa9b0` | [Reserve a slot for the resource collection](geography.md#rva-0x007aa9b0) | Reserve a slot for the resource collection | C |
| `0x007aab10` | `0x1407aab10` | [Resource map clear releases collection; final release nested cleanup then 0x18 free](geography.md#rva-0x007aab10) | Resource map clear releases collection; final release nested cleanup then 0x18 free | C |
| `0x007aabd0` | `0x1407aabd0` | [Assign the reference-counted caller output holder](geography.md#rva-0x007aabd0) | Assign the reference-counted caller output holder | C |
| `0x007ab510` | `0x1407ab510` | [Handle displaced outer-map holder ownership](geography.md#rva-0x007ab510) | Handle displaced outer-map holder ownership | C |
| `0x007ab6a0` | `0x1407ab6a0` | [Destroy the erased collection and point storage](geography.md#rva-0x007ab6a0) | Destroy the erased collection and point storage | C |
| `0x007ab730` | `0x1407ab730` | [Resolve source-table collisions during relocation](geography.md#rva-0x007ab730) | Resolve source-table collisions during relocation | C |
| `0x007abaf0` | `0x1407abaf0` | [Rehash the outer source-pointer map](geography.md#rva-0x007abaf0) | Rehash the outer source-pointer map | C |
| `0x007abc90` | `0x1407abc90` | [Rehash resource collection entries](geography.md#rva-0x007abc90) | Rehash resource collection entries | C |
| `0x007abe80` | `0x1407abe80` | [Native and saved-receipt checkpoint · entry](geography.md#rva-0x007abe80) | Original report discusses this roster entry under Native and saved-receipt checkpoint. | C |
| `0x007ac0d0` | `0x1407ac0d0` | [Deep point copy; separate shallow refcount holder assignment; rehash transfer helpers](geography.md#rva-0x007ac0d0) | Deep point copy; separate shallow refcount holder assignment; rehash transfer helpers | C |
| `0x007ac260` | `0x1407ac260` | [Destroy a region collection after final release](geography.md#rva-0x007ac260) | Destroy a region collection after final release | C |
| `0x007ac2f0` | `0x1407ac2f0` | [Append region; copy nested points; final nested allocation cleanup](geography.md#rva-0x007ac2f0) | Append region; copy nested points; final nested allocation cleanup | C |
| `0x007ac3d0` | `0x1407ac3d0` | [Append an accepted PCM preparation record](geography.md#rva-0x007ac3d0) | Append an accepted PCM preparation record | C |
| `0x007ac4d0` | `0x1407ac4d0` | [PCM/content preparation has a different mutable map · entry](geography.md#rva-0x007ac4d0) | Original report discusses this roster entry under PCM/content preparation has a different mutable map. | C |
| `0x007ad160` | `0x1407ad160` | [PCM/content preparation has a different mutable map · entry](geography.md#rva-0x007ad160) | Original report discusses this roster entry under PCM/content preparation has a different mutable map. | C |
| `0x007af1a0` | `0x1407af1a0` | [generation overlap iterator](geography.md#rva-0x007af1a0) | generation overlap iterator | B |
| `0x007af470` | `0x1407af470` | [Order candidate resources by descending rarity](geography.md#rva-0x007af470) | Order candidate resources by descending rarity | C |
| `0x007af790` | `0x1407af790` | [Producer to provider · entry](geography.md#rva-0x007af790) | Original report discusses this roster entry under Producer to provider. | C |
| `0x007af970` | `0x1407af970` | [Collect rectangular coordinate work](geography.md#rva-0x007af970) | Collect rectangular coordinate work | C |
| `0x007afae0` | `0x1407afae0` | [Descriptor, focus and request identity · entry](geography.md#rva-0x007afae0) | Original report discusses this roster entry under Descriptor, focus and request identity. | C |
| `0x007afd70` | `0x1407afd70` | [Producer to provider · entry](geography.md#rva-0x007afd70) | Original report discusses this roster entry under Producer to provider. | C |
| `0x007affb0` | `0x1407affb0` | [Inspect retained resource regions for the point query](geography.md#rva-0x007affb0) | Inspect retained resource regions for the point query | C |
| `0x007b0880` | `0x1407b0880` | [Workshop bounds thunk](workshop.md#rva-0x007b0880) | Workshop bounds thunk | C |
| `0x007b0980` | `0x1407b0980` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007b0980) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007b0990` | `0x1407b0990` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007b0990) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007b1410` | `0x1407b1410` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007b1410) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007b1420` | `0x1407b1420` | [Dispatch region task](geography.md#rva-0x007b1420) | Dispatch region task | C |
| `0x007b1460` | `0x1407b1460` | [Preflight cell-range placement demand](geography.md#rva-0x007b1460) | Preflight cell-range placement demand | C |
| `0x007b19f0` | `0x1407b19f0` | [Release the nested node's manager reader](geography.md#rva-0x007b19f0) | Release the nested node's manager reader | C |
| `0x007b1b10` | `0x1407b1b10` | [Destroy the detached continuation](geography.md#rva-0x007b1b10) | Destroy the detached continuation | C |
| `0x007b1bd0` | `0x1407b1bd0` | [Forwarded receivers and captured contexts · entry](geography.md#rva-0x007b1bd0) | Original report discusses this roster entry under Forwarded receivers and captured contexts. | C |
| `0x007b1fe0` | `0x1407b1fe0` | [Reach ordinary resource demand](geography.md#rva-0x007b1fe0) | Reach ordinary resource demand | C |
| `0x007b1ff0` | `0x1407b1ff0` | [Construct manager content-module subobject](geography.md#rva-0x007b1ff0) | Construct manager content-module subobject | C |
| `0x007b2340` | `0x1407b2340` | [Wait on resource site during reset](geography.md#rva-0x007b2340) | Wait on resource site during reset | C |
| `0x007b2370` | `0x1407b2370` | [Demand prefix, admitted pair and historical invocation state · wrapper](geography.md#rva-0x007b2370) | Original report discusses this roster entry under Demand prefix, admitted pair and historical invocation state. | C |
| `0x007b2390` | `0x1407b2390` | [Acquire focus-driven resource handles](geography.md#rva-0x007b2390) | Acquire focus-driven resource handles | C |
| `0x007b2880` | `0x1407b2880` | [Grid shift/retirement and focus-derived bounds expose runtime inputs and outer…](geography.md#rva-0x007b2880) | Grid shift/retirement and focus-derived bounds expose runtime inputs and outer synchronization boundary. | C |
| `0x007b30c0` | `0x1407b30c0` | [Demand prefix, admitted pair and historical invocation state · entry](geography.md#rva-0x007b30c0) | Original report discusses this roster entry under Demand prefix, admitted pair and historical invocation state. | C |
| `0x007b3aa0` | `0x1407b3aa0` | [Grid shift/retirement and focus-derived bounds expose runtime inputs and outer…](geography.md#rva-0x007b3aa0) | Grid shift/retirement and focus-derived bounds expose runtime inputs and outer synchronization boundary. | C |
| `0x007b3c50` | `0x1407b3c50` | [Grid shift/retirement and focus-derived bounds expose runtime inputs and outer…](geography.md#rva-0x007b3c50) | Grid shift/retirement and focus-derived bounds expose runtime inputs and outer synchronization boundary. | C |
| `0x007b3cd0` | `0x1407b3cd0` | [Find existing rectangular resource entries](geography.md#rva-0x007b3cd0) | Find existing rectangular resource entries | C |
| `0x007b4750` | `0x1407b4750` | [Initialization and successful-construction obligations · entry](geography.md#rva-0x007b4750) | Original report discusses this roster entry under Initialization and successful-construction obligations. | C |
| `0x007b4770` | `0x1407b4770` | [related resource database cleanup](geography.md#rva-0x007b4770) | related resource database cleanup | B |
| `0x007b4bb0` | `0x1407b4bb0` | [layer dependency preparation](geography.md#rva-0x007b4bb0) | layer dependency preparation | B |
| `0x007b5160` | `0x1407b5160` | [generation lifecycle consumer](geography.md#rva-0x007b5160) | generation lifecycle consumer | B |
| `0x007b5470` | `0x1407b5470` | [ProcGenLayersDB entry acquisition](geography.md#rva-0x007b5470) | ProcGenLayersDB entry acquisition | B |
| `0x007b55b0` | `0x1407b55b0` | [layer task registration](geography.md#rva-0x007b55b0) | layer task registration | B |
| `0x007b5850` | `0x1407b5850` | [layer task dispatch wrapper](geography.md#rva-0x007b5850) | layer task dispatch wrapper | B |
| `0x007b5870` | `0x1407b5870` | [Single-cell placement demand callback](geography.md#rva-0x007b5870) | Single-cell placement demand callback | C |
| `0x007b58a0` | `0x1407b58a0` | [layer task construction](geography.md#rva-0x007b58a0) | layer task construction | B |
| `0x007b5a00` | `0x1407b5a00` | [layer entry request](geography.md#rva-0x007b5a00) | layer entry request | B |
| `0x007b5bd0` | `0x1407b5bd0` | [Gated source worker consumes PCM placements and publishes request preparation collection](geography.md#rva-0x007b5bd0) | Gated source worker consumes PCM placements and publishes request preparation collection | C |
| `0x007b5dd0` | `0x1407b5dd0` | [Link coordinate dependency](geography.md#rva-0x007b5dd0) | Link coordinate dependency | C |
| `0x007b6360` | `0x1407b6360` | [Participate in body-world naming during overlay construction](workshop.md#rva-0x007b6360) | Participate in body-world naming during overlay construction | C |
| `0x007b75b0` | `0x1407b75b0` | [scanner species update wrapper](production.md#rva-0x007b75b0) | scanner species update wrapper | B |
| `0x007b77d0` | `0x1407b77d0` | [increment scans and grant keyword prefix](production.md#rva-0x007b77d0) | increment scans and grant keyword prefix | B |
| `0x007bc300` | `0x1407bc300` | [Prepare temporary resource dictionary](geography.md#rva-0x007bc300) | Prepare temporary resource dictionary | C |
| `0x007bc3d0` | `0x1407bc3d0` | [Collect a runtime owner's supplemental resource lists](geography.md#rva-0x007bc3d0) | Traverses owner/type components and exchanges ordered supplemental arrays into a root-keyed map. | A |
| `0x007bcdc0` | `0x1407bcdc0` | [Select active body ECS context](workshop.md#rva-0x007bcdc0) | Select active body ECS context | C |
| `0x007bcfb0` | `0x1407bcfb0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x007bcfb0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x007be780` | `0x1407be780` | [Derive a snapped or indexed world point](workshop.md#rva-0x007be780) | Derive a snapped or indexed world point | C |
| `0x007bea00` | `0x1407bea00` | [Derive the paired snapped or indexed world point](workshop.md#rva-0x007bea00) | Derive the paired snapped or indexed world point | C |
| `0x007c0720` | `0x1407c0720` | [current-key admission predicate](geography.md#rva-0x007c0720) | current-key admission predicate | B |
| `0x007c07b0` | `0x1407c07b0` | [bounded current epoch key construction](geography.md#rva-0x007c07b0) | bounded current epoch key construction | B |
| `0x007c6080` | `0x1407c6080` | [Fixed placement predecessor · entry](geography.md#rva-0x007c6080) | Original report discusses this roster entry under Fixed placement predecessor. | C |
| `0x00839820` | `0x140839820` | [body time scalar wrapper](production.md#rva-0x00839820) | body time scalar wrapper | B |
| `0x00839900` | `0x140839900` | [body time conversion provider](production.md#rva-0x00839900) | body time conversion provider | B |
| `0x00848660` | `0x140848660` | [Supply terrain samples for height adjustment](workshop.md#rva-0x00848660) | Supply terrain samples for height adjustment | C |
| `0x00849670` | `0x140849670` | [Construct surface Grid source](geography.md#rva-0x00849670) | Construct surface Grid source | C |
| `0x0084f2a0` | `0x14084f2a0` | [Select keyed fallback terrain sample](workshop.md#rva-0x0084f2a0) | Select keyed fallback terrain sample | C |
| `0x00850f30` | `0x140850f30` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x00850f30) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x00851b40` | `0x140851b40` | [orientation/stride setup](workshop.md#rva-0x00851b40) | orientation/stride setup | C |
| `0x00851d20` | `0x140851d20` | [centered orientation matrix operation](workshop.md#rva-0x00851d20) | centered orientation matrix operation | C |
| `0x00851e10` | `0x140851e10` | [TerrainDB is a real scheduling and context-lifetime dependency · entry](geography.md#rva-0x00851e10) | Original report discusses this roster entry under TerrainDB is a real scheduling and context-lifetime dependency. | C |
| `0x00852100` | `0x140852100` | [TerrainDB is a real scheduling and context-lifetime dependency · entry](geography.md#rva-0x00852100) | Original report discusses this roster entry under TerrainDB is a real scheduling and context-lifetime dependency. | C |
| `0x00852460` | `0x140852460` | [TerrainDB is a real scheduling and context-lifetime dependency · entry](geography.md#rva-0x00852460) | Original report discusses this roster entry under TerrainDB is a real scheduling and context-lifetime dependency. | C |
| `0x00852f20` | `0x140852f20` | [Support reflected atmosphere source loading](geography.md#rva-0x00852f20) | Support reflected atmosphere source loading | C |
| `0x008bda70` | `0x1408bda70` | [Register atmosphere resource field metadata](geography.md#rva-0x008bda70) | Register atmosphere resource field metadata | C |
| `0x008e2df0` | `0x1408e2df0` | [Clear and reserve the bound atmosphere list](geography.md#rva-0x008e2df0) | Clear and reserve the bound atmosphere list | C |
| `0x00904560` | `0x140904560` | [Read the ExtraDE snap relation](workshop.md#rva-0x00904560) | Read the ExtraDE snap relation | C |
| `0x00904d60` | `0x140904d60` | [Commit both snap endpoint relations](workshop.md#rva-0x00904d60) | Commit both snap endpoint relations | C |
| `0x00904f30` | `0x140904f30` | [Revert automatic behavior on snap disconnect](workshop.md#rva-0x00904f30) | Revert automatic behavior on snap disconnect | C |
| `0x00910690` | `0x140910690` | [Derive reference planetary context](production.md#rva-0x00910690) | Derive reference planetary context | C |
| `0x00910af0` | `0x140910af0` | [Supply the fallback Locations body context](interfaces.md#rva-0x00910af0) | Supply the fallback Locations body context | C |
| `0x00910bd0` | `0x140910bd0` | [Footer gaps investigated · entry](workshop.md#rva-0x00910bd0) | Original report discusses this roster entry under Footer gaps investigated. | C |
| `0x00911600` | `0x140911600` | [Participate in the null-result location fallback](workshop.md#rva-0x00911600) | Participate in the null-result location fallback | C |
| `0x00911b70` | `0x140911b70` | [Footer gaps investigated · entry](workshop.md#rva-0x00911b70) | Original report discusses this roster entry under Footer gaps investigated. | C |
| `0x00922b30` | `0x140922b30` | [Resolve the child handle in open-state follow-up](power.md#rva-0x00922b30) | Resolve the child handle in open-state follow-up | C |
| `0x009403e0` | `0x1409403e0` | [base property-sheet component resolution](production.md#rva-0x009403e0) | base property-sheet component resolution | B |
| `0x0094e3d0` | `0x14094e3d0` | [Grid, terrain and density preparation · entry](geography.md#rva-0x0094e3d0) | Original report discusses this roster entry under Grid, terrain and density preparation. | C |
| `0x009518b0` | `0x1409518b0` | [Initialize the relevant terrain module state](geography.md#rva-0x009518b0) | Initialize the relevant terrain module state | C |
| `0x0096ae90` | `0x14096ae90` | [SFBK DNAM to Block+40/+44](workshop.md#rva-0x0096ae90) | SFBK DNAM to Block+40/+44 | C |
| `0x0096b8e0` | `0x14096b8e0` | [Existing linked tree reuse versus permitted missing-tree construction](geography.md#rva-0x0096b8e0) | Existing linked tree reuse versus permitted missing-tree construction | C |
| `0x0096b9c0` | `0x14096b9c0` | [Filter the candidate pattern by style identity](workshop.md#rva-0x0096b9c0) | Filter the candidate pattern by style identity | C |
| `0x0096bae0` | `0x14096bae0` | [Apply resolved surface-block slot definitions](geography.md#rva-0x0096bae0) | Apply resolved surface-block slot definitions | C |
| `0x0096bba0` | `0x14096bba0` | [multi-subdivision footprint remapping](workshop.md#rva-0x0096bba0) | multi-subdivision footprint remapping | C |
| `0x0096be70` | `0x14096be70` | [pattern remap cache selection](workshop.md#rva-0x0096be70) | pattern remap cache selection | C |
| `0x0096bf00` | `0x14096bf00` | [Load surface-pattern style and source-slot fields](geography.md#rva-0x0096bf00) | Load surface-pattern style and source-slot fields | C |
| `0x0096da90` | `0x14096da90` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0096da90) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0096df80` | `0x14096df80` | [Calculate native lowest-level hierarchy index](geography.md#rva-0x0096df80) | Calculate native lowest-level hierarchy index | C |
| `0x0096e060` | `0x14096e060` | [Primary joins and attractive negative controls · entry](geography.md#rva-0x0096e060) | Original report discusses this roster entry under Primary joins and attractive negative controls. | C |
| `0x0096eb90` | `0x14096eb90` | [angle grid and canonical lookup](workshop.md#rva-0x0096eb90) | angle grid and canonical lookup | C |
| `0x0096ecb0` | `0x14096ecb0` | [nested clamped angle quantization](workshop.md#rva-0x0096ecb0) | nested clamped angle quantization | C |
| `0x0096efb0` | `0x14096efb0` | [subdivision snapping](workshop.md#rva-0x0096efb0) | subdivision snapping | C |
| `0x0096f1a0` | `0x14096f1a0` | [Fractional position producers and consumers · entry](workshop.md#rva-0x0096f1a0) | Original report discusses this roster entry under Fractional position producers and consumers. | C |
| `0x0096f4d0` | `0x14096f4d0` | [explicit half-step cell center](workshop.md#rva-0x0096f4d0) | explicit half-step cell center | C |
| `0x0096f5c0` | `0x14096f5c0` | [signed remainder wrap and tags](workshop.md#rva-0x0096f5c0) | signed remainder wrap and tags | C |
| `0x0096f940` | `0x14096f940` | [seam-aware grid difference](workshop.md#rva-0x0096f940) | seam-aware grid difference | C |
| `0x0096fa90` | `0x14096fa90` | [Packed grid-key encoder](interfaces.md#rva-0x0096fa90) | Packed grid-key encoder | C |
| `0x0096fb40` | `0x14096fb40` | [Unpack explicit world context key](geography.md#rva-0x0096fb40) | Unpack explicit world context key | C |
| `0x0096fde0` | `0x14096fde0` | [SFTR dimensions and face arrays](geography.md#rva-0x0096fde0) | SFTR dimensions and face arrays | C |
| `0x00970830` | `0x140970830` | [Load SFTR definition data](interfaces.md#rva-0x00970830) | Dispatches the BFCB block to the component loader. | B |
| `0x00970d50` | `0x140970d50` | [Fold the surface hierarchy seed inputs](geography.md#rva-0x00970d50) | Fold the surface hierarchy seed inputs | C |
| `0x00971d70` | `0x140971d70` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x00971d70) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x00972f00` | `0x140972f00` | [Consume Grid corner index for alignment](geography.md#rva-0x00972f00) | Consume Grid corner index for alignment | C |
| `0x00975030` | `0x140975030` | [Erase a source entry from the ProcGen source map](geography.md#rva-0x00975030) | Removes the mapped source-pointer entry for Grid clear or standalone retirement. | B |
| `0x00975e00` | `0x140975e00` | [Search water neighbors for biome evaluation](geography.md#rva-0x00975e00) | Search water neighbors for biome evaluation | C |
| `0x00976940` | `0x140976940` | [Active branch checkpoints · entry](geography.md#rva-0x00976940) | Original report discusses this roster entry under Active branch checkpoints. | C |
| `0x00976950` | `0x140976950` | [Construct the File-derived terrain object](geography.md#rva-0x00976950) | Construct the File-derived terrain object | C |
| `0x00978280` | `0x140978280` | [Protect and publish one prepared GridFile block](geography.md#rva-0x00978280) | Protect and publish one prepared GridFile block | C |
| `0x009783c0` | `0x1409783c0` | [Dispatch the paired inherited GridFile method](geography.md#rva-0x009783c0) | Dispatch the paired inherited GridFile method | C |
| `0x00978760` | `0x140978760` | [Dispatch the inherited GridFile preparation method](geography.md#rva-0x00978760) | Dispatch the inherited GridFile preparation method | C |
| `0x00979060` | `0x140979060` | [Concrete File callbacks and the numeric boundary · entry](geography.md#rva-0x00979060) | Original report discusses this roster entry under Concrete File callbacks and the numeric boundary. | C |
| `0x0097b6d0` | `0x14097b6d0` | [Concrete File callbacks and the numeric boundary · entry](geography.md#rva-0x0097b6d0) | Original report discusses this roster entry under Concrete File callbacks and the numeric boundary. | C |
| `0x0097b7f0` | `0x14097b7f0` | [Concrete File callbacks and the numeric boundary · entry](geography.md#rva-0x0097b7f0) | Original report discusses this roster entry under Concrete File callbacks and the numeric boundary. | C |
| `0x0097c380` | `0x14097c380` | [Active branch checkpoints · entry](geography.md#rva-0x0097c380) | Original report discusses this roster entry under Active branch checkpoints. | C |
| `0x0097d080` | `0x14097d080` | [Enumerate GridCornerFile dependencies](geography.md#rva-0x0097d080) | Enumerate GridCornerFile dependencies | C |
| `0x0097d190` | `0x14097d190` | [Combine corner terrain ROI payloads](geography.md#rva-0x0097d190) | Combine corner terrain ROI payloads | C |
| `0x009816d0` | `0x1409816d0` | [Active branch checkpoints · entry](geography.md#rva-0x009816d0) | Original report discusses this roster entry under Active branch checkpoints. | C |
| `0x00982090` | `0x140982090` | [Fold the source key for Grid lookup](geography.md#rva-0x00982090) | Fold the source key for Grid lookup | C |
| `0x00982390` | `0x140982390` | [Construct Grid input and modifier storage](geography.md#rva-0x00982390) | Construct Grid input and modifier storage | C |
| `0x00982930` | `0x140982930` | [Destroy and clear the Grid base](geography.md#rva-0x00982930) | Destroy and clear the Grid base | C |
| `0x009829b0` | `0x1409829b0` | [Clear Grid source entries](geography.md#rva-0x009829b0) | Clear Grid source entries | C |
| `0x00982b70` | `0x140982b70` | [Retire standalone Grid source](geography.md#rva-0x00982b70) | Retire standalone Grid source | C |
| `0x00982c50` | `0x140982c50` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x00982c50) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x00982d00` | `0x140982d00` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00982d00) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x00982d90` | `0x140982d90` | [Find or allocate a Grid source](geography.md#rva-0x00982d90) | Deduplicates or constructs a source object and attempts to publish it to the Grid. | A |
| `0x009831f0` | `0x1409831f0` | [ABI, loss and capability comparison · entry](geography.md#rva-0x009831f0) | Original report discusses this roster entry under ABI, loss and capability comparison. | C |
| `0x00983270` | `0x140983270` | [Initialization and successful-construction obligations · entry](geography.md#rva-0x00983270) | Original report discusses this roster entry under Initialization and successful-construction obligations. | C |
| `0x009832e0` | `0x1409832e0` | [Read source-rooted context](geography.md#rva-0x009832e0) | Read source-rooted context | C |
| `0x00983880` | `0x140983880` | [Publish GridFillFile source alias](geography.md#rva-0x00983880) | Publish GridFillFile source alias | C |
| `0x00985870` | `0x140985870` | [bounded source index slot lookup](geography.md#rva-0x00985870) | bounded source index slot lookup | B |
| `0x009858d0` | `0x1409858d0` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x009858d0) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x00985900` | `0x140985900` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00985900) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x00985c20` | `0x140985c20` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x00985c20) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x00985c50` | `0x140985c50` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00985c50) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x00986050` | `0x140986050` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x00986050) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x00986080` | `0x140986080` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00986080) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x009865e0` | `0x1409865e0` | [Enumeration and source-admission chain · entry](geography.md#rva-0x009865e0) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x009868f0` | `0x1409868f0` | [Return a Grid file-holder value](geography.md#rva-0x009868f0) | Return a Grid file-holder value | C |
| `0x009869a0` | `0x1409869a0` | [Return a paired Grid file-holder value](geography.md#rva-0x009869a0) | Return a paired Grid file-holder value | C |
| `0x00986a50` | `0x140986a50` | [Return the alternate Grid file-holder value](geography.md#rva-0x00986a50) | Return the alternate Grid file-holder value | C |
| `0x00986da0` | `0x140986da0` | [Shift Grid and rebase source anchors](geography.md#rva-0x00986da0) | Shift Grid and rebase source anchors | C |
| `0x00987080` | `0x140987080` | [Select a source for retirement by overlap](geography.md#rva-0x00987080) | Select a source for retirement by overlap | C |
| `0x009870d0` | `0x1409870d0` | [source index origin resolution](geography.md#rva-0x009870d0) | source index origin resolution | B |
| `0x00987190` | `0x140987190` | [Destroy the derived Grid through its base](geography.md#rva-0x00987190) | Destroy the derived Grid through its base | C |
| `0x009871d0` | `0x1409871d0` | [Read parent Grid cells through the derived Grid](geography.md#rva-0x009871d0) | Read parent Grid cells through the derived Grid | C |
| `0x00988100` | `0x140988100` | [Map-locked erasure followed by unlocked source destruction; conditional retirement.](geography.md#rva-0x00988100) | Map-locked erasure followed by unlocked source destruction; conditional retirement. | C |
| `0x00988220` | `0x140988220` | [Enumeration and source-admission chain · entry](geography.md#rva-0x00988220) | Original report discusses this roster entry under Enumeration and source-admission chain. | C |
| `0x00988240` | `0x140988240` | [Fill emits its nonnull contributor through append.](geography.md#rva-0x00988240) | Fill emits its nonnull contributor through append. | C |
| `0x00988330` | `0x140988330` | [Edge emits two nonnull slots in order.](geography.md#rva-0x00988330) | Edge emits two nonnull slots in order. | C |
| `0x00988380` | `0x140988380` | [Native boundaries and replay inputs · entry](geography.md#rva-0x00988380) | Original report discusses this roster entry under Native boundaries and replay inputs. | C |
| `0x009884e0` | `0x1409884e0` | [Store the raw source pointer in the initial Grid cell slot](geography.md#rva-0x009884e0) | Store the raw source pointer in the initial Grid cell slot | C |
| `0x00988540` | `0x140988540` | [Native boundaries and replay inputs · entry](geography.md#rva-0x00988540) | Original report discusses this roster entry under Native boundaries and replay inputs. | C |
| `0x00988670` | `0x140988670` | [Store source slots for fill, edge or corner cells](geography.md#rva-0x00988670) | Store source slots for fill, edge or corner cells | C |
| `0x00988760` | `0x140988760` | [Corner emits up to four nonnull slots in order.](geography.md#rva-0x00988760) | Corner emits up to four nonnull slots in order. | C |
| `0x00988ab0` | `0x140988ab0` | [Append a raw source pointer to the caller list](geography.md#rva-0x00988ab0) | Copies one source-pointer value into the caller's temporary chunk list. | B |
| `0x00988b60` | `0x140988b60` | [Independent challenge: Grid construction, backing copies and the clear tail · entry](geography.md#rva-0x00988b60) | Original report discusses this roster entry under Independent challenge: Grid construction, backing copies and the clear tail. | C |
| `0x00989170` | `0x140989170` | [Update the world-height context](geography.md#rva-0x00989170) | Update the world-height context | C |
| `0x0098ed90` | `0x14098ed90` | [Active branch checkpoints · entry](geography.md#rva-0x0098ed90) | Original report discusses this roster entry under Active branch checkpoints. | C |
| `0x0098f380` | `0x14098f380` | [Active branch checkpoints · entry](geography.md#rva-0x0098f380) | Original report discusses this roster entry under Active branch checkpoints. | C |
| `0x00991db0` | `0x140991db0` | [Construct the PageStitch preparation object](geography.md#rva-0x00991db0) | Construct the PageStitch preparation object | C |
| `0x00992110` | `0x140992110` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x00992110) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x009921f0` | `0x1409921f0` | [Destroy the PageStitch task object](geography.md#rva-0x009921f0) | Destroy the PageStitch task object | C |
| `0x00992330` | `0x140992330` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x00992330) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x00992ab0` | `0x140992ab0` | [Preserve the MultiFiles Grid table during height binding](geography.md#rva-0x00992ab0) | Preserve the MultiFiles Grid table during height binding | C |
| `0x00993110` | `0x140993110` | [d5ad input provenance · entry](geography.md#rva-0x00993110) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x00993e70` | `0x140993e70` | [TerrainDB is a real scheduling and context-lifetime dependency · entry](geography.md#rva-0x00993e70) | Original report discusses this roster entry under TerrainDB is a real scheduling and context-lifetime dependency. | C |
| `0x00995630` | `0x140995630` | [Construct the PageTransform preparation object](geography.md#rva-0x00995630) | Construct the PageTransform preparation object | C |
| `0x00995d20` | `0x140995d20` | [Release PageTransform preparation state](geography.md#rva-0x00995d20) | Release PageTransform preparation state | C |
| `0x00998fc0` | `0x140998fc0` | [d5ad input provenance · entry](geography.md#rva-0x00998fc0) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x00999120` | `0x140999120` | [d5ad input provenance · entry](geography.md#rva-0x00999120) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x0099ab90` | `0x14099ab90` | [Grid, terrain and density preparation · entry](geography.md#rva-0x0099ab90) | Original report discusses this roster entry under Grid, terrain and density preparation. | C |
| `0x0099f230` | `0x14099f230` | [Focus-invalid initialization refinement · entry](geography.md#rva-0x0099f230) | Original report discusses this roster entry under Focus-invalid initialization refinement. | C |
| `0x0099f280` | `0x14099f280` | [Focus-invalid initialization refinement · entry](geography.md#rva-0x0099f280) | Original report discusses this roster entry under Focus-invalid initialization refinement. | C |
| `0x0099f2c0` | `0x14099f2c0` | [Confirmation and transition ingress · entry](geography.md#rva-0x0099f2c0) | Original report discusses this roster entry under Confirmation and transition ingress. | C |
| `0x0099ff50` | `0x14099ff50` | [Fractional position producers and consumers · entry](geography.md#rva-0x0099ff50) | Original report discusses this roster entry under Fractional position producers and consumers. | C |
| `0x009a02b0` | `0x1409a02b0` | [Support fractional local-height interpolation](workshop.md#rva-0x009a02b0) | Support fractional local-height interpolation | C |
| `0x009a0db0` | `0x1409a0db0` | [Further resolved branches (exports 23–28) · entry](geography.md#rva-0x009a0db0) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x009a0f20` | `0x1409a0f20` | [Fractional position producers and consumers · entry](geography.md#rva-0x009a0f20) | Original report discusses this roster entry under Fractional position producers and consumers. | C |
| `0x009a2380` | `0x1409a2380` | [Dispatch the admitted terrain task](geography.md#rva-0x009a2380) | Dispatch the admitted terrain task | C |
| `0x009a7950` | `0x1409a7950` | [Demand prefix, admitted pair and historical invocation state · entry](geography.md#rva-0x009a7950) | Original report discusses this roster entry under Demand prefix, admitted pair and historical invocation state. | C |
| `0x009a7ad0` | `0x1409a7ad0` | [Demand prefix, admitted pair and historical invocation state · entry](geography.md#rva-0x009a7ad0) | Original report discusses this roster entry under Demand prefix, admitted pair and historical invocation state. | C |
| `0x009a7ca0` | `0x1409a7ca0` | [Reset terrain clip and subscriber state](geography.md#rva-0x009a7ca0) | Reset terrain clip and subscriber state | C |
| `0x009a89e0` | `0x1409a89e0` | [Process the material stage of the terrain task](geography.md#rva-0x009a89e0) | Process the material stage of the terrain task | C |
| `0x009ac2d0` | `0x1409ac2d0` | [Checkpoint 3 — incremental claims and upstream dependencies · entry](geography.md#rva-0x009ac2d0) | Original report discusses this roster entry under Checkpoint 3 — incremental claims and upstream dependencies. | C |
| `0x009af3d0` | `0x1409af3d0` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x009af3d0) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x009b0570` | `0x1409b0570` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x009b0570) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x009dd080` | `0x1409dd080` | [atmosphere type resolution](geography.md#rva-0x009dd080) | atmosphere type resolution | B |
| `0x009dd250` | `0x1409dd250` | [Rebuild typed atmosphere resource list](geography.md#rva-0x009dd250) | Rebuild typed atmosphere resource list | C |
| `0x009df850` | `0x1409df850` | [Load biome RNAM identities](geography.md#rva-0x009df850) | Load biome RNAM identities | C |
| `0x009e1640` | `0x1409e1640` | [Resolve biome RNAM identities](geography.md#rva-0x009e1640) | Resolve biome RNAM identities | C |
| `0x009e4690` | `0x1409e4690` | [Participate in the biome RNAM load and fixup route](geography.md#rva-0x009e4690) | Participate in the biome RNAM load and fixup route | C |
| `0x009e5a00` | `0x1409e5a00` | [Dispatch nested condition evaluation](workshop.md#rva-0x009e5a00) | Dispatch nested condition evaluation | C |
| `0x009e6c20` | `0x1409e6c20` | [Initialize resolved default-object storage](geography.md#rva-0x009e6c20) | Initialize resolved default-object storage | C |
| `0x009e6ed0` | `0x1409e6ed0` | [Load default-object definition data](geography.md#rva-0x009e6ed0) | Load default-object definition data | C |
| `0x009e7770` | `0x1409e7770` | [Reset the native IRES definition state](production.md#rva-0x009e7770) | Reset the native IRES definition state | C |
| `0x009e7890` | `0x1409e7890` | [resource color fallback](interfaces.md#rva-0x009e7890) | resource color fallback | C |
| `0x009e7900` | `0x1409e7900` | [IRES definition loader](population.md#rva-0x009e7900) | IRES definition loader | B |
| `0x009e8570` | `0x1409e8570` | [IRES reference fixup](population.md#rva-0x009e8570) | IRES reference fixup | B |
| `0x009e8700` | `0x1409e8700` | [Enumerate positive resource actor values](production.md#rva-0x009e8700) | Enumerate positive resource actor values | C |
| `0x009e8950` | `0x1409e8950` | [Placement and registration use distinct resource operations · entry](geography.md#rva-0x009e8950) | Original report discusses this roster entry under Placement and registration use distinct resource operations. | C |
| `0x009e8b70` | `0x1409e8b70` | [Enumerate fauna resource candidates](production.md#rva-0x009e8b70) | Enumerate fauna resource candidates | C |
| `0x009e8f20` | `0x1409e8f20` | [fallback resource property collector](production.md#rva-0x009e8f20) | fallback resource property collector | B |
| `0x009e9150` | `0x1409e9150` | [Enumerate effective properties for resource registration](geography.md#rva-0x009e9150) | Enumerate effective properties for resource registration | C |
| `0x009e9360` | `0x1409e9360` | [Resource-registration property iterator](geography.md#rva-0x009e9360) | Resource-registration property iterator | C |
| `0x009e9640` | `0x1409e9640` | [property-linked recipe capability](production.md#rva-0x009e9640) | property-linked recipe capability | B |
| `0x009e9700` | `0x1409e9700` | [Recognize recipe-bearing resources](production.md#rva-0x009e9700) | Recognize recipe-bearing resources | C |
| `0x009e97a0` | `0x1409e97a0` | [first selected source product set](production.md#rva-0x009e97a0) | first selected source product set | B |
| `0x009e9960` | `0x1409e9960` | [source product ingredient compatibility](production.md#rva-0x009e9960) | source product ingredient compatibility | B |
| `0x009ea3f0` | `0x1409ea3f0` | [generic recipe-capability fallback callback](production.md#rva-0x009ea3f0) | generic recipe-capability fallback callback | B |
| `0x009ea440` | `0x1409ea440` | [Resource-registration callback](geography.md#rva-0x009ea440) | Resource-registration callback | C |
| `0x009ea490` | `0x1409ea490` | [generic fallback resource collection callback](production.md#rva-0x009ea490) | generic fallback resource collection callback | B |
| `0x009ea530` | `0x1409ea530` | [positive-resource enumeration callback](production.md#rva-0x009ea530) | positive-resource enumeration callback | B |
| `0x009eed50` | `0x1409eed50` | [d5ad input provenance · entry](geography.md#rva-0x009eed50) | Original report discusses this roster entry under d5ad input provenance. | C |
| `0x009efb20` | `0x1409efb20` | [Definition loading and postlink readiness · entry](geography.md#rva-0x009efb20) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x009efc60` | `0x1409efc60` | [Resolve resource-generation descriptor references](geography.md#rva-0x009efc60) | Resolve resource-generation descriptor references | C |
| `0x00a02160` | `0x140a02160` | [load JNAM at COBJ+178](population.md#rva-0x00a02160) | load JNAM at COBJ+178 | C |
| `0x00a179f0` | `0x140a179f0` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00a179f0) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00a19cd0` | `0x140a19cd0` | [CONT component retrieval](production.md#rva-0x00a19cd0) | CONT component retrieval | B |
| `0x00a1a140` | `0x140a1a140` | [CONT PRPS dispatch](production.md#rva-0x00a1a140) | CONT PRPS dispatch | B |
| `0x00a1d4c0` | `0x140a1d4c0` | [Materialize the PackIn replacement target](workshop.md#rva-0x00a1d4c0) | Materialize the PackIn replacement target | C |
| `0x00a21d10` | `0x140a21d10` | [Copy or merge material-swap metadata](workshop.md#rva-0x00a21d10) | Copy or merge material-swap metadata | C |
| `0x00a23de0` | `0x140a23de0` | [Read the version-gated ExtraDA representation](interfaces.md#rva-0x00a23de0) | Consumes the qualified queued identities and conditional fields. | B |
| `0x00a30980` | `0x140a30980` | [Definition and discovery chain · entry](workshop.md#rva-0x00a30980) | Original report discusses this roster entry under Definition and discovery chain. | C |
| `0x00a30fc0` | `0x140a30fc0` | [Definition and discovery chain · entry](workshop.md#rva-0x00a30fc0) | Original report discusses this roster entry under Definition and discovery chain. | C |
| `0x00a31050` | `0x140a31050` | [Apply automatic-wall pair behavior](workshop.md#rva-0x00a31050) | Apply automatic-wall pair behavior | C |
| `0x00a31210` | `0x140a31210` | [Reverse the automatic-wall pairing behavior](workshop.md#rva-0x00a31210) | Reverse the automatic-wall pairing behavior | C |
| `0x00a31400` | `0x140a31400` | [Resolve and apply automatic snap behavior](workshop.md#rva-0x00a31400) | Dispatches configured snap operations for the connected endpoints. | B |
| `0x00a314c0` | `0x140a314c0` | [Apply the enabled automatic-wall pair path](workshop.md#rva-0x00a314c0) | Apply the enabled automatic-wall pair path | C |
| `0x00a316c0` | `0x140a316c0` | [Participate in variant discovery and validation](workshop.md#rva-0x00a316c0) | Participate in variant discovery and validation | C |
| `0x00a32780` | `0x140a32780` | [Dispatch an admitted snap variant action](workshop.md#rva-0x00a32780) | Executes the selected replace, remove or add operation. | B |
| `0x00a74420` | `0x140a74420` | [switch activation category predicate](power.md#rva-0x00a74420) | switch activation category predicate | B |
| `0x00a84690` | `0x140a84690` | [CONT filter form fixup](inventory.md#rva-0x00a84690) | CONT filter form fixup | C |
| `0x00a84810` | `0x140a84810` | [CONT ONAM filter loader](inventory.md#rva-0x00a84810) | CONT ONAM filter loader | C |
| `0x00a94740` | `0x140a94740` | [Install the MISC item weight component](inventory.md#rva-0x00a94740) | Install the MISC item weight component | C |
| `0x00a94c30` | `0x140a94c30` | [MISC DATA loader](inventory.md#rva-0x00a94c30) | MISC DATA loader | C |
| `0x00aab770` | `0x140aab770` | [Decode the location DATA record fields](interfaces.md#rva-0x00aab770) | Decode the location DATA record fields | C |
| `0x00ab8030` | `0x140ab8030` | [Dispatch location DATA decoding](interfaces.md#rva-0x00ab8030) | Dispatch location DATA decoding | C |
| `0x00ab9f80` | `0x140ab9f80` | [Fix up the location DATA link](interfaces.md#rva-0x00ab9f80) | Fix up the location DATA link | C |
| `0x00aba950` | `0x140aba950` | [Select the first available owner context](interfaces.md#rva-0x00aba950) | Select the first available owner context | C |
| `0x00abf3f0` | `0x140abf3f0` | [Enumerate forced location-reference entries](workshop.md#rva-0x00abf3f0) | Enumerate forced location-reference entries | C |
| `0x00ac8b60` | `0x140ac8b60` | [Append a location-reference entry and identity](workshop.md#rva-0x00ac8b60) | Append a location-reference entry and identity | C |
| `0x00ac9e90` | `0x140ac9e90` | [Append a location-reference entry and identity](workshop.md#rva-0x00ac9e90) | Append a location-reference entry and identity | C |
| `0x00acc660` | `0x140acc660` | [Read a component of the Actor native suffix](population.md#rva-0x00acc660) | Read a component of the Actor native suffix | C |
| `0x00acc9f0` | `0x140acc9f0` | [Participate in the world setup wrapper route](workshop.md#rva-0x00acc9f0) | Participate in the world setup wrapper route | C |
| `0x00accc10` | `0x140accc10` | [dimension-derived inclusive bounds](workshop.md#rva-0x00accc10) | dimension-derived inclusive bounds | C |
| `0x00accd30` | `0x140accd30` | [component nominal bounds](workshop.md#rva-0x00accd30) | component nominal bounds | C |
| `0x00acd180` | `0x140acd180` | [Build and apply edge translation vector](workshop.md#rva-0x00acd180) | Build and apply edge translation vector | C |
| `0x00ace640` | `0x140ace640` | [Read overlay terrain sample](workshop.md#rva-0x00ace640) | Read overlay terrain sample | C |
| `0x00ace740` | `0x140ace740` | [Compute an adjustment using terrain samples](workshop.md#rva-0x00ace740) | Compute an adjustment using terrain samples | C |
| `0x00acf480` | `0x140acf480` | [height terrain sampling](workshop.md#rva-0x00acf480) | height terrain sampling | C |
| `0x00ad0400` | `0x140ad0400` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ad0400) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ad0650` | `0x140ad0650` | [Construct and name planetary overlay](workshop.md#rva-0x00ad0650) | Construct and name planetary overlay | C |
| `0x00ad08d0` | `0x140ad08d0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ad08d0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ad0b90` | `0x140ad0b90` | [Test terrain exclusion overlap](workshop.md#rva-0x00ad0b90) | Test terrain exclusion overlap | C |
| `0x00ad0fb0` | `0x140ad0fb0` | [identity/forced versus bounds collision](workshop.md#rva-0x00ad0fb0) | identity/forced versus bounds collision | C |
| `0x00ad11c0` | `0x140ad11c0` | [invalidates world context](workshop.md#rva-0x00ad11c0) | invalidates world context | C |
| `0x00ad1510` | `0x140ad1510` | [Forward frame translation setup](workshop.md#rva-0x00ad1510) | Forward frame translation setup | C |
| `0x00ad1660` | `0x140ad1660` | [collision selection/create/height/register](workshop.md#rva-0x00ad1660) | collision selection/create/height/register | C |
| `0x00ad30a0` | `0x140ad30a0` | [keyed inclusive-bound selection](workshop.md#rva-0x00ad30a0) | keyed inclusive-bound selection | C |
| `0x00ad31a0` | `0x140ad31a0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ad31a0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ad3240` | `0x140ad3240` | [Select containing edge and destination](workshop.md#rva-0x00ad3240) | Select containing edge and destination | C |
| `0x00ad3410` | `0x140ad3410` | [Ordinary entry and eligible density task · entry](geography.md#rva-0x00ad3410) | Original report discusses this roster entry under Ordinary entry and eligible density task. | C |
| `0x00ad3610` | `0x140ad3610` | [Resolve placement encounter and location context](workshop.md#rva-0x00ad3610) | Resolve placement encounter and location context | C |
| `0x00ad36d0` | `0x140ad36d0` | [Resolve loaded spatial location context](geography.md#rva-0x00ad36d0) | Resolve loaded spatial location context | C |
| `0x00ad3b20` | `0x140ad3b20` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ad3b20) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ad3c30` | `0x140ad3c30` | [body/component and world pair lookup](workshop.md#rva-0x00ad3c30) | body/component and world pair lookup | C |
| `0x00ad3ed0` | `0x140ad3ed0` | [Form cell-route frame translation](workshop.md#rva-0x00ad3ed0) | Form cell-route frame translation | C |
| `0x00ad40c0` | `0x140ad40c0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ad40c0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ad47e0` | `0x140ad47e0` | [initialize typed shifts/pair/flags](workshop.md#rva-0x00ad47e0) | initialize typed shifts/pair/flags | C |
| `0x00ad4a00` | `0x140ad4a00` | [component bounds and sourceworld](workshop.md#rva-0x00ad4a00) | component bounds and sourceworld | C |
| `0x00ad4fa0` | `0x140ad4fa0` | [Update selected overlay edge context](workshop.md#rva-0x00ad4fa0) | Update selected overlay edge context | C |
| `0x00ad55b0` | `0x140ad55b0` | [Format planetary overlay coordinate name](workshop.md#rva-0x00ad55b0) | Format planetary overlay coordinate name | C |
| `0x00ad5950` | `0x140ad5950` | [Clear or invalidate selected terrain edges](workshop.md#rva-0x00ad5950) | Clear or invalidate selected terrain edges | C |
| `0x00ad5f20` | `0x140ad5f20` | [Saved world component transfer](interfaces.md#rva-0x00ad5f20) | Saved world component transfer | C |
| `0x00ad6150` | `0x140ad6150` | [Saved world component transfer counterpart](interfaces.md#rva-0x00ad6150) | Saved world component transfer counterpart | C |
| `0x00ad6cb0` | `0x140ad6cb0` | [State classification and its limits · entry](geography.md#rva-0x00ad6cb0) | Original report discusses this roster entry under State classification and its limits. | C |
| `0x00ad7040` | `0x140ad7040` | [Further resolved branches (exports 23–28) · entry](workshop.md#rva-0x00ad7040) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x00ad7200` | `0x140ad7200` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ad7200) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ad7330` | `0x140ad7330` | [factory create callback](workshop.md#rva-0x00ad7330) | factory create callback | C |
| `0x00ad7b80` | `0x140ad7b80` | [component store insertion](workshop.md#rva-0x00ad7b80) | component store insertion | C |
| `0x00ad80d0` | `0x140ad80d0` | [Append selected world identities to the auxiliary list](geography.md#rva-0x00ad80d0) | Append selected world identities to the auxiliary list | C |
| `0x00ad8930` | `0x140ad8930` | [State classification and its limits · entry](geography.md#rva-0x00ad8930) | Original report discusses this roster entry under State classification and its limits. | C |
| `0x00ad8ec0` | `0x140ad8ec0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ad8ec0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ad8ed0` | `0x140ad8ed0` | [Further resolved branches (exports 23–28) · entry](workshop.md#rva-0x00ad8ed0) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x00ad92e0` | `0x140ad92e0` | [Terrain coverage route entry](workshop.md#rva-0x00ad92e0) | Terrain coverage route entry | C |
| `0x00ad94a0` | `0x140ad94a0` | [invalidation dispatcher](workshop.md#rva-0x00ad94a0) | invalidation dispatcher | C |
| `0x00ad9810` | `0x140ad9810` | [queued pairs and selected edge update](workshop.md#rva-0x00ad9810) | queued pairs and selected edge update | C |
| `0x00ad9cd0` | `0x140ad9cd0` | [subtract rebase from shift and bounds](workshop.md#rva-0x00ad9cd0) | subtract rebase from shift and bounds | C |
| `0x00ada240` | `0x140ada240` | [Select cell-route height operand](workshop.md#rva-0x00ada240) | Select cell-route height operand | C |
| `0x00ada3a0` | `0x140ada3a0` | [shift*100 and height read](workshop.md#rva-0x00ada3a0) | shift*100 and height read | C |
| `0x00ada760` | `0x140ada760` | [Resolve overlay validity independently of status](workshop.md#rva-0x00ada760) | Resolve overlay validity independently of status | C |
| `0x00ada960` | `0x140ada960` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00ada960) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00adab20` | `0x140adab20` | [Select an activated overlay payload](workshop.md#rva-0x00adab20) | Select an activated overlay payload | C |
| `0x00adb6b0` | `0x140adb6b0` | [Saved destination and later exterior activation · entry](geography.md#rva-0x00adb6b0) | Original report discusses this roster entry under Saved destination and later exterior activation. | C |
| `0x00adbc50` | `0x140adbc50` | [world to associated planetary pair](workshop.md#rva-0x00adbc50) | world to associated planetary pair | C |
| `0x00adccf0` | `0x140adccf0` | [command component registration](workshop.md#rva-0x00adccf0) | command component registration | C |
| `0x00adcde0` | `0x140adcde0` | [queued activated command references](workshop.md#rva-0x00adcde0) | queued activated command references | C |
| `0x00adcf50` | `0x140adcf50` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00adcf50) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00adcfd0` | `0x140adcfd0` | [typed payload copy](workshop.md#rva-0x00adcfd0) | typed payload copy | C |
| `0x00add2a0` | `0x140add2a0` | [Dispatch the world setup wrapper](workshop.md#rva-0x00add2a0) | Dispatch the world setup wrapper | C |
| `0x00add2d0` | `0x140add2d0` | [Further resolved branches (exports 23–28) · entry](workshop.md#rva-0x00add2d0) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x00add2e0` | `0x140add2e0` | [Dispatch deferred overlay registration](workshop.md#rva-0x00add2e0) | Dispatch deferred overlay registration | C |
| `0x00add310` | `0x140add310` | [keyed activated edge insertion](workshop.md#rva-0x00add310) | keyed activated edge insertion | C |
| `0x00add580` | `0x140add580` | [Continue the world setup chain](workshop.md#rva-0x00add580) | Continue the world setup chain | C |
| `0x00add770` | `0x140add770` | [Further resolved branches (exports 23–28) · entry](workshop.md#rva-0x00add770) | Original report discusses this roster entry under Further resolved branches (exports 23–28). | C |
| `0x00add850` | `0x140add850` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00add850) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00ae6830` | `0x140ae6830` | [Native CELL DATA read to receiver+0x48, two/four-byte cases](geography.md#rva-0x00ae6830) | Native CELL DATA read to receiver+0x48, two/four-byte cases | C |
| `0x00aed020` | `0x140aed020` | [Prepare exterior cell request](geography.md#rva-0x00aed020) | Prepare exterior cell request | C |
| `0x00aef010` | `0x140aef010` | [Participate in cell-based biome state selection](geography.md#rva-0x00aef010) | Participate in cell-based biome state selection | C |
| `0x00aef1e0` | `0x140aef1e0` | [Participate in world-based biome state selection](geography.md#rva-0x00aef1e0) | Participate in world-based biome state selection | C |
| `0x00af4c50` | `0x140af4c50` | [Resolve the eligible cell or world location](workshop.md#rva-0x00af4c50) | Resolve the eligible cell or world location | C |
| `0x00af6a60` | `0x140af6a60` | [Restore extra transform under type gates](workshop.md#rva-0x00af6a60) | Restore extra transform under type gates | C |
| `0x00afb220` | `0x140afb220` | [Demand prefix, admitted pair and historical invocation state · entry](geography.md#rva-0x00afb220) | Original report discusses this roster entry under Demand prefix, admitted pair and historical invocation state. | C |
| `0x00afe0d0` | `0x140afe0d0` | [Continue initialization association](power.md#rva-0x00afe0d0) | Continue initialization association | C |
| `0x00b02630` | `0x140b02630` | [Conditionally emit the loaded reference event](power.md#rva-0x00b02630) | Conditionally emit the loaded reference event | C |
| `0x00b03360` | `0x140b03360` | [Checkpoint: verified inputs and first five export passes · entry](geography.md#rva-0x00b03360) | Original report discusses this roster entry under Checkpoint: verified inputs and first five export passes. | C |
| `0x00b04ad0` | `0x140b04ad0` | [Supply elapsed time to the reference movement update](inventory.md#rva-0x00b04ad0) | Routes the engine frame delta into the qualified reference movement path. | B |
| `0x00b0fd40` | `0x140b0fd40` | [Process reference attach association](power.md#rva-0x00b0fd40) | Process reference attach association | C |
| `0x00b11780` | `0x140b11780` | [Process the cell-attach callback](power.md#rva-0x00b11780) | Process the cell-attach callback | C |
| `0x00b19a60` | `0x140b19a60` | [Initialize the reference association path](power.md#rva-0x00b19a60) | Initialize the reference association path | C |
| `0x00b1e190` | `0x140b1e190` | [cell reference pointer-array visitor](power.md#rva-0x00b1e190) | cell reference pointer-array visitor | B |
| `0x00b1e720` | `0x140b1e720` | [Resolve the saved CalculatedPackinData reference](workshop.md#rva-0x00b1e720) | Resolve the saved CalculatedPackinData reference | C |
| `0x00b21e70` | `0x140b21e70` | [Install the reference movement dispatch table](inventory.md#rva-0x00b21e70) | Install the reference movement dispatch table | C |
| `0x00b21fd0` | `0x140b21fd0` | [Construct reference actor-value interface](production.md#rva-0x00b21fd0) | Construct reference actor-value interface | C |
| `0x00b22630` | `0x140b22630` | [Write other reference flags while preserving the frame bit](workshop.md#rva-0x00b22630) | Write other reference flags while preserving the frame bit | C |
| `0x00b22bf0` | `0x140b22bf0` | [Reset reference transform fields](workshop.md#rva-0x00b22bf0) | Reset reference transform fields | C |
| `0x00b230a0` | `0x140b230a0` | [reference definition subrecord loader](power.md#rva-0x00b230a0) | reference definition subrecord loader | B |
| `0x00b24af0` | `0x140b24af0` | [Initialize stock when the source inventory field is null](inventory.md#rva-0x00b24af0) | Initialize stock when the source inventory field is null | C |
| `0x00b24ca0` | `0x140b24ca0` | [reference base TESContainer component query](inventory.md#rva-0x00b24ca0) | reference base TESContainer component query | C |
| `0x00b24da0` | `0x140b24da0` | [Initialize and retain the player backing store](inventory.md#rva-0x00b24da0) | Initialize and retain the player backing store | C |
| `0x00b25520` | `0x140b25520` | [Preparation and the two service pumps · entry](geography.md#rva-0x00b25520) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x00b27a80` | `0x140b27a80` | [Preparation and the two service pumps · entry](geography.md#rva-0x00b27a80) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x00b29470` | `0x140b29470` | [reference original default-open helper](power.md#rva-0x00b29470) | reference original default-open helper | B |
| `0x00b29700` | `0x140b29700` | [reference save-body dispatcher](power.md#rva-0x00b29700) | reference save-body dispatcher | B |
| `0x00b29990` | `0x140b29990` | [reference saved-state restore dispatcher](power.md#rva-0x00b29990) | reference saved-state restore dispatcher | B |
| `0x00b2bc70` | `0x140b2bc70` | [reference post-load open-state reconstruction](power.md#rva-0x00b2bc70) | reference post-load open-state reconstruction | B |
| `0x00b2d0c0` | `0x140b2d0c0` | [Movement selection and admission · entry](inventory.md#rva-0x00b2d0c0) | Original report discusses this roster entry under Movement selection and admission. | C |
| `0x00b2dbd0` | `0x140b2dbd0` | [Write backing inventory rows](inventory.md#rva-0x00b2dbd0) | Write backing inventory rows | C |
| `0x00b2dcc0` | `0x140b2dcc0` | [Save/load authority and remote meaning · entry](inventory.md#rva-0x00b2dcc0) | Original report discusses this roster entry under Save/load authority and remote meaning. | C |
| `0x00b36310` | `0x140b36310` | [Check membership in the reference form-type family](workshop.md#rva-0x00b36310) | Check membership in the reference form-type family | C |
| `0x00b38130` | `0x140b38130` | [Write ordinary reference scale](workshop.md#rva-0x00b38130) | Write ordinary reference scale | C |
| `0x00b3cbc0` | `0x140b3cbc0` | [reference initialization open-state request](power.md#rva-0x00b3cbc0) | reference initialization open-state request | B |
| `0x00b3e1e0` | `0x140b3e1e0` | [New construction suppresses default stock · entry](inventory.md#rva-0x00b3e1e0) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x00b40430` | `0x140b40430` | [Emit the loaded-reference event from a move or 3D path](power.md#rva-0x00b40430) | Emit the loaded-reference event from a move or 3D path | C |
| `0x00b40660` | `0x140b40660` | [Check whether to admit the loaded reference](power.md#rva-0x00b40660) | Check whether to admit the loaded reference | C |
| `0x00b43f80` | `0x140b43f80` | [Supply material swap data to the merge path](workshop.md#rva-0x00b43f80) | Supply material swap data to the merge path | C |
| `0x00b47420` | `0x140b47420` | [ExtraAction bit set and current-open difference marking](power.md#rva-0x00b47420) | ExtraAction bit set and current-open difference marking | B |
| `0x00b475b0` | `0x140b475b0` | [ExtraAction bit clear and current-open difference marking](power.md#rva-0x00b475b0) | ExtraAction bit clear and current-open difference marking | B |
| `0x00b48ca0` | `0x140b48ca0` | [Replace reference parent and move context](workshop.md#rva-0x00b48ca0) | Replace reference parent and move context | C |
| `0x00b4a0b0` | `0x140b4a0b0` | [Dispatch immediate frame conversion](workshop.md#rva-0x00b4a0b0) | Dispatch immediate frame conversion | C |
| `0x00b4c620` | `0x140b4c620` | [Apply the item pickup or transfer branch](inventory.md#rva-0x00b4c620) | Apply the item pickup or transfer branch | C |
| `0x00b4cbc0` | `0x140b4cbc0` | [destination generic add handoff](inventory.md#rva-0x00b4cbc0) | destination generic add handoff | C |
| `0x00b4cd10` | `0x140b4cd10` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00b4cd10) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00b4cee0` | `0x140b4cee0` | [reference indexed position derivation](geography.md#rva-0x00b4cee0) | reference indexed position derivation | B |
| `0x00b4d430` | `0x140b4d430` | [Replace the existing reference base in the non-PackIn branch](workshop.md#rva-0x00b4d430) | Replace the existing reference base in the non-PackIn branch | C |
| `0x00b4d650` | `0x140b4d650` | [Enter PackIn replacement for the hab-wall rule](workshop.md#rva-0x00b4d650) | Enter PackIn replacement for the hab-wall rule | C |
| `0x00b4dc20` | `0x140b4dc20` | [Participate in non-PackIn base replacement](workshop.md#rva-0x00b4dc20) | Participate in non-PackIn base replacement | C |
| `0x00b4e260` | `0x140b4e260` | [Restore reference rotation members](workshop.md#rva-0x00b4e260) | Restore reference rotation members | C |
| `0x00b4e410` | `0x140b4e410` | [Preparation and the two service pumps · entry](geography.md#rva-0x00b4e410) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x00b4e4e0` | `0x140b4e4e0` | [Write ordinary reference parent](geography.md#rva-0x00b4e4e0) | Write ordinary reference parent | C |
| `0x00b4e5f0` | `0x140b4e5f0` | [Resolve the proposed reference's placement identity](workshop.md#rva-0x00b4e5f0) | Resolve the proposed reference's placement identity | C |
| `0x00b4e650` | `0x140b4e650` | [Storage, inventory and cargo native entry](inventory.md#rva-0x00b4e650) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00b4eb40` | `0x140b4eb40` | [Support world-position location lookup without a parent cell](workshop.md#rva-0x00b4eb40) | Support world-position location lookup without a parent cell | C |
| `0x00b4ef90` | `0x140b4ef90` | [destination receiving wrapper](inventory.md#rva-0x00b4ef90) | destination receiving wrapper | C |
| `0x00b56c50` | `0x140b56c50` | [Damage and operational consequences · entry](population.md#rva-0x00b56c50) | Original report discusses this roster entry under Damage and operational consequences. | C |
| `0x00b58cf0` | `0x140b58cf0` | [Apply the cell-finish visitor predicate](power.md#rva-0x00b58cf0) | Apply the cell-finish visitor predicate | C |
| `0x00b58d50` | `0x140b58d50` | [Participate in the special reference location branch](workshop.md#rva-0x00b58d50) | Participate in the special reference location branch | C |
| `0x00b5c350` | `0x140b5c350` | [finish cell visitor deferred notification](power.md#rva-0x00b5c350) | finish cell visitor deferred notification | B |
| `0x00b5d040` | `0x140b5d040` | [Insert expanded product](production.md#rva-0x00b5d040) | Insert expanded product | C |
| `0x00b61610` | `0x140b61610` | [Capacity-aware bulk inventory transfer](inventory.md#rva-0x00b61610) | Capacity-aware bulk inventory transfer | C |
| `0x00b631b0` | `0x140b631b0` | [Copy or sum ingredient source rows](inventory.md#rva-0x00b631b0) | Copy or sum ingredient source rows | C |
| `0x00b63d40` | `0x140b63d40` | [Count available ingredient](production.md#rva-0x00b63d40) | Count available ingredient | C |
| `0x00b647d0` | `0x140b647d0` | [Refresh after creation](production.md#rva-0x00b647d0) | Refresh after creation | C |
| `0x00b64da0` | `0x140b64da0` | [Test the resolved shared-storage keyword](inventory.md#rva-0x00b64da0) | Test the resolved shared-storage keyword | C |
| `0x00b64e10` | `0x140b64e10` | [Dispatch the event after inventory transfer](inventory.md#rva-0x00b64e10) | Dispatch the event after inventory transfer | C |
| `0x00b64fc0` | `0x140b64fc0` | [general item insertion](population.md#rva-0x00b64fc0) | general item insertion | B |
| `0x00b65df0` | `0x140b65df0` | [Handle inventory attachment reconciliation and cleanup](inventory.md#rva-0x00b65df0) | Handle inventory attachment reconciliation and cleanup | C |
| `0x00b66680` | `0x140b66680` | [source transfer virtual458](inventory.md#rva-0x00b66680) | source transfer virtual458 | C |
| `0x00b67100` | `0x140b67100` | [bounded removal callback](inventory.md#rva-0x00b67100) | bounded removal callback | C |
| `0x00b67380` | `0x140b67380` | [actual removed quantity to destination virtual4d0](inventory.md#rva-0x00b67380) | actual removed quantity to destination virtual4d0 | C |
| `0x00b67a30` | `0x140b67a30` | [Participate in the ordered cargo stack subtraction path](inventory.md#rva-0x00b67a30) | Participate in the ordered cargo stack subtraction path | C |
| `0x00b693b0` | `0x140b693b0` | [New construction suppresses default stock · entry](inventory.md#rva-0x00b693b0) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x00b69650` | `0x140b69650` | [CalcContainerWeight callback](inventory.md#rva-0x00b69650) | CalcContainerWeight callback | C |
| `0x00b69760` | `0x140b69760` | [inventory weight query](inventory.md#rva-0x00b69760) | inventory weight query | C |
| `0x00b69c10` | `0x140b69c10` | [ordinary reference identity mass adjustment](inventory.md#rva-0x00b69c10) | ordinary reference identity mass adjustment | C |
| `0x00b6bba0` | `0x140b6bba0` | [Count special resource ingredient](production.md#rva-0x00b6bba0) | Count special resource ingredient | C |
| `0x00b6cb60` | `0x140b6cb60` | [reference modifier extra provider](production.md#rva-0x00b6cb60) | reference modifier extra provider | B |
| `0x00b6cbe0` | `0x140b6cbe0` | [get/create ExtraBF storage](production.md#rva-0x00b6cbe0) | get/create ExtraBF storage | B |
| `0x00b6ce20` | `0x140b6ce20` | [reference effective AV getter](production.md#rva-0x00b6ce20) | reference effective AV getter | B |
| `0x00b6cee0` | `0x140b6cee0` | [Read the permanent reference actor value](population.md#rva-0x00b6cee0) | Read the permanent reference actor value | C |
| `0x00b6cfa0` | `0x140b6cfa0` | [reference base AV getter](production.md#rva-0x00b6cfa0) | reference base AV getter | B |
| `0x00b6d190` | `0x140b6d190` | [set reference base actor value](production.md#rva-0x00b6d190) | set reference base actor value | B |
| `0x00b6d4d0` | `0x140b6d4d0` | [Damage and operational consequences · entry](population.md#rva-0x00b6d4d0) | Original report discusses this roster entry under Damage and operational consequences. | C |
| `0x00b6d720` | `0x140b6d720` | [restore AV negative modifier](power.md#rva-0x00b6d720) | restore AV negative modifier | B |
| `0x00b6ee30` | `0x140b6ee30` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x00b6ee30) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x00b70a80` | `0x140b70a80` | [general insertion fit count](production.md#rva-0x00b70a80) | general insertion fit count | B |
| `0x00b73310` | `0x140b73310` | [Add signed reference frame vector](workshop.md#rva-0x00b73310) | Add signed reference frame vector | C |
| `0x00b734c0` | `0x140b734c0` | [Apply ordinary reference frame conversion](workshop.md#rva-0x00b734c0) | Apply ordinary reference frame conversion | C |
| `0x00b756c0` | `0x140b756c0` | [base component lookup wrapper](inventory.md#rva-0x00b756c0) | base component lookup wrapper | C |
| `0x00b79750` | `0x140b79750` | [Dispatch equipped armor restoration](inventory.md#rva-0x00b79750) | Dispatch equipped armor restoration | C |
| `0x00b79970` | `0x140b79970` | [Dispatch equipped weapon restoration](inventory.md#rva-0x00b79970) | Dispatch equipped weapon restoration | C |
| `0x00b7bd20` | `0x140b7bd20` | [Invoke the selected stack update path](inventory.md#rva-0x00b7bd20) | Invoke the selected stack update path | C |
| `0x00b7c100` | `0x140b7c100` | [Ownership and player action · entry](inventory.md#rva-0x00b7c100) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x00b7c560` | `0x140b7c560` | [Dispatch inventory row visits](inventory.md#rva-0x00b7c560) | Dispatch inventory row visits | C |
| `0x00b7d5b0` | `0x140b7d5b0` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x00b7d5b0) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x00b82b40` | `0x140b82b40` | [base-sheet AV value provider](production.md#rva-0x00b82b40) | base-sheet AV value provider | B |
| `0x00b89690` | `0x140b89690` | [Dispatch cargo stack subtraction to the inventory route](inventory.md#rva-0x00b89690) | Dispatch cargo stack subtraction to the inventory route | C |
| `0x00b89fd0` | `0x140b89fd0` | [Ownership and player action · entry](inventory.md#rva-0x00b89fd0) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x00b8a8c0` | `0x140b8a8c0` | [Dispatch the quantity-removal route](inventory.md#rva-0x00b8a8c0) | Dispatch the quantity-removal route | C |
| `0x00b8f540` | `0x140b8f540` | [Participate in cargo inventory row subtraction](inventory.md#rva-0x00b8f540) | Participate in cargo inventory row subtraction | C |
| `0x00b90250` | `0x140b90250` | [Dispatch deferred cell-finish event work](power.md#rva-0x00b90250) | Dispatch deferred cell-finish event work | C |
| `0x00b979c0` | `0x140b979c0` | [reference notification via separate source](power.md#rva-0x00b979c0) | reference notification via separate source | B |
| `0x00b97ac0` | `0x140b97ac0` | [Participate in dispatch for an admitted loaded reference](power.md#rva-0x00b97ac0) | Participate in dispatch for an admitted loaded reference | C |
| `0x00b97bd0` | `0x140b97bd0` | [Perform bookkeeping on the production path](production.md#rva-0x00b97bd0) | Perform bookkeeping on the production path | C |
| `0x00b994d0` | `0x140b994d0` | [Reach the separate notification registration route](inventory.md#rva-0x00b994d0) | Reach the separate notification registration route | C |
| `0x00b9a110` | `0x140b9a110` | [Reach the source for the reference-bearing cell-finish event](power.md#rva-0x00b9a110) | Reach the source for the reference-bearing cell-finish event | C |
| `0x00b9a340` | `0x140b9a340` | [Reach the object-loaded notification route](inventory.md#rva-0x00b9a340) | Reach the object-loaded notification route | C |
| `0x00b9bdf0` | `0x140b9bdf0` | [Emit builder-selection event](production.md#rva-0x00b9bdf0) | Emit builder-selection event | C |
| `0x00ba0d40` | `0x140ba0d40` | [lifecycle · entry](inventory.md#rva-0x00ba0d40) | Original report discusses this roster entry under lifecycle. | C |
| `0x00ba4eb0` | `0x140ba4eb0` | [Ownership and player action · entry](inventory.md#rva-0x00ba4eb0) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x00ba5700` | `0x140ba5700` | [Ownership and player action · entry](inventory.md#rva-0x00ba5700) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x00bb54a0` | `0x140bb54a0` | [Preparation and the two service pumps · entry](geography.md#rva-0x00bb54a0) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x00bb5570` | `0x140bb5570` | [Typed restoration and packed origin (exports 42–49) · entry](geography.md#rva-0x00bb5570) | Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49). | C |
| `0x00bbb170` | `0x140bbb170` | [Request exterior single-cell preparation](geography.md#rva-0x00bbb170) | Calls the placement preparation path for one admitted cell. | B |
| `0x00bbd270` | `0x140bbd270` | [parent world context resolution](geography.md#rva-0x00bbd270) | parent world context resolution | B |
| `0x00bbda00` | `0x140bbda00` | [Preparation and the two service pumps · entry](geography.md#rva-0x00bbda00) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x00bbdf70` | `0x140bbdf70` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00bbdf70) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00bbe250` | `0x140bbe250` | [Remove cell membership through the worldspace path](geography.md#rva-0x00bbe250) | Remove cell membership through the worldspace path | C |
| `0x00bbe590` | `0x140bbe590` | [Begin removal of the worldspace cell membership](geography.md#rva-0x00bbe590) | Begin removal of the worldspace cell membership | C |
| `0x00bc17b0` | `0x140bc17b0` | [Support world-position lookup before ExtraLocation fallback](workshop.md#rva-0x00bc17b0) | Support world-position lookup before ExtraLocation fallback | C |
| `0x00bc4650` | `0x140bc4650` | [Preparation and the two service pumps · entry](geography.md#rva-0x00bc4650) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x00be3fb0` | `0x140be3fb0` | [Condition callback for the base actor value](population.md#rva-0x00be3fb0) | Condition callback for the base actor value | C |
| `0x00be51a0` | `0x140be51a0` | [Apply the native GetDead condition predicate](population.md#rva-0x00be51a0) | Apply the native GetDead condition predicate | C |
| `0x00bee540` | `0x140bee540` | [HasPerk nonzero rank Boolean evaluator](production.md#rva-0x00bee540) | HasPerk nonzero rank Boolean evaluator | B |
| `0x00bee630` | `0x140bee630` | [Read the perk rank for a native condition](workshop.md#rva-0x00bee630) | Read the perk rank for a native condition | C |
| `0x00bf34a0` | `0x140bf34a0` | [BodyHasKeyword condition](power.md#rva-0x00bf34a0) | BodyHasKeyword condition | B |
| `0x00bf45f0` | `0x140bf45f0` | [Handle CellLoad class 865 source demand](geography.md#rva-0x00bf45f0) | Handle CellLoad class 865 source demand | C |
| `0x00c01fe0` | `0x140c01fe0` | [Wrap the native fuel-readiness condition](inventory.md#rva-0x00c01fe0) | Wrap the native fuel-readiness condition | C |
| `0x00c05220` | `0x140c05220` | [Call the workshop activator diagnostic helper](workshop.md#rva-0x00c05220) | Call the workshop activator diagnostic helper | C |
| `0x00c05610` | `0x140c05610` | [IsPowered numeric condition](production.md#rva-0x00c05610) | IsPowered numeric condition | B |
| `0x00c05630` | `0x140c05630` | [IsPowered condition wrapper](power.md#rva-0x00c05630) | IsPowered condition wrapper | C |
| `0x00c06e00` | `0x140c06e00` | [Evaluate a nested condition form](workshop.md#rva-0x00c06e00) | Evaluate a nested condition form | C |
| `0x00c07e70` | `0x140c07e70` | [Research completion state condition query](production.md#rva-0x00c07e70) | Research completion state condition query | B |
| `0x00c0ad70` | `0x140c0ad70` | [body keyword source evaluation](power.md#rva-0x00c0ad70) | body keyword source evaluation | B |
| `0x00c0b0e0` | `0x140c0b0e0` | [Planetary Habitation: exact environment predicates · entry](workshop.md#rva-0x00c0b0e0) | Original report discusses this roster entry under Planetary Habitation: exact environment predicates. | C |
| `0x00c0b1e0` | `0x140c0b1e0` | [Test associated body keyword sources](workshop.md#rva-0x00c0b1e0) | Test associated body keyword sources | C |
| `0x00c1f400` | `0x140c1f400` | [Dispatch the native local redistribution command](inventory.md#rva-0x00c1f400) | Dispatch the native local redistribution command | C |
| `0x00c228a0` | `0x140c228a0` | [Route the separate text-command setting change](geography.md#rva-0x00c228a0) | Provides a distinct mutation route for the setting. | B |
| `0x00c22a60` | `0x140c22a60` | [Convert and apply a text-driven float setting](geography.md#rva-0x00c22a60) | Convert and apply a text-driven float setting | C |
| `0x00c411c0` | `0x140c411c0` | [HasPerk condition adapter](production.md#rva-0x00c411c0) | HasPerk condition adapter | B |
| `0x00c412a0` | `0x140c412a0` | [prerequisites · entry](inventory.md#rva-0x00c412a0) | Original report discusses this roster entry under prerequisites. | C |
| `0x00c49960` | `0x140c49960` | [HasKeyword condition callback](population.md#rva-0x00c49960) | HasKeyword condition callback | B |
| `0x00c4a810` | `0x140c4a810` | [Resolve the command-side power actor value](power.md#rva-0x00c4a810) | Resolve the command-side power actor value | C |
| `0x00c59ab0` | `0x140c59ab0` | [CanProduceForWorkshop condition](production.md#rva-0x00c59ab0) | CanProduceForWorkshop condition | B |
| `0x00c5b1d0` | `0x140c5b1d0` | [HasKeyword native condition callback](workshop.md#rva-0x00c5b1d0) | HasKeyword native condition callback | C |
| `0x00c5c0c0` | `0x140c5c0c0` | [prerequisites · entry](inventory.md#rva-0x00c5c0c0) | Original report discusses this roster entry under prerequisites. | C |
| `0x00c5c550` | `0x140c5c550` | [ResourceVeinHasKeyword native condition](geography.md#rva-0x00c5c550) | ResourceVeinHasKeyword native condition | B |
| `0x00c7af90` | `0x140c7af90` | [Call the outpost beacon validation lead](workshop.md#rva-0x00c7af90) | Call the outpost beacon validation lead | C |
| `0x00c93cf0` | `0x140c93cf0` | [conditional entry-point evaluator](population.md#rva-0x00c93cf0) | conditional entry-point evaluator | B |
| `0x00c94060` | `0x140c94060` | [variadic entry-point dispatch](population.md#rva-0x00c94060) | variadic entry-point dispatch | B |
| `0x00c94350` | `0x140c94350` | [perk operation 2 arithmetic](power.md#rva-0x00c94350) | perk operation 2 arithmetic | B |
| `0x00c94430` | `0x140c94430` | [single-float multiply operation](population.md#rva-0x00c94430) | single-float multiply operation | B |
| `0x00c954b0` | `0x140c954b0` | [OneValue four-byte field loader](population.md#rva-0x00c954b0) | OneValue four-byte field loader | B |
| `0x00c9cfb0` | `0x140c9cfb0` | [Decode the alias type-5 placement data](workshop.md#rva-0x00c9cfb0) | Decode the alias type-5 placement data | C |
| `0x00c9fda0` | `0x140c9fda0` | [operation index getter](population.md#rva-0x00c9fda0) | operation index getter | B |
| `0x00ca0540` | `0x140ca0540` | [PERK entry type allocation](population.md#rva-0x00ca0540) | PERK entry type allocation | B |
| `0x00ca13b0` | `0x140ca13b0` | [entry-point data loader](population.md#rva-0x00ca13b0) | entry-point data loader | B |
| `0x00ca1a20` | `0x140ca1a20` | [active entry-point registration](population.md#rva-0x00ca1a20) | active entry-point registration | B |
| `0x00ca1bd0` | `0x140ca1bd0` | [active entry-point removal](population.md#rva-0x00ca1bd0) | active entry-point removal | B |
| `0x00ca2490` | `0x140ca2490` | [PERK entry loader](population.md#rva-0x00ca2490) | PERK entry loader | B |
| `0x00ca3670` | `0x140ca3670` | [Compare entries during perk cache insertion](production.md#rva-0x00ca3670) | Compare entries during perk cache insertion | C |
| `0x00ca3910` | `0x140ca3910` | [remove old and install selected perk rank](population.md#rva-0x00ca3910) | remove old and install selected perk rank | B |
| `0x00ca4be0` | `0x140ca4be0` | [sorted active entry insertion](population.md#rva-0x00ca4be0) | sorted active entry insertion | B |
| `0x00cd77d0` | `0x140cd77d0` | [part-specific NPC copy; bit 3 selected grants](population.md#rva-0x00cd77d0) | part-specific NPC copy; bit 3 selected grants | C |
| `0x00cdf140` | `0x140cdf140` | [Participate in effective NPC template assembly](population.md#rva-0x00cdf140) | Participate in effective NPC template assembly | C |
| `0x00cdfde0` | `0x140cdfde0` | [Participate in effective NPC template assembly](population.md#rva-0x00cdfde0) | Participate in effective NPC template assembly | C |
| `0x00cf72d0` | `0x140cf72d0` | [Resolve a group object ID through PackIn metadata](workshop.md#rva-0x00cf72d0) | Resolve a group object ID through PackIn metadata | C |
| `0x00d049b0` | `0x140d049b0` | [Resolve the qualified quest alias fill](workshop.md#rva-0x00d049b0) | Resolve the qualified quest alias fill | C |
| `0x00d4ae40` | `0x140d4ae40` | [Preserved failed routes · entry](inventory.md#rva-0x00d4ae40) | Original report discusses this roster entry under Preserved failed routes. | C |
| `0x00d83ae0` | `0x140d83ae0` | [required fauna scans from player and settings](production.md#rva-0x00d83ae0) | required fauna scans from player and settings | B |
| `0x00d83b80` | `0x140d83b80` | [required flora scans from player and settings](production.md#rva-0x00d83b80) | required flora scans from player and settings | B |
| `0x00d96680` | `0x140d96680` | [Actual causal chain · entry](workshop.md#rva-0x00d96680) | Original report discusses this roster entry under Actual causal chain. | C |
| `0x00d96b20` | `0x140d96b20` | [built-in AV registry initialization](production.md#rva-0x00d96b20) | built-in AV registry initialization | B |
| `0x00d9d170` | `0x140d9d170` | [AVIF field loader](production.md#rva-0x00d9d170) | AVIF field loader | B |
| `0x00e065f0` | `0x140e065f0` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e065f0) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e06760` | `0x140e06760` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e06760) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e06a80` | `0x140e06a80` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e06a80) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e06bb0` | `0x140e06bb0` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e06bb0) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e06ea0` | `0x140e06ea0` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e06ea0) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e06f60` | `0x140e06f60` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e06f60) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e08e90` | `0x140e08e90` | [Movement selection and admission · entry](inventory.md#rva-0x00e08e90) | Original report discusses this roster entry under Movement selection and admission. | C |
| `0x00e09360` | `0x140e09360` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e09360) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e09c90` | `0x140e09c90` | [What progresses without a visible ship · entry](inventory.md#rva-0x00e09c90) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x00e0a140` | `0x140e0a140` | [Entity/field correspondence matrix · entry](inventory.md#rva-0x00e0a140) | Original report discusses this roster entry under Entity/field correspondence matrix. | C |
| `0x00e0a360` | `0x140e0a360` | [Entity/field correspondence matrix · entry](inventory.md#rva-0x00e0a360) | Original report discusses this roster entry under Entity/field correspondence matrix. | C |
| `0x00e466f0` | `0x140e466f0` | [Dispatch generic behavior evaluation](workshop.md#rva-0x00e466f0) | Dispatch generic behavior evaluation | C |
| `0x00e46d70` | `0x140e46d70` | [Evaluate snap-behavior conditions for the resolved context](workshop.md#rva-0x00e46d70) | Evaluate snap-behavior conditions for the resolved context | C |
| `0x00ea6420` | `0x140ea6420` | [Entity/field correspondence matrix · entry](inventory.md#rva-0x00ea6420) | Original report discusses this roster entry under Entity/field correspondence matrix. | C |
| `0x00ea6540` | `0x140ea6540` | [Entity/field correspondence matrix · entry](inventory.md#rva-0x00ea6540) | Original report discusses this roster entry under Entity/field correspondence matrix. | C |
| `0x00eb0340` | `0x140eb0340` | [Build a FlyLand path](inventory.md#rva-0x00eb0340) | Build a FlyLand path | C |
| `0x00eb4a40` | `0x140eb4a40` | [Full flight: geometry, movement profiles and actions · entry](inventory.md#rva-0x00eb4a40) | Original report discusses this roster entry under Full flight: geometry, movement profiles and actions. | C |
| `0x00eb4b90` | `0x140eb4b90` | [Concrete completion provider and detached movement · entry](inventory.md#rva-0x00eb4b90) | Original report discusses this roster entry under Concrete completion provider and detached movement. | C |
| `0x00f2f0e0` | `0x140f2f0e0` | [Classify candidate placement eligibility](workshop.md#rva-0x00f2f0e0) | Classify candidate placement eligibility | C |
| `0x00f2fc50` | `0x140f2fc50` | [Dispatch the reference damage route](population.md#rva-0x00f2fc50) | Dispatch the reference damage route | C |
| `0x00f2fd40` | `0x140f2fd40` | [Damage and operational consequences · entry](workshop.md#rva-0x00f2fd40) | Original report discusses this roster entry under Damage and operational consequences. | C |
| `0x00f2ffb0` | `0x140f2ffb0` | [Transfer a reference handle into the clearing state](workshop.md#rva-0x00f2ffb0) | Transfer a reference handle into the clearing state | C |
| `0x00f30380` | `0x140f30380` | [Restore the mapped reference placement state](workshop.md#rva-0x00f30380) | Restore the mapped reference placement state | C |
| `0x00f30820` | `0x140f30820` | [Commit the mapped reference placement state](workshop.md#rva-0x00f30820) | Commit the mapped reference placement state | C |
| `0x00f33180` | `0x140f33180` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f33180) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f34590` | `0x140f34590` | [cached Workshop summary reader](production.md#rva-0x00f34590) | cached Workshop summary reader | B |
| `0x00f34650` | `0x140f34650` | [removal through cleanup](population.md#rva-0x00f34650) | removal through cleanup | C |
| `0x00f34be0` | `0x140f34be0` | [Handle Workshop context for the display attachment](inventory.md#rva-0x00f34be0) | Handle Workshop context for the display attachment | C |
| `0x00f35090` | `0x140f35090` | [Invoke the follow-up for a changed power reference](power.md#rva-0x00f35090) | Invoke the follow-up for a changed power reference | C |
| `0x00f35870` | `0x140f35870` | [Receive the workshop activator diagnostic call](workshop.md#rva-0x00f35870) | Receive the workshop activator diagnostic call | C |
| `0x00f35940` | `0x140f35940` | [Workshop catalogue map builder](workshop.md#rva-0x00f35940) | Workshop catalogue map builder | C |
| `0x00f36310` | `0x140f36310` | [Restore existing-reference Health and destruction state](population.md#rva-0x00f36310) | Restore existing-reference Health and destruction state | C |
| `0x00f366c0` | `0x140f366c0` | [Storage, inventory and cargo native entry](inventory.md#rva-0x00f366c0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00f38600` | `0x140f38600` | [New construction suppresses default stock · entry](inventory.md#rva-0x00f38600) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x00f386a0` | `0x140f386a0` | [Native population · entry](population.md#rva-0x00f386a0) | Original report discusses this roster entry under Native population. | C |
| `0x00f387f0` | `0x140f387f0` | [Deployment allowance and ordinary beacon operation · entry](workshop.md#rva-0x00f387f0) | Original report discusses this roster entry under Deployment allowance and ordinary beacon operation. | C |
| `0x00f38a40` | `0x140f38a40` | [native · entry](workshop.md#rva-0x00f38a40) | Original report discusses this roster entry under native. | C |
| `0x00f38cb0` | `0x140f38cb0` | [Territory and POI context · entry](workshop.md#rva-0x00f38cb0) | Original report discusses this roster entry under Territory and POI context. | C |
| `0x00f38d80` | `0x140f38d80` | [Other admission boundaries and persistence · entry](workshop.md#rva-0x00f38d80) | Original report discusses this roster entry under Other admission boundaries and persistence. | C |
| `0x00f38e30` | `0x140f38e30` | [Obtain Workshop geometry radius](workshop.md#rva-0x00f38e30) | Obtain Workshop geometry radius | C |
| `0x00f39010` | `0x140f39010` | [Territory and POI context · entry](workshop.md#rva-0x00f39010) | Original report discusses this roster entry under Territory and POI context. | C |
| `0x00f391c0` | `0x140f391c0` | [Territory and POI context · entry](workshop.md#rva-0x00f391c0) | Original report discusses this roster entry under Territory and POI context. | C |
| `0x00f3a640` | `0x140f3a640` | [Supply references to placement clearing](workshop.md#rva-0x00f3a640) | Supply references to placement clearing | C |
| `0x00f3a6e0` | `0x140f3a6e0` | [Remove display roots and child references](inventory.md#rva-0x00f3a6e0) | Remove display roots and child references | C |
| `0x00f3b080` | `0x140f3b080` | [construction base to COBJ lookup](population.md#rva-0x00f3b080) | construction base to COBJ lookup | C |
| `0x00f3b170` | `0x140f3b170` | [count matching recipe limit global in selected-context item set](population.md#rva-0x00f3b170) | count matching recipe limit global in selected-context item set | C |
| `0x00f3b300` | `0x140f3b300` | [Insert an eligible Workshop handle](workshop.md#rva-0x00f3b300) | Insert an eligible Workshop handle | C |
| `0x00f3b500` | `0x140f3b500` | [Remove a Workshop handle from the registry](workshop.md#rva-0x00f3b500) | Remove a Workshop handle from the registry | C |
| `0x00f3bfc0` | `0x140f3bfc0` | [Test the resolved Locations exclusion keyword](interfaces.md#rva-0x00f3bfc0) | Tests a reference for the resolved WorkshopUseDecorateTextKeyword default object. | B |
| `0x00f3c7e0` | `0x140f3c7e0` | [Participate in existing-beacon availability](workshop.md#rva-0x00f3c7e0) | Participate in existing-beacon availability | C |
| `0x00f3c8c0` | `0x140f3c8c0` | [Other admission boundaries and persistence · entry](workshop.md#rva-0x00f3c8c0) | Original report discusses this roster entry under Other admission boundaries and persistence. | C |
| `0x00f3cc90` | `0x140f3cc90` | [Repair, identity and accounting · entry](workshop.md#rva-0x00f3cc90) | Original report discusses this roster entry under Repair, identity and accounting. | C |
| `0x00f3ce30` | `0x140f3ce30` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f3ce30) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f3ced0` | `0x140f3ced0` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f3ced0) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f3cf40` | `0x140f3cf40` | [WorkshopItem owner relationship](population.md#rva-0x00f3cf40) | WorkshopItem owner relationship | C |
| `0x00f3dd50` | `0x140f3dd50` | [Fold eligible crew power additions per generator](power.md#rva-0x00f3dd50) | Dispatches DB entries for eligible assigned actors and can invalidate failed E2 handle slots. | A |
| `0x00f3df70` | `0x140f3df70` | [Resolve Workshop through the operation interface](workshop.md#rva-0x00f3df70) | Resolve Workshop through the operation interface | C |
| `0x00f3e2e0` | `0x140f3e2e0` | [Nearby scenery clearing versus collision · entry](geography.md#rva-0x00f3e2e0) | Original report discusses this roster entry under Nearby scenery clearing versus collision. | C |
| `0x00f3f680` | `0x140f3f680` | [Continue the candidate placement physics route](workshop.md#rva-0x00f3f680) | Continue the candidate placement physics route | C |
| `0x00f3f9a0` | `0x140f3f9a0` | [Fold final placement admission into candidate status](workshop.md#rva-0x00f3f9a0) | Updates the selected candidate status after spatial, resource and quota checks. | B |
| `0x00f404f0` | `0x140f404f0` | [remove wrappers through 1421c6b90](population.md#rva-0x00f404f0) | remove wrappers through 1421c6b90 | C |
| `0x00f412c0` | `0x140f412c0` | [Reconcile old and new placement clearing sets](workshop.md#rva-0x00f412c0) | Reconcile old and new placement clearing sets | C |
| `0x00f42df0` | `0x140f42df0` | [Enumerate reverse Workshop membership edges](workshop.md#rva-0x00f42df0) | Enumerate reverse Workshop membership edges | C |
| `0x00f42ec0` | `0x140f42ec0` | [New construction suppresses default stock · entry](inventory.md#rva-0x00f42ec0) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x00f44c00` | `0x140f44c00` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00f44c00) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00f460c0` | `0x140f460c0` | [Dispatch candidate placement physics checks](workshop.md#rva-0x00f460c0) | Dispatch candidate placement physics checks | C |
| `0x00f46370` | `0x140f46370` | [Continue candidate placement physics checks](workshop.md#rva-0x00f46370) | Continue candidate placement physics checks | C |
| `0x00f46840` | `0x140f46840` | [Sample heights for Workshop border mesh](workshop.md#rva-0x00f46840) | Sample heights for Workshop border mesh | C |
| `0x00f46910` | `0x140f46910` | [Build Workshop border vertex arrays](workshop.md#rva-0x00f46910) | Build Workshop border vertex arrays | C |
| `0x00f47de0` | `0x140f47de0` | [Find terrain coverage for Workshop border](workshop.md#rva-0x00f47de0) | Find terrain coverage for Workshop border | C |
| `0x00f48480` | `0x140f48480` | [Refine Workshop border samples](workshop.md#rva-0x00f48480) | Refine Workshop border samples | C |
| `0x00f48a60` | `0x140f48a60` | [Sample Workshop border ring](workshop.md#rva-0x00f48a60) | Sample Workshop border ring | C |
| `0x00f49440` | `0x140f49440` | [Build circular Workshop border](workshop.md#rva-0x00f49440) | Build circular Workshop border | C |
| `0x00f49c50` | `0x140f49c50` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00f49c50) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00f4a140` | `0x140f4a140` | [Workshop area descriptor builder](geography.md#rva-0x00f4a140) | Workshop area descriptor builder | B |
| `0x00f4a5b0` | `0x140f4a5b0` | [Clean up the placement descriptor](workshop.md#rva-0x00f4a5b0) | Clean up the placement descriptor | C |
| `0x00f4a910` | `0x140f4a910` | [Workshop descriptor boundary predicate](power.md#rva-0x00f4a910) | Workshop descriptor boundary predicate | B |
| `0x00f4aa50` | `0x140f4aa50` | [Territory and POI context · entry](workshop.md#rva-0x00f4aa50) | Original report discusses this roster entry under Territory and POI context. | C |
| `0x00f4aab0` | `0x140f4aab0` | [candidate world and position gate](power.md#rva-0x00f4aab0) | candidate world and position gate | B |
| `0x00f4ab80` | `0x140f4ab80` | [Resolve current Workshop center](workshop.md#rva-0x00f4ab80) | Resolve current Workshop center | C |
| `0x00f4ac50` | `0x140f4ac50` | [vertex acceptance helper](geography.md#rva-0x00f4ac50) | vertex acceptance helper | B |
| `0x00f4af20` | `0x140f4af20` | [Support multipoint descriptor geometry tests](geography.md#rva-0x00f4af20) | Support multipoint descriptor geometry tests | C |
| `0x00f4c770` | `0x140f4c770` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f4c770) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f4c7f0` | `0x140f4c7f0` | [Causal path · entry](workshop.md#rva-0x00f4c7f0) | Original report discusses this roster entry under Causal path. | C |
| `0x00f4c980` | `0x140f4c980` | [Mutations, movement and restored state · entry](workshop.md#rva-0x00f4c980) | Original report discusses this roster entry under Mutations, movement and restored state. | C |
| `0x00f4ca70` | `0x140f4ca70` | [Account for budget usage on deletion](workshop.md#rva-0x00f4ca70) | Account for budget usage on deletion | C |
| `0x00f4cb70` | `0x140f4cb70` | [Causal path · entry](workshop.md#rva-0x00f4cb70) | Original report discusses this roster entry under Causal path. | C |
| `0x00f4cc70` | `0x140f4cc70` | [Definition to category map · entry](workshop.md#rva-0x00f4cc70) | Original report discusses this roster entry under Definition to category map. | C |
| `0x00f4cf60` | `0x140f4cf60` | [Allocate a conditional builder catalogue entry](workshop.md#rva-0x00f4cf60) | Allocate a conditional builder catalogue entry | C |
| `0x00f4d630` | `0x140f4d630` | [Loaded COBJ discovery walk](workshop.md#rva-0x00f4d630) | Loaded COBJ discovery walk | C |
| `0x00f4e760` | `0x140f4e760` | [Concrete sub-item controls · entry](workshop.md#rva-0x00f4e760) | Original report discusses this roster entry under Concrete sub-item controls. | C |
| `0x00f4ecd0` | `0x140f4ecd0` | [Concrete sub-item controls · entry](workshop.md#rva-0x00f4ecd0) | Original report discusses this roster entry under Concrete sub-item controls. | C |
| `0x00f4fa20` | `0x140f4fa20` | [Obtain ItemProduced event source](production.md#rva-0x00f4fa20) | Obtain ItemProduced event source | C |
| `0x00f4ffc0` | `0x140f4ffc0` | [Construct typed Workshop ExtraData](workshop.md#rva-0x00f4ffc0) | Initializes the concrete type and its compensation fields. | B |
| `0x00f50660` | `0x140f50660` | [Serialize Workshop producer state](production.md#rva-0x00f50660) | Serialize Workshop producer state | C |
| `0x00f50880` | `0x140f50880` | [Restore Workshop extra and producer-map data](production.md#rva-0x00f50880) | Restore Workshop extra and producer-map data | C |
| `0x00f51350` | `0x140f51350` | [Get typed Workshop ExtraData from a qualified reference](workshop.md#rva-0x00f51350) | Checks the reference and obtains Workshop ExtraData through the reference's extra list. | B |
| `0x00f515a0` | `0x140f515a0` | [Workshop row iterator serializes resource/object identity plus 17 body bytes from 0x1c…](geography.md#rva-0x00f515a0) | Workshop row iterator serializes resource/object identity plus 17 body bytes from 0x1c native rows; not region arrays | C |
| `0x00f51ee0` | `0x140f51ee0` | [Nearby scenery clearing versus collision · entry](workshop.md#rva-0x00f51ee0) | Original report discusses this roster entry under Nearby scenery clearing versus collision. | C |
| `0x00f5a800` | `0x140f5a800` | [Dispatch generated foundation or stair support](workshop.md#rva-0x00f5a800) | Dispatch generated foundation or stair support | C |
| `0x00f5b130` | `0x140f5b130` | [Dispatch the paired generated support or stair operation](workshop.md#rva-0x00f5b130) | Dispatch the paired generated support or stair operation | C |
| `0x00f5b260` | `0x140f5b260` | [Construct a native item representative](workshop.md#rva-0x00f5b260) | Construct a native item representative | C |
| `0x00f5b8f0` | `0x140f5b8f0` | [Initialize the item root identity](workshop.md#rva-0x00f5b8f0) | Initialize the item root identity | C |
| `0x00f5bb30` | `0x140f5bb30` | [Resolve the target for generated foundation or stair support](workshop.md#rva-0x00f5bb30) | Resolve the target for generated foundation or stair support | C |
| `0x00f5bd50` | `0x140f5bd50` | [Participate in support and generated-child construction](workshop.md#rva-0x00f5bd50) | Participate in support and generated-child construction | C |
| `0x00f5c1b0` | `0x140f5c1b0` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f5c1b0) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f5f2d0` | `0x140f5f2d0` | [registry callback exclusion predicate](population.md#rva-0x00f5f2d0) | registry callback exclusion predicate | C |
| `0x00f60db0` | `0x140f60db0` | [Read the native single-item root](workshop.md#rva-0x00f60db0) | Read the native single-item root | C |
| `0x00f60f60` | `0x140f60f60` | [SingleWorkshopItem virtual method at +A0 placement](population.md#rva-0x00f60f60) | SingleWorkshopItem virtual method at +A0 placement | C |
| `0x00f62170` | `0x140f62170` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f62170) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f64b00` | `0x140f64b00` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f64b00) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f65870` | `0x140f65870` | [UI link creation command](inventory.md#rva-0x00f65870) | UI link creation command | C |
| `0x00f65ae0` | `0x140f65ae0` | [commit selected explicit wire](power.md#rva-0x00f65ae0) | commit selected explicit wire | B |
| `0x00f65c50` | `0x140f65c50` | [Replace old wire connection](power.md#rva-0x00f65c50) | Replace old wire connection | C |
| `0x00f65fa0` | `0x140f65fa0` | [Read the native member range](workshop.md#rva-0x00f65fa0) | Read the native member range | C |
| `0x00f661e0` | `0x140f661e0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x00f661e0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x00f66220` | `0x140f66220` | [Commit a PackIn snap connection](workshop.md#rva-0x00f66220) | Commit a PackIn snap connection | C |
| `0x00f686f0` | `0x140f686f0` | [Read the native PackIn root](workshop.md#rva-0x00f686f0) | Read the native PackIn root | C |
| `0x00f69b90` | `0x140f69b90` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f69b90) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f6e260` | `0x140f6e260` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x00f6e260) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x00f7ba90` | `0x140f7ba90` | [Allowance, admission and action · entry](workshop.md#rva-0x00f7ba90) | Original report discusses this roster entry under Allowance, admission and action. | C |
| `0x00f7bd20` | `0x140f7bd20` | [Fold assigned actor and player production-timer modifiers](production.md#rva-0x00f7bd20) | Applies eligible A1 entries to the current producer interval. | A |
| `0x00f7bf10` | `0x140f7bf10` | [effective resource interval](production.md#rva-0x00f7bf10) | effective resource interval | B |
| `0x00f7bf80` | `0x140f7bf80` | [effective nominal rate per minute](production.md#rva-0x00f7bf80) | effective nominal rate per minute | B |
| `0x00f7c000` | `0x140f7c000` | [effective harvester multiplier](production.md#rva-0x00f7c000) | effective harvester multiplier | B |
| `0x00f7c060` | `0x140f7c060` | [React to actor-value changes](power.md#rva-0x00f7c060) | React to actor-value changes | C |
| `0x00f7c1e0` | `0x140f7c1e0` | [base resource interval](production.md#rva-0x00f7c1e0) | base resource interval | B |
| `0x00f7c210` | `0x140f7c210` | [destination capacity gate](production.md#rva-0x00f7c210) | destination capacity gate | B |
| `0x00f7c290` | `0x140f7c290` | [Query resources for a selected candidate](geography.md#rva-0x00f7c290) | Query resources for a selected candidate | C |
| `0x00f7c510` | `0x140f7c510` | [Placement and registration use distinct resource operations · entry](workshop.md#rva-0x00f7c510) | Original report discusses this roster entry under Placement and registration use distinct resource operations. | C |
| `0x00f7c9f0` | `0x140f7c9f0` | [Test the harvester category](geography.md#rva-0x00f7c9f0) | Test the harvester category | C |
| `0x00f7cab0` | `0x140f7cab0` | [Test Builder category](production.md#rva-0x00f7cab0) | Test Builder category | C |
| `0x00f7cb70` | `0x140f7cb70` | [Test alternate production category](production.md#rva-0x00f7cb70) | Test alternate production category | C |
| `0x00f7cc70` | `0x140f7cc70` | [production halt predicate](production.md#rva-0x00f7cc70) | production halt predicate | B |
| `0x00f7d030` | `0x140f7d030` | [Test production fuel category](production.md#rva-0x00f7d030) | Test production fuel category | C |
| `0x00f7d0b0` | `0x140f7d0b0` | [Check whether to admit the destination container](inventory.md#rva-0x00f7d0b0) | Check whether to admit the destination container | C |
| `0x00f7d120` | `0x140f7d120` | [Evaluate current producer eligibility reason](production.md#rva-0x00f7d120) | Selects a current production reason, with a charged-pad exception in mode 0. | A |
| `0x00f7d510` | `0x140f7d510` | [Select production destination](production.md#rva-0x00f7d510) | Select production destination | C |
| `0x00f7d6a0` | `0x140f7d6a0` | [Request due producer work and ingredient removal](production.md#rva-0x00f7d6a0) | Caps production to available ingredients and issues removal requests for a fueled cargo pad. | A |
| `0x00f7dfa0` | `0x140f7dfa0` | [producer row refresh](production.md#rva-0x00f7dfa0) | producer row refresh | B |
| `0x00f7e530` | `0x140f7e530` | [Handle the container-changed event callback](inventory.md#rva-0x00f7e530) | Handle the container-changed event callback | C |
| `0x00f7e6f0` | `0x140f7e6f0` | [Workshop and transfer state serializer](production.md#rva-0x00f7e6f0) | Workshop and transfer state serializer | B |
| `0x00f7ea10` | `0x140f7ea10` | [Workshop and transfer state restoration](production.md#rva-0x00f7ea10) | Workshop and transfer state restoration | B |
| `0x00f7ee40` | `0x140f7ee40` | [Positive lifecycle chain · entry](inventory.md#rva-0x00f7ee40) | Original report discusses this roster entry under Positive lifecycle chain. | C |
| `0x00f7ef20` | `0x140f7ef20` | [Update registered Workshop producers](production.md#rva-0x00f7ef20) | Passes caller-supplied elapsed time to producer rows for resolvable registered Workshops. | A |
| `0x00f7f1e0` | `0x140f7f1e0` | [Advance one shared Workshop production schedule](production.md#rva-0x00f7f1e0) | Computes due cycles and conditionally dispatches production before refreshing interval state. | A |
| `0x00f7f6f0` | `0x140f7f6f0` | [recipe resource-count selection](production.md#rva-0x00f7f6f0) | recipe resource-count selection | B |
| `0x00f7fd50` | `0x140f7fd50` | [Collect ingredients for qualifying immediate destinations](inventory.md#rva-0x00f7fd50) | Collect ingredients for qualifying immediate destinations | C |
| `0x00f80af0` | `0x140f80af0` | [direct outgoing destination handles](production.md#rva-0x00f80af0) | direct outgoing destination handles | B |
| `0x00f81000` | `0x140f81000` | [predict incompatible links for recipe](production.md#rva-0x00f81000) | predict incompatible links for recipe | B |
| `0x00f81200` | `0x140f81200` | [insert directional transfer edge](production.md#rva-0x00f81200) | insert directional transfer edge | B |
| `0x00f81a90` | `0x140f81a90` | [remove directional transfer edge](production.md#rva-0x00f81a90) | remove directional transfer edge | B |
| `0x00f81cc0` | `0x140f81cc0` | [revalidate/prune links after resource change](production.md#rva-0x00f81cc0) | revalidate/prune links after resource change | B |
| `0x00f82160` | `0x140f82160` | [Actual movement triggers and scheduler boundary · entry](inventory.md#rva-0x00f82160) | Original report discusses this roster entry under Actual movement triggers and scheduler boundary. | C |
| `0x00f82820` | `0x140f82820` | [Directed identity and traversal · entry](inventory.md#rva-0x00f82820) | Original report discusses this roster entry under Directed identity and traversal. | C |
| `0x00f82c30` | `0x140f82c30` | [Select transitive local storage](inventory.md#rva-0x00f82c30) | Select transitive local storage | C |
| `0x00f82f30` | `0x140f82f30` | [Clear the producer registry and caches on global reset](inventory.md#rva-0x00f82f30) | Clear the producer registry and caches on global reset | C |
| `0x00f83020` | `0x140f83020` | [saves · entry](inventory.md#rva-0x00f83020) | Original report discusses this roster entry under saves. | C |
| `0x00f83120` | `0x140f83120` | [Refresh producer eligibility after resource changes](power.md#rva-0x00f83120) | Refresh producer eligibility after resource changes | C |
| `0x00f83450` | `0x140f83450` | [Refresh producer eligibility after state changes](power.md#rva-0x00f83450) | Refresh producer eligibility after state changes | C |
| `0x00f836e0` | `0x140f836e0` | [Perform the UI deletion update](inventory.md#rva-0x00f836e0) | Perform the UI deletion update | C |
| `0x00f83900` | `0x140f83900` | [deregister selected resource row](production.md#rva-0x00f83900) | deregister selected resource row | B |
| `0x00f83b90` | `0x140f83b90` | [producer registration](production.md#rva-0x00f83b90) | producer registration | B |
| `0x00f83f60` | `0x140f83f60` | [source capability and outgoing prohibition](inventory.md#rva-0x00f83f60) | source capability and outgoing prohibition | C |
| `0x00f84020` | `0x140f84020` | [Participate in capacity and filter evaluation](inventory.md#rva-0x00f84020) | Participate in capacity and filter evaluation | C |
| `0x00f841c0` | `0x140f841c0` | [outgoing destination compatibility](production.md#rva-0x00f841c0) | outgoing destination compatibility | B |
| `0x00f843e0` | `0x140f843e0` | [transfer topology guard wrapper](production.md#rva-0x00f843e0) | transfer topology guard wrapper | B |
| `0x00f84470` | `0x140f84470` | [transfer endpoint compatibility decision](production.md#rva-0x00f84470) | transfer endpoint compatibility decision | B |
| `0x00f84c40` | `0x140f84c40` | [per-item local destination exclusion](inventory.md#rva-0x00f84c40) | per-item local destination exclusion | C |
| `0x00f84d70` | `0x140f84d70` | [local descriptor execution wrapper](inventory.md#rva-0x00f84d70) | local descriptor execution wrapper | C |
| `0x00f84fc0` | `0x140f84fc0` | [floor-fit transfer descriptor construction](inventory.md#rva-0x00f84fc0) | floor-fit transfer descriptor construction | C |
| `0x00f85760` | `0x140f85760` | [Validate and add an output edge before redistribution](inventory.md#rva-0x00f85760) | Validate and add an output edge before redistribution | C |
| `0x00f85900` | `0x140f85900` | [fauna domesticability](production.md#rva-0x00f85900) | fauna domesticability | B |
| `0x00f85970` | `0x140f85970` | [flora resource normalization](production.md#rva-0x00f85970) | flora resource normalization | B |
| `0x00f859d0` | `0x140f859d0` | [organic selector list builder](production.md#rva-0x00f859d0) | organic selector list builder | B |
| `0x00f85f80` | `0x140f85f80` | [resource eligibility dedup fold](production.md#rva-0x00f85f80) | resource eligibility dedup fold | B |
| `0x00f86060` | `0x140f86060` | [Check organic construction capability](workshop.md#rva-0x00f86060) | Check organic construction capability | C |
| `0x00f86170` | `0x140f86170` | [organic default selection initialization](production.md#rva-0x00f86170) | organic default selection initialization | B |
| `0x00f86360` | `0x140f86360` | [planet fauna candidates](production.md#rva-0x00f86360) | planet fauna candidates | B |
| `0x00f864c0` | `0x140f864c0` | [planet flora candidates](production.md#rva-0x00f864c0) | planet flora candidates | B |
| `0x00f86590` | `0x140f86590` | [flora resource and knowledge rows](production.md#rva-0x00f86590) | flora resource and knowledge rows | B |
| `0x00f87f00` | `0x140f87f00` | [Queue loaded output-link cache reconstruction](inventory.md#rva-0x00f87f00) | Queue loaded output-link cache reconstruction | C |
| `0x00f881c0` | `0x140f881c0` | [incoming production source traversal](production.md#rva-0x00f881c0) | incoming production source traversal | B |
| `0x00f894c0` | `0x140f894c0` | [Traverse link topology](production.md#rva-0x00f894c0) | Traverse link topology | C |
| `0x00f89d00` | `0x140f89d00` | [Filter inventory items before local transfer](inventory.md#rva-0x00f89d00) | Filter inventory items before local transfer | C |
| `0x00f8a020` | `0x140f8a020` | [Actual movement triggers and scheduler boundary · entry](inventory.md#rva-0x00f8a020) | Original report discusses this roster entry under Actual movement triggers and scheduler boundary. | C |
| `0x00f8a920` | `0x140f8a920` | [Traverse domesticability ancestry](production.md#rva-0x00f8a920) | Traverse domesticability ancestry | C |
| `0x00f8b530` | `0x140f8b530` | [Match flora recipe product](production.md#rva-0x00f8b530) | Match flora recipe product | C |
| `0x00f8b570` | `0x140f8b570` | [Dispatch loaded output-link cache reconstruction](inventory.md#rva-0x00f8b570) | Dispatch loaded output-link cache reconstruction | C |
| `0x00f8bbd0` | `0x140f8bbd0` | [fauna knowledge rows](production.md#rva-0x00f8bbd0) | fauna knowledge rows | B |
| `0x00f8be60` | `0x140f8be60` | [manufactured catalogue callback](production.md#rva-0x00f8be60) | manufactured catalogue callback | B |
| `0x00f8c580` | `0x140f8c580` | [Replay eligible pending production on object load](production.md#rva-0x00f8c580) | Conditionally dispatches pending production for the matching producer row. | B |
| `0x00f8ccf0` | `0x140f8ccf0` | [Build the base-container inventory view](inventory.md#rva-0x00f8ccf0) | Build the base-container inventory view | C |
| `0x00f8ce70` | `0x140f8ce70` | [flora planet range traversal](production.md#rva-0x00f8ce70) | flora planet range traversal | B |
| `0x01116580` | `0x141116580` | [point to segment distance squared](geography.md#rva-0x01116580) | point to segment distance squared | B |
| `0x01271140` | `0x141271140` | [Elapsed producer and staged consumers · entry](inventory.md#rva-0x01271140) | Original report discusses this roster entry under Elapsed producer and staged consumers. | C |
| `0x012aa710` | `0x1412aa710` | [Resolve the Actor or component movement controller](inventory.md#rva-0x012aa710) | Resolve the Actor or component movement controller | C |
| `0x012ab460` | `0x1412ab460` | [What progresses without a visible ship · entry](inventory.md#rva-0x012ab460) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x012ac500` | `0x1412ac500` | [Elapsed producer and staged consumers · entry](inventory.md#rva-0x012ac500) | Original report discusses this roster entry under Elapsed producer and staged consumers. | C |
| `0x012aeb90` | `0x1412aeb90` | [Resolve and dispatch a reference movement controller](inventory.md#rva-0x012aeb90) | Checks the reference and resolves an Actor or component controller before update dispatch. | B |
| `0x012aee90` | `0x1412aee90` | [Forward elapsed time through the reference movement wrapper](inventory.md#rva-0x012aee90) | Retains a floating elapsed input through preliminary state work. | B |
| `0x012af0e0` | `0x1412af0e0` | [Pass frame delta to the controller update slot](inventory.md#rva-0x012af0e0) | Moves the floating elapsed operand into the virtual controller update. | B |
| `0x012b5c60` | `0x1412b5c60` | [additional perk rank record update](population.md#rva-0x012b5c60) | additional perk rank record update | B |
| `0x012b60a0` | `0x1412b60a0` | [Write additional selected actor perk ranks](population.md#rva-0x012b60a0) | Write additional selected actor perk ranks | C |
| `0x012b62f0` | `0x1412b62f0` | [Selected rank and load reconstruction · entry](population.md#rva-0x012b62f0) | Original report discusses this roster entry under Selected rank and load reconstruction. | C |
| `0x012b6eb0` | `0x1412b6eb0` | [Read the actor owned-perk rank list](population.md#rva-0x012b6eb0) | Read the actor owned-perk rank list | C |
| `0x012b7020` | `0x1412b7020` | [Read the other actor perk-state representation](population.md#rva-0x012b7020) | Read the other actor perk-state representation | C |
| `0x012ed2a0` | `0x1412ed2a0` | [Install retained resource output storage](geography.md#rva-0x012ed2a0) | Install retained resource output storage | C |
| `0x012fd300` | `0x1412fd300` | [Display component row writer](inventory.md#rva-0x012fd300) | Display component row writer | C |
| `0x012fd450` | `0x1412fd450` | [Display component row reader](inventory.md#rva-0x012fd450) | Display component row reader | C |
| `0x012fd650` | `0x1412fd650` | [Display item identity fixup](inventory.md#rva-0x012fd650) | Display item identity fixup | C |
| `0x012fd980` | `0x1412fd980` | [Restore dropped-reference attachment context](inventory.md#rva-0x012fd980) | Restore dropped-reference attachment context | C |
| `0x012fdfb0` | `0x1412fdfb0` | [Reconcile qualified display inventories after load](inventory.md#rva-0x012fdfb0) | Reconcile qualified display inventories after load | C |
| `0x012fe780` | `0x1412fe780` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x012fe780) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x012fe810` | `0x1412fe810` | [Display component loader](inventory.md#rva-0x012fe810) | Display component loader | C |
| `0x012fea50` | `0x1412fea50` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x012fea50) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x012ff2d0` | `0x1412ff2d0` | [Compose the selected display rule and item data](inventory.md#rva-0x012ff2d0) | Compose the selected display rule and item data | C |
| `0x012ff580` | `0x1412ff580` | [Inventory instance to displayed reference · entry](inventory.md#rva-0x012ff580) | Original report discusses this roster entry under Inventory instance to displayed reference. | C |
| `0x012ffae0` | `0x1412ffae0` | [Inventory instance to displayed reference · entry](inventory.md#rva-0x012ffae0) | Original report discusses this roster entry under Inventory instance to displayed reference. | C |
| `0x01300fc0` | `0x141300fc0` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x01300fc0) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x013026e0` | `0x1413026e0` | [Register loaded and unloaded display components](inventory.md#rva-0x013026e0) | Register loaded and unloaded display components | C |
| `0x01302bb0` | `0x141302bb0` | [Handle the display-component load callback](inventory.md#rva-0x01302bb0) | Handle the display-component load callback | C |
| `0x01302bc0` | `0x141302bc0` | [Handle the display-component load callback](inventory.md#rva-0x01302bc0) | Handle the display-component load callback | C |
| `0x01303ce0` | `0x141303ce0` | [Look up the display-case component](inventory.md#rva-0x01303ce0) | Look up the display-case component | C |
| `0x01303d30` | `0x141303d30` | [Serialize unloaded display components](inventory.md#rva-0x01303d30) | Serialize unloaded display components | C |
| `0x01303fa0` | `0x141303fa0` | [Serialize loaded display components](inventory.md#rva-0x01303fa0) | Serialize loaded display components | C |
| `0x013049e0` | `0x1413049e0` | [New construction suppresses default stock · entry](inventory.md#rva-0x013049e0) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x01304dd0` | `0x141304dd0` | [Update the selected display rule's component list](inventory.md#rva-0x01304dd0) | Update the selected display rule's component list | C |
| `0x01304f40` | `0x141304f40` | [Remove displayed reference from slot lists](inventory.md#rva-0x01304f40) | Remove displayed reference from slot lists | C |
| `0x01305190` | `0x141305190` | [Update the display component after clearing stock](inventory.md#rva-0x01305190) | Update the display component after clearing stock | C |
| `0x01308640` | `0x141308640` | [full scan and currently eligible info completeness](production.md#rva-0x01308640) | full scan and currently eligible info completeness | B |
| `0x01308d40` | `0x141308d40` | [evaluate ordered scanner keyword conditions](production.md#rva-0x01308d40) | evaluate ordered scanner keyword conditions | B |
| `0x01308ee0` | `0x141308ee0` | [rebuild species eligible keyword cache](production.md#rva-0x01308ee0) | rebuild species eligible keyword cache | B |
| `0x0130a3e0` | `0x14130a3e0` | [species knowledge membership](production.md#rva-0x0130a3e0) | species knowledge membership | B |
| `0x0130caa0` | `0x14130caa0` | [Deduplicate available crew registration](population.md#rva-0x0130caa0) | Deduplicate available crew registration | C |
| `0x0130cd20` | `0x14130cd20` | [Remove old crew assignments before insertion](population.md#rva-0x0130cd20) | Remove old crew assignments before insertion | C |
| `0x0130ce90` | `0x14130ce90` | [Serialize the unassigned registry](population.md#rva-0x0130ce90) | Serialize the unassigned registry | C |
| `0x0130d540` | `0x14130d540` | [Persistence classes · entry](population.md#rva-0x0130d540) | Original report discusses this roster entry under Persistence classes. | C |
| `0x0130d650` | `0x14130d650` | [Persistence classes · entry](population.md#rva-0x0130d650) | Original report discusses this roster entry under Persistence classes. | C |
| `0x0130fa20` | `0x14130fa20` | [Access a unit-6 typed component row](geography.md#rva-0x0130fa20) | Access a unit-6 typed component row | C |
| `0x0130fba0` | `0x14130fba0` | [Enumerate ship management components for registry serialization](population.md#rva-0x0130fba0) | Enumerate ship management components for registry serialization | C |
| `0x0130feb0` | `0x14130feb0` | [Entry points and actual source lists · entry](population.md#rva-0x0130feb0) | Original report discusses this roster entry under Entry points and actual source lists. | C |
| `0x0132d260` | `0x14132d260` | [Descriptor writer](interfaces.md#rva-0x0132d260) | Descriptor writer | C |
| `0x0132d500` | `0x14132d500` | [Read generated-world descriptor](geography.md#rva-0x0132d500) | Read generated-world descriptor | C |
| `0x0132e880` | `0x14132e880` | [Create a DisposableInstancedFormDB resource entry](workshop.md#rva-0x0132e880) | Create a DisposableInstancedFormDB resource entry | C |
| `0x01350a00` | `0x141350a00` | [metadata field constructor](interfaces.md#rva-0x01350a00) | metadata field constructor | C |
| `0x01350b10` | `0x141350b10` | [physical item to resource association](interfaces.md#rva-0x01350b10) | physical item to resource association | C |
| `0x01351790` | `0x141351790` | [resource metadata construction](interfaces.md#rva-0x01351790) | resource metadata construction | C |
| `0x0135d210` | `0x14135d210` | [ResourceEntry fields](interfaces.md#rva-0x0135d210) | ResourceEntry fields | C |
| `0x0135d570` | `0x14135d570` | [Bind the Locations body and system names](interfaces.md#rva-0x0135d570) | Bind the Locations body and system names | C |
| `0x0135d890` | `0x14135d890` | [Supply the Locations faction caption](interfaces.md#rva-0x0135d890) | Supply the Locations faction caption | C |
| `0x0135dcb0` | `0x14135dcb0` | [Register the Locations data providers](interfaces.md#rva-0x0135dcb0) | Register the Locations data providers | C |
| `0x0135df40` | `0x14135df40` | [provider destruction/unregistration](interfaces.md#rva-0x0135df40) | provider destruction/unregistration | C |
| `0x0135e120` | `0x14135e120` | [Collect Locations body and outpost data](interfaces.md#rva-0x0135e120) | Collect Locations body and outpost data | C |
| `0x0135e270` | `0x14135e270` | [body selection event](interfaces.md#rva-0x0135e270) | body selection event | C |
| `0x0135e350` | `0x14135e350` | [service event body refresh only](interfaces.md#rva-0x0135e350) | service event body refresh only | C |
| `0x0135e390` | `0x14135e390` | [favorite selection event](interfaces.md#rva-0x0135e390) | favorite selection event | C |
| `0x0135e580` | `0x14135e580` | [outpost pressed event](interfaces.md#rva-0x0135e580) | outpost pressed event | C |
| `0x0135eb10` | `0x14135eb10` | [Supply separate Locations body data](interfaces.md#rva-0x0135eb10) | Supply separate Locations body data | C |
| `0x0135f0e0` | `0x14135f0e0` | [Build the selected Locations body data](interfaces.md#rva-0x0135f0e0) | Build the selected Locations body data | C |
| `0x0135fcc0` | `0x14135fcc0` | [Dispatch Locations system-body data replacement](interfaces.md#rva-0x0135fcc0) | Dispatch Locations system-body data replacement | C |
| `0x01360e80` | `0x141360e80` | [Build the Locations outpost aggregate and displayed maximum](interfaces.md#rva-0x01360e80) | Filters registered Workshop references and copies live summary lanes into Locations rows. | A |
| `0x01361ad0` | `0x141361ad0` | [default resource/count visitor](interfaces.md#rva-0x01361ad0) | default resource/count visitor | C |
| `0x01361c10` | `0x141361c10` | [Receive queued Locations outpost rows](interfaces.md#rva-0x01361c10) | Rebuilds the outpost entry list and forwards its stored maximum to the provider. | B |
| `0x01362bc0` | `0x141362bc0` | [Resolve display context for the Locations upper map](interfaces.md#rva-0x01362bc0) | Resolve display context for the Locations upper map | C |
| `0x013630c0` | `0x1413630c0` | [Project system component positions for the upper map](interfaces.md#rva-0x013630c0) | Project system component positions for the upper map | C |
| `0x01363960` | `0x141363960` | [Queue the outpost vector](interfaces.md#rva-0x01363960) | Queue the outpost vector | C |
| `0x01364300` | `0x141364300` | [Bind the Locations marker array](interfaces.md#rva-0x01364300) | Bind the Locations marker array | C |
| `0x013644b0` | `0x1413644b0` | [outpost list binding](interfaces.md#rva-0x013644b0) | outpost list binding | C |
| `0x01364550` | `0x141364550` | [Bind list and maximum to Locations data](interfaces.md#rva-0x01364550) | Bind list and maximum to Locations data | C |
| `0x01364930` | `0x141364930` | [Bind the Locations body data fields](interfaces.md#rva-0x01364930) | Bind the Locations body data fields | C |
| `0x01368bf0` | `0x141368bf0` | [Entry points and actual source lists · entry](inventory.md#rva-0x01368bf0) | Original report discusses this roster entry under Entry points and actual source lists. | C |
| `0x01368cf0` | `0x141368cf0` | [container AV gate shared substitution dedup](interfaces.md#rva-0x01368cf0) | container AV gate shared substitution dedup | C |
| `0x01369750` | `0x141369750` | [aligned count insertion](interfaces.md#rva-0x01369750) | aligned count insertion | C |
| `0x01369b80` | `0x141369b80` | [Handle the Locations system-body data route](interfaces.md#rva-0x01369b80) | Handle the Locations system-body data route | C |
| `0x0136a980` | `0x14136a980` | [resource-name sorted insertion](interfaces.md#rva-0x0136a980) | resource-name sorted insertion | C |
| `0x0136ac90` | `0x14136ac90` | [Almanac row vector queue](production.md#rva-0x0136ac90) | Almanac row vector queue | B |
| `0x0136bbb0` | `0x14136bbb0` | [resource FormID map insertion](interfaces.md#rva-0x0136bbb0) | resource FormID map insertion | C |
| `0x0136be50` | `0x14136be50` | [initialized inventory resource/count visitor](interfaces.md#rva-0x0136be50) | initialized inventory resource/count visitor | C |
| `0x0136c060` | `0x14136c060` | [default inventory path](interfaces.md#rva-0x0136c060) | default inventory path | C |
| `0x0136c980` | `0x14136c980` | [Almanac outpost field binder](production.md#rva-0x0136c980) | Almanac outpost field binder | B |
| `0x0136cf60` | `0x14136cf60` | [Bind body identity and coordinates for the upper map](interfaces.md#rva-0x0136cf60) | Bind body identity and coordinates for the upper map | C |
| `0x0136dc00` | `0x14136dc00` | [UI command receiver](interfaces.md#rva-0x0136dc00) | UI command receiver | C |
| `0x0136dc40` | `0x14136dc40` | [Dispatch the queued system-body data update](interfaces.md#rva-0x0136dc40) | Dispatch the queued system-body data update | C |
| `0x01382c00` | `0x141382c00` | [non-provider Workshop-tab control](interfaces.md#rva-0x01382c00) | non-provider Workshop-tab control | C |
| `0x013da8f0` | `0x1413da8f0` | [Call the producer power-upgrade transition](production.md#rva-0x013da8f0) | Call the producer power-upgrade transition | C |
| `0x0140c8c0` | `0x14140c8c0` | [Typed restoration and packed origin (exports 42–49) · entry](workshop.md#rva-0x0140c8c0) | Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49). | C |
| `0x0140ff80` | `0x14140ff80` | [Site tuple transfer](interfaces.md#rva-0x0140ff80) | Site tuple transfer | C |
| `0x014128c0` | `0x1414128c0` | [Site tuple transfer counterpart](interfaces.md#rva-0x014128c0) | Site tuple transfer counterpart | C |
| `0x01413a80` | `0x141413a80` | [Iterate galaxy site edges for serialization](workshop.md#rva-0x01413a80) | Iterate galaxy site edges for serialization | C |
| `0x01413dd0` | `0x141413dd0` | [Iterate galaxy site edges for save framing](workshop.md#rva-0x01413dd0) | Iterate galaxy site edges for save framing | C |
| `0x0141bc70` | `0x14141bc70` | [Call the bounded terrain query preparation](geography.md#rva-0x0141bc70) | Call the bounded terrain query preparation | C |
| `0x0141ccd0` | `0x14141ccd0` | [Producer-to-consumer closure · entry](workshop.md#rva-0x0141ccd0) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x0141dc70` | `0x14141dc70` | [Producer-to-consumer closure · entry](workshop.md#rva-0x0141dc70) | Original report discusses this roster entry under Producer-to-consumer closure. | C |
| `0x01422810` | `0x141422810` | [Gather current or fallback grid-centre inputs](geography.md#rva-0x01422810) | Gather current or fallback grid-centre inputs | C |
| `0x01424ec0` | `0x141424ec0` | [Released terrain and bounded-LOD branches · entry](geography.md#rva-0x01424ec0) | Original report discusses this roster entry under Released terrain and bounded-LOD branches. | C |
| `0x01429880` | `0x141429880` | [Prepare bounded LOD locality demand](geography.md#rva-0x01429880) | Prepare bounded LOD locality demand | C |
| `0x0143f450` | `0x14143f450` | [Publish the Workshop status provider](interfaces.md#rva-0x0143f450) | Publish the Workshop status provider | C |
| `0x0143f690` | `0x14143f690` | [build status snapshot queue](production.md#rva-0x0143f690) | build status snapshot queue | B |
| `0x0143f8a0` | `0x14143f8a0` | [build status value adapter](production.md#rva-0x0143f8a0) | build status value adapter | B |
| `0x0143fa60` | `0x14143fa60` | [Receive the Workshop summary event](interfaces.md#rva-0x0143fa60) | Receive the Workshop summary event | C |
| `0x0143fb40` | `0x14143fb40` | [Workshop status field binder](production.md#rva-0x0143fb40) | Workshop status field binder | B |
| `0x0143fdc0` | `0x14143fdc0` | [build status queued consumer](production.md#rva-0x0143fdc0) | build status queued consumer | B |
| `0x01440d30` | `0x141440d30` | [New construction suppresses default stock · entry](inventory.md#rva-0x01440d30) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x014410f0` | `0x1414410f0` | [Receive reference context for property handling](inventory.md#rva-0x014410f0) | Receive reference context for property handling | C |
| `0x01441730` | `0x141441730` | [Register the mannequin display property](inventory.md#rva-0x01441730) | Register the mannequin display property | C |
| `0x01441b10` | `0x141441b10` | [New construction suppresses default stock · entry](inventory.md#rva-0x01441b10) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x01441f70` | `0x141441f70` | [Dispatch reference context into the property route](inventory.md#rva-0x01441f70) | Dispatch reference context into the property route | C |
| `0x01445660` | `0x141445660` | [Prepare bench and ingredient provider inputs](inventory.md#rva-0x01445660) | Prepare bench and ingredient provider inputs | C |
| `0x014462c0` | `0x1414462c0` | [Refresh the crafting menu ingredient sources](inventory.md#rva-0x014462c0) | Refresh the crafting menu ingredient sources | C |
| `0x01446bb0` | `0x141446bb0` | [Refresh the paired crafting menu source path](inventory.md#rva-0x01446bb0) | Refresh the paired crafting menu source path | C |
| `0x0144e220` | `0x14144e220` | [Find or update an existing Crew row](population.md#rva-0x0144e220) | Find or update an existing Crew row | C |
| `0x0144e3d0` | `0x14144e3d0` | [Installed movie and UI actions · entry](population.md#rva-0x0144e3d0) | Original report discusses this roster entry under Installed movie and UI actions. | C |
| `0x0144f510` | `0x14144f510` | [Insert a Crew row in sorted order](population.md#rva-0x0144f510) | Insert a Crew row in sorted order | C |
| `0x014681d0` | `0x1414681d0` | [Resolve the inventory shown by the container menu](inventory.md#rva-0x014681d0) | Resolve the inventory shown by the container menu | C |
| `0x0146ba60` | `0x14146ba60` | [Construct the player ship inventory model](inventory.md#rva-0x0146ba60) | Construct the player ship inventory model | C |
| `0x0146bc10` | `0x14146bc10` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x0146bc10) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x0146d800` | `0x14146d800` | [OpenContainerMenuEventData source identity](inventory.md#rva-0x0146d800) | OpenContainerMenuEventData source identity | C |
| `0x015026c0` | `0x1415026c0` | [Counts, ingredient plans and actual depletion · entry](inventory.md#rva-0x015026c0) | Original report discusses this roster entry under Counts, ingredient plans and actual depletion. | C |
| `0x0153cfe0` | `0x14153cfe0` | [Merge unassigned and destination lists](population.md#rva-0x0153cfe0) | Merge unassigned and destination lists | C |
| `0x0153d170` | `0x14153d170` | [Native population · entry](population.md#rva-0x0153d170) | Original report discusses this roster entry under Native population. | C |
| `0x0153d900` | `0x14153d900` | [Row fields and skills · entry](population.md#rva-0x0153d900) | Original report discusses this roster entry under Row fields and skills. | C |
| `0x0153dc70` | `0x14153dc70` | [Fill actor row and crew perks](population.md#rva-0x0153dc70) | Fill actor row and crew perks | C |
| `0x0153e290` | `0x14153e290` | [Inspect possessed perks for screen display admission](population.md#rva-0x0153e290) | Inspect possessed perks for screen display admission | C |
| `0x0153e4f0` | `0x14153e4f0` | [Fill an assigned or unassigned Crew row](population.md#rva-0x0153e4f0) | Fill an assigned or unassigned Crew row | C |
| `0x0153eb90` | `0x14153eb90` | [Populate Crew provider](population.md#rva-0x0153eb90) | Populate Crew provider | C |
| `0x0153f4d0` | `0x14153f4d0` | [Populate the crew assignment picker](population.md#rva-0x0153f4d0) | Populate the crew assignment picker | C |
| `0x0153f6d0` | `0x14153f6d0` | [Native population · entry](population.md#rva-0x0153f6d0) | Original report discusses this roster entry under Native population. | C |
| `0x0153f7d0` | `0x14153f7d0` | [Native population · entry](population.md#rva-0x0153f7d0) | Original report discusses this roster entry under Native population. | C |
| `0x01578250` | `0x141578250` | [AreaResources model constructor](geography.md#rva-0x01578250) | AreaResources model constructor | B |
| `0x01578440` | `0x141578440` | [UI command request](geography.md#rva-0x01578440) | UI command request | B |
| `0x01578500` | `0x141578500` | [Build AreaResources UI rows](geography.md#rva-0x01578500) | Reads three shared area ranges, then constructs typed resource rows. | B |
| `0x01578e50` | `0x141578e50` | [Definition to category map · entry](workshop.md#rva-0x01578e50) | Original report discusses this roster entry under Definition to category map. | C |
| `0x015791a0` | `0x1415791a0` | [Bind the build-category preview icons](workshop.md#rva-0x015791a0) | Bind the build-category preview icons | C |
| `0x015795f0` | `0x1415795f0` | [Definition to category map · entry](workshop.md#rva-0x015795f0) | Original report discusses this roster entry under Definition to category map. | C |
| `0x01579fc0` | `0x141579fc0` | [Build selected category preview rows](workshop.md#rva-0x01579fc0) | Build selected category preview rows | C |
| `0x0157a1c0` | `0x14157a1c0` | [Definition to category map · entry](workshop.md#rva-0x0157a1c0) | Original report discusses this roster entry under Definition to category map. | C |
| `0x0157a740` | `0x14157a740` | [Definition to category map · entry](workshop.md#rva-0x0157a740) | Original report discusses this roster entry under Definition to category map. | C |
| `0x0157ad10` | `0x14157ad10` | [Update the selected item card](workshop.md#rva-0x0157ad10) | Update the selected item card | C |
| `0x0157b0c0` | `0x14157b0c0` | [Provider and compiled consumer · entry](workshop.md#rva-0x0157b0c0) | Original report discusses this roster entry under Provider and compiled consumer. | C |
| `0x0157c6a0` | `0x14157c6a0` | [Provider and compiled consumer · entry](workshop.md#rva-0x0157c6a0) | Original report discusses this roster entry under Provider and compiled consumer. | C |
| `0x0157d570` | `0x14157d570` | [typed payload binder](geography.md#rva-0x0157d570) | typed payload binder | B |
| `0x0157eb30` | `0x14157eb30` | [Definition to category map · entry](workshop.md#rva-0x0157eb30) | Original report discusses this roster entry under Definition to category map. | C |
| `0x0157f0f0` | `0x14157f0f0` | [Dispatch the selected item card update](workshop.md#rva-0x0157f0f0) | Dispatch the selected item card update | C |
| `0x0157fcf0` | `0x14157fcf0` | [typed row construction existing capacity](geography.md#rva-0x0157fcf0) | typed row construction existing capacity | B |
| `0x01581060` | `0x141581060` | [Bind build-category variant fields](workshop.md#rva-0x01581060) | Bind build-category variant fields | C |
| `0x01581290` | `0x141581290` | [AreaResources row binder](geography.md#rva-0x01581290) | AreaResources row binder | C |
| `0x01581960` | `0x141581960` | [Refresh and cache epochs · entry](workshop.md#rva-0x01581960) | Original report discusses this roster entry under Refresh and cache epochs. | C |
| `0x015819a0` | `0x1415819a0` | [Refresh and cache epochs · entry](workshop.md#rva-0x015819a0) | Original report discusses this roster entry under Refresh and cache epochs. | C |
| `0x01581a80` | `0x141581a80` | [UI shuttle application](geography.md#rva-0x01581a80) | UI shuttle application | B |
| `0x01582340` | `0x141582340` | [builder menu data producer](production.md#rva-0x01582340) | builder menu data producer | B |
| `0x01583410` | `0x141583410` | [apply selected resource AV](production.md#rva-0x01583410) | apply selected resource AV | B |
| `0x01586950` | `0x141586950` | [builder item UI field binding](production.md#rva-0x01586950) | builder item UI field binding | B |
| `0x01589840` | `0x141589840` | [Workshop action mask source gate](inventory.md#rva-0x01589840) | Workshop action mask source gate | C |
| `0x0158a6e0` | `0x14158a6e0` | [Produce the selected reference integrity indicator](population.md#rva-0x0158a6e0) | Produce the selected reference integrity indicator | C |
| `0x0158e280` | `0x14158e280` | [Preview spinner constructor](interfaces.md#rva-0x0158e280) | Preview spinner constructor | C |
| `0x0158e410` | `0x14158e410` | [Destroy the Workshop state data model](workshop.md#rva-0x0158e410) | Destroy the Workshop state data model | C |
| `0x0158e570` | `0x14158e570` | [Write and queue the preview model state](workshop.md#rva-0x0158e570) | Write and queue the preview model state | C |
| `0x0158eb10` | `0x14158eb10` | [Choose and publish the outpost display name](workshop.md#rva-0x0158eb10) | Choose and publish the outpost display name | C |
| `0x0158ec80` | `0x14158ec80` | [Footer gaps investigated · entry](workshop.md#rva-0x0158ec80) | Original report discusses this roster entry under Footer gaps investigated. | C |
| `0x0158ef80` | `0x14158ef80` | [Provider and compiled consumer · entry](workshop.md#rva-0x0158ef80) | Original report discusses this roster entry under Provider and compiled consumer. | C |
| `0x0158f230` | `0x14158f230` | [Preview spinner input binding](interfaces.md#rva-0x0158f230) | Preview spinner input binding | C |
| `0x0158f860` | `0x14158f860` | [Participate in planet and system caption publication](workshop.md#rva-0x0158f860) | Participate in planet and system caption publication | C |
| `0x0158fa50` | `0x14158fa50` | [Selected preview UI data update](interfaces.md#rva-0x0158fa50) | Selected preview UI data update | C |
| `0x015902a0` | `0x1415902a0` | [Preview UI service](interfaces.md#rva-0x015902a0) | Preview UI service | C |
| `0x01590320` | `0x141590320` | [Participate in the queued planet and system caption path](workshop.md#rva-0x01590320) | Participate in the queued planet and system caption path | C |
| `0x01590400` | `0x141590400` | [Dispatch the queued current-state update](workshop.md#rva-0x01590400) | Dispatch the queued current-state update | C |
| `0x015f6710` | `0x1415f6710` | [Perform the broader placement cleanup route](workshop.md#rva-0x015f6710) | Perform the broader placement cleanup route | C |
| `0x015f69c0` | `0x1415f69c0` | [Deployment allowance and ordinary beacon operation · entry](workshop.md#rva-0x015f69c0) | Original report discusses this roster entry under Deployment allowance and ordinary beacon operation. | C |
| `0x015f6a90` | `0x1415f6a90` | [Deployment allowance and ordinary beacon operation · entry](workshop.md#rva-0x015f6a90) | Original report discusses this roster entry under Deployment allowance and ordinary beacon operation. | C |
| `0x015f9080` | `0x1415f9080` | [Deployment allowance and ordinary beacon operation · entry](workshop.md#rva-0x015f9080) | Original report discusses this roster entry under Deployment allowance and ordinary beacon operation. | C |
| `0x01613410` | `0x141613410` | [Dispatch the Research ingredient evaluation](inventory.md#rva-0x01613410) | Dispatch the Research ingredient evaluation | C |
| `0x01625260` | `0x141625260` | [Final menu capacity check/assignment](population.md#rva-0x01625260) | Final menu capacity check/assignment | C |
| `0x0166c0a0` | `0x14166c0a0` | [Dispatch save UI selection](interfaces.md#rva-0x0166c0a0) | Dispatch save UI selection | C |
| `0x0166c190` | `0x14166c190` | [Handle save selection](interfaces.md#rva-0x0166c190) | Handle save selection | C |
| `0x0166cf00` | `0x14166cf00` | [Register pause-menu save behavior](interfaces.md#rva-0x0166cf00) | Register pause-menu save behavior | C |
| `0x0166e4a0` | `0x14166e4a0` | [Obtain current save selection](interfaces.md#rva-0x0166e4a0) | Obtain current save selection | C |
| `0x0166f3c0` | `0x14166f3c0` | [Forward queued save selection](interfaces.md#rva-0x0166f3c0) | Forward queued save selection | C |
| `0x0167f7e0` | `0x14167f7e0` | [Named property binding candidate](workshop.md#rva-0x0167f7e0) | Named property binding candidate | C |
| `0x01686000` | `0x141686000` | [Handle planetary site selection](workshop.md#rva-0x01686000) | Handle planetary site selection | C |
| `0x01686a00` | `0x141686a00` | [Convert map selection to spherical angles](workshop.md#rva-0x01686a00) | Convert map selection to spherical angles | C |
| `0x016874f0` | `0x1416874f0` | [Process selected-site angle pair](workshop.md#rva-0x016874f0) | Process selected-site angle pair | C |
| `0x016885d0` | `0x1416885d0` | [Store selected-site coordinates](workshop.md#rva-0x016885d0) | Store selected-site coordinates | C |
| `0x016aa880` | `0x1416aa880` | [Bind system-body diagram identity and display fields](interfaces.md#rva-0x016aa880) | Bind system-body diagram identity and display fields | C |
| `0x016aa920` | `0x1416aa920` | [Supply body type and scan state for the diagram](interfaces.md#rva-0x016aa920) | Supply body type and scan state for the diagram | C |
| `0x016aab70` | `0x1416aab70` | [Bind the Locations system-body diagram payload](interfaces.md#rva-0x016aab70) | Bind the Locations system-body diagram payload | C |
| `0x016aac10` | `0x1416aac10` | [Participate in the Locations system-root diagram route](interfaces.md#rva-0x016aac10) | Participate in the Locations system-root diagram route | C |
| `0x016aacd0` | `0x1416aacd0` | [Participate in the Locations system-root diagram route](interfaces.md#rva-0x016aacd0) | Participate in the Locations system-root diagram route | C |
| `0x016ab670` | `0x1416ab670` | [Replace the Locations system-body data](interfaces.md#rva-0x016ab670) | Replace the Locations system-body data | C |
| `0x016b6310` | `0x1416b6310` | [Receive the Locations body and system name data](interfaces.md#rva-0x016b6310) | Receive the Locations body and system name data | C |
| `0x016bd210` | `0x1416bd210` | [two-reference inventory menu handoff](inventory.md#rva-0x016bd210) | two-reference inventory menu handoff | C |
| `0x016cd320` | `0x1416cd320` | [Participate in selected body data construction](interfaces.md#rva-0x016cd320) | Participate in selected body data construction | C |
| `0x016ceb20` | `0x1416ceb20` | [Supply color from the relevant body component](interfaces.md#rva-0x016ceb20) | Supply color from the relevant body component | C |
| `0x016ceb90` | `0x1416ceb90` | [Participate in normalized Locations body sizing](interfaces.md#rva-0x016ceb90) | Participate in normalized Locations body sizing | C |
| `0x016cf0f0` | `0x1416cf0f0` | [Participate in selected body data construction](interfaces.md#rva-0x016cf0f0) | Participate in selected body data construction | C |
| `0x016cf8f0` | `0x1416cf8f0` | [Supply the Locations system designation name](interfaces.md#rva-0x016cf8f0) | Supply the Locations system designation name | C |
| `0x016d1c50` | `0x1416d1c50` | [Accumulate display size ranges by body type](interfaces.md#rva-0x016d1c50) | Accumulate display size ranges by body type | C |
| `0x016d47e0` | `0x1416d47e0` | [Workshop reverse-link Transfer Container query](inventory.md#rva-0x016d47e0) | Workshop reverse-link Transfer Container query | C |
| `0x016d7a00` | `0x1416d7a00` | [Workshop relationship Transfer Container selection](inventory.md#rva-0x016d7a00) | Workshop relationship Transfer Container selection | C |
| `0x01716e70` | `0x141716e70` | [Parse facility selection ID](production.md#rva-0x01716e70) | Parse facility selection ID | C |
| `0x01717fd0` | `0x141717fd0` | [UI ChangeBuildItem event consumer](production.md#rva-0x01717fd0) | UI ChangeBuildItem event consumer | B |
| `0x01719040` | `0x141719040` | [Queue facility resource selection apply](production.md#rva-0x01719040) | Queue facility resource selection apply | C |
| `0x01719fb0` | `0x141719fb0` | [Definition to category map · entry](workshop.md#rva-0x01719fb0) | Original report discusses this roster entry under Definition to category map. | C |
| `0x0171a050` | `0x14171a050` | [Definition to category map · entry](workshop.md#rva-0x0171a050) | Original report discusses this roster entry under Definition to category map. | C |
| `0x0171a140` | `0x14171a140` | [Forward the concrete selected variant ID](workshop.md#rva-0x0171a140) | Forward the concrete selected variant ID | C |
| `0x0171a1a0` | `0x14171a1a0` | [Definition to category map · entry](workshop.md#rva-0x0171a1a0) | Original report discusses this roster entry under Definition to category map. | C |
| `0x0171a290` | `0x14171a290` | [Forward category and current-node changes](workshop.md#rva-0x0171a290) | Forward category and current-node changes | C |
| `0x0171a2f0` | `0x14171a2f0` | [Definition to category map · entry](workshop.md#rva-0x0171a2f0) | Original report discusses this roster entry under Definition to category map. | C |
| `0x0171a3e0` | `0x14171a3e0` | [Advance or decrement the selected variant index](workshop.md#rva-0x0171a3e0) | Advance or decrement the selected variant index | C |
| `0x0171d930` | `0x14171d930` | [Callbacks and admission handoff · entry](workshop.md#rva-0x0171d930) | Original report discusses this roster entry under Callbacks and admission handoff. | C |
| `0x01720ef0` | `0x141720ef0` | [Register cargo link UI data](inventory.md#rva-0x01720ef0) | Register cargo link UI data | C |
| `0x017216e0` | `0x1417216e0` | [Terminal, eligibility and pairing · entry](inventory.md#rva-0x017216e0) | Original report discusses this roster entry under Terminal, eligibility and pairing. | C |
| `0x017219c0` | `0x1417219c0` | [Terminal, eligibility and pairing · entry](workshop.md#rva-0x017219c0) | Original report discusses this roster entry under Terminal, eligibility and pairing. | C |
| `0x017227b0` | `0x1417227b0` | [Apply initial cargo link source metadata](inventory.md#rva-0x017227b0) | Apply initial cargo link source metadata | C |
| `0x01722990` | `0x141722990` | [Refresh, caches and persistence · entry](inventory.md#rva-0x01722990) | Original report discusses this roster entry under Refresh, caches and persistence. | C |
| `0x01722a70` | `0x141722a70` | [Refresh, caches and persistence · entry](inventory.md#rva-0x01722a70) | Original report discusses this roster entry under Refresh, caches and persistence. | C |
| `0x01722e90` | `0x141722e90` | [Terminal, eligibility and pairing · entry](inventory.md#rva-0x01722e90) | Original report discusses this roster entry under Terminal, eligibility and pairing. | C |
| `0x017239e0` | `0x1417239e0` | [Exact UI binding and rendering · entry](inventory.md#rva-0x017239e0) | Original report discusses this roster entry under Exact UI binding and rendering. | C |
| `0x01723c80` | `0x141723c80` | [Refresh, caches and persistence · entry](inventory.md#rva-0x01723c80) | Original report discusses this roster entry under Refresh, caches and persistence. | C |
| `0x01724330` | `0x141724330` | [Visit one cargo inventory entry](inventory.md#rva-0x01724330) | Visit one cargo inventory entry | C |
| `0x01724670` | `0x141724670` | [Resource providers and the decisive direct-edge boundary · entry](inventory.md#rva-0x01724670) | Original report discusses this roster entry under Resource providers and the decisive direct-edge boundary. | C |
| `0x01724a00` | `0x141724a00` | [Store the selected cargo endpoint handle](inventory.md#rva-0x01724a00) | Store the selected cargo endpoint handle | C |
| `0x01724af0` | `0x141724af0` | [Refresh, caches and persistence · entry](inventory.md#rva-0x01724af0) | Original report discusses this roster entry under Refresh, caches and persistence. | C |
| `0x01724be0` | `0x141724be0` | [Handle cargo link hover context](inventory.md#rva-0x01724be0) | Handle cargo link hover context | C |
| `0x01724cd0` | `0x141724cd0` | [Apply queued cargo link hover details](inventory.md#rva-0x01724cd0) | Apply queued cargo link hover details | C |
| `0x017278b0` | `0x1417278b0` | [report · entry](inventory.md#rva-0x017278b0) | Original report discusses this roster entry under report. | C |
| `0x017283e0` | `0x1417283e0` | [Read base-container content for UI inventory](inventory.md#rva-0x017283e0) | Read base-container content for UI inventory | C |
| `0x01729010` | `0x141729010` | [Dispatch the queued cargo link hover path](inventory.md#rva-0x01729010) | Dispatch the queued cargo link hover path | C |
| `0x017290f0` | `0x1417290f0` | [Refresh, caches and persistence · entry](inventory.md#rva-0x017290f0) | Original report discusses this roster entry under Refresh, caches and persistence. | C |
| `0x0172bc70` | `0x14172bc70` | [Resolve faction-type keyword for Locations display](interfaces.md#rva-0x0172bc70) | Resolve faction-type keyword for Locations display | C |
| `0x017324f0` | `0x1417324f0` | [New construction suppresses default stock · entry](inventory.md#rva-0x017324f0) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x01732620` | `0x141732620` | [New construction suppresses default stock · entry](inventory.md#rva-0x01732620) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x01739c50` | `0x141739c50` | [Prepare item-card operational data](interfaces.md#rva-0x01739c50) | Prepare item-card operational data | C |
| `0x0173a9f0` | `0x14173a9f0` | [Prepare item-card operational data](interfaces.md#rva-0x0173a9f0) | Prepare item-card operational data | C |
| `0x0173ae90` | `0x14173ae90` | [UI filter keyword category classification](inventory.md#rva-0x0173ae90) | UI filter keyword category classification | C |
| `0x01741660` | `0x141741660` | [Participate in framing reference and string counts](workshop.md#rva-0x01741660) | Participate in framing reference and string counts | C |
| `0x0177a1f0` | `0x14177a1f0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0177a1f0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x017ca630` | `0x1417ca630` | [Invocation lifetime and a retirement interval · entry](geography.md#rva-0x017ca630) | Original report discusses this roster entry under Invocation lifetime and a retirement interval. | C |
| `0x017cab70` | `0x1417cab70` | [Supply engine frame elapsed](production.md#rva-0x017cab70) | Supply engine frame elapsed | C |
| `0x017cbbe0` | `0x1417cbbe0` | [Supply frame elapsed to production](production.md#rva-0x017cbbe0) | Supply frame elapsed to production | C |
| `0x017cc1d0` | `0x1417cc1d0` | [Schedule the frame update callback](production.md#rva-0x017cc1d0) | Schedule the frame update callback | C |
| `0x017ced70` | `0x1417ced70` | [Wrap the main-update task graph](geography.md#rva-0x017ced70) | Wrap the main-update task graph | C |
| `0x017dec70` | `0x1417dec70` | [Reset callers and predicates · helper](geography.md#rva-0x017dec70) | Original report discusses this roster entry under Reset callers and predicates. | C |
| `0x017df210` | `0x1417df210` | [Script authority and native deadline · entry](inventory.md#rva-0x017df210) | Original report discusses this roster entry under Script authority and native deadline. | C |
| `0x017dfdf0` | `0x1417dfdf0` | [Pass planet owner context to manager initialization](geography.md#rva-0x017dfdf0) | Pass planet owner context to manager initialization | C |
| `0x017e11b0` | `0x1417e11b0` | [Register reference world or Workshop context](workshop.md#rva-0x017e11b0) | Register reference world or Workshop context | C |
| `0x017e2180` | `0x1417e2180` | [Mark world or Workshop frame context](workshop.md#rva-0x017e2180) | Mark world or Workshop frame context | C |
| `0x017eb150` | `0x1417eb150` | [Resolve crew actors in the inspected E2 callback](production.md#rva-0x017eb150) | Resolve crew actors in the inspected E2 callback | C |
| `0x017f6690` | `0x1417f6690` | [Counts, ingredient plans and actual depletion · entry](inventory.md#rva-0x017f6690) | Original report discusses this roster entry under Counts, ingredient plans and actual depletion. | C |
| `0x017f6fa0` | `0x1417f6fa0` | [Build a temporary ingredient aggregation reference](inventory.md#rva-0x017f6fa0) | Build a temporary ingredient aggregation reference | C |
| `0x017f8db0` | `0x1417f8db0` | [Complete the crafting job](inventory.md#rva-0x017f8db0) | Complete the crafting job | C |
| `0x017f8f70` | `0x1417f8f70` | [Dispatch the ordinary crafting event job](inventory.md#rva-0x017f8f70) | Dispatch the ordinary crafting event job | C |
| `0x017f9a20` | `0x1417f9a20` | [Dispatch the ordinary crafting job](inventory.md#rva-0x017f9a20) | Dispatch the ordinary crafting job | C |
| `0x017faca0` | `0x1417faca0` | [Continue the ordinary crafting job](inventory.md#rva-0x017faca0) | Continue the ordinary crafting job | C |
| `0x017fb210` | `0x1417fb210` | [Spend reachable crafting components](inventory.md#rva-0x017fb210) | Spend reachable crafting components | C |
| `0x017fd940` | `0x1417fd940` | [Create the temporary inventory reference](inventory.md#rva-0x017fd940) | Create the temporary inventory reference | C |
| `0x017fe930` | `0x1417fe930` | [Entry points and actual source lists · entry](inventory.md#rva-0x017fe930) | Original report discusses this roster entry under Entry points and actual source lists. | C |
| `0x01800f20` | `0x141800f20` | [research material/progress completion](production.md#rva-0x01800f20) | research material/progress completion | B |
| `0x01801ee0` | `0x141801ee0` | [recursive Research Project completion](production.md#rva-0x01801ee0) | recursive Research Project completion | B |
| `0x01803ba0` | `0x141803ba0` | [Name the promoted-reference change flag](workshop.md#rva-0x01803ba0) | Name the promoted-reference change flag | C |
| `0x01804c70` | `0x141804c70` | [Definition loading and postlink readiness · entry](geography.md#rva-0x01804c70) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x01809400` | `0x141809400` | [Read the compact change-record count](interfaces.md#rva-0x01809400) | Supplies the count grammar used by the native framing walker. | B |
| `0x0180b410` | `0x14180b410` | [Remap native saved identity](geography.md#rva-0x0180b410) | Remap native saved identity | C |
| `0x01814050` | `0x141814050` | [Wrap save name and serialization](interfaces.md#rva-0x01814050) | Wrap save name and serialization | C |
| `0x01814220` | `0x141814220` | [Serialize the native save payload](interfaces.md#rva-0x01814220) | Uses a caller-held context and file/storage object in the mapped serializer path. | B |
| `0x01815620` | `0x141815620` | [Drain generation during loading](geography.md#rva-0x01815620) | Drain generation during loading | C |
| `0x0181aa30` | `0x14181aa30` | [UI, save framing and lifecycle native entry](interfaces.md#rva-0x0181aa30) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0181af40` | `0x14181af40` | [UI, save framing and lifecycle native entry](interfaces.md#rva-0x0181af40) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0181b8e0` | `0x14181b8e0` | [Subtract selected translation in reference registration](workshop.md#rva-0x0181b8e0) | Subtract selected translation in reference registration | C |
| `0x0181cdc0` | `0x14181cdc0` | [Checkpoint: preparation closure and coordinate-domain qualification · entry](geography.md#rva-0x0181cdc0) | Original report discusses this roster entry under Checkpoint: preparation closure and coordinate-domain qualification. | C |
| `0x0181ce30` | `0x14181ce30` | [Gate the AddChange path](workshop.md#rva-0x0181ce30) | Gate the AddChange path | C |
| `0x0181cff0` | `0x14181cff0` | [Dispatch the conditional saved component envelope](workshop.md#rva-0x0181cff0) | Dispatch the conditional saved component envelope | C |
| `0x01821b70` | `0x141821b70` | [Handle save serialization callback](interfaces.md#rva-0x01821b70) | Handle save serialization callback | C |
| `0x01822170` | `0x141822170` | [Forward save serialization callback](interfaces.md#rva-0x01822170) | Forward save serialization callback | C |
| `0x01822570` | `0x141822570` | [Save unit 6 dispatch](interfaces.md#rva-0x01822570) | Save unit 6 dispatch | C |
| `0x018234e0` | `0x1418234e0` | [Resolve each display component owner for fixup](inventory.md#rva-0x018234e0) | Resolve each display component owner for fixup | C |
| `0x018236c0` | `0x1418236c0` | [Direct serialization edges recovered (exports 36–40) · entry](population.md#rva-0x018236c0) | Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40). | C |
| `0x018237f0` | `0x1418237f0` | [Dispatch global save work to typed serialization](workshop.md#rva-0x018237f0) | Dispatch global save work to typed serialization | C |
| `0x01824020` | `0x141824020` | [Save loading and interior residency · entry](geography.md#rva-0x01824020) | Original report discusses this roster entry under Save loading and interior residency. | C |
| `0x01824a60` | `0x141824a60` | [Save unit 3 dispatch](interfaces.md#rva-0x01824a60) | Save unit 3 dispatch | C |
| `0x01825820` | `0x141825820` | [Direct serialization edges recovered (exports 36–40) · entry](population.md#rva-0x01825820) | Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40). | C |
| `0x01825ac0` | `0x141825ac0` | [Restore saved world descriptor array](geography.md#rva-0x01825ac0) | Restore saved world descriptor array | C |
| `0x01825e00` | `0x141825e00` | [global-data load dispatcher](power.md#rva-0x01825e00) | global-data load dispatcher | B |
| `0x01827380` | `0x141827380` | [global-data finish dispatcher](power.md#rva-0x01827380) | global-data finish dispatcher | B |
| `0x018278c0` | `0x1418278c0` | [Dispatch the global revert type range](geography.md#rva-0x018278c0) | Dispatch the global revert type range | C |
| `0x01827960` | `0x141827960` | [Save loading and interior residency · entry](geography.md#rva-0x01827960) | Original report discusses this roster entry under Save loading and interior residency. | C |
| `0x018286f0` | `0x1418286f0` | [Write the type-9 saved-destination frame](interfaces.md#rva-0x018286f0) | Pairs with the type-9 global-data reader. | B |
| `0x01829ec0` | `0x141829ec0` | [Load the type-9 saved-destination frame](interfaces.md#rva-0x01829ec0) | Receives native global-data dispatch case 9. | B |
| `0x0182d350` | `0x14182d350` | [Read the type-9 saved-destination world prefix](interfaces.md#rva-0x0182d350) | Resolves the initial saved world token through legacy identity and type checks. | B |
| `0x0182dc30` | `0x14182dc30` | [Typed restoration and packed origin (exports 42–49) · entry](workshop.md#rva-0x0182dc30) | Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49). | C |
| `0x0182e280` | `0x14182e280` | [Typed component restoration](interfaces.md#rva-0x0182e280) | Typed component restoration | C |
| `0x01830550` | `0x141830550` | [Closing dependency dispositions · entry](geography.md#rva-0x01830550) | Original report discusses this roster entry under Closing dependency dispositions. | C |
| `0x01832000` | `0x141832000` | [Write case-5 initial wire state](workshop.md#rva-0x01832000) | Write case-5 initial wire state | C |
| `0x018325a0` | `0x1418325a0` | [Select saved parent and world context](workshop.md#rva-0x018325a0) | Select saved parent and world context | C |
| `0x01832f00` | `0x141832f00` | [Select conditional saved-reference case](workshop.md#rva-0x01832f00) | Select conditional saved-reference case | C |
| `0x01832fd0` | `0x141832fd0` | [Dispatch saved initial position and frame writing](workshop.md#rva-0x01832fd0) | Dispatch saved initial position and frame writing | C |
| `0x01833b20` | `0x141833b20` | [Saved initial frame conversion](interfaces.md#rva-0x01833b20) | Saved initial frame conversion | C |
| `0x01835060` | `0x141835060` | [Dispatch the save-side allocation callback](workshop.md#rva-0x01835060) | Dispatch the save-side allocation callback | C |
| `0x01835450` | `0x141835450` | [Write the 12-byte initial position](workshop.md#rva-0x01835450) | Write the 12-byte initial position | C |
| `0x01835610` | `0x141835610` | [Read initial reference context](workshop.md#rva-0x01835610) | Read initial reference context | C |
| `0x01835c20` | `0x141835c20` | [Decode case-5 transform](workshop.md#rva-0x01835c20) | Decode case-5 transform | C |
| `0x01839c60` | `0x141839c60` | [Construct save-load manager context](interfaces.md#rva-0x01839c60) | Construct save-load manager context | C |
| `0x0183a8d0` | `0x14183a8d0` | [Construct save file context](interfaces.md#rva-0x0183a8d0) | Construct save file context | C |
| `0x0183aaf0` | `0x14183aaf0` | [Set up save finalization](interfaces.md#rva-0x0183aaf0) | Set up save finalization | C |
| `0x0183ac80` | `0x14183ac80` | [Finalize local save storage](interfaces.md#rva-0x0183ac80) | Finalize local save storage | C |
| `0x0183c3c0` | `0x14183c3c0` | [Handle alternate save request](interfaces.md#rva-0x0183c3c0) | Handle alternate save request | C |
| `0x0183c590` | `0x14183c590` | [Request a save through the ordinary native UI path](interfaces.md#rva-0x0183c590) | Handles a build-pinned save request candidate and invokes save preparation. | B |
| `0x0183c830` | `0x14183c830` | [Prepare save file object](interfaces.md#rva-0x0183c830) | Prepare save file object | C |
| `0x01840f50` | `0x141840f50` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x01840f50) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x01841460` | `0x141841460` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x01841460) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x01841610` | `0x141841610` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x01841610) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x01846ef0` | `0x141846ef0` | [Check save request conditions](interfaces.md#rva-0x01846ef0) | Check save request conditions | C |
| `0x0184ab70` | `0x14184ab70` | [Update save metadata](interfaces.md#rva-0x0184ab70) | Update save metadata | C |
| `0x0184cee0` | `0x14184cee0` | [Update save selection bookkeeping](interfaces.md#rva-0x0184cee0) | Update save selection bookkeeping | C |
| `0x0184eec0` | `0x14184eec0` | [Generate save name](interfaces.md#rva-0x0184eec0) | Generate save name | C |
| `0x018501b0` | `0x1418501b0` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x018501b0) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x01850940` | `0x141850940` | [Apply save manager status](interfaces.md#rva-0x01850940) | Apply save manager status | C |
| `0x018509c0` | `0x1418509c0` | [Handle alternate save manager status](interfaces.md#rva-0x018509c0) | Handle alternate save manager status | C |
| `0x01854180` | `0x141854180` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x01854180) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x01854c00` | `0x141854c00` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x01854c00) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x01855a20` | `0x141855a20` | [Forward queued save finalization](interfaces.md#rva-0x01855a20) | Forward queued save finalization | C |
| `0x01856d10` | `0x141856d10` | [Prepare qualified reference output transform](workshop.md#rva-0x01856d10) | Prepare qualified reference output transform | C |
| `0x018599a0` | `0x1418599a0` | [Native tagged ID decode and remapping boundary](geography.md#rva-0x018599a0) | Native tagged ID decode and remapping boundary | C |
| `0x0185e180` | `0x14185e180` | [Read the change-record framing header](interfaces.md#rva-0x0185e180) | Reads the native header used by the R3 framing model. | B |
| `0x01863e00` | `0x141863e00` | [Build native save buffer](workshop.md#rva-0x01863e00) | Build native save buffer | C |
| `0x018650d0` | `0x1418650d0` | [Read queued saved reference](workshop.md#rva-0x018650d0) | Read queued saved reference | C |
| `0x01865370` | `0x141865370` | [Read compact save count](power.md#rva-0x01865370) | Read compact save count | C |
| `0x01865960` | `0x141865960` | [Read queued saved string index](workshop.md#rva-0x01865960) | Read queued saved string index | C |
| `0x018663f0` | `0x1418663f0` | [Process the saved component envelope before generic flags](workshop.md#rva-0x018663f0) | Process the saved component envelope before generic flags | C |
| `0x01867470` | `0x141867470` | [Process the component envelope before generic self flags](workshop.md#rva-0x01867470) | Process the component envelope before generic self flags | C |
| `0x01867660` | `0x141867660` | [Participate in framing reference and string counts](workshop.md#rva-0x01867660) | Participate in framing reference and string counts | C |
| `0x018686b0` | `0x1418686b0` | [Write save body bytes](power.md#rva-0x018686b0) | Write save body bytes | C |
| `0x01868770` | `0x141868770` | [Write compact save count](power.md#rva-0x01868770) | Write compact save count | C |
| `0x01868de0` | `0x141868de0` | [Encode saved FormID](power.md#rva-0x01868de0) | Encode saved FormID | C |
| `0x018695e0` | `0x1418695e0` | [Sixth trace round: typed load paths and active key · entry](workshop.md#rva-0x018695e0) | Original report discusses this roster entry under Sixth trace round: typed load paths and active key. | C |
| `0x018698d0` | `0x1418698d0` | [Direct serialization edges recovered (exports 36–40) · entry](population.md#rva-0x018698d0) | Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40). | C |
| `0x0186b8e0` | `0x14186b8e0` | [Read typed saved identity](workshop.md#rva-0x0186b8e0) | Read typed saved identity | C |
| `0x0186b940` | `0x14186b940` | [Independent registry boundary and positive unassigned input · entry](population.md#rva-0x0186b940) | Original report discusses this roster entry under Independent registry boundary and positive unassigned input. | C |
| `0x0186bc80` | `0x14186bc80` | [Decode typed saved identity](workshop.md#rva-0x0186bc80) | Decode typed saved identity | C |
| `0x0186bd40` | `0x14186bd40` | [Write identity through the typed wire helper](workshop.md#rva-0x0186bd40) | Write identity through the typed wire helper | C |
| `0x0186c250` | `0x14186c250` | [Build alternate native save buffer](workshop.md#rva-0x0186c250) | Build alternate native save buffer | C |
| `0x0186dfc0` | `0x14186dfc0` | [Evidence checkpoints · entry](geography.md#rva-0x0186dfc0) | Original report discusses this roster entry under Evidence checkpoints. | C |
| `0x018778e0` | `0x1418778e0` | [calendar elapsed consumer](production.md#rva-0x018778e0) | calendar elapsed consumer | B |
| `0x0187b5a0` | `0x14187b5a0` | [reference relationship cleanup](power.md#rva-0x0187b5a0) | reference relationship cleanup | B |
| `0x0187bb60` | `0x14187bb60` | [unresolved-owner reference cleanup entry](power.md#rva-0x0187bb60) | unresolved-owner reference cleanup entry | B |
| `0x0187d800` | `0x14187d800` | [Continue conditional unresolved-owner cleanup](power.md#rva-0x0187d800) | Continue conditional unresolved-owner cleanup | C |
| `0x0187f9d0` | `0x14187f9d0` | [d5ae eligibility readiness map · entry](geography.md#rva-0x0187f9d0) | Original report discusses this roster entry under d5ae eligibility readiness map. | C |
| `0x0187fbd0` | `0x14187fbd0` | [Startup admission and the Save52 branch · entry](geography.md#rva-0x0187fbd0) | Original report discusses this roster entry under Startup admission and the Save52 branch. | C |
| `0x01881660` | `0x141881660` | [Overlay factory registration](workshop.md#rva-0x01881660) | Overlay factory registration | C |
| `0x01883440` | `0x141883440` | [Definition loading and postlink readiness · entry](inventory.md#rva-0x01883440) | Original report discusses this roster entry under Definition loading and postlink readiness. | C |
| `0x01884350` | `0x141884350` | [Supply streaming context or player fallback](workshop.md#rva-0x01884350) | Supply streaming context or player fallback | C |
| `0x01887c90` | `0x141887c90` | [main frame clock producer](production.md#rva-0x01887c90) | main frame clock producer | B |
| `0x01893ee0` | `0x141893ee0` | [Grid, terrain and density preparation · entry](inventory.md#rva-0x01893ee0) | Original report discusses this roster entry under Grid, terrain and density preparation. | C |
| `0x01895460` | `0x141895460` | [Save loading and interior residency · entry](geography.md#rva-0x01895460) | Original report discusses this roster entry under Save loading and interior residency. | C |
| `0x01895cc0` | `0x141895cc0` | [Save loading and interior residency · entry](geography.md#rva-0x01895cc0) | Original report discusses this roster entry under Save loading and interior residency. | C |
| `0x01896280` | `0x141896280` | [Action/state transition matrix · entry](geography.md#rva-0x01896280) | Original report discusses this roster entry under Action/state transition matrix. | C |
| `0x01898210` | `0x141898210` | [Gate pending load on startup readiness](geography.md#rva-0x01898210) | Gate pending load on startup readiness | C |
| `0x01898870` | `0x141898870` | [Concrete worker and publication order · entry](geography.md#rva-0x01898870) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x018a8b80` | `0x1418a8b80` | [PCM constructor owns maps and initializes seed/RNG](geography.md#rva-0x018a8b80) | PCM constructor owns maps and initializes seed/RNG | C |
| `0x018a9270` | `0x1418a9270` | [PCM seed initial producer override or random plus log and RNG reset](geography.md#rva-0x018a9270) | PCM seed initial producer override or random plus log and RNG reset | C |
| `0x018a9350` | `0x1418a9350` | [Demand seed from saved PCM +0x420, PNDT and packed cell, then MT reset](geography.md#rva-0x018a9350) | Demand seed from saved PCM +0x420, PNDT and packed cell, then MT reset | C |
| `0x018a9550` | `0x1418a9550` | [PCM overlay selection reseed from persisted seed and caller context](geography.md#rva-0x018a9550) | PCM overlay selection reseed from persisted seed and caller context | C |
| `0x018a9810` | `0x1418a9810` | [Persisted PCM seed folds with caller identity for generation seed](geography.md#rva-0x018a9810) | Persisted PCM seed folds with caller identity for generation seed | C |
| `0x018a9900` | `0x1418a9900` | [Residual placement generation consumes persisted-seed-derived input](geography.md#rva-0x018a9900) | Residual placement generation consumes persisted-seed-derived input | C |
| `0x018a9c60` | `0x1418a9c60` | [Checkpoint: completion callbacks and the preparation antecedent · entry](geography.md#rva-0x018a9c60) | Original report discusses this roster entry under Checkpoint: completion callbacks and the preparation antecedent. | C |
| `0x018aa1c0` | `0x1418aa1c0` | [World/cell placement reuse age/prune residual generation and return](geography.md#rva-0x018aa1c0) | World/cell placement reuse age/prune residual generation and return | C |
| `0x018ab060` | `0x1418ab060` | [Checkpoint: completion callbacks and the preparation antecedent · entry](geography.md#rva-0x018ab060) | Original report discusses this roster entry under Checkpoint: completion callbacks and the preparation antecedent. | C |
| `0x018ab1c0` | `0x1418ab1c0` | [Selected placement append representation](geography.md#rva-0x018ab1c0) | Selected placement append representation | C |
| `0x018ab2d0` | `0x1418ab2d0` | [Enumerate retained body content](workshop.md#rva-0x018ab2d0) | Enumerate retained body content | C |
| `0x018ab600` | `0x1418ab600` | [Fractional position producers and consumers · entry](geography.md#rva-0x018ab600) | Original report discusses this roster entry under Fractional position producers and consumers. | C |
| `0x018ab8d0` | `0x1418ab8d0` | [Selected content world lookup/creation and activation through 0x140798030](geography.md#rva-0x018ab8d0) | Selected content world lookup/creation and activation through 0x140798030 | C |
| `0x018abd60` | `0x1418abd60` | [Call integer projection in the bounded content path](workshop.md#rva-0x018abd60) | Call integer projection in the bounded content path | C |
| `0x018ad2b0` | `0x1418ad2b0` | [Restored BlockContent demand restores world references and activation](geography.md#rva-0x018ad2b0) | Restored BlockContent demand restores world references and activation | C |
| `0x018ae790` | `0x1418ae790` | [PCM BlockContent existing-or-create lookup by PNDT/tree block](geography.md#rva-0x018ae790) | PCM BlockContent existing-or-create lookup by PNDT/tree block | C |
| `0x018aee00` | `0x1418aee00` | [Existing content replay versus alternative selection request](geography.md#rva-0x018aee00) | Existing content replay versus alternative selection request | C |
| `0x018aefd0` | `0x1418aefd0` | [Queue a pending planet content request copy](workshop.md#rva-0x018aefd0) | Queue a pending planet content request copy | C |
| `0x018af110` | `0x1418af110` | [Existing content pending predicate and queued overlay request with persisted seed](geography.md#rva-0x018af110) | Existing content pending predicate and queued overlay request with persisted seed | C |
| `0x018af8e0` | `0x1418af8e0` | [Alternative missing SFTR creation then content demand](geography.md#rva-0x018af8e0) | Alternative missing SFTR creation then content demand | C |
| `0x018b0920` | `0x1418b0920` | [Call integer projection in the paired content path](workshop.md#rva-0x018b0920) | Call integer projection in the paired content path | C |
| `0x018b1b40` | `0x1418b1b40` | [PCM pending counter drain and in-flight object cleanup](geography.md#rva-0x018b1b40) | PCM pending counter drain and in-flight object cleanup | C |
| `0x018b1eb0` | `0x1418b1eb0` | [Write global type-7 PlanetContentManager state](interfaces.md#rva-0x018b1eb0) | Serializes the PCM seed, maps and subsequent type-7 fields. | B |
| `0x018b20f0` | `0x1418b20f0` | [PCM world block and placement writer](geography.md#rva-0x018b20f0) | PCM world block and placement writer | C |
| `0x018b22c0` | `0x1418b22c0` | [Restore global type-7 PlanetContentManager state](interfaces.md#rva-0x018b22c0) | Restores saved PCM fields and reconstructs typed references under version and resolution gates. | B |
| `0x018b2cb0` | `0x1418b2cb0` | [Ordinary global type 7 revert drains clears both maps and reseeds working RNG](geography.md#rva-0x018b2cb0) | Ordinary global type 7 revert drains clears both maps and reseeds working RNG | C |
| `0x018b2f90` | `0x1418b2f90` | [Global type 7 finish deferred removed-world cleanup](geography.md#rva-0x018b2f90) | Global type 7 finish deferred removed-world cleanup | C |
| `0x018b34e0` | `0x1418b34e0` | [Poll the resulting alias location](workshop.md#rva-0x018b34e0) | Poll the resulting alias location | C |
| `0x018b36b0` | `0x1418b36b0` | [PCM BlockContent writer](geography.md#rva-0x018b36b0) | PCM BlockContent writer | C |
| `0x018b38a0` | `0x1418b38a0` | [PCM BlockContent reader](geography.md#rva-0x018b38a0) | PCM BlockContent reader | C |
| `0x018b3e30` | `0x1418b3e30` | [PCM content item reader typed world and content node](geography.md#rva-0x018b3e30) | PCM content item reader typed world and content node | C |
| `0x018b4050` | `0x1418b4050` | [Saved item state application to reconstructed world references](geography.md#rva-0x018b4050) | Saved item state application to reconstructed world references | C |
| `0x018b4170` | `0x1418b4170` | [Age refresh prunes unprotected placements resets applied flag](geography.md#rva-0x018b4170) | Age refresh prunes unprotected placements resets applied flag | C |
| `0x018b4270` | `0x1418b4270` | [Initialization and successful-construction obligations · entry](geography.md#rva-0x018b4270) | Original report discusses this roster entry under Initialization and successful-construction obligations. | C |
| `0x018b5ea0` | `0x1418b5ea0` | [Receive candidate body identities for an alias request](workshop.md#rva-0x018b5ea0) | Receive candidate body identities for an alias request | C |
| `0x018ba0c0` | `0x1418ba0c0` | [Typed content-node ID restoration](geography.md#rva-0x018ba0c0) | Typed content-node ID restoration | C |
| `0x018ba850` | `0x1418ba850` | [Existing restored content item world replay](geography.md#rva-0x018ba850) | Existing restored content item world replay | C |
| `0x018bab90` | `0x1418bab90` | [Write PNDT-keyed PCM content map](interfaces.md#rva-0x018bab90) | Serializes the type-7 map of planetary content blocks. | B |
| `0x018bad70` | `0x1418bad70` | [Write world-token-keyed PCM placement map](interfaces.md#rva-0x018bad70) | Serializes the type-7 map of world placements. | B |
| `0x018baef0` | `0x1418baef0` | [Revert collect PNDT content worlds into deferred removed-ID set](geography.md#rva-0x018baef0) | Revert collect PNDT content worlds into deferred removed-ID set | C |
| `0x018bb0d0` | `0x1418bb0d0` | [Revert collect world map IDs into deferred removed-ID set](geography.md#rva-0x018bb0d0) | Revert collect world map IDs into deferred removed-ID set | C |
| `0x018bb7e0` | `0x1418bb7e0` | [Dispatch the queued planet content request](workshop.md#rva-0x018bb7e0) | Dispatch the queued planet content request | C |
| `0x018bb8d0` | `0x1418bb8d0` | [Fractional position producers and consumers · entry](workshop.md#rva-0x018bb8d0) | Original report discusses this roster entry under Fractional position producers and consumers. | C |
| `0x018bc060` | `0x1418bc060` | [Fourth trace round · entry](workshop.md#rva-0x018bc060) | Original report discusses this roster entry under Fourth trace round. | C |
| `0x018bcfb0` | `0x1418bcfb0` | [pending open-close completion retirement](power.md#rva-0x018bcfb0) | pending open-close completion retirement | B |
| `0x018be3e0` | `0x1418be3e0` | [Handle the inspected damage path call](population.md#rva-0x018be3e0) | Handle the inspected damage path call | C |
| `0x018be6e0` | `0x1418be6e0` | [Dispatch actor versus destructible reference handling](population.md#rva-0x018be6e0) | Dispatch actor versus destructible reference handling | C |
| `0x018c1f10` | `0x1418c1f10` | [Dispatch the existing-reference base replacement service](workshop.md#rva-0x018c1f10) | Dispatch the existing-reference base replacement service | C |
| `0x018c28b0` | `0x1418c28b0` | [Dispatch queued frame conversion](workshop.md#rva-0x018c28b0) | Dispatch queued frame conversion | C |
| `0x018c2a60` | `0x1418c2a60` | [pending open-close state lookup](power.md#rva-0x018c2a60) | pending open-close state lookup | B |
| `0x018c2af0` | `0x1418c2af0` | [pending open-close enqueue](power.md#rva-0x018c2af0) | pending open-close enqueue | B |
| `0x018c3600` | `0x1418c3600` | [Type1 abilities: ship Fusion and destination state · entry](population.md#rva-0x018c3600) | Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state. | C |
| `0x018c4f00` | `0x1418c4f00` | [dispatch or queue perk rank transition](population.md#rva-0x018c4f00) | dispatch or queue perk rank transition | B |
| `0x018c50a0` | `0x1418c50a0` | [resolved actor rank transition](population.md#rva-0x018c50a0) | resolved actor rank transition | B |
| `0x018c7270` | `0x1418c7270` | [Participate in the designated-thread power update route](power.md#rva-0x018c7270) | Participate in the designated-thread power update route | C |
| `0x018c7550` | `0x1418c7550` | [Participate in the designated-thread power update route](power.md#rva-0x018c7550) | Participate in the designated-thread power update route | C |
| `0x018cafc0` | `0x1418cafc0` | [Dispatch the reference base setter route](workshop.md#rva-0x018cafc0) | Dispatch the reference base setter route | C |
| `0x018ccbd0` | `0x1418ccbd0` | [Selected rank and load reconstruction · entry](population.md#rva-0x018ccbd0) | Original report discusses this roster entry under Selected rank and load reconstruction. | C |
| `0x018d8ea0` | `0x1418d8ea0` | [Entry-storage loss and return · entry](population.md#rva-0x018d8ea0) | Original report discusses this roster entry under Entry-storage loss and return. | C |
| `0x018dba40` | `0x1418dba40` | [Emit the loaded-reference event from a move or 3D path](power.md#rva-0x018dba40) | Emit the loaded-reference event from a move or 3D path | C |
| `0x018e17d0` | `0x1418e17d0` | [Entry-storage loss and return · entry](population.md#rva-0x018e17d0) | Original report discusses this roster entry under Entry-storage loss and return. | C |
| `0x018e2540` | `0x1418e2540` | [Entry-storage loss and return · entry](population.md#rva-0x018e2540) | Original report discusses this roster entry under Entry-storage loss and return. | C |
| `0x018e4540` | `0x1418e4540` | [Life state, absence and replacement · entry](population.md#rva-0x018e4540) | Original report discusses this roster entry under Life state, absence and replacement. | C |
| `0x018e9cb0` | `0x1418e9cb0` | [Elapsed producer and staged consumers · entry](inventory.md#rva-0x018e9cb0) | Original report discusses this roster entry under Elapsed producer and staged consumers. | C |
| `0x018f53e0` | `0x1418f53e0` | [Resolve the exact inventory form and instance row](inventory.md#rva-0x018f53e0) | Resolve the exact inventory form and instance row | C |
| `0x018f56d0` | `0x1418f56d0` | [Check the selected inventory row bit](inventory.md#rva-0x018f56d0) | Check the selected inventory row bit | C |
| `0x0190bee0` | `0x14190bee0` | [Resolve effective carry weight for the inventory path](inventory.md#rva-0x0190bee0) | Resolve effective carry weight for the inventory path | C |
| `0x01916b30` | `0x141916b30` | [Write the Actor private owned-perk channel](population.md#rva-0x01916b30) | Write the Actor private owned-perk channel | C |
| `0x01917e40` | `0x141917e40` | [Read additional selected actor perk ranks](population.md#rva-0x01917e40) | Read additional selected actor perk ranks | C |
| `0x019198a0` | `0x1419198a0` | [Actor finalization and perk-bucket reset](population.md#rva-0x019198a0) | Actor finalization and perk-bucket reset | C |
| `0x01924af0` | `0x141924af0` | [Forward submission to the path state handler](inventory.md#rva-0x01924af0) | Forward submission to the path state handler | C |
| `0x01924dc0` | `0x141924dc0` | [What progresses without a visible ship · entry](inventory.md#rva-0x01924dc0) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x01935370` | `0x141935370` | [active actor entry-point copy](population.md#rva-0x01935370) | active actor entry-point copy | B |
| `0x01936490` | `0x141936490` | [Entry-storage loss and return · entry](population.md#rva-0x01936490) | Original report discusses this roster entry under Entry-storage loss and return. | C |
| `0x01948250` | `0x141948250` | [Entry-storage loss and return · entry](population.md#rva-0x01948250) | Original report discusses this roster entry under Entry-storage loss and return. | C |
| `0x01954810` | `0x141954810` | [actor perk rank update](population.md#rva-0x01954810) | actor perk rank update | B |
| `0x01954f20` | `0x141954f20` | [Handle cache and state follow-up after a perk transition](production.md#rva-0x01954f20) | Handle cache and state follow-up after a perk transition | C |
| `0x01955080` | `0x141955080` | [actor effective perk rank lookup](population.md#rva-0x01955080) | actor effective perk rank lookup | B |
| `0x01955350` | `0x141955350` | [Read the active actor perk bucket](population.md#rva-0x01955350) | Read the active actor perk bucket | C |
| `0x01955400` | `0x141955400` | [Replay base and added actor perk ranks](population.md#rva-0x01955400) | Replay base and added actor perk ranks | C |
| `0x01955f80` | `0x141955f80` | [Selected rank and load reconstruction · entry](population.md#rva-0x01955f80) | Original report discusses this roster entry under Selected rank and load reconstruction. | C |
| `0x01958550` | `0x141958550` | [Update dependent state after the perk transition](production.md#rva-0x01958550) | Update dependent state after the perk transition | C |
| `0x0196cdc0` | `0x14196cdc0` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x0196cdc0) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x01976dc0` | `0x141976dc0` | [Read the base value for the outpost panel maximum](interfaces.md#rva-0x01976dc0) | Read the base value for the outpost panel maximum | C |
| `0x019776f0` | `0x1419776f0` | [Deployment allowance and ordinary beacon operation · entry](population.md#rva-0x019776f0) | Original report discusses this roster entry under Deployment allowance and ordinary beacon operation. | C |
| `0x01994ed0` | `0x141994ed0` | [What progresses without a visible ship · entry](inventory.md#rva-0x01994ed0) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x01995020` | `0x141995020` | [What progresses without a visible ship · entry](inventory.md#rva-0x01995020) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x019a3330` | `0x1419a3330` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x019a3330) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x019a47d0` | `0x1419a47d0` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x019a47d0) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x019a9040` | `0x1419a9040` | [Resolve instance equipment data in the restore route](inventory.md#rva-0x019a9040) | Resolve instance equipment data in the restore route | C |
| `0x019aa500` | `0x1419aa500` | [Unequip and clear the saved equipment nibble](inventory.md#rva-0x019aa500) | Unequip and clear the saved equipment nibble | C |
| `0x019ae7f0` | `0x1419ae7f0` | [AV modifier total](production.md#rva-0x019ae7f0) | AV modifier total | B |
| `0x019ae970` | `0x1419ae970` | [Apply a reference actor-value modifier](population.md#rva-0x019ae970) | Apply a reference actor-value modifier | C |
| `0x019aec20` | `0x1419aec20` | [serialize base AV and modifiers](production.md#rva-0x019aec20) | serialize base AV and modifiers | B |
| `0x019aeff0` | `0x1419aeff0` | [restore base AV and modifiers](production.md#rva-0x019aeff0) | restore base AV and modifiers | B |
| `0x019af700` | `0x1419af700` | [explicit base AV lookup](production.md#rva-0x019af700) | explicit base AV lookup | B |
| `0x019af7c0` | `0x1419af7c0` | [upsert explicit base AV row](production.md#rva-0x019af7c0) | upsert explicit base AV row | B |
| `0x019b4d10` | `0x1419b4d10` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x019b4d10) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x019ce030` | `0x1419ce030` | [Process an admitted defense target](population.md#rva-0x019ce030) | Process an admitted defense target | C |
| `0x019d0690` | `0x1419d0690` | [Refresh equipment and 3D after the mannequin inventory change](inventory.md#rva-0x019d0690) | Refresh equipment and 3D after the mannequin inventory change | C |
| `0x019f7b80` | `0x1419f7b80` | [Selected rank and load reconstruction · entry](population.md#rva-0x019f7b80) | Original report discusses this roster entry under Selected rank and load reconstruction. | C |
| `0x019f8f40` | `0x1419f8f40` | [Entry-storage loss and return · destructor](population.md#rva-0x019f8f40) | Original report discusses this roster entry under Entry-storage loss and return. | C |
| `0x01a154d0` | `0x141a154d0` | [Read a companion Actor suffix field](population.md#rva-0x01a154d0) | Read a companion Actor suffix field | C |
| `0x01a20380` | `0x141a20380` | [Native transition table · entry](geography.md#rva-0x01a20380) | Original report discusses this roster entry under Native transition table. | C |
| `0x01a25420` | `0x141a25420` | [Confirmation and transition ingress · entry](geography.md#rva-0x01a25420) | Original report discusses this roster entry under Confirmation and transition ingress. | C |
| `0x01a278a0` | `0x141a278a0` | [Native transition table · entry](geography.md#rva-0x01a278a0) | Original report discusses this roster entry under Native transition table. | C |
| `0x01a27d80` | `0x141a27d80` | [travel skipped-time update](production.md#rva-0x01a27d80) | travel skipped-time update | B |
| `0x01a38840` | `0x141a38840` | [Finish the mapped wait-loop tail](production.md#rva-0x01a38840) | Finish the mapped wait-loop tail | C |
| `0x01a38ba0` | `0x141a38ba0` | [wait or sleep skipped-time update](production.md#rva-0x01a38ba0) | wait or sleep skipped-time update | B |
| `0x01a44770` | `0x141a44770` | [Remove the dropper and slot relationship](inventory.md#rva-0x01a44770) | Remove the dropper and slot relationship | C |
| `0x01a45dc0` | `0x141a45dc0` | [Ownership and player action · entry](inventory.md#rva-0x01a45dc0) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x01a46940` | `0x141a46940` | [Player writer carrying the shared inventory](inventory.md#rva-0x01a46940) | Player writer carrying the shared inventory | C |
| `0x01a48f50` | `0x141a48f50` | [Player loader carrying the shared inventory](inventory.md#rva-0x01a48f50) | Player loader carrying the shared inventory | C |
| `0x01a4b590` | `0x141a4b590` | [Selected rank and load reconstruction · wrapper](population.md#rva-0x01a4b590) | Original report discusses this roster entry under Selected rank and load reconstruction. | C |
| `0x01a4bf80` | `0x141a4bf80` | [Save/load authority and remote meaning · entry](inventory.md#rva-0x01a4bf80) | Original report discusses this roster entry under Save/load authority and remote meaning. | C |
| `0x01a67830` | `0x141a67830` | [Confirmation and transition ingress · entry](geography.md#rva-0x01a67830) | Original report discusses this roster entry under Confirmation and transition ingress. | C |
| `0x01a9e680` | `0x141a9e680` | [Handle path submission in the registered FlyLand route](inventory.md#rva-0x01a9e680) | Handle path submission in the registered FlyLand route | C |
| `0x01b30b30` | `0x141b30b30` | [Combat and non-effect role metadata · entry](population.md#rva-0x01b30b30) | Original report discusses this roster entry under Combat and non-effect role metadata. | C |
| `0x01c2c840` | `0x141c2c840` | [Every retained size-scan literal · entry](geography.md#rva-0x01c2c840) | Original report discusses this roster entry under Every retained size-scan literal. | C |
| `0x01eab810` | `0x141eab810` | [ContainerMenu separate inventory model construction](inventory.md#rva-0x01eab810) | ContainerMenu separate inventory model construction | C |
| `0x01eac0e0` | `0x141eac0e0` | [Participate in player ship inventory display filtering](inventory.md#rva-0x01eac0e0) | Participate in player ship inventory display filtering | C |
| `0x01eaca10` | `0x141eaca10` | [Participate in player ship inventory display filtering](inventory.md#rva-0x01eaca10) | Participate in player ship inventory display filtering | C |
| `0x01eadb50` | `0x141eadb50` | [Assign the display menu predicate](inventory.md#rva-0x01eadb50) | Assign the display menu predicate | C |
| `0x01eadf60` | `0x141eadf60` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x01eadf60) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x01eae1f0` | `0x141eae1f0` | [Recognition, definitions and ordinary admission · entry](inventory.md#rva-0x01eae1f0) | Original report discusses this roster entry under Recognition, definitions and ordinary admission. | C |
| `0x01eaf090` | `0x141eaf090` | [manual item and bound callable acceptance](inventory.md#rva-0x01eaf090) | manual item and bound callable acceptance | C |
| `0x01eaf900` | `0x141eaf900` | [manual ContainerMenu TransferItem sink](inventory.md#rva-0x01eaf900) | manual ContainerMenu TransferItem sink | C |
| `0x01eaf9e0` | `0x141eaf9e0` | [manual item identity and inventory command](inventory.md#rva-0x01eaf9e0) | manual item identity and inventory command | C |
| `0x01eafe00` | `0x141eafe00` | [manual per-item transfer admission and dispatch](inventory.md#rva-0x01eafe00) | manual per-item transfer admission and dispatch | C |
| `0x01eb01a0` | `0x141eb01a0` | [Check display-specific transfer eligibility](inventory.md#rva-0x01eb01a0) | Distinguishes store and take routes before display inventory movement. | B |
| `0x01eb1640` | `0x141eb1640` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x01eb1640) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x01eb1730` | `0x141eb1730` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x01eb1730) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x01eb6060` | `0x141eb6060` | [Mannequin script, equipment and restoration · entry](inventory.md#rva-0x01eb6060) | Original report discusses this roster entry under Mannequin script, equipment and restoration. | C |
| `0x01eb7950` | `0x141eb7950` | [Forward the inventory item interaction](inventory.md#rva-0x01eb7950) | Forward the inventory item interaction | C |
| `0x01ee7130` | `0x141ee7130` | [Dispatch the spatially bounded storage path](inventory.md#rva-0x01ee7130) | Dispatch the spatially bounded storage path | C |
| `0x01ee7440` | `0x141ee7440` | [Handle the single-form mannequin inventory branch](inventory.md#rva-0x01ee7440) | Handle the single-form mannequin inventory branch | C |
| `0x01ee80e0` | `0x141ee80e0` | [Continue spatially bounded storage selection](inventory.md#rva-0x01ee80e0) | Continue spatially bounded storage selection | C |
| `0x01ee8d20` | `0x141ee8d20` | [spatial Transfer Container candidate selection](inventory.md#rva-0x01ee8d20) | spatial Transfer Container candidate selection | C |
| `0x01f76dd0` | `0x141f76dd0` | [NPC script bit 9/slot 9 source selection and original-handle binding](population.md#rva-0x01f76dd0) | NPC script bit 9/slot 9 source selection and original-handle binding | C |
| `0x01fb3670` | `0x141fb3670` | [Script authority and native deadline · entry](inventory.md#rva-0x01fb3670) | Original report discusses this roster entry under Script authority and native deadline. | C |
| `0x01fb3710` | `0x141fb3710` | [Service VM game-time timer delivery](inventory.md#rva-0x01fb3710) | Suppresses delivery during the mapped wait/sleep flag and resumes dispatch of pending deadlines. | A |
| `0x01fb5de0` | `0x141fb5de0` | [NPC form callback invokes inherited script binding](population.md#rva-0x01fb5de0) | NPC form callback invokes inherited script binding | C |
| `0x01fb8ae0` | `0x141fb8ae0` | [Script authority and native deadline · entry](inventory.md#rva-0x01fb8ae0) | Original report discusses this roster entry under Script authority and native deadline. | C |
| `0x01fc48e0` | `0x141fc48e0` | [Actor AddPerk callback](population.md#rva-0x01fc48e0) | Actor AddPerk callback | B |
| `0x01fc7f50` | `0x141fc7f50` | [Handle the IsBleedingOut native callback](population.md#rva-0x01fc7f50) | Handle the IsBleedingOut native callback | C |
| `0x01fc7fb0` | `0x141fc7fb0` | [Return the script-facing actor death predicate](population.md#rva-0x01fc7fb0) | Return the script-facing actor death predicate | C |
| `0x01fc8c70` | `0x141fc8c70` | [Ownership and player action · entry](inventory.md#rva-0x01fc8c70) | Original report discusses this roster entry under Ownership and player action. | C |
| `0x01fcc740` | `0x141fcc740` | [Bind Actor AddPerk to its native path](production.md#rva-0x01fcc740) | Bind Actor AddPerk to its native path | C |
| `0x01fd1470` | `0x141fd1470` | [Handle the IsUnconscious native callback](population.md#rva-0x01fd1470) | Handle the IsUnconscious native callback | C |
| `0x02008540` | `0x142008540` | [Add an unassigned actor to availability](population.md#rva-0x02008540) | Admits a nonnull actor without current assignment to the available roster. | B |
| `0x0200e610` | `0x14200e610` | [Game IsResearchComplete callback](production.md#rva-0x0200e610) | Game IsResearchComplete callback | B |
| `0x0200f5a0` | `0x14200f5a0` | [Continue available and assigned crew bookkeeping](population.md#rva-0x0200f5a0) | Continue available and assigned crew bookkeeping | C |
| `0x02010740` | `0x142010740` | [Register the GetPlayer native function](workshop.md#rva-0x02010740) | Register the GetPlayer native function | C |
| `0x020188d0` | `0x1420188d0` | [Construct the GetPlayer Papyrus native binding](workshop.md#rva-0x020188d0) | Construct the GetPlayer Papyrus native binding | C |
| `0x02032570` | `0x142032570` | [What progresses without a visible ship · entry](inventory.md#rva-0x02032570) | Original report discusses this roster entry under What progresses without a visible ship. | C |
| `0x0204d600` | `0x14204d600` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0204d600) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x02065260` | `0x142065260` | [Execute the damage object functor](population.md#rva-0x02065260) | Execute the damage object functor | C |
| `0x02068a10` | `0x142068a10` | [AddTransferLink callback](production.md#rva-0x02068a10) | AddTransferLink callback | B |
| `0x02068d70` | `0x142068d70` | [Bridge script AssignCrew with admission bypass](population.md#rva-0x02068d70) | Obtains the owner's E2 and calls shared membership insertion with its bypass option. | B |
| `0x0206ab30` | `0x14206ab30` | [Bridge cargo readiness to producer eligibility](inventory.md#rva-0x0206ab30) | Checks whether the mapped pad passes mode 0 producer eligibility for ship script use. | B |
| `0x0206b1b0` | `0x14206b1b0` | [Dispatch the damage-object operation](population.md#rva-0x0206b1b0) | Dispatch the damage-object operation | C |
| `0x0206e3e0` | `0x14206e3e0` | [GetActorBaseForResource callback](production.md#rva-0x0206e3e0) | GetActorBaseForResource callback | B |
| `0x0206f3b0` | `0x14206f3b0` | [GetAllCrewMembers callback](population.md#rva-0x0206f3b0) | GetAllCrewMembers callback | B |
| `0x020702e0` | `0x1420702e0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x020702e0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x02070300` | `0x142070300` | [Workshop identity, construction and position native entry](workshop.md#rva-0x02070300) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x02070320` | `0x142070320` | [Workshop identity, construction and position native entry](workshop.md#rva-0x02070320) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x02070ff0` | `0x142070ff0` | [GetFloraForResource callback](production.md#rva-0x02070ff0) | GetFloraForResource callback | B |
| `0x02072580` | `0x142072580` | [Workshop identity, construction and position native entry](workshop.md#rva-0x02072580) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x02072590` | `0x142072590` | [Workshop identity, construction and position native entry](workshop.md#rva-0x02072590) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x020725a0` | `0x1420725a0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x020725a0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x02073cf0` | `0x142073cf0` | [Forward the registered GetWorkshop callback](workshop.md#rva-0x02073cf0) | Supplies a registered Workshop key and forwards into the keyed reference lookup. | B |
| `0x02073dc0` | `0x142073dc0` | [FUN_142073dc0](workshop.md#rva-0x02073dc0) | FUN_142073dc0 | C |
| `0x02074870` | `0x142074870` | [FUN_142074870](workshop.md#rva-0x02074870) | FUN_142074870 | C |
| `0x02077ac0` | `0x142077ac0` | [Actual movement triggers and scheduler boundary · entry](inventory.md#rva-0x02077ac0) | Original report discusses this roster entry under Actual movement triggers and scheduler boundary. | C |
| `0x02085050` | `0x142085050` | [Register inherited GetCurrentLocation native function](workshop.md#rva-0x02085050) | Register inherited GetCurrentLocation native function | C |
| `0x0208b8f0` | `0x14208b8f0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0208b8f0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0208b990` | `0x14208b990` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0208b990) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0208b9e0` | `0x14208b9e0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x0208b9e0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x0208ba90` | `0x14208ba90` | [Read the deleted runtime form flag](workshop.md#rva-0x0208ba90) | Read the deleted runtime form flag | C |
| `0x0208bab0` | `0x14208bab0` | [Read the disabled runtime form flag](workshop.md#rva-0x0208bab0) | Read the disabled runtime form flag | C |
| `0x02092b00` | `0x142092b00` | [Register the cargo inventory transfer native function](inventory.md#rva-0x02092b00) | Register the cargo inventory transfer native function | C |
| `0x0209ba00` | `0x14209ba00` | [Bind the GetWorkshopResourceObjects native callback](workshop.md#rva-0x0209ba00) | Bind the GetWorkshopResourceObjects native callback | C |
| `0x0209bc00` | `0x14209bc00` | [Bind the GetWorkshopOwnedObjects native callback](workshop.md#rva-0x0209bc00) | Bind the GetWorkshopOwnedObjects native callback | C |
| `0x0209be00` | `0x14209be00` | [Bind the GetWorkshop native callback](workshop.md#rva-0x0209be00) | Bind the GetWorkshop native callback | C |
| `0x0209ec60` | `0x14209ec60` | [Construct the GetCurrentLocation Papyrus native binding](workshop.md#rva-0x0209ec60) | Construct the GetCurrentLocation Papyrus native binding | C |
| `0x0209ff50` | `0x14209ff50` | [Register the crew-members callback](production.md#rva-0x0209ff50) | Register the crew-members callback | C |
| `0x020c02b0` | `0x1420c02b0` | [Ordinary causal trace · entry](population.md#rva-0x020c02b0) | Original report discusses this roster entry under Ordinary causal trace. | C |
| `0x020f8970` | `0x1420f8970` | [Write the pending timer deadline and script identity](inventory.md#rva-0x020f8970) | Write the pending timer deadline and script identity | C |
| `0x020f8d00` | `0x1420f8d00` | [Restore the pending timer record](inventory.md#rva-0x020f8d00) | Restore the pending timer record | C |
| `0x020f9f90` | `0x1420f9f90` | [Dispatch due game-time timer](inventory.md#rva-0x020f9f90) | Dispatch due game-time timer | C |
| `0x020fa390` | `0x1420fa390` | [Save pending VM game-time timers](inventory.md#rva-0x020fa390) | Preserves pending timer identity, pause fields and the remaining time rather than heap identity. | B |
| `0x020fa920` | `0x1420fa920` | [Dispatch pending game-time timer serialization](inventory.md#rva-0x020fa920) | Dispatch pending game-time timer serialization | C |
| `0x020fa9a0` | `0x1420fa9a0` | [Wait, fast travel and reload · entry](inventory.md#rva-0x020fa9a0) | Original report discusses this roster entry under Wait, fast travel and reload. | C |
| `0x020fb880` | `0x1420fb880` | [Start a game-time timer](inventory.md#rva-0x020fb880) | Start a game-time timer | C |
| `0x020fcc70` | `0x1420fcc70` | [Dispatch pending game-time timer restoration](inventory.md#rva-0x020fcc70) | Dispatch pending game-time timer restoration | C |
| `0x02104ff0` | `0x142104ff0` | [Receive the selected-site state update](workshop.md#rva-0x02104ff0) | Receive the selected-site state update | C |
| `0x021159b0` | `0x1421159b0` | [AA: ship capacity, not a CONT CarryWeight aura · entry](population.md#rva-0x021159b0) | Original report discusses this roster entry under AA: ship capacity, not a CONT CarryWeight aura. | C |
| `0x02116840` | `0x142116840` | [cell-context reference resolver](power.md#rva-0x02116840) | cell-context reference resolver | B |
| `0x021177b0` | `0x1421177b0` | [Compare ship extents against destination size limits](workshop.md#rva-0x021177b0) | Compare ship extents against destination size limits | C |
| `0x021190b0` | `0x1421190b0` | [Resolve the containing reference location context](workshop.md#rva-0x021190b0) | Resolve the containing reference location context | C |
| `0x0211a000` | `0x14211a000` | [Reset callers and predicates · entry](geography.md#rva-0x0211a000) | Original report discusses this roster entry under Reset callers and predicates. | C |
| `0x0211b700` | `0x14211b700` | [Effective ship cargo capacity](inventory.md#rva-0x0211b700) | Effective ship cargo capacity | C |
| `0x02121570` | `0x142121570` | [Traverse cell location and special-reference data](workshop.md#rva-0x02121570) | Traverse cell location and special-reference data | C |
| `0x021230a0` | `0x1421230a0` | [AA: ship capacity, not a CONT CarryWeight aura · entry](inventory.md#rva-0x021230a0) | Original report discusses this roster entry under AA: ship capacity, not a CONT CarryWeight aura. | C |
| `0x02128f70` | `0x142128f70` | [Request the ship fast-travel marker type](workshop.md#rva-0x02128f70) | Request the ship fast-travel marker type | C |
| `0x0212d230` | `0x14212d230` | [Resolve the ship-associated actor](population.md#rva-0x0212d230) | Resolve the ship-associated actor | C |
| `0x021661c0` | `0x1421661c0` | [Select type-4 reconstruction for an existing owner](workshop.md#rva-0x021661c0) | Select type-4 reconstruction for an existing owner | C |
| `0x0219bb40` | `0x14219bb40` | [Qualify vehicle state for beacon placement](workshop.md#rva-0x0219bb40) | Qualify vehicle state for beacon placement | C |
| `0x021a5fc0` | `0x1421a5fc0` | [Callbacks and admission handoff · entry](workshop.md#rva-0x021a5fc0) | Original report discusses this roster entry under Callbacks and admission handoff. | C |
| `0x021a6680` | `0x1421a6680` | [Apply category and current-node changes](workshop.md#rva-0x021a6680) | Apply category and current-node changes | C |
| `0x021a6810` | `0x1421a6810` | [Callbacks and admission handoff · entry](workshop.md#rva-0x021a6810) | Original report discusses this roster entry under Callbacks and admission handoff. | C |
| `0x021a6b60` | `0x1421a6b60` | [Consume the concrete selected variant ID](workshop.md#rva-0x021a6b60) | Consume the concrete selected variant ID | C |
| `0x021a7060` | `0x1421a7060` | [Construction ingredient availability](inventory.md#rva-0x021a7060) | Construction ingredient availability | C |
| `0x021a7950` | `0x1421a7950` | [Construction ingredient spending](inventory.md#rva-0x021a7950) | Construction ingredient spending | C |
| `0x021a9840` | `0x1421a9840` | [Footer gaps investigated · entry](workshop.md#rva-0x021a9840) | Original report discusses this roster entry under Footer gaps investigated. | C |
| `0x021a98b0` | `0x1421a98b0` | [Footer gaps investigated · entry](workshop.md#rva-0x021a98b0) | Original report discusses this roster entry under Footer gaps investigated. | C |
| `0x021ad290` | `0x1421ad290` | [Workshop event listener registration](power.md#rva-0x021ad290) | Workshop event listener registration | B |
| `0x021ad550` | `0x1421ad550` | [Unregister the Workshop object-loaded event sink](inventory.md#rva-0x021ad550) | Unregister the Workshop object-loaded event sink | C |
| `0x021ad860` | `0x1421ad860` | [Workshop listener vtable construction](power.md#rva-0x021ad860) | Workshop listener vtable construction | B |
| `0x021adb00` | `0x1421adb00` | [operation state construction](geography.md#rva-0x021adb00) | operation state construction | B |
| `0x021ae260` | `0x1421ae260` | [operation state teardown](geography.md#rva-0x021ae260) | operation state teardown | B |
| `0x021ae590` | `0x1421ae590` | [availability state teardown](geography.md#rva-0x021ae590) | availability state teardown | B |
| `0x021aec70` | `0x1421aec70` | [Handle the snap behavior change event](workshop.md#rva-0x021aec70) | Handle the snap behavior change event | C |
| `0x021b03c0` | `0x1421b03c0` | [Build-mode repair wrapper](population.md#rva-0x021b03c0) | Build-mode repair wrapper | C |
| `0x021b10b0` | `0x1421b10b0` | [successful construction inserts item](population.md#rva-0x021b10b0) | successful construction inserts item | C |
| `0x021b11a0` | `0x1421b11a0` | [accumulating writer](workshop.md#rva-0x021b11a0) | accumulating writer | C |
| `0x021b1450` | `0x1421b1450` | [Mutations, movement and restored state · entry](workshop.md#rva-0x021b1450) | Original report discusses this roster entry under Mutations, movement and restored state. | C |
| `0x021b2030` | `0x1421b2030` | [Manual user action to authoritative operation · entry](workshop.md#rva-0x021b2030) | Original report discusses this roster entry under Manual user action to authoritative operation. | C |
| `0x021b2360` | `0x1421b2360` | [normal build requires candidate status 2](population.md#rva-0x021b2360) | normal build requires candidate status 2 | C |
| `0x021b2570` | `0x1421b2570` | [established initialization caller](geography.md#rva-0x021b2570) | established initialization caller | B |
| `0x021b2ca0` | `0x1421b2ca0` | [Exit and reset the placement publisher](workshop.md#rva-0x021b2ca0) | Exit and reset the placement publisher | C |
| `0x021b2e20` | `0x1421b2e20` | [normal attempt requires status 2](population.md#rva-0x021b2e20) | normal attempt requires status 2 | C |
| `0x021b41f0` | `0x1421b41f0` | [preview operation update](geography.md#rva-0x021b41f0) | preview operation update | B |
| `0x021b44b0` | `0x1421b44b0` | [Call the accumulating Workshop compensation writer](workshop.md#rva-0x021b44b0) | Supplies one of the endpoint-ordered call paths into the writer. | B |
| `0x021b5720` | `0x1421b5720` | [Initialize Wait3D timers and latch](interfaces.md#rva-0x021b5720) | Initialize Wait3D timers and latch | C |
| `0x021b5750` | `0x1421b5750` | [Request spinner-off on Wait3D exit](interfaces.md#rva-0x021b5750) | Request spinner-off on Wait3D exit | C |
| `0x021b5970` | `0x1421b5970` | [Wait3D update](interfaces.md#rva-0x021b5970) | Wait3D update | C |
| `0x021b5e70` | `0x1421b5e70` | [Dispatch indirect placement update](workshop.md#rva-0x021b5e70) | Dispatch indirect placement update | C |
| `0x021b62c0` | `0x1421b62c0` | [Initialize placement reference creation](workshop.md#rva-0x021b62c0) | Initialize placement reference creation | C |
| `0x021b64c0` | `0x1421b64c0` | [operation transition caller](geography.md#rva-0x021b64c0) | operation transition caller | B |
| `0x021b6a10` | `0x1421b6a10` | [Clear resource population range ends](geography.md#rva-0x021b6a10) | Clear resource population range ends | C |
| `0x021b6be0` | `0x1421b6be0` | [reset clears item caches](population.md#rva-0x021b6be0) | reset clears item caches | C |
| `0x021b7200` | `0x1421b7200` | [Handle ordinary beacon removal](workshop.md#rva-0x021b7200) | Handle ordinary beacon removal | C |
| `0x021ba1b0` | `0x1421ba1b0` | [Disable the publisher from a separate placement state](workshop.md#rva-0x021ba1b0) | Disable the publisher from a separate placement state | C |
| `0x021ba2e0` | `0x1421ba2e0` | [Call the native geometry clear and radius reset](workshop.md#rva-0x021ba2e0) | Call the native geometry clear and radius reset | C |
| `0x021ba8a0` | `0x1421ba8a0` | [exit clears selected item set](population.md#rva-0x021ba8a0) | exit clears selected item set | C |
| `0x021ba960` | `0x1421ba960` | [statistics worker caller](production.md#rva-0x021ba960) | statistics worker caller | B |
| `0x021bab50` | `0x1421bab50` | [Definition to category map · entry](workshop.md#rva-0x021bab50) | Original report discusses this roster entry under Definition to category map. | C |
| `0x021bb3d0` | `0x1421bb3d0` | [Definition to category map · entry](workshop.md#rva-0x021bb3d0) | Original report discusses this roster entry under Definition to category map. | C |
| `0x021bb4a0` | `0x1421bb4a0` | [Handle the second preview timer crossing](workshop.md#rva-0x021bb4a0) | Handle the second preview timer crossing | C |
| `0x021bb570` | `0x1421bb570` | [FUN_1421bb570](workshop.md#rva-0x021bb570) | FUN_1421bb570 | C |
| `0x021bb860` | `0x1421bb860` | [clamp](workshop.md#rva-0x021bb860) | clamp | C |
| `0x021be130` | `0x1421be130` | [Dispatch the placement-state publisher](workshop.md#rva-0x021be130) | Dispatch the placement-state publisher | C |
| `0x021bfbb0` | `0x1421bfbb0` | [Manual user action to authoritative operation · entry](workshop.md#rva-0x021bfbb0) | Original report discusses this roster entry under Manual user action to authoritative operation. | C |
| `0x021c3bf0` | `0x1421c3bf0` | [UI valid target highlighting](inventory.md#rva-0x021c3bf0) | UI valid target highlighting | C |
| `0x021c45a0` | `0x1421c45a0` | [wire candidate highlighter](power.md#rva-0x021c45a0) | wire candidate highlighter | B |
| `0x021c6890` | `0x1421c6890` | [item set insertion and secondary maps](population.md#rva-0x021c6890) | item set insertion and secondary maps | C |
| `0x021c6b90` | `0x1421c6b90` | [item and reference map removal](population.md#rva-0x021c6b90) | item and reference map removal | C |
| `0x021c6d00` | `0x1421c6d00` | [rebuild member mappings](population.md#rva-0x021c6d00) | rebuild member mappings | C |
| `0x021c6e30` | `0x1421c6e30` | [remove member mappings](population.md#rva-0x021c6e30) | remove member mappings | C |
| `0x021c6f90` | `0x1421c6f90` | [selected-owner reverse 4D WorkshopItem registry rebuild](population.md#rva-0x021c6f90) | selected-owner reverse 4D WorkshopItem registry rebuild | C |
| `0x021c71b0` | `0x1421c71b0` | [resolve/deduplicate/qualify construction representatives](population.md#rva-0x021c71b0) | resolve/deduplicate/qualify construction representatives | C |
| `0x021c77b0` | `0x1421c77b0` | [erase item-set entry](population.md#rva-0x021c77b0) | erase item-set entry | C |
| `0x021c7990` | `0x1421c7990` | [set insertion helper](population.md#rva-0x021c7990) | set insertion helper | C |
| `0x021c8950` | `0x1421c8950` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x021c8950) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x021cb740` | `0x1421cb740` | [Workshop identity, construction and position native entry](workshop.md#rva-0x021cb740) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x021cbac0` | `0x1421cbac0` | [Workshop identity, construction and position native entry](workshop.md#rva-0x021cbac0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x021cbc20` | `0x1421cbc20` | [Display placement helper](inventory.md#rva-0x021cbc20) | Display placement helper | C |
| `0x021cbf40` | `0x1421cbf40` | [Run stock clearing checks for the assembly preview](inventory.md#rva-0x021cbf40) | Run stock clearing checks for the assembly preview | C |
| `0x021d0650` | `0x1421d0650` | [operation population range reset](geography.md#rva-0x021d0650) | operation population range reset | B |
| `0x021d5ce0` | `0x1421d5ce0` | [Refresh clearing during preview initialization](workshop.md#rva-0x021d5ce0) | Refresh clearing during preview initialization | C |
| `0x021d6100` | `0x1421d6100` | [Follow limited clearing candidates](workshop.md#rva-0x021d6100) | Follow limited clearing candidates | C |
| `0x021d64f0` | `0x1421d64f0` | [Nearby scenery clearing versus collision · entry](workshop.md#rva-0x021d64f0) | Original report discusses this roster entry under Nearby scenery clearing versus collision. | C |
| `0x021d69b0` | `0x1421d69b0` | [persistence · entry](workshop.md#rva-0x021d69b0) | Original report discusses this roster entry under persistence. | C |
| `0x021d6fd0` | `0x1421d6fd0` | [persistence · entry](workshop.md#rva-0x021d6fd0) | Original report discusses this roster entry under persistence. | C |
| `0x021d74b0` | `0x1421d74b0` | [Refresh candidate transforms and nearby clearing](workshop.md#rva-0x021d74b0) | Refresh candidate transforms and nearby clearing | C |
| `0x021d9230` | `0x1421d9230` | [New construction suppresses default stock · entry](inventory.md#rva-0x021d9230) | Original report discusses this roster entry under New construction suppresses default stock. | C |
| `0x021dcb10` | `0x1421dcb10` | [count>=nonnegative floor(global+48) at frame offset 61F](population.md#rva-0x021dcb10) | count>=nonnegative floor(global+48) at frame offset 61F | C |
| `0x021dd600` | `0x1421dd600` | [placement owner/actor/slot/event path](population.md#rva-0x021dd600) | placement owner/actor/slot/event path | C |
| `0x021de3f0` | `0x1421de3f0` | [invoke item virtual method at +A0 then placement notifications](population.md#rva-0x021de3f0) | invoke item virtual method at +A0 then placement notifications | C |
| `0x021de660` | `0x1421de660` | [deconstruction path](population.md#rva-0x021de660) | deconstruction path | C |
| `0x021e07d0` | `0x1421e07d0` | [Refresh Workshop area resource identities](geography.md#rva-0x021e07d0) | Reads resident ProcGen geometry into Workshop area lists when refresh predicates require it. | A |
| `0x021e0f50` | `0x1421e0f50` | [Filter a resident source's regions for Workshop](geography.md#rva-0x021e0f50) | Resolves resource keys and inserts qualifying Workshop area identities. | A |
| `0x021e1950` | `0x1421e1950` | [Charge operands and efficient evaluation · entry](workshop.md#rva-0x021e1950) | Original report discusses this roster entry under Charge operands and efficient evaluation. | C |
| `0x021e3880` | `0x1421e3880` | [Participate in conditional placement and context registration](workshop.md#rva-0x021e3880) | Participate in conditional placement and context registration | C |
| `0x021e3f50` | `0x1421e3f50` | [Ordinary outpost repair service](population.md#rva-0x021e3f50) | Ordinary outpost repair service | C |
| `0x021e48e0` | `0x1421e48e0` | [Dispatch immediate or queued item refresh](workshop.md#rva-0x021e48e0) | Dispatch immediate or queued item refresh | C |
| `0x021e7e20` | `0x1421e7e20` | [UI closest eligible target selection](inventory.md#rva-0x021e7e20) | UI closest eligible target selection | C |
| `0x021e9b50` | `0x1421e9b50` | [Repair service continuation](population.md#rva-0x021e9b50) | Repair service continuation | C |
| `0x021ea3a0` | `0x1421ea3a0` | [persistence · entry](workshop.md#rva-0x021ea3a0) | Original report discusses this roster entry under persistence. | C |
| `0x021ea490` | `0x1421ea490` | [Nearby scenery clearing versus collision · callback](workshop.md#rva-0x021ea490) | Original report discusses this roster entry under Nearby scenery clearing versus collision. | C |
| `0x021eab70` | `0x1421eab70` | [Check clearing at the proposed placement position](workshop.md#rva-0x021eab70) | Check clearing at the proposed placement position | C |
| `0x021eb180` | `0x1421eb180` | [nearest eligible wire target](power.md#rva-0x021eb180) | nearest eligible wire target | B |
| `0x021efb30` | `0x1421efb30` | [React to a PowerGenerated value change](power.md#rva-0x021efb30) | React to a PowerGenerated value change | C |
| `0x021eff10` | `0x1421eff10` | [Route reference power and open-close state changes](power.md#rva-0x021eff10) | Route reference power and open-close state changes | C |
| `0x021f01f0` | `0x1421f01f0` | [Route reference power and open-close state changes](power.md#rva-0x021f01f0) | Route reference power and open-close state changes | C |
| `0x021f0340` | `0x1421f0340` | [Workshop object-loaded event power entry](power.md#rva-0x021f0340) | Workshop object-loaded event power entry | B |
| `0x021f09a0` | `0x1421f09a0` | [Participate in variant discovery and validation](workshop.md#rva-0x021f09a0) | Participate in variant discovery and validation | C |
| `0x021f0b00` | `0x1421f0b00` | [Manual user action to authoritative operation · entry](workshop.md#rva-0x021f0b00) | Original report discusses this roster entry under Manual user action to authoritative operation. | C |
| `0x021f0e80` | `0x1421f0e80` | [Participate in variant discovery and validation](workshop.md#rva-0x021f0e80) | Participate in variant discovery and validation | C |
| `0x021f0fc0` | `0x1421f0fc0` | [Participate in variant discovery and validation](workshop.md#rva-0x021f0fc0) | Participate in variant discovery and validation | C |
| `0x021f1500` | `0x1421f1500` | [Manual user action to authoritative operation · entry](workshop.md#rva-0x021f1500) | Original report discusses this roster entry under Manual user action to authoritative operation. | C |
| `0x021f16b0` | `0x1421f16b0` | [Manual user action to authoritative operation · entry](workshop.md#rva-0x021f16b0) | Original report discusses this roster entry under Manual user action to authoritative operation. | C |
| `0x021f2680` | `0x1421f2680` | [power-summary aggregation boundary](production.md#rva-0x021f2680) | power-summary aggregation boundary | B |
| `0x021f2890` | `0x1421f2890` | [power callback field boundary](production.md#rva-0x021f2890) | power callback field boundary | B |
| `0x021f2ac0` | `0x1421f2ac0` | [Workshop statistics request sink](production.md#rva-0x021f2ac0) | Workshop statistics request sink | B |
| `0x021f2cb0` | `0x1421f2cb0` | [Workshop statistics cache updater](production.md#rva-0x021f2cb0) | Workshop statistics cache updater | B |
| `0x021f34d0` | `0x1421f34d0` | [cargo summary field boundary](production.md#rva-0x021f34d0) | cargo summary field boundary | B |
| `0x021f3690` | `0x1421f3690` | [Run aggregate power callback](power.md#rva-0x021f3690) | Run aggregate power callback | C |
| `0x021f36b0` | `0x1421f36b0` | [nominal producer rate aggregate](production.md#rva-0x021f36b0) | nominal producer rate aggregate | B |
| `0x021f4310` | `0x1421f4310` | [Provider and compiled consumer · entry](workshop.md#rva-0x021f4310) | Original report discusses this roster entry under Provider and compiled consumer. | C |
| `0x021f4ed0` | `0x1421f4ed0` | [Definition to category map · entry](workshop.md#rva-0x021f4ed0) | Original report discusses this roster entry under Definition to category map. | C |
| `0x021f4f30` | `0x1421f4f30` | [Queue the manual snap behavior change](workshop.md#rva-0x021f4f30) | Queue the manual snap behavior change | C |
| `0x021f6420` | `0x1421f6420` | [Preview spinner request](interfaces.md#rva-0x021f6420) | Preview spinner request | C |
| `0x021f66c0` | `0x1421f66c0` | [Evaluate the configured availability nodes](inventory.md#rva-0x021f66c0) | Evaluate the configured availability nodes | C |
| `0x021f68f0` | `0x1421f68f0` | [Gate a selected harvester resource](geography.md#rva-0x021f68f0) | Reads population data for the selected harvester's resource predicate. | B |
| `0x021f6bd0` | `0x1421f6bd0` | [Positive mechanisms and controls · entry](workshop.md#rva-0x021f6bd0) | Original report discusses this roster entry under Positive mechanisms and controls. | C |
| `0x021f6dc0` | `0x1421f6dc0` | [Check category-level entry eligibility](geography.md#rva-0x021f6dc0) | Check category-level entry eligibility | C |
| `0x021f6e40` | `0x1421f6e40` | [Supply qualifying tab categories](workshop.md#rva-0x021f6e40) | Supply qualifying tab categories | C |
| `0x021f6f00` | `0x1421f6f00` | [Evaluate the paired configured node path](inventory.md#rva-0x021f6f00) | Evaluate the paired configured node path | C |
| `0x021f8120` | `0x1421f8120` | [common pointer union](geography.md#rva-0x021f8120) | common pointer union | B |
| `0x022c7ad0` | `0x1422c7ad0` | [Evidence checkpoints · entry](geography.md#rva-0x022c7ad0) | Original report discusses this roster entry under Evidence checkpoints. | C |
| `0x022c8200` | `0x1422c8200` | [Evidence checkpoints · entry](geography.md#rva-0x022c8200) | Original report discusses this roster entry under Evidence checkpoints. | C |
| `0x022c8d10` | `0x1422c8d10` | [Acquire the Grid source deduplication lock](geography.md#rva-0x022c8d10) | Acquire the Grid source deduplication lock | C |
| `0x022cba00` | `0x1422cba00` | [Dynamic vector growth frees old backing storage before pointer publication.](geography.md#rva-0x022cba00) | Dynamic vector growth frees old backing storage before pointer publication. | C |
| `0x022cc0d0` | `0x1422cc0d0` | [Reserve storage in the mapped native array path](geography.md#rva-0x022cc0d0) | Provides reserve behavior used by the provider before its visited append. | B |
| `0x022cc350` | `0x1422cc350` | [Acquire shared owner-wide lock](geography.md#rva-0x022cc350) | Acquire shared owner-wide lock | C |
| `0x022cc3d0` | `0x1422cc3d0` | [Acquire exclusive owner-wide lock](geography.md#rva-0x022cc3d0) | Acquire exclusive owner-wide lock | C |
| `0x022ccd40` | `0x1422ccd40` | [frame scale update](production.md#rva-0x022ccd40) | frame scale update | B |
| `0x022cce10` | `0x1422cce10` | [engine frame seconds update](production.md#rva-0x022cce10) | engine frame seconds update | B |
| `0x022cd0c0` | `0x1422cd0c0` | [nested time freeze leave](production.md#rva-0x022cd0c0) | nested time freeze leave | B |
| `0x022cd140` | `0x1422cd140` | [nested time freeze enter](production.md#rva-0x022cd140) | nested time freeze enter | B |
| `0x022cf120` | `0x1422cf120` | [Concrete worker and publication order · entry](geography.md#rva-0x022cf120) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x022cf230` | `0x1422cf230` | [Concrete worker and publication order · entry](geography.md#rva-0x022cf230) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x0231d000` | `0x14231d000` | [Register planetary overlay component type](workshop.md#rva-0x0231d000) | Register planetary overlay component type | C |
| `0x0231da10` | `0x14231da10` | [Participate in resource component registration](geography.md#rva-0x0231da10) | Participate in resource component registration | C |
| `0x0231de80` | `0x14231de80` | [Read existing typed components for reconstruction](geography.md#rva-0x0231de80) | Read existing typed components for reconstruction | C |
| `0x0231f860` | `0x14231f860` | [Validate the containing root body](interfaces.md#rva-0x0231f860) | Validate the containing root body | C |
| `0x023204d0` | `0x1423204d0` | [Locate typed planetary overlay component factory](workshop.md#rva-0x023204d0) | Locate typed planetary overlay component factory | C |
| `0x02322520` | `0x142322520` | [Positive typed alternatives · entry](geography.md#rva-0x02322520) | Original report discusses this roster entry under Positive typed alternatives. | C |
| `0x023321f0` | `0x1423321f0` | [Geography and resource generation native entry](geography.md#rva-0x023321f0) | Located member of an original operation group. Individual role remains unqualified. | C |
| `0x02332410` | `0x142332410` | [Chart query projects to geographic binary64 values with explicit horizontal binary32 stage.](geography.md#rva-0x02332410) | Chart query projects to geographic binary64 values with explicit horizontal binary32 stage. | C |
| `0x02332d90` | `0x142332d90` | [Resolve a planet owner through system and body index](geography.md#rva-0x02332d90) | Resolve a planet owner through system and body index | C |
| `0x02332ea0` | `0x142332ea0` | [Persistent identity and reconstruction · entry](workshop.md#rva-0x02332ea0) | Original report discusses this roster entry under Persistent identity and reconstruction. | C |
| `0x02332f70` | `0x142332f70` | [Retrieve the body-keyed name component](geography.md#rva-0x02332f70) | Retrieve the body-keyed name component | C |
| `0x02333000` | `0x142333000` | [Retrieve the body-keyed name component](geography.md#rva-0x02333000) | Retrieve the body-keyed name component | C |
| `0x02333270` | `0x142333270` | [Read body size component data for the display path](interfaces.md#rva-0x02333270) | Read body size component data for the display path | C |
| `0x02334600` | `0x142334600` | [Calculate system displacement for link distance](inventory.md#rva-0x02334600) | Calculate system displacement for link distance | C |
| `0x023353a0` | `0x1423353a0` | [Match the indexed body and obtain its owner ID](geography.md#rva-0x023353a0) | Match the indexed body and obtain its owner ID | C |
| `0x023390f0` | `0x1423390f0` | [nearest raster row-major index](geography.md#rva-0x023390f0) | nearest raster row-major index | C |
| `0x023391d0` | `0x1423391d0` | [Convert chart inputs in the biome sampling path](geography.md#rva-0x023391d0) | Convert chart inputs in the biome sampling path | C |
| `0x02339250` | `0x142339250` | [Convert angular inputs in the biome sampling path](geography.md#rva-0x02339250) | Convert angular inputs in the biome sampling path | C |
| `0x02339340` | `0x142339340` | [map mask nibble lookup](geography.md#rva-0x02339340) | map mask nibble lookup | C |
| `0x02346a60` | `0x142346a60` | [Inorganic relationships · entry](geography.md#rva-0x02346a60) | Original report discusses this roster entry under Inorganic relationships. | C |
| `0x02346b30` | `0x142346b30` | [Test candidate XY against a resident region](geography.md#rva-0x02346b30) | Test candidate XY against a resident region | C |
| `0x02346f80` | `0x142346f80` | [Interpolate a binary32 range from one MT draw](geography.md#rva-0x02346f80) | Interpolate a binary32 range from one MT draw | C |
| `0x023ff430` | `0x1423ff430` | [Save name and serialization command helper](interfaces.md#rva-0x023ff430) | Save name and serialization command helper | C |
| `0x023ff640` | `0x1423ff640` | [Obtain manager context for candidate resource reads](production.md#rva-0x023ff640) | Obtain manager context for candidate resource reads | C |
| `0x02403520` | `0x142403520` | [Expose the body-name component type](geography.md#rva-0x02403520) | Expose the body-name component type | C |
| `0x02404230` | `0x142404230` | [Read storage phase consistency](geography.md#rva-0x02404230) | Read storage phase consistency | C |
| `0x02404ef0` | `0x142404ef0` | [Store optional metadata for a geometric candidate](workshop.md#rva-0x02404ef0) | Store optional metadata for a geometric candidate | C |
| `0x02406db0` | `0x142406db0` | [Content-request type correction and factory consumers (exports 29–32) · entry](workshop.md#rva-0x02406db0) | Original report discusses this roster entry under Content-request type correction and factory consumers (exports 29–32). | C |
| `0x02406e90` | `0x142406e90` | [Content-request type correction and factory consumers (exports 29–32) · entry](workshop.md#rva-0x02406e90) | Original report discusses this roster entry under Content-request type correction and factory consumers (exports 29–32). | C |
| `0x02407350` | `0x142407350` | [Native dependency order · entry](geography.md#rva-0x02407350) | Original report discusses this roster entry under Native dependency order. | C |
| `0x02412d60` | `0x142412d60` | [Content-request type correction and factory consumers (exports 29–32) · entry](workshop.md#rva-0x02412d60) | Original report discusses this roster entry under Content-request type correction and factory consumers (exports 29–32). | C |
| `0x02413270` | `0x142413270` | [Native dependency order · entry](geography.md#rva-0x02413270) | Original report discusses this roster entry under Native dependency order. | C |
| `0x02417130` | `0x142417130` | [Execute the queued component command callback](geography.md#rva-0x02417130) | Execute the queued component command callback | C |
| `0x0241e7f0` | `0x14241e7f0` | [Preview readiness test](interfaces.md#rva-0x0241e7f0) | Preview readiness test | C |
| `0x02426480` | `0x142426480` | [Checkpoint: common ingress, native keys and dispatcher counterexample · entry](geography.md#rva-0x02426480) | Original report discusses this roster entry under Checkpoint: common ingress, native keys and dispatcher counterexample. | C |
| `0x024cb7d0` | `0x1424cb7d0` | [Manipulate a reflected component collection](workshop.md#rva-0x024cb7d0) | Manipulate a reflected component collection | C |
| `0x024d39c0` | `0x1424d39c0` | [Manipulate a reflected component collection](workshop.md#rva-0x024d39c0) | Manipulate a reflected component collection | C |
| `0x02682e60` | `0x142682e60` | [Participate in transit path geometry modification](inventory.md#rva-0x02682e60) | Participate in transit path geometry modification | C |
| `0x026830e0` | `0x1426830e0` | [Participate in transit line-of-sight modification](inventory.md#rva-0x026830e0) | Participate in transit line-of-sight modification | C |
| `0x02685190` | `0x142685190` | [Receive the transit path modification route](inventory.md#rva-0x02685190) | Receive the transit path modification route | C |
| `0x02707520` | `0x142707520` | [Elapsed producer and staged consumers · entry](inventory.md#rva-0x02707520) | Original report discusses this roster entry under Elapsed producer and staged consumers. | C |
| `0x02707540` | `0x142707540` | [Elapsed producer and staged consumers · entry](inventory.md#rva-0x02707540) | Original report discusses this roster entry under Elapsed producer and staged consumers. | C |
| `0x027076d0` | `0x1427076d0` | [Invoke the detached-stage agent update interface](inventory.md#rva-0x027076d0) | Invoke the detached-stage agent update interface | C |
| `0x02708c90` | `0x142708c90` | [Concrete completion provider and detached movement · entry](inventory.md#rva-0x02708c90) | Original report discusses this roster entry under Concrete completion provider and detached movement. | C |
| `0x027091d0` | `0x1427091d0` | [Concrete completion provider and detached movement · entry](inventory.md#rva-0x027091d0) | Original report discusses this roster entry under Concrete completion provider and detached movement. | C |
| `0x0271e190` | `0x14271e190` | [Advance full flight motion for the supplied elapsed time](inventory.md#rva-0x0271e190) | Uses nested elapsed context in physical path-following work. | B |
| `0x0271fd10` | `0x14271fd10` | [Compute transit steering and avoidance corrections](inventory.md#rva-0x0271fd10) | Compute transit steering and avoidance corrections | C |
| `0x027216f0` | `0x1427216f0` | [Full flight: geometry, movement profiles and actions · entry](inventory.md#rva-0x027216f0) | Original report discusses this roster entry under Full flight: geometry, movement profiles and actions. | C |
| `0x02723220` | `0x142723220` | [Full flight: geometry, movement profiles and actions · constructor](inventory.md#rva-0x02723220) | Original report discusses this roster entry under Full flight: geometry, movement profiles and actions. | C |
| `0x02731f50` | `0x142731f50` | [Update the detached flight elapsed accumulator](inventory.md#rva-0x02731f50) | Consumes the supplied elapsed scalar on the detached movement route. | B |
| `0x027321d0` | `0x1427321d0` | [Accept and retain a flight path](inventory.md#rva-0x027321d0) | Accept and retain a flight path | C |
| `0x02732280` | `0x142732280` | [Preserved failures and corrections · entry](inventory.md#rva-0x02732280) | Original report discusses this roster entry under Preserved failures and corrections. | C |
| `0x02732320` | `0x142732320` | [Detached path: thresholded completion · entry](inventory.md#rva-0x02732320) | Original report discusses this roster entry under Detached path: thresholded completion. | C |
| `0x027327f0` | `0x1427327f0` | [Concrete completion provider and detached movement · constructor](inventory.md#rva-0x027327f0) | Original report discusses this roster entry under Concrete completion provider and detached movement. | C |
| `0x027342e0` | `0x1427342e0` | [Dispatch elapsed context to active movement arbiters](inventory.md#rva-0x027342e0) | Stores the actual frame delta and calls each admitted arbiter update. | B |
| `0x02738c60` | `0x142738c60` | [Movement selection and admission · entry](inventory.md#rva-0x02738c60) | Original report discusses this roster entry under Movement selection and admission. | C |
| `0x02738d90` | `0x142738d90` | [Rebuild the selected travel mode state](inventory.md#rva-0x02738d90) | Rebuild the selected travel mode state | C |
| `0x02738ef0` | `0x142738ef0` | [Movement selection and admission · entry](inventory.md#rva-0x02738ef0) | Original report discusses this roster entry under Movement selection and admission. | C |
| `0x027bdbd0` | `0x1427bdbd0` | [Read the reflection class schema](geography.md#rva-0x027bdbd0) | Read the reflection class schema | C |
| `0x027be8e0` | `0x1427be8e0` | [Dispatch reflected DIFF data](geography.md#rva-0x027be8e0) | Dispatch reflected DIFF data | C |
| `0x027becd0` | `0x1427becd0` | [Read the reflected DIFF root value](geography.md#rva-0x027becd0) | Read the reflected DIFF root value | C |
| `0x027c2f90` | `0x1427c2f90` | [Read the reflected LIST count](geography.md#rva-0x027c2f90) | Read the reflected LIST count | C |
| `0x027c5c70` | `0x1427c5c70` | [Read the reflected enum operand](geography.md#rva-0x027c5c70) | Read the reflected enum operand | C |
| `0x027d42c0` | `0x1427d42c0` | [Acquire the fresh CellRefDB entry](geography.md#rva-0x027d42c0) | Acquire the fresh CellRefDB entry | C |
| `0x027d4ae0` | `0x1427d4ae0` | [database entry state request](geography.md#rva-0x027d4ae0) | database entry state request | B |
| `0x027d4be0` | `0x1427d4be0` | [database entry state acquisition/wait](geography.md#rva-0x027d4be0) | database entry state acquisition/wait | B |
| `0x027e4950` | `0x1427e4950` | [Insert ready resource task](geography.md#rva-0x027e4950) | Insert ready resource task | C |
| `0x027e49a0` | `0x1427e49a0` | [Rekey resource ready task](geography.md#rva-0x027e49a0) | Rekey resource ready task | C |
| `0x027e4ab0` | `0x1427e4ab0` | [Destroy the completed task record](geography.md#rva-0x027e4ab0) | Destroy the completed task record | C |
| `0x027e5630` | `0x1427e5630` | [Producer to provider · entry](geography.md#rva-0x027e5630) | Original report discusses this roster entry under Producer to provider. | C |
| `0x027e56d0` | `0x1427e56d0` | [Dispatch ready mode-two task](geography.md#rva-0x027e56d0) | Dispatch ready mode-two task | C |
| `0x027e5880` | `0x1427e5880` | [Invoke admitted work node](geography.md#rva-0x027e5880) | Invoke admitted work node | C |
| `0x027e5a00` | `0x1427e5a00` | [Publish native task completion](geography.md#rva-0x027e5a00) | Posts a TargetBatchPage command for the completion path. | B |
| `0x027e5e80` | `0x1427e5e80` | [Remove task dependency edges after completion](geography.md#rva-0x027e5e80) | Applies dependency-category-specific removal and last-edge evaluation. | B |
| `0x027e6330` | `0x1427e6330` | [Dependency completion and effective ordering · entry](geography.md#rva-0x027e6330) | Original report discusses this roster entry under Dependency completion and effective ordering. | C |
| `0x027e6770` | `0x1427e6770` | [Preparation and the two service pumps · entry](geography.md#rva-0x027e6770) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x027e6830` | `0x1427e6830` | [Conditional graph and discriminating counterfactuals · entry](geography.md#rva-0x027e6830) | Original report discusses this roster entry under Conditional graph and discriminating counterfactuals. | C |
| `0x027e6a00` | `0x1427e6a00` | [Ordinary entry and eligible density task · entry](geography.md#rva-0x027e6a00) | Original report discusses this roster entry under Ordinary entry and eligible density task. | C |
| `0x027e6b90` | `0x1427e6b90` | [Propagate resource node rank](geography.md#rva-0x027e6b90) | Propagate resource node rank | C |
| `0x027e6c00` | `0x1427e6c00` | [Preparation and the two service pumps · entry](geography.md#rva-0x027e6c00) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x027e6d10` | `0x1427e6d10` | [Scan the ready task tree before dispatch](geography.md#rva-0x027e6d10) | Passes eligible ready work to 0x1427e6a00 and 0x1427e56d0. | B |
| `0x027e6f40` | `0x1427e6f40` | [Add node dependency](geography.md#rva-0x027e6f40) | Add node dependency | C |
| `0x027e70e0` | `0x1427e70e0` | [Commit resource dependency work](geography.md#rva-0x027e70e0) | Commit resource dependency work | C |
| `0x027e7180` | `0x1427e7180` | [Dependency completion and effective ordering · entry](geography.md#rva-0x027e7180) | Original report discusses this roster entry under Dependency completion and effective ordering. | C |
| `0x027e7720` | `0x1427e7720` | [Checkpoint: completion callbacks and the preparation antecedent · entry](geography.md#rva-0x027e7720) | Original report discusses this roster entry under Checkpoint: completion callbacks and the preparation antecedent. | C |
| `0x027eaf50` | `0x1427eaf50` | [Producer to provider · entry](geography.md#rva-0x027eaf50) | Original report discusses this roster entry under Producer to provider. | C |
| `0x027eb6b0` | `0x1427eb6b0` | [Route queued work to worker pool](geography.md#rva-0x027eb6b0) | Route queued work to worker pool | C |
| `0x027ec100` | `0x1427ec100` | [Demand prefix, admitted pair and historical invocation state · entry](geography.md#rva-0x027ec100) | Original report discusses this roster entry under Demand prefix, admitted pair and historical invocation state. | C |
| `0x027ec2e0` | `0x1427ec2e0` | [Dispatch worker callback](geography.md#rva-0x027ec2e0) | Dispatch worker callback | C |
| `0x027edc20` | `0x1427edc20` | [Dependency completion and effective ordering · entry](geography.md#rva-0x027edc20) | Original report discusses this roster entry under Dependency completion and effective ordering. | C |
| `0x027eecc0` | `0x1427eecc0` | [Dependency completion and effective ordering · entry](geography.md#rva-0x027eecc0) | Original report discusses this roster entry under Dependency completion and effective ordering. | C |
| `0x027eecf0` | `0x1427eecf0` | [Dispatch published task completion to edge removal](geography.md#rva-0x027eecf0) | Routes the published TargetBatchPage command to 0x1427e5e80. | B |
| `0x027eedb0` | `0x1427eedb0` | [Construct the ProcGen Resources JobSite](geography.md#rva-0x027eedb0) | Construct the ProcGen Resources JobSite | C |
| `0x027eef10` | `0x1427eef10` | [Wait for generation job site](geography.md#rva-0x027eef10) | Wait for generation job site | C |
| `0x027fcc10` | `0x1427fcc10` | [snapshot handle-keyed script list](population.md#rva-0x027fcc10) | snapshot handle-keyed script list | C |
| `0x027fd870` | `0x1427fd870` | [install handle-keyed script list; shared VMAD setter](population.md#rva-0x027fd870) | install handle-keyed script list; shared VMAD setter | C |
| `0x027ff160` | `0x1427ff160` | [VMAD parser feeds script-list setter](population.md#rva-0x027ff160) | VMAD parser feeds script-list setter | C |
| `0x028caea0` | `0x1428caea0` | [Release the captured allocation identity](geography.md#rva-0x028caea0) | Release the captured allocation identity | C |
| `0x028ccc40` | `0x1428ccc40` | [manager handle generation and index resolution](power.md#rva-0x028ccc40) | manager handle generation and index resolution | B |
| `0x028cce50` | `0x1428cce50` | [Receive the unresolved-owner reference-manager operation](power.md#rva-0x028cce50) | Receive the unresolved-owner reference-manager operation | C |
| `0x028cd500` | `0x1428cd500` | [Classify the setting's name-derived type](geography.md#rva-0x028cd500) | Classify the setting's name-derived type | C |
| `0x028d1420` | `0x1428d1420` | [Concrete worker and publication order · entry](geography.md#rva-0x028d1420) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x028d1450` | `0x1428d1450` | [Concrete worker and publication order · entry](geography.md#rva-0x028d1450) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x028d1550` | `0x1428d1550` | [Concrete worker and publication order · entry](geography.md#rva-0x028d1550) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x028d1650` | `0x1428d1650` | [Construct the Jobs2Adaptor and embedded pool](geography.md#rva-0x028d1650) | Construct the Jobs2Adaptor and embedded pool | C |
| `0x028d1880` | `0x1428d1880` | [Get bound resource job site](geography.md#rva-0x028d1880) | Get bound resource job site | C |
| `0x028d2b80` | `0x1428d2b80` | [Publish work to worker ring](geography.md#rva-0x028d2b80) | Publish work to worker ring | C |
| `0x028d2e80` | `0x1428d2e80` | [TerrainDB is a real scheduling and context-lifetime dependency · entry](geography.md#rva-0x028d2e80) | Original report discusses this roster entry under TerrainDB is a real scheduling and context-lifetime dependency. | C |
| `0x028d2f90` | `0x1428d2f90` | [Concrete worker and publication order · entry](geography.md#rva-0x028d2f90) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x028d2fc0` | `0x1428d2fc0` | [Initialize the embedded pool's worker context state](geography.md#rva-0x028d2fc0) | Initialize the embedded pool's worker context state | C |
| `0x028d33f0` | `0x1428d33f0` | [Concrete worker and publication order · constructor](geography.md#rva-0x028d33f0) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x028d3530` | `0x1428d3530` | [Prepare the embedded pool's worker context allocation](geography.md#rva-0x028d3530) | Prepare the embedded pool's worker context allocation | C |
| `0x028d37a0` | `0x1428d37a0` | [Concrete worker and publication order · entry](geography.md#rva-0x028d37a0) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x028d3960` | `0x1428d3960` | [Claim pending worker task](geography.md#rva-0x028d3960) | Claim pending worker task | C |
| `0x028d3b90` | `0x1428d3b90` | [Invoke queued resource worker callback](geography.md#rva-0x028d3b90) | Invoke queued resource worker callback | C |
| `0x028d4540` | `0x1428d4540` | [TerrainDB is a real scheduling and context-lifetime dependency · entry](geography.md#rva-0x028d4540) | Original report discusses this roster entry under TerrainDB is a real scheduling and context-lifetime dependency. | C |
| `0x028d79b0` | `0x1428d79b0` | [Concrete worker and publication order · entry](geography.md#rva-0x028d79b0) | Original report discusses this roster entry under Concrete worker and publication order. | C |
| `0x028d7b60` | `0x1428d7b60` | [Preparation and the two service pumps · entry](geography.md#rva-0x028d7b60) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x028d7bd0` | `0x1428d7bd0` | [Preparation and the two service pumps · entry](geography.md#rva-0x028d7bd0) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x028d7f40` | `0x1428d7f40` | [Preparation and the two service pumps · entry](geography.md#rva-0x028d7f40) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x028d8060` | `0x1428d8060` | [Receive queued resource service work](geography.md#rva-0x028d8060) | Receive queued resource service work | C |
| `0x028d86c0` | `0x1428d86c0` | [Preparation and the two service pumps · entry](geography.md#rva-0x028d86c0) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x028d89b0` | `0x1428d89b0` | [Pump resource worker service](geography.md#rva-0x028d89b0) | Pump resource worker service | C |
| `0x028d8fe0` | `0x1428d8fe0` | [Checkpoint: service-pump binding and retirement qualification · entry](geography.md#rva-0x028d8fe0) | Original report discusses this roster entry under Checkpoint: service-pump binding and retirement qualification. | C |
| `0x028d9560` | `0x1428d9560` | [Enter the queued JobSite pump](geography.md#rva-0x028d9560) | Enter the queued JobSite pump | C |
| `0x028d9600` | `0x1428d9600` | [Preparation and the two service pumps · entry](geography.md#rva-0x028d9600) | Original report discusses this roster entry under Preparation and the two service pumps. | C |
| `0x028d96c0` | `0x1428d96c0` | [Wake resource worker service](geography.md#rva-0x028d96c0) | Wake resource worker service | C |
| `0x02be45c0` | `0x142be45c0` | [Project system positions into Locations display coordinates](interfaces.md#rva-0x02be45c0) | Project system positions into Locations display coordinates | C |
| `0x02bf4850` | `0x142bf4850` | [Compute region center and radius](geography.md#rva-0x02bf4850) | Compute region center and radius | C |
| `0x0341c0a0` | `0x14341c0a0` | [Existing xrefs to both coordinate names at 0x14341c207/251](workshop.md#rva-0x0341c0a0) | Existing xrefs to both coordinate names at 0x14341c207/251 | C |
| `0x0374dcc0` | `0x14374dcc0` | [Dispatch the native SIMD angular helper by CPU state](workshop.md#rva-0x0374dcc0) | Dispatch the native SIMD angular helper by CPU state | C |
| `0x0374dcd2` | `0x14374dcd2` | [Original query to ordinary mask · wrapper](geography.md#rva-0x0374dcd2) | Original report discusses this roster entry under Original query to ordinary mask. | C |
| `0x0374dda0` | `0x14374dda0` | [Original query to ordinary mask · entry](geography.md#rva-0x0374dda0) | Original report discusses this roster entry under Original query to ordinary mask. | C |
| `0x0374e650` | `0x14374e650` | [Execute the qualified FMA angular path](geography.md#rva-0x0374e650) | Execute the qualified FMA angular path | C |
| `0x0388f200` | `0x14388f200` | [Forward SFTR name-registry shutdown](interfaces.md#rva-0x0388f200) | Computes the registry subobject and jumps to the clear routine. | B |
| `0x038b5f40` | `0x1438b5f40` | [Destroy the scoped setting on exit](geography.md#rva-0x038b5f40) | Destroy the scoped setting on exit | C |
