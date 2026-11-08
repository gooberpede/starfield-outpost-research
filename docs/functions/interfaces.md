# UI, save framing and lifecycle

[Subject navigation and ABI limits](README.md) · [RVA index](index.md)

Entries use the pinned `Starfield.exe` 1.16.244.0 image. Internal-only observation. External invocation remains unvalidated.

Follow a mapped path

- [Locations adapter](interfaces.md#rva-0x01360e80)
- [Queued Locations receiver](interfaces.md#rva-0x01361c10)
- [Extra33 reader](interfaces.md#rva-0x00404a10)
- [Extra33 writer](interfaces.md#rva-0x00404cf0)
- [Native save payload](interfaces.md#rva-0x01814220)
- [SFTR factory lookup](interfaces.md#rva-0x004628b0)
- [SFTR name registration](interfaces.md#rva-0x004613d0)
- [SFTR shutdown thunk](interfaces.md#rva-0x0388f200)
- [Type-7 PCM writer](interfaces.md#rva-0x018b1eb0)
- [Type-7 PCM reader](interfaces.md#rva-0x018b22c0)

## RVA 0x000255c0

**Initialize the easy StarMap level threshold** · Level C · preferred VA `0x1400255c0`

Analysis labels recorded in the original sources are `FUN_1400255c0`.

Recorded scope — Initialize the easy StarMap level threshold

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 158)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 134)

## RVA 0x001366a0

**Initialize the Freestar faction default object** · Level C · preferred VA `0x1401366a0`

Analysis labels recorded in the original sources are `FUN_1401366a0`.

Recorded scope — Initialize the Freestar faction default object

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 150)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 157)

## RVA 0x001595f0

**Construct the outpost panel exclusion default object** · Level C · preferred VA `0x1401595f0`

Analysis labels recorded in the original sources are `FUN_1401595f0`.

Recorded scope — Construct the outpost panel exclusion default object

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 33)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 139)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 158)

## RVA 0x002b9480

**Resolve the location link field in fixup** · Level C · preferred VA `0x1402b9480`

Analysis labels recorded in the original sources are `FUN_1402b9480`.

Recorded scope — Resolve the location link field in fixup

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 140)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 159)

## RVA 0x002cb870

**Find an interned name in the SFTR factory map** · Level B · preferred VA `0x1402cb870`

Looks up the exact name through the matching key and hash namespace.

The lookup uses the interned character pointer and interned-object key. It shares the key namespace with 0x1402d26d0, while the type-number registry follows a different route. A failed name lookup does not qualify other registry namespaces.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 280)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 281)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 283)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 92) · `D5AD-SV91`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 92) · `D5AD-SV91` · Name hash-map lookup

## RVA 0x002cb9f0

**Release keys and clear the name registry** · Level B · preferred VA `0x1402cb9f0`

Clears backing storage on the mapped shutdown path.

The known shutdown caller is the forwarding stub at 0x14388f200. The target releases keys and clears backing storage. The original direct-graph trace found no factory insertion in this path. The function remains distinct from the forwarding stub.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 287)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 288)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 289)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 290)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 150) · `D5AD-SV149`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 150) · `D5AD-SV149` · Name-registry shutdown target releases keys and clears backing storage without insertion

## RVA 0x002cedd0

**UI, save framing and lifecycle native entry** · Level C · preferred VA `0x1402cedd0`

Recorded scope — Located member of an original operation group. Individual role remains unqualified.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 112) · `SOR-FN-0049`
  Original group scope — Workshop resource-prefix loading path

## RVA 0x002d26d0

**Insert an interned name and factory in the map** · Level B · preferred VA `0x1402d26d0`

Hashes and compares the name in the exact-name namespace.

The mapped insertion hashes the interned character pointer and compares the same interned-object key used by 0x1402cb870. Registration stores the supplied key and factory. Full map layout and safe mutation prerequisites remain open.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 280)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 281)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 282)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 124) · `D5AD-SV123`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 124) · `D5AD-SV123` · Interned name-map insertion hash/equality namespace

## RVA 0x002d66a0

**Set the StarMap level thresholds** · Level C · preferred VA `0x1402d66a0`

Analysis labels recorded in the original sources are `FUN_1402d66a0`.

Recorded scope — Set the StarMap level thresholds

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 159)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 138)

## RVA 0x00404a10

**Read the Extra33 mod-instance list** · Level B · preferred VA `0x140404a10`

Analysis labels recorded in the original sources are `FUN_140404a10`.

Reads a mod-instance list from ExtraData loader case 0x33.

The case dispatch reaches this reader and `0x140406e80`/`0x1418650d0`. The qualified Save52 sample reconciles two queued identities, optional-field masks and the following ExtraData boundary. Full flag coverage, declaration and return remain unknown.

Original records

- [configuration ui · save52](../experiments/cargo-links/configuration-ui/save52.md) (line 56)
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 59)
- [configuration ui · save52](../experiments/cargo-links/configuration-ui/save52.md) (line 60)
  Original report discusses this roster entry under Specific ship representation gap resolved.

## RVA 0x00404cf0

**Write the Extra33 mod-instance list** · Level B · preferred VA `0x140404cf0`

Analysis labels recorded in the original sources are `FUN_140404cf0`.

Writes the mod-instance list selected by ExtraData writer case 0x33.

The paired writer and reader corroborate list framing with optional fields and queued identity operands. In the examined Save52 case, flag `0x02` leads to a compact count of two and zero three-bit masks. That witnesses two queued identities with no optional per-mod bytes for this case. Other flags and the complete writer ABI remain unknown.

Original records

- [configuration ui · save52](../experiments/cargo-links/configuration-ui/save52.md) (line 56)
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 73)
- [configuration ui · save52](../experiments/cargo-links/configuration-ui/save52.md) (line 62)
  Original report discusses this roster entry under Specific ship representation gap resolved.
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 111)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 40)

## RVA 0x004613d0

**Register an SFTR factory by interned name** · Level B · preferred VA `0x1404613d0`

Stores a name key and supplied factory in the name registry.

The inspected registration obtains the registry through 0x1404639f0 and inserts through 0x1402d26d0. The direct-caller census distinguishes insertion from consumers that only obtain and operate a factory. Arbitrary indirect installation and runtime registry contents remain outside that census.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 279)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 280)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 282)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 286)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 94) · `D5AD-SV93`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 94) · `D5AD-SV93` · Name-factory registration and complete direct-call XREFs

## RVA 0x00461f10

**Look up the current body-name component** · Level C · preferred VA `0x140461f10`

Analysis labels recorded in the original sources are `FUN_140461f10`.

Recorded scope — Look up the current body-name component

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 96)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 63)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 96)

## RVA 0x004628b0

**Look up an SFTR factory by interned name** · Level B · preferred VA `0x1404628b0`

Returns a matching factory or null in the qualified lookup.

The mapped loader uses the same name registry that registration populates. It obtains the registry through 0x1404639f0 and reaches 0x1402cb870. The distinct type-number registry does not substitute for this exact-name lookup. The full ABI remains unqualified.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 278)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 279)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 283)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 90) · `D5AD-SV89`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 90) · `D5AD-SV89` · Exact interned-name map lookup null or factory

## RVA 0x004639f0

**Obtain the SFTR name-factory registry** · Level B · preferred VA `0x1404639f0`

Supplies the shared registry to registration and loader lookup.

The pinned registry is at preferred static VA 0x14620e240. Its mapped lifecycle distinguishes initialization, registration, lookup and shutdown. A registry address does not establish which factories are present at a particular point in load.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 279)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 280)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 285)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 287)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 91) · `D5AD-SV90`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 91) · `D5AD-SV90` · Initially empty name-factory registry

## RVA 0x00463ed0

**Dispatch a component block by exact name** · Level B · preferred VA `0x140463ed0`

Routes the named component lookup into the factory registry.

The SFTR BFCB path reaches 0x1404628b0 through this dispatch. An unresolved factory name can prevent a component loader from being selected. The full native declaration and indirect registry mutation are unqualified.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 39)

## RVA 0x0047fce0

**Workshop keyword recognition** · Level C · preferred VA `0x14047fce0`

Analysis labels recorded in the original sources are `FUN_14047fce0`.

Recorded scope — Workshop keyword recognition

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 7) · `n028`
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 148)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 213)

## RVA 0x0051ea30

**Serialize typed ExtraData cases** · Level A · preferred VA `0x14051ea30`

Analysis labels recorded in the original sources are `FUN_14051ea30`.

Dispatches type-specific saved framing for native ExtraData lists.

The saver emits linked-list order and uses a type bitset. On mapped E2 it prunes unresolved handles via `0x14040a0d0`, writes a compact count through `0x141868770`, and emits resolving actor FormIDs through saved-identity encoder `0x140306db0`. Case `0x33` calls mod-list writer `0x140404cf0`. Case `0x81` copies the cached pair with its identifiers. These are scoped case descriptions. A runtime handle, a compact saved identity and a physical file offset are separate domains. Outer change/presence flags and type-dependent layouts govern whether these bytes are written. Full dispatch and declaration remain unknown.

Original records

- [configuration ui · save52](../experiments/cargo-links/configuration-ui/save52.md) (line 58)
- [crew · current assignments](../experiments/crew/current-assignments.md) (line 110)
- [power · saved](../experiments/power/saved.md) (line 140) · Serialize typed reference extra data
  Case CB emits count and each FormID/word entry; other extra cases have separate formats.
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 48)
- [workshop membership · dependencies](../experiments/workshop-membership/dependencies.md) (line 33)
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 46)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 105)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 14)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 3)
- [outpost defense · persistence](../experiments/outpost-defense/persistence.md) (line 67)
  Original report discusses this roster entry under L1 historical turret owner gap: closed for the pair.
- [static exhaustion · call and dataflow](../experiments/static-exhaustion/call-and-dataflow.md) (line 133)
  Original report discusses this roster entry under Fractional position producers and consumers.
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 15)
- [static exhaustion · residual map](../experiments/static-exhaustion/residual-map.md) (line 34)
  Original report discusses this roster entry under Producer-to-consumer closure.

## RVA 0x00521620

**Load typed ExtraData cases** · Level B · preferred VA `0x140521620`

Analysis labels recorded in the original sources are `FUN_140521620`.

Dispatches type-specific ExtraData readers under the containing load framing.

Case `0x33` reaches `0x140404a10`, then `0x140406e80` and `0x1418650d0` for the bounded mod-list representation. Case `0x4c` reaches `0x140547c90` and `0x140562ef0` for linked-reference identities whose framing depends on mode. These case locators identify branches of this dispatcher. Full declaration, return and all load cases remain unknown.

Original records

- [configuration ui · save52](../experiments/cargo-links/configuration-ui/save52.md) (line 58)
- [crew · current assignments](../experiments/crew/current-assignments.md) (line 114)
- [power · saved](../experiments/power/saved.md) (line 184) · Restore typed reference extra data
  Dispatches saved extra variants, including historical ExtraFlags.
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 47)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 26)
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 41)
  Original report discusses this roster entry under Persistence classes.
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 4)
- [outpost defense · persistence](../experiments/outpost-defense/persistence.md) (line 68)
  Original report discusses this roster entry under L1 historical turret owner gap: closed for the pair.
- [docs · function register](../function-register.md) (line 122) · `SOR-FN-0042`
  Original group scope — Explicit +0x60/+0x68 save/load; buffer-version and variable-prefix conditions

## RVA 0x0054c2f0

**UI, save framing and lifecycle native entry** · Level C · preferred VA `0x14054c2f0`

Analysis labels recorded in the original sources are `FUN_14054c2f0`.

Recorded scope — Located member of an original operation group. Individual role remains unqualified.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 175) · `SOR-FN-0021`
  Original group scope — ExtraPromotedRef0x84 counted ref/byte pairs versus ExtraOwnership0x1f; player promotion ref is not an owner field. Inherited ownership and actual execution remain unvalidated.

## RVA 0x005e0930

**Load an SFTR BFCB component block** · Level B · preferred VA `0x1405e0930`

Resolves a named factory and skips bounded data if none exists.

The mapped component block uses exact-name dispatch 0x140463ed0 to 0x1404628b0. If the factory is missing, the loop skips DAT2 through BFCE. The direct registration-name census does not establish the contents of an arbitrary live registry.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 39)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 87) · `D5AD-SV86` · BFCB exact-name factory loader null skips DAT2

## RVA 0x005e3fb0

**Look up the planet subtitle name** · Level C · preferred VA `0x1405e3fb0`

Analysis labels recorded in the original sources are `FUN_1405e3fb0`.

Recorded scope — Look up the planet subtitle name

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · field lineage](../experiments/locations-outpost/field-lineage.md) (line 21)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 19)

## RVA 0x005e40a0

**Resolve a name for the outpost body context** · Level C · preferred VA `0x1405e40a0`

Analysis labels recorded in the original sources are `FUN_1405e40a0`.

Recorded scope — Resolve a name for the outpost body context

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 95)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 37)

## RVA 0x0063e4e0

**Receive the prepared default inventory count** · Level C · preferred VA `0x14063e4e0`

Recorded scope — The caller prepares one for a zero base-entry count before passing it here. The inspected evidence does not establish the constructor's complete default and leveled realization.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · aggregation](../experiments/stored-resources/aggregation.md) (line 56)

## RVA 0x0064a770

**localized symbol resolution** · Level C · preferred VA `0x14064a770`

Recorded scope — localized symbol resolution

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 29) · `n029`

## RVA 0x00786690

**Look up the primary Locations body context** · Level C · preferred VA `0x140786690`

Analysis labels recorded in the original sources are `FUN_140786690`.

Recorded scope — Look up the primary Locations body context

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 121)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 34)

## RVA 0x00910af0

**Supply the fallback Locations body context** · Level C · preferred VA `0x140910af0`

Analysis labels recorded in the original sources are `FUN_140910af0`.

Recorded scope — Supply the fallback Locations body context

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 121)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 178)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 33)

## RVA 0x0096fa90

**Packed grid-key encoder** · Level C · preferred VA `0x14096fa90`

Recorded scope — Packed grid-key encoder

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 63)

## RVA 0x00970830

**Load SFTR definition data** · Level B · preferred VA `0x140970830`

Dispatches the BFCB block to the component loader.

This pinned ESM loader routes BFCB to 0x1405e0930. The separately inspected SFTR changeform slots use base framing with identity and generic flags. The installed ESM route and saved-state route have different inputs and coverage.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 39)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 85) · `D5AD-SV84` · SFTR loader BFCB dispatch

## RVA 0x009e7890

**resource color fallback** · Level C · preferred VA `0x1409e7890`

Recorded scope — resource color fallback

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 28) · `n020`

## RVA 0x00a23de0

**Read the version-gated ExtraDA representation** · Level B · preferred VA `0x140a23de0`

Analysis labels recorded in the original sources are `FUN_140a23de0`.

Consumes the qualified queued identities and conditional fields.

The original native-backed membership completion distinguishes ExtraDA's version-dependent grammar from a fixed-size skip. Its queued identities use separate framing from the body fields. Full version and variant coverage remains unqualified.

Original records

- [experiments · active outpost membership completion](../experiments/active-outpost-membership-completion.md) (line 69) · Read the version-gated ExtraDA fields
- [crew · functions](../experiments/crew/functions.csv) (line 111)

## RVA 0x00aab770

**Decode the location DATA record fields** · Level C · preferred VA `0x140aab770`

Analysis labels recorded in the original sources are `FUN_140aab770`.

Recorded scope — Decode the location DATA record fields

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 139)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 103)

## RVA 0x00ab8030

**Dispatch location DATA decoding** · Level C · preferred VA `0x140ab8030`

Analysis labels recorded in the original sources are `FUN_140ab8030`.

Recorded scope — Dispatch location DATA decoding

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 139)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 87)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 101)

## RVA 0x00ab9f80

**Fix up the location DATA link** · Level C · preferred VA `0x140ab9f80`

Analysis labels recorded in the original sources are `FUN_140ab9f80`.

Recorded scope — Fix up the location DATA link

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 140)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 151)

## RVA 0x00aba950

**Select the first available owner context** · Level C · preferred VA `0x140aba950`

Analysis labels recorded in the original sources are `FUN_140aba950`.

Recorded scope — Select the first available owner context

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 128)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 42)

## RVA 0x00ad5f20

**Saved world component transfer** · Level C · preferred VA `0x140ad5f20`

Recorded scope — Saved world component transfer

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 122)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 83)

## RVA 0x00ad6150

**Saved world component transfer counterpart** · Level C · preferred VA `0x140ad6150`

Recorded scope — Saved world component transfer counterpart

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 34)
  Original report discusses this roster entry under State classification and its limits.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 14) · `D5AD-SV13`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 122)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 135)
  Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 84)

## RVA 0x00f3bfc0

**Test the resolved Locations exclusion keyword** · Level B · preferred VA `0x140f3bfc0`

Analysis labels recorded in the original sources are `FUN_140f3bfc0`.

Tests a reference for the resolved WorkshopUseDecorateTextKeyword default object.

The inspected path reaches the reference's keyword interface at +0x68 and dispatches through virtual byte displacement +0x08 with the object from global 0x145f0c6d0. The later LO1 constructor and definition join identify the default object and confirm DFOB 0x003e4f4a to KYWD 0x003e4f4b. This resolves the original register's keyword uncertainty for the mapped build and qualifies the exclusion when the default resolves as KYWD. Global membership or player-control authority remains open.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 32)
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 38)
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 6) · `n015` · outer exclusion property query
- [docs · function register](../function-register.md) (line 176) · `SOR-FN-0022` · Exclusion-property query through reference+0x68 with global 145f0c6d0
  Exclusion-property query through reference+0x68 with global 145f0c6d0. Resolved keyword/FormID and equivalence to BlockPlayerActivation unknown; no complete player-control proof.
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 88)

## RVA 0x0132d260

**Descriptor writer** · Level C · preferred VA `0x14132d260`

Recorded scope — Descriptor writer

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 31)
  Original report discusses this roster entry under State classification and its limits.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 3) · `D5AD-SV02`
- [resource retained population · d5z sources](../experiments/resource-retained-population/d5z-sources.csv) (line 324) · `D5Z-S0251`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 153)
  Original report discusses this roster entry under Final graph expansion and dispositions.
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 105)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 309)
  Original report discusses this roster entry under Eighth trace round: generated-world descriptor persistence.

## RVA 0x01350a00

**metadata field constructor** · Level C · preferred VA `0x141350a00`

Recorded scope — metadata field constructor

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 16) · `n018`

## RVA 0x01350b10

**physical item to resource association** · Level C · preferred VA `0x141350b10`

Recorded scope — physical item to resource association

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 14) · `n017`

## RVA 0x01351790

**resource metadata construction** · Level C · preferred VA `0x141351790`

Recorded scope — resource metadata construction

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 15) · `n015`

## RVA 0x0135d210

**ResourceEntry fields** · Level C · preferred VA `0x14135d210`

Recorded scope — ResourceEntry fields

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 24) · `n019`

## RVA 0x0135d570

**Bind the Locations body and system names** · Level C · preferred VA `0x14135d570`

Analysis labels recorded in the original sources are `FUN_14135d570`.

Recorded scope — Bind the Locations body and system names

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 115)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 27)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 44)

## RVA 0x0135d890

**Supply the Locations faction caption** · Level C · preferred VA `0x14135d890`

Analysis labels recorded in the original sources are `FUN_14135d890`.

Recorded scope — Supply the Locations faction caption

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · field lineage](../experiments/locations-outpost/field-lineage.md) (line 35)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 30)

## RVA 0x0135dcb0

**Register the Locations data providers** · Level C · preferred VA `0x14135dcb0`

Analysis labels recorded in the original sources are `FUN_14135dcb0`.

Recorded scope — Register the Locations data providers

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 18)
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 2) · `n020` · Locations provider registration
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 11)

## RVA 0x0135df40

**provider destruction/unregistration** · Level C · preferred VA `0x14135df40`

Recorded scope — provider destruction/unregistration

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 3) · `n019`

## RVA 0x0135e120

**Collect Locations body and outpost data** · Level C · preferred VA `0x14135e120`

Analysis labels recorded in the original sources are `FUN_14135e120`.

Recorded scope — Collect Locations body and outpost data

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 20)
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 4) · `n019` · Locations entry and collector call
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 8)

## RVA 0x0135e270

**body selection event** · Level C · preferred VA `0x14135e270`

Analysis labels recorded in the original sources are `FUN_14135e270`.

Recorded scope — body selection event

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 31) · `n022`
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 46)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 53)

## RVA 0x0135e350

**service event body refresh only** · Level C · preferred VA `0x14135e350`

Analysis labels recorded in the original sources are `FUN_14135e350`.

Recorded scope — service event body refresh only

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 34) · `n027`
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 39)

## RVA 0x0135e390

**favorite selection event** · Level C · preferred VA `0x14135e390`

Analysis labels recorded in the original sources are `FUN_14135e390`.

Recorded scope — favorite selection event

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 32) · `n023`
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 40)

## RVA 0x0135e580

**outpost pressed event** · Level C · preferred VA `0x14135e580`

Analysis labels recorded in the original sources are `FUN_14135e580`.

Recorded scope — outpost pressed event

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 33) · `n018`
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 22)

## RVA 0x0135eb10

**Supply separate Locations body data** · Level C · preferred VA `0x14135eb10`

Analysis labels recorded in the original sources are `FUN_14135eb10`.

Recorded scope — Supply separate Locations body data

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 233)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 4)

## RVA 0x0135f0e0

**Build the selected Locations body data** · Level C · preferred VA `0x14135f0e0`

Analysis labels recorded in the original sources are `FUN_14135f0e0`.

Recorded scope — Build the selected Locations body data

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 109)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 21)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 156)

## RVA 0x0135fcc0

**Dispatch Locations system-body data replacement** · Level C · preferred VA `0x14135fcc0`

Analysis labels recorded in the original sources are `FUN_14135fcc0`.

Recorded scope — Dispatch Locations system-body data replacement

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 203)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 26)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 56)

## RVA 0x01360e80

**Build the Locations outpost aggregate and displayed maximum** · Level A · preferred VA `0x141360e80`

Analysis labels recorded in the original sources are `FUN_141360e80`.

Filters registered Workshop references and copies live summary lanes into Locations rows.

The adapter reads handle storage `0x145f0ba80` and count `0x145f0ba78`. Row admission resolves the handle, rejects positive `0x140f3bfc0`, and requires ACTI `0x1e`, the Workshop keyword and ExtraBC. It requests type 5 refresh and pumps `0x1421ba960`, then copies summary lanes from ExtraBC `+0x7c..+0x93` and the name at `+0x70` into a 72-byte aggregate. For a valid AVIF in `0x145f0c570`, the displayed maximum uses truncated player base `0x141976dc0` output. Missing/wrong-type default leaves zero. Queued receiver `0x141361c10` moves the maximum and vector onward. This has no general active-player ownership guarantee, and the refresh does not certify settled inventories. Full prototype and return meaning are unknown.

Scoped pseudocode abstraction. It covers the described branch and omits unqualified paths.

```text
Abstraction of row admission and maximum calculation. Queue and cache internals are omitted.

for each handle in the Locations registry:
    resolve reference
    when valid, not excluded, and ACTI with Workshop keyword and ExtraBC:
        request summary refresh and pump its service
        append copied summary lanes and name
maximum = 0
if the default maximum actor value is a valid AVIF:
    maximum = truncate(player_base_value(default_maximum))
queue rows and maximum
```

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 172).

- **Inputs** — Almanac state
- **Outputs** — Named 72-byte rows using cached production+84
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Enumerates Workshop registry; copies summary
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 172) · `N171` · Almanac outpost row producer
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 17)
  Filters registered Workshop references and copies live summary lanes into Locations rows.
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 32)
  Filters registered Workshop references and copies live summary lanes into Locations rows.
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 41)
  Filters registered Workshop references and copies live summary lanes into Locations rows.
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 69)
  Filters registered Workshop references and copies live summary lanes into Locations rows.
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 5) · `n012` · registered outposts and eligible inventories
- [limits · functions](../experiments/limits/functions.csv) (line 29)
- [limits · functions](../experiments/limits/functions.csv) (line 31)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 2)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 155)

## RVA 0x01361ad0

**default resource/count visitor** · Level C · preferred VA `0x141361ad0`

Recorded scope — default resource/count visitor

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 13) · `n016`

## RVA 0x01361c10

**Receive queued Locations outpost rows** · Level B · preferred VA `0x141361c10`

Analysis labels recorded in the original sources are `FUN_141361c10`.

Rebuilds the outpost entry list and forwards its stored maximum to the provider.

The receiver rebuilds entries and transfers aggregate `+0x18` to `iMaxOutposts`. `0x141364550` binds the list and maximum, and the mapped UI numerator is its entry count. ExtraBC source computations remain separate from this adapter. Native queue ABI, return and exceptional branches remain unknown. The Stored Resources route also rebuilds resource entries, sorts them by name through 0x14136a980 and inserts each count at the same index through 0x141369750. The shared receiver therefore preserves alignment of the parallel resource and count arrays.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 174).

- **Inputs** — Input row vector; UI model
- **Outputs** — Row+20 binary32 to fProductionPerMin
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Copies values into UI rows
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 174) · `N173` · Almanac UI row adapter
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 52)
  Rebuilds the outpost entry list and forwards its stored maximum to the provider.
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 69)
  Rebuilds the outpost entry list and forwards its stored maximum to the provider.
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 20) · `n012` · OutpostEntry and resource/count population
- [stored resources · provider](../experiments/stored-resources/provider.md) (line 58–66)
  Rebuilds the outpost entry list and forwards its stored maximum to the provider.
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 3)

## RVA 0x01362bc0

**Resolve display context for the Locations upper map** · Level C · preferred VA `0x141362bc0`

Analysis labels recorded in the original sources are `FUN_141362bc0`.

Recorded scope — Resolve display context for the Locations upper map

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 180)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 57)

## RVA 0x013630c0

**Project system component positions for the upper map** · Level C · preferred VA `0x1413630c0`

Analysis labels recorded in the original sources are `FUN_1413630c0`.

Recorded scope — Project system component positions for the upper map

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 181)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 61)

## RVA 0x01363960

**Queue the outpost vector** · Level C · preferred VA `0x141363960`

Recorded scope — Queue the outpost vector

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 52)

## RVA 0x01364300

**Bind the Locations marker array** · Level C · preferred VA `0x141364300`

Analysis labels recorded in the original sources are `FUN_141364300`.

Recorded scope — Bind the Locations marker array

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 184)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 17)

## RVA 0x013644b0

**outpost list binding** · Level C · preferred VA `0x1413644b0`

Recorded scope — outpost list binding

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 26) · `n027`

## RVA 0x01364550

**Bind list and maximum to Locations data** · Level C · preferred VA `0x141364550`

Analysis labels recorded in the original sources are `FUN_141364550`.

Recorded scope — Bind list and maximum to Locations data

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 53)
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 25) · `n023` · OutpostStaticData construction
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 9)

## RVA 0x01364930

**Bind the Locations body data fields** · Level C · preferred VA `0x141364930`

Analysis labels recorded in the original sources are `FUN_141364930`.

Recorded scope — Bind the Locations body data fields

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 161)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 15)

## RVA 0x01368cf0

**container AV gate shared substitution dedup** · Level C · preferred VA `0x141368cf0`

Recorded scope — container AV gate shared substitution dedup

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 8) · `n014`
- [shared outpost storage · consumers](../experiments/shared-outpost-storage/consumers.md) (line 61)
  Original report discusses this roster entry under Entry points and actual source lists.
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 29)

## RVA 0x01369750

**aligned count insertion** · Level C · preferred VA `0x141369750`

Recorded scope — aligned count insertion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 22) · `n028`

## RVA 0x01369b80

**Handle the Locations system-body data route** · Level C · preferred VA `0x141369b80`

Analysis labels recorded in the original sources are `FUN_141369b80`.

Recorded scope — Handle the Locations system-body data route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · field lineage](../experiments/locations-outpost/field-lineage.md) (line 13)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 45)

## RVA 0x0136a980

**resource-name sorted insertion** · Level C · preferred VA `0x14136a980`

Recorded scope — resource-name sorted insertion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 21) · `n020`

## RVA 0x0136bbb0

**resource FormID map insertion** · Level C · preferred VA `0x14136bbb0`

Recorded scope — resource FormID map insertion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 17) · `n015`

## RVA 0x0136be50

**initialized inventory resource/count visitor** · Level C · preferred VA `0x14136be50`

Recorded scope — initialized inventory resource/count visitor

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 11) · `n014`

## RVA 0x0136c060

**default inventory path** · Level C · preferred VA `0x14136c060`

Recorded scope — default inventory path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 12) · `n014`

## RVA 0x0136cf60

**Bind body identity and coordinates for the upper map** · Level C · preferred VA `0x14136cf60`

Analysis labels recorded in the original sources are `FUN_14136cf60`.

Recorded scope — Bind body identity and coordinates for the upper map

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 185)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 126)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 161)

## RVA 0x0136dc00

**UI command receiver** · Level C · preferred VA `0x14136dc00`

Recorded scope — UI command receiver

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 19) · `n017`

## RVA 0x0136dc40

**Dispatch the queued system-body data update** · Level C · preferred VA `0x14136dc40`

Analysis labels recorded in the original sources are `FUN_14136dc40`.

Recorded scope — Dispatch the queued system-body data update

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · field lineage](../experiments/locations-outpost/field-lineage.md) (line 13)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 54)

## RVA 0x01382c00

**non-provider Workshop-tab control** · Level C · preferred VA `0x141382c00`

Recorded scope — non-provider Workshop-tab control

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 30) · `n003`

## RVA 0x0140ff80

**Site tuple transfer** · Level C · preferred VA `0x14140ff80`

Recorded scope — Site tuple transfer

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 121)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 109)

## RVA 0x014128c0

**Site tuple transfer counterpart** · Level C · preferred VA `0x1414128c0`

Recorded scope — Site tuple transfer counterpart

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 34)
  Original report discusses this roster entry under State classification and its limits.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 15) · `D5AD-SV14`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 134)
  Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 110)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 224)
  Original report discusses this roster entry under Sixth trace round: typed load paths and active key.

## RVA 0x0143f450

**Publish the Workshop status provider** · Level C · preferred VA `0x14143f450`

Recorded scope — Publishes WorkshopStatusData and subscribes to the summary event.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [build budget · ui](../experiments/build-budget/ui.md) (line 43)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 88)

## RVA 0x0143fa60

**Receive the Workshop summary event** · Level C · preferred VA `0x14143fa60`

Recorded scope — The receiver invokes 0x14143f690 on this status data path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [build budget · ui](../experiments/build-budget/ui.md) (line 44)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 75)

## RVA 0x0158e280

**Preview spinner constructor** · Level C · preferred VA `0x14158e280`

Recorded scope — Preview spinner constructor

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 57–62) · `SOR-FN-0057`

## RVA 0x0158f230

**Preview spinner input binding** · Level C · preferred VA `0x14158f230`

Recorded scope — Preview spinner input binding

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 57–62) · `SOR-FN-0057`

## RVA 0x0158fa50

**Selected preview UI data update** · Level C · preferred VA `0x14158fa50`

Recorded scope — Selected preview UI data update

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 57–62) · `SOR-FN-0057`

## RVA 0x015902a0

**Preview UI service** · Level C · preferred VA `0x1415902a0`

Analysis labels recorded in the original sources are `FUN_1415902a0`.

Recorded scope — Preview UI service

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 57–62) · `SOR-FN-0057`
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 75)

## RVA 0x0166c0a0

**Dispatch save UI selection** · Level C · preferred VA `0x14166c0a0`

Analysis labels recorded in the original sources are `FUN_14166c0a0`.

Recorded scope — Queries selection then directly or asynchronously invokes the save selection handler.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 37)
- [docs · function register](../function-register.md) (line 184) · `SOR-FN-0014`
  Original group scope — UI dispatch/save selection; direct or queued path, new-slot call passes manager/null/-1/0. Earliest UI thread UNKNOWN

## RVA 0x0166c190

**Handle save selection** · Level C · preferred VA `0x14166c190`

Analysis labels recorded in the original sources are `FUN_14166c190`.

Recorded scope — New-slot branch sets EBX=-1 and passes manager, null name, slot candidate and zero option.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 38)
- [docs · function register](../function-register.md) (line 184) · `SOR-FN-0014`
  Original group scope — UI dispatch/save selection; direct or queued path, new-slot call passes manager/null/-1/0. Earliest UI thread UNKNOWN

## RVA 0x0166cf00

**Register pause-menu save behavior** · Level C · preferred VA `0x14166cf00`

Recorded scope — References a deletion label during registration; deletion body remains unestablished.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 46)

## RVA 0x0166e4a0

**Obtain current save selection** · Level C · preferred VA `0x14166e4a0`

Recorded scope — Callee of the UI callback.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 37)

## RVA 0x0166f3c0

**Forward queued save selection** · Level C · preferred VA `0x14166f3c0`

Recorded scope — Distinct queue thunk identified from the UI callback route.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 37)

## RVA 0x016aa880

**Bind system-body diagram identity and display fields** · Level C · preferred VA `0x1416aa880`

Analysis labels recorded in the original sources are `FUN_1416aa880`.

Recorded scope — Bind system-body diagram identity and display fields

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 205)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 108)

## RVA 0x016aa920

**Supply body type and scan state for the diagram** · Level C · preferred VA `0x1416aa920`

Analysis labels recorded in the original sources are `FUN_1416aa920`.

Recorded scope — Supply body type and scan state for the diagram

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 195)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 68)

## RVA 0x016aab70

**Bind the Locations system-body diagram payload** · Level C · preferred VA `0x1416aab70`

Analysis labels recorded in the original sources are `FUN_1416aab70`.

Recorded scope — Bind the Locations system-body diagram payload

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 203)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 124)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 132)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 160)

## RVA 0x016aac10

**Participate in the Locations system-root diagram route** · Level C · preferred VA `0x1416aac10`

Analysis labels recorded in the original sources are `FUN_1416aac10`.

Recorded scope — Participate in the Locations system-root diagram route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 193)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 32)

## RVA 0x016aacd0

**Participate in the Locations system-root diagram route** · Level C · preferred VA `0x1416aacd0`

Analysis labels recorded in the original sources are `FUN_1416aacd0`.

Recorded scope — Participate in the Locations system-root diagram route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 193)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 52)

## RVA 0x016ab670

**Replace the Locations system-body data** · Level C · preferred VA `0x1416ab670`

Analysis labels recorded in the original sources are `FUN_1416ab670`.

Recorded scope — Replace the Locations system-body data

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 203)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 62)

## RVA 0x016b6310

**Receive the Locations body and system name data** · Level C · preferred VA `0x1416b6310`

Analysis labels recorded in the original sources are `FUN_1416b6310`.

Recorded scope — Receive the Locations body and system name data

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 115)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 81)

## RVA 0x016cd320

**Participate in selected body data construction** · Level C · preferred VA `0x1416cd320`

Analysis labels recorded in the original sources are `FUN_1416cd320`.

Recorded scope — Participate in selected body data construction

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 110)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 36)

## RVA 0x016ceb20

**Supply color from the relevant body component** · Level C · preferred VA `0x1416ceb20`

Analysis labels recorded in the original sources are `FUN_1416ceb20`.

Recorded scope — Supply color from the relevant body component

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 196)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 72)

## RVA 0x016ceb90

**Participate in normalized Locations body sizing** · Level C · preferred VA `0x1416ceb90`

Analysis labels recorded in the original sources are `FUN_1416ceb90`.

Recorded scope — Participate in normalized Locations body sizing

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 197)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 73)

## RVA 0x016cf0f0

**Participate in selected body data construction** · Level C · preferred VA `0x1416cf0f0`

Analysis labels recorded in the original sources are `FUN_1416cf0f0`.

Recorded scope — Participate in selected body data construction

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 110)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 31)

## RVA 0x016cf8f0

**Supply the Locations system designation name** · Level C · preferred VA `0x1416cf8f0`

Analysis labels recorded in the original sources are `FUN_1416cf8f0`.

Recorded scope — Supply the Locations system designation name

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · field lineage](../experiments/locations-outpost/field-lineage.md) (line 22)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 51)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 100)
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 115)

## RVA 0x016d1c50

**Accumulate display size ranges by body type** · Level C · preferred VA `0x1416d1c50`

Analysis labels recorded in the original sources are `FUN_1416d1c50`.

Recorded scope — Accumulate display size ranges by body type

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 198)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 110)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 118)

## RVA 0x0172bc70

**Resolve faction-type keyword for Locations display** · Level C · preferred VA `0x14172bc70`

Analysis labels recorded in the original sources are `FUN_14172bc70`.

Recorded scope — Resolve faction-type keyword for Locations display

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 134)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 43)

## RVA 0x01739c50

**Prepare item-card operational data** · Level C · preferred VA `0x141739c50`

Analysis labels recorded in the original sources are `FUN_141739c50`.

Recorded scope — One of the two verified helpers used to obtain inputs and produced resources through temporary form-backed references, including PackIn members. The report describes their shared preparation path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [build catalogue · ui](../experiments/build-catalogue/ui.md) (line 40)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 161)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 177)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 183)

## RVA 0x0173a9f0

**Prepare item-card operational data** · Level C · preferred VA `0x14173a9f0`

Analysis labels recorded in the original sources are `FUN_14173a9f0`.

Recorded scope — One of the two verified helpers used to obtain inputs and produced resources through temporary form-backed references, including PackIn members. The report describes their shared preparation path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [build catalogue · ui](../experiments/build-catalogue/ui.md) (line 40)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 160)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 176)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 182)

## RVA 0x01809400

**Read the compact change-record count** · Level B · preferred VA `0x141809400`

Supplies the count grammar used by the native framing walker.

The original R3 framing follows the installed compact-count reader and validates record boundaries independently of the outpost membership classifier. The full native declaration remains unqualified.

Original records

- [experiments · active outpost identification](../experiments/active-outpost-identification.md) (line 38–48)

## RVA 0x01814050

**Wrap save name and serialization** · Level C · preferred VA `0x141814050`

Analysis labels recorded in the original sources are `FUN_141814050`.

Recorded scope — Builds name, captures callback state and dispatches a component command.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 41)
- [docs · function register](../function-register.md) (line 186) · `SOR-FN-0016`
  Original group scope — File-object preparation and serialization wrapper; storage context is not a bare name buffer; command/wait semantics incomplete

## RVA 0x01814220

**Serialize the native save payload** · Level B · preferred VA `0x141814220`

Analysis labels recorded in the original sources are `FUN_141814220`.

Uses a caller-held context and file/storage object in the mapped serializer path.

The observed caller uses `RCX` pointing to a stored object pointer, `RDX` service reference, `R8` original file/storage object and `R9` generated name buffer. The entry dereferences `RCX` and atomically ORs bit `4` into object `+0x3a8`. The diagnostic and observed edge support the serialization role. The body is incompletely characterized, and the diagnostic's apparent completion precedes additional storage activity. Return, complete ABI and durability remain unknown.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 41)
- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 42) · Serialize save game
  Dereferences RCX before setting object +0x3a8 flag; complete body and ABI remain unresolved.
- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 48)
- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 104)
- [docs · function register](../function-register.md) (line 187) · `SOR-FN-0017` · Serializer candidate, RCX indirection observed at caller
  Serializer candidate, RCX indirection observed at caller; no old SFSE prototype transfer. Large body, not a safe integration point

## RVA 0x0181aa30

**UI, save framing and lifecycle native entry** · Level C · preferred VA `0x14181aa30`

Recorded scope — Located member of an original operation group. Individual role remains unqualified.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 104) · `SOR-FN-0047`
  Original group scope — Reference-frame caller

## RVA 0x0181af40

**UI, save framing and lifecycle native entry** · Level C · preferred VA `0x14181af40`

Recorded scope — Located member of an original operation group. Individual role remains unqualified.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 104) · `SOR-FN-0047`
  Original group scope — Reference-frame caller

## RVA 0x01821b70

**Handle save serialization callback** · Level C · preferred VA `0x141821b70`

Recorded scope — Calls serializer from the callback path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 41)

## RVA 0x01822170

**Forward save serialization callback** · Level C · preferred VA `0x141822170`

Recorded scope — Distinct callback routes to serialization handler.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 41)

## RVA 0x01822570

**Save unit 6 dispatch** · Level C · preferred VA `0x141822570`

Analysis labels recorded in the original sources are `FUN_141822570`.

Recorded scope — Save unit 6 dispatch

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 44)
- [containers displays · native](../experiments/containers-displays/native.md) (line 274)
  Original report discusses this roster entry under New construction suppresses default stock.
- [crew · current functions](../experiments/crew/current-functions.csv) (line 12)
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 120)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 122)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 120)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 187)
  Original report discusses this roster entry under Fifth trace round.

## RVA 0x01824a60

**Save unit 3 dispatch** · Level C · preferred VA `0x141824a60`

Recorded scope — Save unit 3 dispatch

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [resource retained population · d5ad investigation ledger](../experiments/resource-retained-population/d5ad-investigation-ledger.md) (line 97)
  Original report discusses this roster entry under Third science challenge.
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 30)
  Original report discusses this roster entry under State classification and its limits.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 2) · `D5AD-SV01`
- [resource retained population · d5z report](../experiments/resource-retained-population/d5z-report.md) (line 228)
  Original report discusses this roster entry under Persistence and load.
- [resource retained population · d5z sources](../experiments/resource-retained-population/d5z-sources.csv) (line 323) · `D5Z-S0250`

## RVA 0x018286f0

**Write the type-9 saved-destination frame** · Level B · preferred VA `0x1418286f0`

Pairs with the type-9 global-data reader.

The writer corroborates the destination framing selected by case 9 of 0x141825e00. The inspected offline Save52 reconstruction qualifies a 60-byte prefix and leaves the later tail opaque. No universal round-trip or native callable declaration is established.

Original records

- [resource retained population · d5ad save destination](../experiments/resource-retained-population/d5ad-save-destination.md) (line 20)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 70) · `D5AD-SV69` · Paired type 9 writer; CELL versus WRLD and saved context/alternate predicates
- [resource retained population · d5z sources](../experiments/resource-retained-population/d5z-sources.csv) (line 75) · `D5Z-S0071`
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 128)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 242)
  Original report discusses this roster entry under Sixth trace round: typed load paths and active key.

## RVA 0x01829ec0

**Load the type-9 saved-destination frame** · Level B · preferred VA `0x141829ec0`

Receives native global-data dispatch case 9.

The loader handles the world/destination prefix, local position and conditional planetary or alternate-reference data in the cited path. A common buffer operation handles later data. The qualified Save52 prefix is distinct from the complete native body and from case 7 PCM state.

Original records

- [resource retained population · d5ad save destination](../experiments/resource-retained-population/d5ad-save-destination.md) (line 18)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 69) · `D5AD-SV68` · Full destination load reader and ordinary CELL/context branch
- [resource retained population · d5aa gameplay transition map](../experiments/resource-retained-population/d5aa-gameplay-transition-map.md) (line 41)
  Original report discusses this roster entry under Confirmation and transition ingress.
- [resource retained population · d5aa gameplay transition map](../experiments/resource-retained-population/d5aa-gameplay-transition-map.md) (line 72)
  Original report discusses this roster entry under Save loading and interior residency.
- [resource retained population · d5ad investigation ledger](../experiments/resource-retained-population/d5ad-investigation-ledger.md) (line 56)
  Original report discusses this roster entry under Independent challenge and additional upstream work.
- [resource retained population · d5ad load chronology](../experiments/resource-retained-population/d5ad-load-chronology.md) (line 29)
  Original report discusses this roster entry under Native dependency order.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 162) · `D5AD-N012`
- [resource retained population · d5z sources](../experiments/resource-retained-population/d5z-sources.csv) (line 76) · `D5Z-S0072`
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 129)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 275)
  Original report discusses this roster entry under Seventh trace round: native packer and six-save context audit.

## RVA 0x0182d350

**Read the type-9 saved-destination world prefix** · Level B · preferred VA `0x14182d350`

Resolves the initial saved world token through legacy identity and type checks.

The inspected prefix reads a saved world token and checks TESWorldSpace. The qualified Save52 token is null. The complete type-9 loader and its later buffer processing are distinct. Other sample or buffer-version paths remain unqualified.

Original records

- [resource retained population · d5ad save destination](../experiments/resource-retained-population/d5ad-save-destination.md) (line 41)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 67) · `D5AD-SV66` · Type 9 initial saved world token reader/cast

## RVA 0x0182e280

**Typed component restoration** · Level C · preferred VA `0x14182e280`

Recorded scope — Typed component restoration

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 134)
  Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49).
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 135)
  Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 131)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 223)
  Original report discusses this roster entry under Sixth trace round: typed load paths and active key.

## RVA 0x01833b20

**Saved initial frame conversion** · Level C · preferred VA `0x141833b20`

Recorded scope — Saved initial frame conversion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052`
- [crew · current functions](../experiments/crew/current-functions.csv) (line 17)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 43)
  Original report discusses this roster entry under State classification and its limits.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 16) · `D5AD-SV15`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 156)
  Original report discusses this roster entry under Final graph expansion and dispositions.
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 135)
- [docs · function register](../function-register.md) (line 138) · `SOR-FN-0037`
  Original group scope — World/initial flags/restoration/rebase; final authority unknown

## RVA 0x01839c60

**Construct save-load manager context** · Level C · preferred VA `0x141839c60`

Recorded scope — Contains save/load manager and thread names and an async request queue; executing thread unresolved.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 46)

## RVA 0x0183a8d0

**Construct save file context** · Level C · preferred VA `0x14183a8d0`

Recorded scope — Builds the file and storage context used for preparation.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 46)
- [resource retained population · d5z sources](../experiments/resource-retained-population/d5z-sources.csv) (line 349) · `D5Z-S0276`

## RVA 0x0183aaf0

**Set up save finalization** · Level C · preferred VA `0x14183aaf0`

Analysis labels recorded in the original sources are `FUN_14183aaf0`.

Recorded scope — Direct or queued route; sets manager +0x8c under observed flag condition.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 43)
- [docs · function register](../function-register.md) (line 188) · `SOR-FN-0018`
  Original group scope — Finalization scheduling, storage/rename/cache/status-clear/wake. Completion candidate, not disk/cloud durability proof

## RVA 0x0183ac80

**Finalize local save storage** · Level C · preferred VA `0x14183ac80`

Analysis labels recorded in the original sources are `FUN_14183ac80`.

Recorded scope — Closes/frees local storage and handles rename/error branches before clearing manager wait state.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 44)
- [docs · function register](../function-register.md) (line 188) · `SOR-FN-0018`
  Original group scope — Finalization scheduling, storage/rename/cache/status-clear/wake. Completion candidate, not disk/cloud durability proof

## RVA 0x0183c3c0

**Handle alternate save request** · Level C · preferred VA `0x14183c3c0`

Recorded scope — Existing-name branch can take this distinct route.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 38)

## RVA 0x0183c590

**Request a save through the ordinary native UI path** · Level B · preferred VA `0x14183c590`

Analysis labels recorded in the original sources are `FUN_14183c590`.

Handles a build-pinned save request candidate and invokes save preparation.

The ordinary new-slot UI edge calls with manager in `RCX`, zero in `RDX`, slot candidate `-1` in `R8D`, zero in `R9D`. Additional mapped paths suggest optional name data in `RDX`, with the option in `R9D` unresolved. The entry checks manager state, calls preparation `0x14183c830`, and participates in serialization/finalization. `AL` is bool-like on the mapped path and does not establish disk durability. The source has an independently checked direct call site `0x14166c1be`, distinct from the entry. General threading, storage and invocation contracts remain unknown.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 37)
- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 39) · Request ordinary save
  Higher-level UI path calls preparation; AL reports a bool-like result, with durability unresolved.
- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 48)
- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 104)
- [docs · function register](../function-register.md) (line 185) · `SOR-FN-0015` · Higher-level request candidate
  Higher-level request candidate; status/gates/name/file preparation. Live manager identity, option meaning and execution contract UNKNOWN

## RVA 0x0183c830

**Prepare save file object** · Level C · preferred VA `0x14183c830`

Analysis labels recorded in the original sources are `FUN_14183c830`.

Recorded scope — RDX carries original object with name at start and storage/status members.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 40)
- [docs · function register](../function-register.md) (line 186) · `SOR-FN-0016`
  Original group scope — File-object preparation and serialization wrapper; storage context is not a bare name buffer; command/wait semantics incomplete

## RVA 0x01846ef0

**Check save request conditions** · Level C · preferred VA `0x141846ef0`

Recorded scope — Gates on menu, player and game conditions.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 46)

## RVA 0x0184ab70

**Update save metadata** · Level C · preferred VA `0x14184ab70`

Recorded scope — Used in the preparation path after its file handling.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 40)

## RVA 0x0184cee0

**Update save selection bookkeeping** · Level C · preferred VA `0x14184cee0`

Recorded scope — Called after documented save-request routing.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 38)

## RVA 0x0184eec0

**Generate save name** · Level C · preferred VA `0x14184eec0`

Recorded scope — Uses name prefixes for Save, Autosave, Quicksave and Exitsave.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 46)

## RVA 0x01850940

**Apply save manager status** · Level C · preferred VA `0x141850940`

Recorded scope — One of the documented manager status helpers.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 46)

## RVA 0x018509c0

**Handle alternate save manager status** · Level C · preferred VA `0x1418509c0`

Recorded scope — One of the documented manager status helpers.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 46)

## RVA 0x01855a20

**Forward queued save finalization** · Level C · preferred VA `0x141855a20`

Recorded scope — Distinct callback thunk for finalization.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 43)

## RVA 0x0185e180

**Read the change-record framing header** · Level B · preferred VA `0x14185e180`

Reads the native header used by the R3 framing model.

The optional header byte is a buffer-version override. Later original analysis corrected the prior type interpretation and follows propagation into LoadBuffer. This does not establish form or membership semantics for the framed record.

Original records

- [experiments · active outpost identification](../experiments/active-outpost-identification.md) (line 38–48)
- [workshop population · routes](../experiments/workshop-population/routes.md) (line 18)

## RVA 0x018b1eb0

**Write global type-7 PlanetContentManager state** · Level B · preferred VA `0x1418b1eb0`

Serializes the PCM seed, maps and subsequent type-7 fields.

The writer serializes the PCM seed at byte offset +0x420 and distinct PNDT and world-keyed maps at +0x360 and +0x3e0, with two triples and a version-gated final ID list. The mapped global type-7 frame is separate from type-9 saved destination and from resident ProcGen contours.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 40)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 99) · `D5AD-SV98` · Paired global type 7 PCM writer
- [resource retained population · d5ad investigation ledger](../experiments/resource-retained-population/d5ad-investigation-ledger.md) (line 97)
  Original report discusses this roster entry under Third science challenge.
- [resource retained population · d5ad load chronology](../experiments/resource-retained-population/d5ad-load-chronology.md) (line 179)
  Original report discusses this roster entry under Separate PCM restoration before destination processing.

## RVA 0x018b22c0

**Restore global type-7 PlanetContentManager state** · Level B · preferred VA `0x1418b22c0`

Restores saved PCM fields and reconstructs typed references under version and resolution gates.

The loader restores the seed, PNDT map, world map, two triples and version-gated ID list. Mapped nested readers apply remapping and type checks and can filter failed resolutions. The exact offline Save52 frame corroborates the wire fields without establishing live resolution or demand order.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 40)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 98) · `D5AD-SV97` · Global type 7 PCM restoration maps seed and final IDs
- [resource retained population · d5ad investigation ledger](../experiments/resource-retained-population/d5ad-investigation-ledger.md) (line 97)
  Original report discusses this roster entry under Third science challenge.
- [resource retained population · d5ad load chronology](../experiments/resource-retained-population/d5ad-load-chronology.md) (line 179)
  Original report discusses this roster entry under Separate PCM restoration before destination processing.
- [resource retained population · d5ad save destination](../experiments/resource-retained-population/d5ad-save-destination.md) (line 19)
  Original report discusses this roster entry under d5ad save destination.
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 228)
  Original report discusses this roster entry under PCM lifecycle, consumers and the ordinary load boundary.
- [resource retained population · d5ag lifecycle consistency](../experiments/resource-retained-population/d5ag-lifecycle-consistency.md) (line 54)
  Original report discusses this roster entry under What the saved preparation state actually constrains.
- [resource retained population · d5ah lifecycle matrix](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md) (line 110)
  Original report discusses this roster entry under Reset and return predicates.

## RVA 0x018bab90

**Write PNDT-keyed PCM content map** · Level B · preferred VA `0x1418bab90`

Serializes the type-7 map of planetary content blocks.

The verified function window identifies the PNDT-keyed content-map writer. It is separate from the map keyed by world tokens. Global type 7 writes both in the scoped PCM contract.

Original records

- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 100)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 100) · `D5AD-SV99` · PNDT-keyed PCM content map writer

## RVA 0x018bad70

**Write world-token-keyed PCM placement map** · Level B · preferred VA `0x1418bad70`

Serializes the type-7 map of world placements.

The verified function window identifies the world-token-keyed placement-map writer. The global type-7 contract keeps this map separate from PNDT content blocks. The recorded save layout does not establish live world resolution.

Original records

- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 101)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 101) · `D5AD-SV100` · World-token-keyed PCM placement map writer

## RVA 0x01976dc0

**Read the base value for the outpost panel maximum** · Level C · preferred VA `0x141976dc0`

Analysis labels recorded in the original sources are `FUN_141976dc0`.

Recorded scope — Read the base value for the outpost panel maximum

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 42)
- [limits · functions](../experiments/limits/functions.csv) (line 26)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 20)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 104)

## RVA 0x021b5720

**Initialize Wait3D timers and latch** · Level C · preferred VA `0x1421b5720`

Recorded scope — Vtable-selected callback boundary from existing instructions. A Ghidra function object was not required for this entry evidence.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [event oracle · preview state](../experiments/event-oracle/preview-state.md) (line 49) · `SOR-FN-0057`

## RVA 0x021b5750

**Request spinner-off on Wait3D exit** · Level C · preferred VA `0x1421b5750`

Recorded scope — Vtable-selected exit stub zeroes ECX and tail-jumps to the spinner request.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [event oracle · preview state](../experiments/event-oracle/preview-state.md) (line 70) · `SOR-FN-0057`

## RVA 0x021b5970

**Wait3D update** · Level C · preferred VA `0x1421b5970`

Recorded scope — Wait3D update

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 57–62) · `SOR-FN-0057`

## RVA 0x021f6420

**Preview spinner request** · Level C · preferred VA `0x1421f6420`

Recorded scope — Preview spinner request

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 57–62) · `SOR-FN-0057`

## RVA 0x0231f860

**Validate the containing root body** · Level C · preferred VA `0x14231f860`

Analysis labels recorded in the original sources are `FUN_14231f860`.

Recorded scope — Validate the containing root body

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 111)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 70)

## RVA 0x02333270

**Read body size component data for the display path** · Level C · preferred VA `0x142333270`

Analysis labels recorded in the original sources are `FUN_142333270`.

Recorded scope — Read body size component data for the display path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 197)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 119)

## RVA 0x023ff430

**Save name and serialization command helper** · Level C · preferred VA `0x1423ff430`

Recorded scope — Save name and serialization command helper

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [experiments · SOR EXP 0002A native save thread mapping](../experiments/SOR-EXP-0002A-native-save-thread-mapping.md) (line 41)

## RVA 0x0241e7f0

**Preview readiness test** · Level C · preferred VA `0x14241e7f0`

Recorded scope — Preview readiness test

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [docs · function register](../function-register.md) (line 57–62) · `SOR-FN-0057`

## RVA 0x02be45c0

**Project system positions into Locations display coordinates** · Level C · preferred VA `0x142be45c0`

Recorded scope — Project system positions into Locations display coordinates

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 182)

## RVA 0x0388f200

**Forward SFTR name-registry shutdown** · Level B · preferred VA `0x14388f200`

Computes the registry subobject and jumps to the clear routine.

The verified entry computes the registry plus byte offset 0x08 and tail-jumps to 0x1402cb9f0. An earlier Ghidra selector reported no function object at this address. The bounded byte replay establishes the stub boundary and its forwarding relation without changing the analysis project.

Original records

- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 288)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 289)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 292)
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 293)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 149) · `D5AD-SV148`
