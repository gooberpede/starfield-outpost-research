# Extractors, organic facilities and fabrication

[Subject navigation and ABI limits](README.md) · [RVA index](index.md)

Entries use the pinned `Starfield.exe` 1.16.244.0 image. Internal-only observation. External invocation remains unvalidated.

Follow a mapped path

- [Shared production scheduler](production.md#rva-0x00f7f1e0)
- [Pending production replay](production.md#rva-0x00f8c580)
- [Crew production-timer contribution](production.md#rva-0x00f7bd20)

## RVA 0x00092260

**Read the resource's base production interval** · Level C · preferred VA `0x140092260`

Recorded scope — Read the resource's base production interval

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 46)

## RVA 0x000a97a0

**Participate in effective harvester interval multiplier lookup** · Level C · preferred VA `0x1400a97a0`

Recorded scope — Participate in effective harvester interval multiplier lookup

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 47)

## RVA 0x000f81e0

**sleep update setting initializer** · Level B · preferred VA `0x1400f81e0`

Analysis labels recorded in the original sources are `FUN_1400f81e0`.

Recorded scope — sleep update setting initializer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 156).

- **Inputs** — No caller inputs established
- **Outputs** — iSecondsToSleepPerUpdate default 900
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Registers setting
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 156) · `N155`

## RVA 0x00127cc0

**actor scanner info list binding** · Level B · preferred VA `0x140127cc0`

Analysis labels recorded in the original sources are `FUN_140127cc0`.

Recorded scope — actor scanner info list binding

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 221).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — actor scanner info list binding
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 221) · `N220`

## RVA 0x00127d00

**flora scanner info list binding** · Level B · preferred VA `0x140127d00`

Analysis labels recorded in the original sources are `FUN_140127d00`.

Recorded scope — flora scanner info list binding

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 222).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — flora scanner info list binding
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 222) · `N221`

## RVA 0x00127e80

**knowledge default keyword binding** · Level B · preferred VA `0x140127e80`

Analysis labels recorded in the original sources are `FUN_140127e80`.

Recorded scope — knowledge default keyword binding

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 224).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — knowledge default keyword binding
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 224) · `N223`

## RVA 0x0012a8d0

**local-to-UT cap initializer** · Level B · preferred VA `0x14012a8d0`

Analysis labels recorded in the original sources are `FUN_14012a8d0`.

Recorded scope — local-to-UT cap initializer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 157).

- **Inputs** — No caller inputs established
- **Outputs** — fMaxUTHourPerLocalHour setting
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Registers setting
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 157) · `N156`

## RVA 0x00156a40

**Initialize the organic facility input default object** · Level C · preferred VA `0x140156a40`

Recorded scope — Initialize the organic facility input default object

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 188)

## RVA 0x00156d00

**domesticability default keyword binding** · Level B · preferred VA `0x140156d00`

Analysis labels recorded in the original sources are `FUN_140156d00`.

Recorded scope — domesticability default keyword binding

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 223).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — domesticability default keyword binding
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 223) · `N222`

## RVA 0x00157280

**Initialize the production halt keyword default** · Level C · preferred VA `0x140157280`

Recorded scope — Initialize the production halt keyword default

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 41)

## RVA 0x00157480

**Initialize the Workshop production interval override** · Level C · preferred VA `0x140157480`

Recorded scope — Initialize the Workshop production interval override

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 88)

## RVA 0x002036f0

**QPC clock initialization** · Level B · preferred VA `0x1402036f0`

Analysis labels recorded in the original sources are `FUN_1402036f0`.

Recorded scope — QPC clock initialization

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 147).

- **Inputs** — No caller inputs established
- **Outputs** — Counter origin and frequency
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Calls QPC APIs; initializes clock globals
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 147) · `N146`

## RVA 0x00407cb0

**Migrate selected groups of crew handles** · Level C · preferred VA `0x140407cb0`

Analysis labels recorded in the original sources are `FUN_140407cb0`.

Recorded scope — Migrate selected groups of crew handles

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 35)
- [crew · functions](../experiments/crew/functions.csv) (line 20)

## RVA 0x00409f10

**Participate in selected-actor perk entry dispatch** · Level C · preferred VA `0x140409f10`

Analysis labels recorded in the original sources are `FUN_140409f10`.

Recorded scope — Participate in selected-actor perk entry dispatch

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 56)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 3)

## RVA 0x0044b590

**property-sheet component descriptor** · Level B · preferred VA `0x14044b590`

Analysis labels recorded in the original sources are `FUN_14044b590`.

Recorded scope — property-sheet component descriptor

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 183).

- **Inputs** — Static component identity
- **Outputs** — BGSPropertySheet_Component descriptor
- **Conditions** — Pinned retail 1.16.244.0; definition-only fallback scope in resource-intervals.md
- **Effects** — Thread-safe lazy descriptor initialization
- **Mapped edges** — 1409403e0 and CONT component getter -> descriptor
- **Limits** — No actual current override/effective-state or realized-output observation
- **Source assessment** — STATIC instruction and definition linkage; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 183) · `N182`

## RVA 0x0044b610

**Test property presence** · Level C · preferred VA `0x14044b610`

Recorded scope — Admission accepts an existing property even when its value is zero.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 52)
- [docs · function register](../function-register.md) (line 31) · `SOR-FN-0063` · Resource-property presence check

## RVA 0x0044b670

**extra property value lookup** · Level B · preferred VA `0x14044b670`

Analysis labels recorded in the original sources are `FUN_14044b670`.

Recorded scope — extra property value lookup

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 140).

- **Inputs** — Property state and AV pointer
- **Outputs** — Matching row float at +10 or zero
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Reads property rows
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 140) · `N139`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 73) · Read ExtraE1 property value
  Selects matching pointer row's +0x10.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 80)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 108)
- [resource retained population · d5v sources](../experiments/resource-retained-population/d5v-sources.csv) (line 125) · `V-S124`
- [docs · function register](../function-register.md) (line 125) · `SOR-FN-0045`
  Original group scope — Property/binding/fallback radius; live overrides unresolved

## RVA 0x00452e20

**raw property-sheet loading** · Level B · preferred VA `0x140452e20`

Analysis labels recorded in the original sources are `FUN_140452e20`.

Recorded scope — raw property-sheet loading

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 178).

- **Inputs** — Sheet storage and ESM reader
- **Outputs** — 12-byte serialized rows become 24-byte native rows; float preserved
- **Conditions** — Pinned retail 1.16.244.0; definition-only fallback scope in resource-intervals.md
- **Effects** — Allocates/resizes sheet; reads data
- **Mapped edges** — CONT loader -> this -> 1404536c0
- **Limits** — No actual current override/effective-state or realized-output observation
- **Source assessment** — STATIC instruction and definition linkage; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 178) · `N177`

## RVA 0x004536c0

**property-row insertion** · Level B · preferred VA `0x1404536c0`

Analysis labels recorded in the original sources are `FUN_1404536c0`.

Recorded scope — property-row insertion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 179).

- **Inputs** — Native sheet and source row
- **Outputs** — Verbatim float at native row+10
- **Conditions** — Pinned retail 1.16.244.0; definition-only fallback scope in resource-intervals.md
- **Effects** — Appends row and moves identity slots
- **Mapped edges** — Raw loader/copy -> this -> base-sheet getter
- **Limits** — No actual current override/effective-state or realized-output observation
- **Source assessment** — STATIC instruction and definition linkage; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 179) · `N178`

## RVA 0x00453740

**property-sheet copy** · Level B · preferred VA `0x140453740`

Analysis labels recorded in the original sources are `FUN_140453740`.

Recorded scope — property-sheet copy

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 180).

- **Inputs** — Destination/source sheets
- **Outputs** — Value-preserving copied rows; identity encoding handled separately
- **Conditions** — Pinned retail 1.16.244.0; definition-only fallback scope in resource-intervals.md
- **Effects** — Allocates/appends rows
- **Mapped edges** — Copy wrapper -> this -> 1404536c0
- **Limits** — No actual current override/effective-state or realized-output observation
- **Source assessment** — STATIC instruction and definition linkage; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 180) · `N179`

## RVA 0x0048eba0

**Get facility base property sheet** · Level C · preferred VA `0x14048eba0`

Recorded scope — Called from generic and organic facility candidate selection.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [fabricators · native](../experiments/fabricators/native.md) (line 31)
- [resource retained population · d5v sources](../experiments/resource-retained-population/d5v-sources.csv) (line 109) · `V-S108`

## RVA 0x0049a430

**actor-value singleton accessor** · Level B · preferred VA `0x14049a430`

Analysis labels recorded in the original sources are `FUN_14049a430`.

Recorded scope — actor-value singleton accessor

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 184).

- **Inputs** — Static singleton state
- **Outputs** — Singleton at 1461de020
- **Conditions** — Pinned retail 1.16.244.0
- **Effects** — Lazy initializes via 140d96b20
- **Mapped edges** — 140b82b40 -> singleton+108 comparison; resource-intervals.md
- **Limits** — Only relevant Health field inspected; not complete registry semantics
- **Source assessment** — STATIC instruction plus named registration; STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 184) · `N183`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 44) · Get actor-value registry
  Supplies singleton storing OrganicResourceType at +0x4c8.
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 13)

## RVA 0x004bcc80

**UI float copy and dirty setter** · Level B · preferred VA `0x1404bcc80`

Analysis labels recorded in the original sources are `FUN_1404bcc80`.

Recorded scope — UI float copy and dirty setter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 170).

- **Inputs** — TUIValue and float source
- **Outputs** — Unchanged binary32 value
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Writes value and dirty notification
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 170) · `N169`

## RVA 0x0051c5d0

**Participate in CrewExtraData E2 access** · Level C · preferred VA `0x14051c5d0`

Recorded scope — Participate in CrewExtraData E2 access

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 18)

## RVA 0x0051c800

**Participate in CrewExtraData E2 access** · Level C · preferred VA `0x14051c800`

Recorded scope — Participate in CrewExtraData E2 access

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 18)

## RVA 0x00531b10

**extra flags mask reader** · Level B · preferred VA `0x140531b10`

Analysis labels recorded in the original sources are `FUN_140531b10`.

Recorded scope — extra flags mask reader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 75).

- **Inputs** — RCX extra list; EDX mask
- **Outputs** — AL mask presence in Extra 9C+18
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — Locked traversal and release
- **Limits** — Missing extra returns false; saved/current distinction
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 75) · `N74`
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 39) · Read current power flag
  Locks the reference extra list, finds type 9c and tests mask 0x40 at extra +0x18; missing extra yields false.

## RVA 0x00593280

**Enumerate actor-value definitions** · Level C · preferred VA `0x140593280`

Recorded scope — Generic zero OrganicResourceType branch enumerates form definitions.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [fabricators · native](../experiments/fabricators/native.md) (line 34)
- [resource retained population · d5ad input provenance](../experiments/resource-retained-population/d5ad-input-provenance.md) (line 159)
  Original report discusses this roster entry under Grid, terrain and density preparation.
- [resource retained population · d5ae eligibility readiness map](../experiments/resource-retained-population/d5ae-eligibility-readiness-map.md) (line 51)
  Original report discusses this roster entry under D5AD handoff and contrary cases.
- [resource retained population · d5ae investigation ledger](../experiments/resource-retained-population/d5ae-investigation-ledger.md) (line 37)
  Original report discusses this roster entry under Dependency and readiness refinement checkpoint.
- [resource retained population · d5ae sources](../experiments/resource-retained-population/d5ae-sources.csv) (line 2) · `D5AE-N001`
- [resource retained population · d5af sources](../experiments/resource-retained-population/d5af-sources.csv) (line 2) · `D5AF-I001`

## RVA 0x005e9000

**Expand special product** · Level C · preferred VA `0x1405e9000`

Recorded scope — Used in the type-0x3f product branch.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 162)

## RVA 0x005f7280

**Participate in a production event branch** · Level C · preferred VA `0x1405f7280`

Recorded scope — Participate in a production event branch

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 148)

## RVA 0x005f7a80

**planet subordinate range** · Level B · preferred VA `0x1405f7a80`

Analysis labels recorded in the original sources are `FUN_1405f7a80`.

Recorded scope — planet subordinate range

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 192).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — planet subordinate range
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 192) · `N191`

## RVA 0x006695c0

**power applicability predicate** · Level B · preferred VA `0x1406695c0`

Analysis labels recorded in the original sources are `FUN_1406695c0`.

Recorded scope — power applicability predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 76).

- **Inputs** — RCX reference; keyword and AV defaults
- **Outputs** — AL applicability
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — Keyword/AV interface; temporary release
- **Limits** — No power-flow or switch tracing
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 76) · `N75`
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 40) · Test power applicability
  Checks a reference keyword then an actor value; gates whether the production reason evaluator consults current power.
- [power · native](../experiments/power/native.md) (line 41) · Test power applicability
  Accepts the keyword or effective actor value; this is independent of current powered state.

## RVA 0x007b75b0

**scanner species update wrapper** · Level B · preferred VA `0x1407b75b0`

Analysis labels recorded in the original sources are `FUN_1407b75b0`.

Recorded scope — scanner species update wrapper

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 215).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — scanner species update wrapper
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 215) · `N214`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 85) · Derive context for scan update
  Obtains planetary/reference context before updating species state.

## RVA 0x007b77d0

**increment scans and grant keyword prefix** · Level B · preferred VA `0x1407b77d0`

Analysis labels recorded in the original sources are `FUN_1407b77d0`.

Recorded scope — increment scans and grant keyword prefix

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 216).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — increment scans and grant keyword prefix
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 216) · `N215`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 86) · Update natural scan state
  Updates species count and derived progress/keyword state.

## RVA 0x00839820

**body time scalar wrapper** · Level B · preferred VA `0x140839820`

Analysis labels recorded in the original sources are `FUN_140839820`.

Recorded scope — body time scalar wrapper

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 154).

- **Inputs** — Body identifier; Boolean
- **Outputs** — Body lookup conversion or fallback
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Acquires manager read context
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 154) · `N153`

## RVA 0x00839900

**body time conversion provider** · Level B · preferred VA `0x140839900`

Analysis labels recorded in the original sources are `FUN_140839900`.

Recorded scope — body time conversion provider

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 155).

- **Inputs** — Lookup context; body identifier
- **Outputs** — 24 divided by absolute body scalar or fallback
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Manager queries; body source interpretation bounded
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 155) · `N154`

## RVA 0x00910690

**Derive reference planetary context** · Level C · preferred VA `0x140910690`

Analysis labels recorded in the original sources are `FUN_140910690`.

Recorded scope — Fallback derives reference cell, world, location and planet context.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 45)
- [limits · functions](../experiments/limits/functions.csv) (line 41)
- [limits · functions](../experiments/limits/functions.csv) (line 45)
- [limits · native](../experiments/limits/native.md) (line 198)
  Original report discusses this roster entry under Planetary Habitation: exact environment predicates.
- [docs · function register](../function-register.md) (line 139) · `SOR-FN-0038`
  Original group scope — Cached/active-world/fallback; body-space consumer also quantizes; no subcell proof

## RVA 0x009403e0

**base property-sheet component resolution** · Level B · preferred VA `0x1409403e0`

Analysis labels recorded in the original sources are `FUN_1409403e0`.

Recorded scope — base property-sheet component resolution

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 182).

- **Inputs** — Base object and manager/provider context
- **Outputs** — Existing component or provider-resolved fallback
- **Conditions** — Pinned retail 1.16.244.0; definition-only fallback scope in resource-intervals.md
- **Effects** — Reads component registry
- **Mapped edges** — 140b82b40 -> this -> component getter
- **Limits** — No actual current override/effective-state or realized-output observation
- **Source assessment** — STATIC instruction and definition linkage; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 182) · `N181`

## RVA 0x009e7770

**Reset the native IRES definition state** · Level C · preferred VA `0x1409e7770`

Recorded scope — Reset the native IRES definition state

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 56)

## RVA 0x009e8700

**Enumerate positive resource actor values** · Level C · preferred VA `0x1409e8700`

Recorded scope — Supplies currently selected resources to the recipe availability routine.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 196)
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 28) · `D5AH-XN027`
- [resource retained population · d5v investigation ledger](../experiments/resource-retained-population/d5v-investigation-ledger.md) (line 102)
  Original report discusses this roster entry under Mechanism and validation checkpoint.
- [resource retained population · d5v lifecycle consumer map](../experiments/resource-retained-population/d5v-lifecycle-consumer-map.md) (line 66)
  Original report discusses this roster entry under Native geometry → area, catalogue and extractor decisions.
- [resource retained population · d5v sources](../experiments/resource-retained-population/d5v-sources.csv) (line 100) · `V-S099`

## RVA 0x009e8b70

**Enumerate fauna resource candidates** · Level C · preferred VA `0x1409e8b70`

Recorded scope — Looks through resource AV/IRES properties and template contexts.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 48)
- [resource retained population · d5v sources](../experiments/resource-retained-population/d5v-sources.csv) (line 124) · `V-S123`

## RVA 0x009e8f20

**fallback resource property collector** · Level B · preferred VA `0x1409e8f20`

Analysis labels recorded in the original sources are `FUN_1409e8f20`.

Recorded scope — fallback resource property collector

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 231).

- **Inputs** — RCX closure; RDX AVIF
- **Outputs** — collection/continuation result
- **Conditions** — Pinned retail 1.16.244.0; Initialized property providers and vector
- **Effects** — Reads several property contexts and positive base fallback; appends IRES
- **Mapped edges** — 1409ea490 -> this
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 231) · `N230`

## RVA 0x009e9640

**property-linked recipe capability** · Level B · preferred VA `0x1409e9640`

Analysis labels recorded in the original sources are `FUN_1409e9640`.

Recorded scope — property-linked recipe capability

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 230).

- **Inputs** — RCX closure; RDX AVIF
- **Outputs** — Boolean capability/continuation
- **Conditions** — Pinned retail 1.16.244.0; AVIF category 9; linked IRES; property sheet
- **Effects** — Reads property presence and recipe/product/ingredient count
- **Mapped edges** — 1409ea3f0 -> this
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 230) · `N229`

## RVA 0x009e9700

**Recognize recipe-bearing resources** · Level C · preferred VA `0x1409e9700`

Recorded scope — Extends positive resource enumeration with recipe-bearing resource handling.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [fabricators · native](../experiments/fabricators/native.md) (line 26)

## RVA 0x009e97a0

**first selected source product set** · Level B · preferred VA `0x1409e97a0`

Analysis labels recorded in the original sources are `FUN_1409e97a0`.

Recorded scope — first selected source product set

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 233).

- **Inputs** — RCX result storage; RDX source reference
- **Outputs** — owned set of product or component IRES identities
- **Conditions** — Pinned retail 1.16.244.0; Positive resource enumeration; first valid recipe/product
- **Effects** — Allocates identity set; caller owns cleanup
- **Mapped edges** — 1409e9960 -> this -> 1409e8700
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 233) · `N232`
- [fabricators · native](../experiments/fabricators/native.md) (line 149) · Enumerate positive source resources
  Supports incoming compatibility, including component resources in the special product path.

## RVA 0x009e9960

**source product ingredient compatibility** · Level B · preferred VA `0x1409e9960`

Analysis labels recorded in the original sources are `FUN_1409e9960`.

Recorded scope — source product ingredient compatibility

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 232).

- **Inputs** — RCX source reference; RDX ingredient form
- **Outputs** — Boolean structural match
- **Conditions** — Pinned retail 1.16.244.0; Resolvable selected source product and ingredient identities
- **Effects** — Allocates and releases product identity set; compares IRES or component-list identities
- **Mapped edges** — 140f81000/140f84470 -> this -> 1409e97a0
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 232) · `N231`
- [fabricators · native](../experiments/fabricators/native.md) (line 146) · Enumerate compatible source component resources
  Used in incoming-builder compatibility; relationship is scoped to documented resource cases.

## RVA 0x009ea3f0

**generic recipe-capability fallback callback** · Level B · preferred VA `0x1409ea3f0`

Analysis labels recorded in the original sources are `FUN_1409ea3f0`.

Recorded scope — generic recipe-capability fallback callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 227).

- **Inputs** — Callback closure; AVIF
- **Outputs** — continue/stop result from property recipe-capability predicate
- **Conditions** — Pinned retail 1.16.244.0; Existing AVIF and property sheet
- **Effects** — Reads category/flags; calls capability helper
- **Mapped edges** — 140f859d0 fallback -> this -> 1409e9640
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 227) · `N226`
- [fabricators · native](../experiments/fabricators/native.md) (line 45) · Evaluate generic resource capability
  Callback used on the capability branch before property admission.

## RVA 0x009ea490

**generic fallback resource collection callback** · Level B · preferred VA `0x1409ea490`

Analysis labels recorded in the original sources are `FUN_1409ea490`.

Recorded scope — generic fallback resource collection callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 228).

- **Inputs** — Callback closure; AVIF
- **Outputs** — owned candidate resource vector
- **Conditions** — Pinned retail 1.16.244.0; Existing AVIF and property contexts
- **Effects** — Reads category/flags and selected/base property state
- **Mapped edges** — 140f859d0 fallback -> this -> 1409e8f20
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 228) · `N227`
- [fabricators · native](../experiments/fabricators/native.md) (line 45) · Evaluate alternate generic resource capability
  Callback used on the capability branch before property admission.

## RVA 0x009ea530

**positive-resource enumeration callback** · Level B · preferred VA `0x1409ea530`

Analysis labels recorded in the original sources are `FUN_1409ea530`.

Recorded scope — positive-resource enumeration callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 229).

- **Inputs** — Callback closure; AVIF
- **Outputs** — selected IRES entries
- **Conditions** — Pinned retail 1.16.244.0; Reference and initialized AV/property providers
- **Effects** — Filters resource AV category/flags; calls selected-resource helper
- **Mapped edges** — 1409e8700 -> this -> 1409e8950
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 229) · `N228`
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 29) · `D5AH-XN028`
- [resource retained population · d5v investigation ledger](../experiments/resource-retained-population/d5v-investigation-ledger.md) (line 102)
  Original report discusses this roster entry under Mechanism and validation checkpoint.
- [resource retained population · d5v lifecycle consumer map](../experiments/resource-retained-population/d5v-lifecycle-consumer-map.md) (line 66)
  Original report discusses this roster entry under Native geometry → area, catalogue and extractor decisions.
- [resource retained population · d5v sources](../experiments/resource-retained-population/d5v-sources.csv) (line 108) · `V-S107`

## RVA 0x00a19cd0

**CONT component retrieval** · Level B · preferred VA `0x140a19cd0`

Analysis labels recorded in the original sources are `FUN_140a19cd0`.

Recorded scope — CONT component retrieval

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 181).

- **Inputs** — CONT object and component descriptor
- **Outputs** — BGSPropertySheet at base+118
- **Conditions** — Pinned retail 1.16.244.0; definition-only fallback scope in resource-intervals.md
- **Effects** — Reads descriptors and base pointer
- **Mapped edges** — Base component provider -> sheet
- **Limits** — No actual current override/effective-state or realized-output observation
- **Source assessment** — STATIC instruction and definition linkage; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 181) · `N180`

## RVA 0x00a1a140

**CONT PRPS dispatch** · Level B · preferred VA `0x140a1a140`

Analysis labels recorded in the original sources are `FUN_140a1a140`.

Recorded scope — CONT PRPS dispatch

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 177).

- **Inputs** — CONT object; current subrecord
- **Outputs** — BGSPropertySheet storage at CONT+118+8
- **Conditions** — Pinned retail 1.16.244.0; definition-only fallback scope in resource-intervals.md
- **Effects** — Dispatches PRPS to raw loader
- **Mapped edges** — CONT -> 140452e20
- **Limits** — No actual current override/effective-state or realized-output observation
- **Source assessment** — STATIC instruction and definition linkage; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 177) · `N176`

## RVA 0x00b21fd0

**Construct reference actor-value interface** · Level C · preferred VA `0x140b21fd0`

Recorded scope — Installs the reference actor-value-owner table at +0x70.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 68)
- [resource retained population · d5s query winner model](../experiments/resource-retained-population/d5s-query-winner-model.md) (line 43)
  Original report discusses this roster entry under Preparation and the two service pumps.
- [resource retained population · d5s sources](../experiments/resource-retained-population/d5s-sources.csv) (line 144) · `D5S-F140b21fd0`

## RVA 0x00b5d040

**Insert expanded product** · Level C · preferred VA `0x140b5d040`

Recorded scope — Insertion helper used after special product expansion.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 162)

## RVA 0x00b63d40

**Count available ingredient** · Level C · preferred VA `0x140b63d40`

Recorded scope — Supports ordinary ingredient availability across sources.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 199)

## RVA 0x00b647d0

**Refresh after creation** · Level C · preferred VA `0x140b647d0`

Recorded scope — Follows the D8 dispatch in the observed ordinary creation path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 171)

## RVA 0x00b6bba0

**Count special resource ingredient** · Level C · preferred VA `0x140b6bba0`

Recorded scope — IRES-special availability path for the recipe cap.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 200)

## RVA 0x00b6cb60

**reference modifier extra provider** · Level B · preferred VA `0x140b6cb60`

Analysis labels recorded in the original sources are `FUN_140b6cb60`.

Recorded scope — reference modifier extra provider

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 137).

- **Inputs** — Reference
- **Outputs** — ExtraBF value state or null
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Locks extra list
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 137) · `N136`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 73) · Select ExtraBF
  Supplies the modifier container for the reference getter.

## RVA 0x00b6cbe0

**get/create ExtraBF storage** · Level B · preferred VA `0x140b6cbe0`

Analysis labels recorded in the original sources are `FUN_140b6cbe0`.

Recorded scope — get/create ExtraBF storage

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 209).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — get/create ExtraBF storage
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 209) · `N208`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 238) · Get or create ExtraBF
  Returns the reference actor-value storage used by the setter.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 66)
- [build budget · native](../experiments/build-budget/native.md) (line 125)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 13)

## RVA 0x00b6ce20

**reference effective AV getter** · Level B · preferred VA `0x140b6ce20`

Analysis labels recorded in the original sources are `FUN_140b6ce20`.

Recorded scope — reference effective AV getter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 135).

- **Inputs** — Reference+70 and AV pointer
- **Outputs** — Binary32 base plus modifier total; owner redirection for type 3
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Resolves owner; reads extras and modifier state
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 135) · `N134`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 69) · Get effective reference actor value
  Ordinary path adds modifier total to base; type 3 can redirect to an owner.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 77)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 14)

## RVA 0x00b6cfa0

**reference base AV getter** · Level B · preferred VA `0x140b6cfa0`

Analysis labels recorded in the original sources are `FUN_140b6cfa0`.

Recorded scope — reference base AV getter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 136).

- **Inputs** — Reference+70 and AV pointer
- **Outputs** — Default or explicit override plus qualified property sources
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Locks and reads extra/base sources
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 136) · `N135`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 70) · Get base reference actor value
  Starts from AVIF +0x178, can use an explicit ExtraBF override and adds qualified property values.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 78)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 89)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 16)

## RVA 0x00b6d190

**set reference base actor value** · Level B · preferred VA `0x140b6d190`

Analysis labels recorded in the original sources are `FUN_140b6d190`.

Recorded scope — set reference base actor value

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 208).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — set reference base actor value
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 208) · `N207`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 238) · Set reference actor base value
  Reference AV-owner virtual +0x20 updates ExtraBF and marks a reference change.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 64)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 101)
- [build budget · native](../experiments/build-budget/native.md) (line 125)
  Original report discusses this roster entry under Mutations, movement and restored state.

## RVA 0x00b70a80

**general insertion fit count** · Level B · preferred VA `0x140b70a80`

Analysis labels recorded in the original sources are `FUN_140b70a80`.

Recorded scope — general insertion fit count

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 158).

- **Inputs** — Destination; product; requested count
- **Outputs** — Capacity-fit integer count
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Queries weight and capacity
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 158) · `N157`
- [storage · functions](../experiments/storage/functions.csv) (line 4) · `S1-003` · ordinary positive capacity insertion fit count
- [storage · functions](../experiments/storage/functions.csv) (line 38) · `S1C-001` · theoretical fit count

## RVA 0x00b82b40

**base-sheet AV value provider** · Level B · preferred VA `0x140b82b40`

Analysis labels recorded in the original sources are `FUN_140b82b40`.

Recorded scope — base-sheet AV value provider

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 141).

- **Inputs** — Manager; base pointer; AV pointer
- **Outputs** — Matching base-sheet float plus separate Health branch
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Manager protection; reference accounting
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 141) · `N140`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 73) · Read base-sheet property value
  Selects matching +0x10 under manager protection.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 79)
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 52)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 118)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 21)
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 30) · `D5AH-XN029`

## RVA 0x00b97bd0

**Perform bookkeeping on the production path** · Level C · preferred VA `0x140b97bd0`

Recorded scope — Perform bookkeeping on the production path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 107)

## RVA 0x00b9bdf0

**Emit builder-selection event** · Level C · preferred VA `0x140b9bdf0`

Recorded scope — Used for dispatch in the selection route.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 162)

## RVA 0x00bee540

**HasPerk nonzero rank Boolean evaluator** · Level B · preferred VA `0x140bee540`

Analysis labels recorded in the original sources are `FUN_140bee540`.

Recorded scope — HasPerk nonzero rank Boolean evaluator

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 220).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — HasPerk nonzero rank Boolean evaluator
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 220) · `N219`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 75) · Test actor perk
  Target of the observed HasPerk callback.

## RVA 0x00c05610

**IsPowered numeric condition** · Level B · preferred VA `0x140c05610`

Analysis labels recorded in the original sources are `FUN_140c05610`.

Recorded scope — IsPowered numeric condition

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 74).

- **Inputs** — Reference wrapper; R9 float output
- **Outputs** — Numeric current powered view; AL evaluation status
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140531b10 mask 40; extra-list access
- **Limits** — Null path may preserve output; not network sufficiency
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 74) · `N73`

## RVA 0x00c07e70

**Research completion state condition query** · Level B · preferred VA `0x140c07e70`

Analysis labels recorded in the original sources are `FUN_140c07e70`.

Recorded scope — Research completion state condition query

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 134).

- **Inputs** — Project context; float result
- **Outputs** — Status2 float Boolean
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Same manager state; full descriptor binding bounded
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 134) · `N133`

## RVA 0x00c411c0

**HasPerk condition adapter** · Level B · preferred VA `0x140c411c0`

Analysis labels recorded in the original sources are `FUN_140c411c0`.

Recorded scope — HasPerk condition adapter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 219).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — HasPerk condition adapter
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 219) · `N218`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 75) · Evaluate HasPerk condition
  Registered command callback delegates to the perk test and supplies a numeric true result on success.

## RVA 0x00c59ab0

**CanProduceForWorkshop condition** · Level B · preferred VA `0x140c59ab0`

Analysis labels recorded in the original sources are `FUN_140c59ab0`.

Recorded scope — CanProduceForWorkshop condition

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 79).

- **Inputs** — R8 reference; stack float output
- **Outputs** — Float 1 if reason zero; AL evaluation status
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f7d120
- **Limits** — No runtime sample
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 79) · `N78`
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 14)
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 48)
  Original report discusses this roster entry under Actual causal chain.

## RVA 0x00ca3670

**Compare entries during perk cache insertion** · Level C · preferred VA `0x140ca3670`

Recorded scope — Compare entries during perk cache insertion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 97)

## RVA 0x00d83ae0

**required fauna scans from player and settings** · Level B · preferred VA `0x140d83ae0`

Analysis labels recorded in the original sources are `FUN_140d83ae0`.

Recorded scope — required fauna scans from player and settings

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 218).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — required fauna scans from player and settings
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 218) · `N217`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 96) · Read fauna scan requirement
  Fauna helper reads required scan count.

## RVA 0x00d83b80

**required flora scans from player and settings** · Level B · preferred VA `0x140d83b80`

Analysis labels recorded in the original sources are `FUN_140d83b80`.

Recorded scope — required flora scans from player and settings

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 217).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — required flora scans from player and settings
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 217) · `N216`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 96) · Read flora scan requirement
  Flora helper reads required scan count.

## RVA 0x00d96b20

**built-in AV registry initialization** · Level B · preferred VA `0x140d96b20`

Analysis labels recorded in the original sources are `FUN_140d96b20`.

Recorded scope — built-in AV registry initialization

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 130).

- **Inputs** — Registry object
- **Outputs** — Health pointer at+108
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 14049a430 returns1461de020
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 185).

- **Inputs** — Actor-value singleton
- **Outputs** — Health registration at singleton+108
- **Conditions** — Pinned retail 1.16.244.0
- **Effects** — Initializes AV registry; reads built-in name
- **Mapped edges** — 140b82b40 -> singleton+108 comparison; resource-intervals.md
- **Limits** — Only relevant Health field inspected; not complete registry semantics
- **Source assessment** — STATIC instruction plus named registration; STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 130) · `N129`
- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 185) · `N184` · built-in actor-value initialization Health field
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 21)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 22)

## RVA 0x00d9d170

**AVIF field loader** · Level B · preferred VA `0x140d9d170`

Analysis labels recorded in the original sources are `FUN_140d9d170`.

Recorded scope — AVIF field loader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 142).

- **Inputs** — AVIF and record reader
- **Outputs** — NAM0 bytes at object+178
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Definition load writes; not runtime query
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 142) · `N141`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 71) · Load actor-value definition default
  NAM0 reads up to four bytes into AVIF +0x178.

## RVA 0x00f34590

**cached Workshop summary reader** · Level B · preferred VA `0x140f34590`

Analysis labels recorded in the original sources are `FUN_140f34590`.

Recorded scope — cached Workshop summary reader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 167).

- **Inputs** — Output summary; Workshop reference
- **Outputs** — 24-byte summary from ExtraWorkshop+7c or zeros
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Validates Workshop and selects extra
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 167) · `N166`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 38)
- [build budget · report](../experiments/build-budget/report.md) (line 56)
  Original report discusses this roster entry under Causal path.

## RVA 0x00f4fa20

**Obtain ItemProduced event source** · Level C · preferred VA `0x140f4fa20`

Recorded scope — Used after ordinary creation; the creator also has a distinct early event branch.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 172)

## RVA 0x00f50660

**Serialize Workshop producer state** · Level C · preferred VA `0x140f50660`

Recorded scope — Part of the original save/load mapping for resource-keyed Workshop producer rows.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 61)
- [resource population lifecycle · native](../experiments/resource-population-lifecycle/native.csv) (line 11) · `N10` · ExtraWorkshop +0x20 object/resource map is distinct from ProcGen source map
  ExtraWorkshop +0x20 object/resource map is distinct from ProcGen source map
- [workshop origin · native map](../experiments/workshop-origin/native-map.csv) (line 5) · `SOR-FN-0042` · saver
  append +60 eight bytes then +68 four
- [build budget · functions](../experiments/build-budget/functions.csv) (line 74)
- [build budget · native](../experiments/build-budget/native.md) (line 154)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 61)
  Original report discusses this roster entry under What is serialized and reconstructed.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 4) · `D5AH-XN003`
- [docs · function register](../function-register.md) (line 122) · `SOR-FN-0042`
  Original group scope — Explicit +0x60/+0x68 save/load; buffer-version and variable-prefix conditions

## RVA 0x00f50880

**Restore Workshop extra and producer-map data** · Level C · preferred VA `0x140f50880`

Analysis labels recorded in the original sources are `FUN_140f50880`.

Recorded scope — The typed ExtraBC load path reads producer data; saved identities require remapping.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 61)
- [resource population lifecycle · native](../experiments/resource-population-lifecycle/native.csv) (line 12) · `N11` · Bounded Workshop restoration and task-trigger inspection; Save52 timing not joined
  Bounded Workshop restoration and task-trigger inspection; Save52 timing not joined
- [workshop origin · native map](../experiments/workshop-origin/native-map.csv) (line 6) · `SOR-FN-0042` · loader
  copy twelve bytes to +60 via 141865020
- [build budget · functions](../experiments/build-budget/functions.csv) (line 73)
- [build budget · native](../experiments/build-budget/native.md) (line 154)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 3) · `S2-002`
- [local output links · saves](../experiments/local-output-links/saves.md) (line 42)
  Original report discusses this roster entry under saves.
- [resource population lifecycle · native](../experiments/resource-population-lifecycle/native.md) (line 123)
  Original report discusses this roster entry under Save and initialization scope.
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 61)
  Original report discusses this roster entry under What is serialized and reconstructed.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 6) · `D5AH-XN005`
- [docs · function register](../function-register.md) (line 112) · `SOR-FN-0049`
  Original group scope — Workshop resource-prefix loading path
- [docs · function register](../function-register.md) (line 122) · `SOR-FN-0042`
  Original group scope — Explicit +0x60/+0x68 save/load; buffer-version and variable-prefix conditions

## RVA 0x00f7bd20

**Fold assigned actor and player production-timer modifiers** · Level A · preferred VA `0x140f7bd20`

Analysis labels recorded in the original sources are `FUN_140f7bd20`.

Applies eligible A1 entries to the current producer interval.

The timer enumerates the supplied Workshop E2 actors. It resolves each actor and gates by life state and Health, then dispatches `0x140c94060` and `0x140c93cf0` with active storage, assignment environment 2, selected-rank and producer context checks. Operation 3 `0x140c94430` multiplies the accumulating duration. Player dispatch follows the actor fold. Failed actor resolution retains the E2 slot on this path, unlike DB. Its interval is consumed at scheduler reset and does not itself create inventory. Full declaration and general caller population remain unknown.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 84).

- **Inputs** — Resource; producer context; modifier actor list
- **Outputs** — Binary32 interval returned through XMM0
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140c94060 entry point 0xa1
- **Limits** — Complete modifier arithmetic unresolved
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 84) · `N83` · effective resource interval
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 46) · Calculate production interval with actor context
  Uses IRES interval GLOB or fallback, scales by 3600 and dispatches eligible actor modifiers.
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 73)
  Applies eligible A1 entries to the current producer interval.
- [robots · effects](../experiments/robots/effects.md) (line 44)
  Applies eligible A1 entries to the current producer interval.
- [robots · lifecycle](../experiments/robots/lifecycle.md) (line 66)
  Applies eligible A1 entries to the current producer interval.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 48)
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 8)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 2)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 18)
  Original report discusses this roster entry under Assignment to a real query.
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 9)
  Original report discusses this roster entry under report.

## RVA 0x00f7bf10

**effective resource interval** · Level B · preferred VA `0x140f7bf10`

Analysis labels recorded in the original sources are `FUN_140f7bf10`.

Recorded scope — effective resource interval

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 143).

- **Inputs** — Resource; producer; Workshop
- **Outputs** — Timer times positive effective HarvesterRateMult or 1
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Resolves crew extra; dispatch bookkeeping
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 143) · `N142`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 56) · Compute effective production interval
  Combines actor-context interval with the current producer multiplier.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 47)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 173)
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 20)

## RVA 0x00f7bf80

**effective nominal rate per minute** · Level B · preferred VA `0x140f7bf80`

Analysis labels recorded in the original sources are `FUN_140f7bf80`.

Recorded scope — effective nominal rate per minute

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 144).

- **Inputs** — Resource; producer; Workshop
- **Outputs** — Binary32 60 divided by interval times effective resource AV
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Reads effective interval and resource AV
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 144) · `N143`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 83) · Compute nominal production per minute
  Combines effective resource quantity with effective interval for presentation.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 9)
- [build catalogue · production](../experiments/build-catalogue/production.md) (line 22)
  Original report discusses this roster entry under Actual expression and population.

## RVA 0x00f7c000

**effective harvester multiplier** · Level B · preferred VA `0x140f7c000`

Analysis labels recorded in the original sources are `FUN_140f7c000`.

Recorded scope — effective harvester multiplier

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 86).

- **Inputs** — Reference+70; resolved default 145eae2c0
- **Outputs** — Positive AV else 1
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f7f1e0 multiplier
- **Limits** — Negative raw PRPS not effective value
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 86) · `N85`
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 47) · Read effective interval multiplier
  Reads effective HarvesterRateMult and uses one unless the value is positive.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 77)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 174)

## RVA 0x00f7c1e0

**base resource interval** · Level B · preferred VA `0x140f7c1e0`

Analysis labels recorded in the original sources are `FUN_140f7c1e0`.

Recorded scope — base resource interval

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 85).

- **Inputs** — Resource+100 optional definition
- **Outputs** — Float hours multiplied by 3600
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — Resource definition or default 145ea7fe8
- **Limits** — Not final effective interval
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 85) · `N84`
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 46) · Convert production interval without actor dispatch
  Converts resource interval or fallback to seconds.

## RVA 0x00f7c210

**destination capacity gate** · Level B · preferred VA `0x140f7c210`

Analysis labels recorded in the original sources are `FUN_140f7c210`.

Recorded scope — destination capacity gate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 159).

- **Inputs** — Destination and context
- **Outputs** — Capacity no greater than current weight Boolean
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Reads current capacity/weight
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 159) · `N158`
- [storage · functions](../experiments/storage/functions.csv) (line 3) · `S1-002` · current full by capacity versus weight
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 103)
  Original report discusses this roster entry under Unload, return and production.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 3) · `D5AH-XN002`
- [storage · capacity native](../experiments/storage/capacity-native.md) (line 118)
  Original report discusses this roster entry under Fit computation does not enforce all generic additions.
- [storage · native](../experiments/storage/native.md) (line 32)
  Original report discusses this roster entry under Owner, weight and capacity.

## RVA 0x00f7cab0

**Test Builder category** · Level C · preferred VA `0x140f7cab0`

Analysis labels recorded in the original sources are `FUN_140f7cab0`.

Recorded scope — Part of the shared recipe-production categorization.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 153)
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 61)

## RVA 0x00f7cb70

**Test alternate production category** · Level C · preferred VA `0x140f7cb70`

Analysis labels recorded in the original sources are `FUN_140f7cb70`.

Recorded scope — One of the predicates selecting resource or recipe counting.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 153)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 82)
- [build catalogue · production](../experiments/build-catalogue/production.md) (line 21)
  Original report discusses this roster entry under Actual expression and population.
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 3)

## RVA 0x00f7cc70

**production halt predicate** · Level B · preferred VA `0x140f7cc70`

Analysis labels recorded in the original sources are `FUN_140f7cc70`.

Recorded scope — production halt predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 77).

- **Inputs** — RCX reference; default keyword
- **Outputs** — AL predicate; group checks
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f366c0; keyword queries
- **Limits** — Broader branches not all halt; setter/activation API unresolved
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 77) · `N76`
- [fabricators · native](../experiments/fabricators/native.md) (line 162) · Test production halt
  Tests OutpostProductionHalted through the reference and grouped members, feeding reason 9.
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 10)

## RVA 0x00f7d030

**Test production fuel category** · Level C · preferred VA `0x140f7d030`

Analysis labels recorded in the original sources are `FUN_140f7d030`.

Recorded scope — One of the predicates selecting resource or recipe counting.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 153)
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 62)
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 2)
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 52)
  Original report discusses this roster entry under Actual causal chain.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 2) · `D5AH-XN001`

## RVA 0x00f7d120

**Evaluate current producer eligibility reason** · Level A · preferred VA `0x140f7d120`

Analysis labels recorded in the original sources are `FUN_140f7d120`.

Selects a current production reason, with a charged-pad exception in mode 0.

The mapped routine checks activation/invalid state, halt, applicable power and other producer reasons. For a pad outside builder/extractor/generator categories, mode 0 with charge 2 bypasses the ingredient cap. Otherwise the admission-only cap `0x140f7f6f0` with null output vector and one requested cycle must find a cycle or reason 7 results. The Papyrus bridge `0x14206ab30` tests mode 0 reason against zero, whereas `0x140f7f1e0` passes mode 1 to force an ingredient recheck on its qualified path. The evaluator is distinct from the later stock-removal request. Exact declaration and unqualified reason semantics remain unknown.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 78).

- **Inputs** — RCX reference; DL mode
- **Outputs** — AL reason; zero eligible
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 1406695c0; 140531b10; 140f7cc70; 140f7f6f0
- **Limits** — Not actual produced count; helper side effects; unnamed reasons
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 78) · `N77` · current production reason evaluator
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 40)
  Selects a current production reason, with a charged-pad exception in mode 0.
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 49)
  Selects a current production reason, with a charged-pad exception in mode 0.
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 42) · Evaluate current production readiness
  RCX reference, DL mode, AL reason; zero is eligible. It may allocate and resolve or invalidate handles.
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 140)
  Selects a current production reason, with a charged-pad exception in mode 0.
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 69)
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 4)
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 43)
  Original report discusses this roster entry under Actual causal chain.
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 29)
- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 101)
  Original report discusses this roster entry under Damage and operational consequences.
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 65)
  Original report discusses this roster entry under What is serialized and reconstructed.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 19) · `D5AH-XN018`

## RVA 0x00f7d510

**Select production destination** · Level C · preferred VA `0x140f7d510`

Analysis labels recorded in the original sources are `FUN_140f7d510`.

Recorded scope — Called from the recipe/product stage of the shared creator.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 151)
- [storage · functions](../experiments/storage/functions.csv) (line 54) · `S1C-017` · production already-full destination selection
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 5) · `S2-004`
- [local output links · traces](../experiments/local-output-links/traces.md) (line 20)
  Original report discusses this roster entry under traces.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 21) · `D5AH-XN020`
- [storage · capacity native](../experiments/storage/capacity-native.md) (line 117)
  Original report discusses this roster entry under Fit computation does not enforce all generic additions.

## RVA 0x00f7d6a0

**Request due producer work and ingredient removal** · Level A · preferred VA `0x140f7d6a0`

Analysis labels recorded in the original sources are `FUN_140f7d6a0`.

Caps production to available ingredients and issues removal requests for a fueled cargo pad.

For a configured fueled pad, classification `0x140f7d030` and cap `0x140f7f6f0` produce removal rows. Each row is stride `0x10` with source handle `+0x00`, quantity `+0x04`, ingredient pointer `+0x08`. After ingredient-to-product resolution, source virtual displacement `+0x458` issues removal. The ordinary pinned recipe consumes five He-3 per accepted cycle on successful removal. A null product suppresses receiving output without canceling this withdrawal. Qualified callers are the shared scheduler and load-event pending replay `0x140f8c580`. The reviewed ship timer paths did not directly call it. Concurrent changes, removal failure behavior and a complete declaration remain unknown.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 87).

- **Inputs** — RCX producer; RDX resource; R8D due cycles
- **Outputs** — Recipe/product creation; ItemProducedEvent
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f7f6f0; 1405e9000; 140b5d040
- **Limits** — No guarantee of outgoing delivery; quantity closure qualified
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 87) · `N86` · unit production boundary
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 49)
  Caps production to available ingredients and issues removal requests for a fueled cargo pad.
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 120)
  Caps production to available ingredients and issues removal requests for a fueled cargo pad.
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 48) · Produce due resource or recipe units
  Takes producer, resource and due cycles; branches on recipe and product before insertion and event dispatch.
- [storage · functions](../experiments/storage/functions.csv) (line 55) · `S1C-018` · production request batch path
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 5)
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 51)
  Original report discusses this roster entry under Actual causal chain.
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 52)
  Original report discusses this roster entry under Actual causal chain.
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 124)
  Original report discusses this roster entry under Rate, lifecycle and modifiers.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 6) · `S2-005`
- [local output links · traces](../experiments/local-output-links/traces.md) (line 20)
  Original report discusses this roster entry under traces.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 20) · `D5AH-XN019`
- [storage · capacity native](../experiments/storage/capacity-native.md) (line 120)
  Original report discusses this roster entry under Fit computation does not enforce all generic additions.

## RVA 0x00f7dfa0

**producer row refresh** · Level B · preferred VA `0x140f7dfa0`

Analysis labels recorded in the original sources are `FUN_140f7dfa0`.

Recorded scope — producer row refresh

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 80).

- **Inputs** — Reference identity and Workshop context
- **Outputs** — Resource-keyed rows; cached eligibility
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f7d120; 140f51350
- **Limits** — Instruction cap possible; not current oracle
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 80) · `N79`
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 43) · Register resource-keyed producer row
  Uses Workshop context and resource identity to record reference handle, base ID and producer values.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 45)
- [build catalogue · production](../experiments/build-catalogue/production.md) (line 42)
  Original report discusses this roster entry under Actual expression and population.
- [build catalogue · production](../experiments/build-catalogue/production.md) (line 47)
  Original report discusses this roster entry under Actual expression and population.
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 18)
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 7) · `S2-006`
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 13)
  Original report discusses this roster entry under Positive lifecycle chain.
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 19)
  Original report discusses this roster entry under Positive lifecycle chain.
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 77)
  Original report discusses this roster entry under Unload, return and production.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 8) · `D5AH-XN007`

## RVA 0x00f7e6f0

**Workshop and transfer state serializer** · Level B · preferred VA `0x140f7e6f0`

Analysis labels recorded in the original sources are `FUN_140f7e6f0`.

Recorded scope — Workshop and transfer state serializer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 93).

- **Inputs** — Save writer context
- **Outputs** — Registered refs; destination and incoming sources
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 1402cedd0; 141868de0
- **Limits** — Saved IDs differ from runtime handles
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 93) · `N92`
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 75)
- [configuration ui · native](../experiments/cargo-links/configuration-ui/native.md) (line 176)
  Original report discusses this roster entry under Refresh, caches and persistence.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 9) · `S2-008`
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 64)
  Original report discusses this roster entry under What is serialized and reconstructed.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 24) · `D5AH-XN023`

## RVA 0x00f7ea10

**Workshop and transfer state restoration** · Level B · preferred VA `0x140f7ea10`

Analysis labels recorded in the original sources are `FUN_140f7ea10`.

Recorded scope — Workshop and transfer state restoration

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 94).

- **Inputs** — Save reader context
- **Outputs** — Rebuilt handles and destination-keyed sets
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 1402cef80; 140f87f00
- **Limits** — No actual current load observed
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 94) · `N93`
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 76)
- [configuration ui · native](../experiments/cargo-links/configuration-ui/native.md) (line 176)
  Original report discusses this roster entry under Refresh, caches and persistence.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 10) · `S2-009`
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 64)
  Original report discusses this roster entry under What is serialized and reconstructed.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 23) · `D5AH-XN022`

## RVA 0x00f7ef20

**Update registered Workshop producers** · Level A · preferred VA `0x140f7ef20`

Analysis labels recorded in the original sources are `FUN_140f7ef20`.

Passes caller-supplied elapsed time to producer rows for resolvable registered Workshops.

The mapped elapsed scalar arrives in `XMM1`. The function snapshots Workshop handles at `0x145916528`/`0x145916530`, resolves ExtraBC and obtains ExtraE2 before dispatching the producer updater `0x140f7f1e0`. The frame, wait/sleep and travel callers supply distinct conversions. A registered and resolvable owner is required in the mapped traversal. The general return meaning, full declaration and exact behavior for every unloaded object are unknown.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 82).

- **Inputs** — XMM1 elapsed scalar
- **Outputs** — Traverses registered handles and resource groups
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f7f1e0
- **Limits** — Full elapsed source/load policy unresolved
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 82) · `N81` · registered Workshop production update
- [inorganic extractors · arithmetic clocks](../experiments/inorganic-extractors/arithmetic-clocks.md) (line 8)
  Passes caller-supplied elapsed time to producer rows for resolvable registered Workshops.
- [inorganic extractors · arithmetic clocks](../experiments/inorganic-extractors/arithmetic-clocks.md) (line 16)
  Passes caller-supplied elapsed time to producer rows for resolvable registered Workshops.
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 44) · Traverse registered Workshops for production
  Consumes elapsed scalar in XMM1 and iterates resource-keyed Workshop maps under the registered-handle context.
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 81)
  Passes caller-supplied elapsed time to producer rows for resolvable registered Workshops.
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 77)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 18)
  Original report discusses this roster entry under Assignment to a real query.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 12) · `S2-011`
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 38)
  Original report discusses this roster entry under Positive lifecycle chain.
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 59)
  Original report discusses this roster entry under State-by-state result.
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 60)
  Original report discusses this roster entry under State-by-state result.
- [local output links · saves](../experiments/local-output-links/saves.md) (line 44)
  Original report discusses this roster entry under saves.

## RVA 0x00f7f1e0

**Advance one shared Workshop production schedule** · Level A · preferred VA `0x140f7f1e0`

Analysis labels recorded in the original sources are `FUN_140f7f1e0`.

Computes due cycles and conditionally dispatches production before refreshing interval state.

A row has stride `0x1c` with handle `+0x00`, base `+0x04`, integer pending bookkeeping `+0x08`, registration quantity `+0x0c`, binary32 remaining and interval at `+0x10/+0x14`, and cached eligibility `+0x18`. For positive interval with elapsed at least the interval, it uses truncated elapsed divided by interval without first subtracting remaining. Otherwise it subtracts elapsed from remaining and schedules one due cycle when nonpositive. The resolved-producer loop rechecks mode 1 reason `0x140f7d120` and only reason zero reaches `0x140f7d6a0`. A due-path reset refreshes both timer fields with effective modifiers and does not carry arbitrary phase or debt. An unresolved handle follows separate sentinel and integer-bookkeeping logic. Extractors, fabricators and fueled cargo markers share this scheduler in the cited paths. Full native declaration, universal timebase and extreme-float behavior remain unknown.

Scoped pseudocode abstraction. It covers the described branch and omits unqualified paths.

```text
Abstraction of ordinary row timing. Omitted cases include unresolved bases, nonzero reason bookkeeping and invalid floating-point inputs.

if interval > 0 and elapsed >= interval:
    due = truncate(elapsed / interval)
else:
    remaining = remaining - elapsed
    due = 1 if remaining <= 0 else 0
if due and producer resolves:
    for each registered iteration:
        if current_reason(mode = 1) == 0:
            request_production(due)
    refresh remaining and interval from current timer
```

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 83).

- **Inputs** — Resource key; row array; elapsed context
- **Outputs** — Countdown reload and production attempts
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f7d120; 140f7d6a0; 140f7bd20
- **Limits** — Actual effective counts not measured
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 83) · `N82` · producer countdown and due update
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 36)
  Computes due cycles and conditionally dispatches production before refreshing interval state.
- [fabricators · reuse](../experiments/fabricators/reuse.md) (line 15)
  Computes due cycles and conditionally dispatches production before refreshing interval state.
- [inorganic extractors · arithmetic clocks](../experiments/inorganic-extractors/arithmetic-clocks.md) (line 79)
  Computes due cycles and conditionally dispatches production before refreshing interval state.
- [inorganic extractors · arithmetic clocks](../experiments/inorganic-extractors/arithmetic-clocks.md) (line 113)
  Computes due cycles and conditionally dispatches production before refreshing interval state.
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 45) · Schedule due producer cycles
  Updates 0x1c-byte rows and invokes creation only when current readiness mode 1 returns zero.
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 117)
  Computes due cycles and conditionally dispatches production before refreshing interval state.
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 6)
- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 39)
  Original report discusses this roster entry under Actual causal chain.
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 3)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 67)
  Original report discusses this roster entry under Production clocks and remote scheduling.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 13) · `S2-012`
- [local output links · saves](../experiments/local-output-links/saves.md) (line 43)
  Original report discusses this roster entry under saves.

## RVA 0x00f7f6f0

**recipe resource-count selection** · Level B · preferred VA `0x140f7f6f0`

Analysis labels recorded in the original sources are `FUN_140f7f6f0`.

Recorded scope — recipe resource-count selection

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 88).

- **Inputs** — Producer; optional output vector; requested count
- **Outputs** — Bounded count and handle/count/form rows
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 1409e8700; 140f881c0
- **Limits** — Complex helper; decompiler types unreliable; no general formula
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 88) · `N87`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 154) · Cap production by recipe inputs
  Supplies input availability and consumption information for the shared producer.
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 7)

## RVA 0x00f80af0

**direct outgoing destination handles** · Level B · preferred VA `0x140f80af0`

Analysis labels recorded in the original sources are `FUN_140f80af0`.

Recorded scope — direct outgoing destination handles

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 91).

- **Inputs** — RDX source; R8 output vector
- **Outputs** — Destination handle vector
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — Scan destination map; source match; handle resolution
- **Limits** — Failed targets skipped; no live census
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 91) · `N90`
- [fabricators · native](../experiments/fabricators/native.md) (line 109) · Query direct outgoing destinations
  Reverses destination-to-source membership in the shared link registry.
- [configuration ui · functions](../experiments/cargo-links/configuration-ui/functions.csv) (line 47)
- [configuration ui · report](../experiments/cargo-links/configuration-ui/report.md) (line 15)
  Original report discusses this roster entry under report.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 14) · `S2-013`

## RVA 0x00f81000

**predict incompatible links for recipe** · Level B · preferred VA `0x140f81000`

Analysis labels recorded in the original sources are `FUN_140f81000`.

Recorded scope — predict incompatible links for recipe

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 203).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — predict incompatible links for recipe
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 203) · `N202`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 167) · Predict links affected by selection
  Checks incoming recipe ingredients and outgoing compatibility with the full candidate vector.

## RVA 0x00f81200

**insert directional transfer edge** · Level B · preferred VA `0x140f81200`

Analysis labels recorded in the original sources are `FUN_140f81200`.

Recorded scope — insert directional transfer edge

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 90).

- **Inputs** — RDX source; R8 destination
- **Outputs** — Destination map gains incoming source
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — Global 145916580 lock 1459165d0
- **Limits** — Mutation/cache refresh; no invocation authority
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 90) · `N89`
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 15) · `S2-014`

## RVA 0x00f81a90

**remove directional transfer edge** · Level B · preferred VA `0x140f81a90`

Analysis labels recorded in the original sources are `FUN_140f81a90`.

Recorded scope — remove directional transfer edge

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 92).

- **Inputs** — RDX source; R8 destination
- **Outputs** — Removes incoming source from destination
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 14207eb00 ->this; cache refresh
- **Limits** — Mutator never invoked
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 92) · `N91`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 175) · Remove incompatible link membership
  Used by the registration revalidation path before cleanup.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 16) · `S2-015`

## RVA 0x00f81cc0

**revalidate/prune links after resource change** · Level B · preferred VA `0x140f81cc0`

Analysis labels recorded in the original sources are `FUN_140f81cc0`.

Recorded scope — revalidate/prune links after resource change

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 204).

- **Inputs** — Workshop and producer context after selection
- **Outputs** — Compatibility-pruned incoming/outgoing links
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Removes edges; refreshes graph/cache
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 204) · `N203`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 170) · Revalidate links on registration
  Registration can remove at most one incompatible membership per invocation in the observed path.

## RVA 0x00f83900

**deregister selected resource row** · Level B · preferred VA `0x140f83900`

Analysis labels recorded in the original sources are `FUN_140f83900`.

Recorded scope — deregister selected resource row

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 202).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — deregister selected resource row
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 202) · `N201`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 153) · Deregister previous resource
  Called after setting the old resource AV to zero.

## RVA 0x00f83b90

**producer registration** · Level B · preferred VA `0x140f83b90`

Analysis labels recorded in the original sources are `FUN_140f83b90`.

Recorded scope — producer registration

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 81).

- **Inputs** — Workshop and producer reference context
- **Outputs** — 1c producer rows
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f7d120; 1409e9150
- **Limits** — Not exhaustive installed census
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 81) · `N80`
- [inorganic extractors · native](../experiments/inorganic-extractors/native.md) (line 43) · Register selected resource
  Feeds producer-row registration; shared with builder paths.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 46)
- [build catalogue · production](../experiments/build-catalogue/production.md) (line 42)
  Original report discusses this roster entry under Actual expression and population.
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 33)
  Original report discusses this roster entry under Placement and registration use distinct resource operations.
- [resource retained population · d5ah extractor ledger](../experiments/resource-retained-population/d5ah-extractor-ledger.md) (line 19)
  Original report discusses this roster entry under Native and saved-receipt checkpoint.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 7) · `D5AH-XN006`

## RVA 0x00f841c0

**outgoing destination compatibility** · Level B · preferred VA `0x140f841c0`

Analysis labels recorded in the original sources are `FUN_140f841c0`.

Recorded scope — outgoing destination compatibility

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 205).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — outgoing destination compatibility
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 205) · `N204`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 168) · Test outgoing builder link compatibility
  Walks stride-0x10 resource candidates and tests compatible destinations.

## RVA 0x00f843e0

**transfer topology guard wrapper** · Level B · preferred VA `0x140f843e0`

Analysis labels recorded in the original sources are `FUN_140f843e0`.

Recorded scope — transfer topology guard wrapper

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 235).

- **Inputs** — Endpoint references; internal context
- **Outputs** — existing traversal result
- **Conditions** — Pinned retail 1.16.244.0; Native handles and registry context
- **Effects** — Resolves endpoint handle and delegates graph traversal
- **Mapped edges** — 140f84470 -> this -> 140f894c0
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 235) · `N234`
- [fabricators · native](../experiments/fabricators/native.md) (line 155) · Guard output-link topology
  Delegates topology checking to existing traversal.
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 22) · `S2-021`
- [local output links · native](../experiments/local-output-links/native.md) (line 38)
  Original report discusses this roster entry under Directed identity and traversal.

## RVA 0x00f84470

**transfer endpoint compatibility decision** · Level B · preferred VA `0x140f84470`

Analysis labels recorded in the original sources are `FUN_140f84470`.

Recorded scope — transfer endpoint compatibility decision

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 234).

- **Inputs** — Source/destination references; internal context
- **Outputs** — zero allowed or category-specific reason
- **Conditions** — Pinned retail 1.16.244.0; Valid same-context refs; selected resources; category and graph state
- **Effects** — Reads selected recipes and structural supplier support; resolves references
- **Mapped edges** — 140f81cc0 -> this -> 1409e9960/140f841c0/140f843e0
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 234) · `N233`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 171) · Test incoming builder link compatibility
  Predicate used to revalidate incoming sources.
- [storage · functions](../experiments/storage/functions.csv) (line 2) · `S1-001` · ordered endpoint pair validator
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 23) · `S2-022`
- [storage · native](../experiments/storage/native.md) (line 90)
  Original report discusses this roster entry under Separate source and pair gates.
- [storage · native](../experiments/storage/native.md) (line 100)
  Original report discusses this roster entry under Separate source and pair gates.

## RVA 0x00f85900

**fauna domesticability** · Level B · preferred VA `0x140f85900`

Analysis labels recorded in the original sources are `FUN_140f85900`.

Recorded scope — fauna domesticability

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 194).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — fauna domesticability
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 194) · `N193`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 49) · Test domesticability
  Uses resolved keyword and can follow template or group ancestry.

## RVA 0x00f85970

**flora resource normalization** · Level B · preferred VA `0x140f85970`

Analysis labels recorded in the original sources are `FUN_140f85970`.

Recorded scope — flora resource normalization

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 195).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — flora resource normalization
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 195) · `N194`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 50) · Normalize flora product to IRES
  Accepts IRES or looks up a resource by recipe product equality.

## RVA 0x00f859d0

**organic selector list builder** · Level B · preferred VA `0x140f859d0`

Analysis labels recorded in the original sources are `FUN_140f859d0`.

Recorded scope — organic selector list builder

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 186).

- **Inputs** — RCX owned return vector; RDX Workshop; R8 base; R9B require-known
- **Outputs** — stride10 knowledge-byte and IRES-pointer choices
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Allocates/releases temporaries; may initialize dummy reference
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 186) · `N185`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 43) · Select facility resource candidates
  Takes output vector, Workshop, facility/base and require-known byte; branches flora, fauna and generic builder.

## RVA 0x00f85f80

**resource eligibility dedup fold** · Level B · preferred VA `0x140f85f80`

Analysis labels recorded in the original sources are `FUN_140f85f80`.

Recorded scope — resource eligibility dedup fold

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 196).

- **Inputs** — Fold context; IRES; knowledge byte
- **Outputs** — Boolean admission; deduplicated IRES vector with OR knowledge
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — May grow caller vector
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 196) · `N195`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 52) · Fold eligible facility resources
  Requires IRES recipe and presence of the associated facility property; deduplicates by pointer and combines knowledge.

## RVA 0x00f86170

**organic default selection initialization** · Level B · preferred VA `0x140f86170`

Analysis labels recorded in the original sources are `FUN_140f86170`.

Recorded scope — organic default selection initialization

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 197).

- **Inputs** — Producer; candidate vector; base context
- **Outputs** — First known resource selected if no current positive resource
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Writes AV and emits selection event
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 197) · `N196`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 112) · Auto-select known facility resource
  May select the first known candidate; this branch does not establish sorting.

## RVA 0x00f86360

**planet fauna candidates** · Level B · preferred VA `0x140f86360`

Analysis labels recorded in the original sources are `FUN_140f86360`.

Recorded scope — planet fauna candidates

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 188).

- **Inputs** — Return vector; Workshop reference
- **Outputs** — Planet NPC knowledge rows
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads manager under lease; resolves/retains references
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 188) · `N187`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 45) · Select planetary fauna candidates
  Gets planet key from Workshop Extra81 or reference context; reads guarded manager state.

## RVA 0x00f864c0

**planet flora candidates** · Level B · preferred VA `0x140f864c0`

Analysis labels recorded in the original sources are `FUN_140f864c0`.

Recorded scope — planet flora candidates

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 187).

- **Inputs** — Return vector; Workshop reference
- **Outputs** — Planet flora/resource/knowledge rows
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads planet/species manager under lease
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 187) · `N186`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 45) · Select planetary flora candidates
  Gets planet key from Workshop Extra81 or reference context; reads guarded manager state.

## RVA 0x00f86590

**flora resource and knowledge rows** · Level B · preferred VA `0x140f86590`

Analysis labels recorded in the original sources are `FUN_140f86590`.

Recorded scope — flora resource and knowledge rows

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 189).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — flora resource and knowledge rows
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 189) · `N188`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 47) · Normalize planetary flora rows
  Resolves species and resource IDs, applies FLOR fallback and deduplicates species/resource pairs.

## RVA 0x00f881c0

**incoming production source traversal** · Level B · preferred VA `0x140f881c0`

Analysis labels recorded in the original sources are `FUN_140f881c0`.

Recorded scope — incoming production source traversal

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 95).

- **Inputs** — Current producer/reference context
- **Outputs** — Reference candidates via incoming sources
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — Destination-keyed map 145916580
- **Limits** — Not direct outgoing lookup; quantity dependencies not universal closure
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 95) · `N94`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 198) · Collect transitive incoming references
  Collects eligible source references for ingredient availability.
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 9)

## RVA 0x00f894c0

**Traverse link topology** · Level C · preferred VA `0x140f894c0`

Analysis labels recorded in the original sources are `FUN_140f894c0`.

Recorded scope — Called by a separate guard after resource/category policy.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [fabricators · native](../experiments/fabricators/native.md) (line 156)
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 28) · `S2-027`
- [local output links · native](../experiments/local-output-links/native.md) (line 38)
  Original report discusses this roster entry under Directed identity and traversal.

## RVA 0x00f8a920

**Traverse domesticability ancestry** · Level C · preferred VA `0x140f8a920`

Recorded scope — Fallback ancestry path where direct keyword testing fails.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 49)

## RVA 0x00f8b530

**Match flora recipe product** · Level C · preferred VA `0x140f8b530`

Recorded scope — Supports first-match resource reverse lookup from flora product.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 50)

## RVA 0x00f8bbd0

**fauna knowledge rows** · Level B · preferred VA `0x140f8bbd0`

Analysis labels recorded in the original sources are `FUN_140f8bbd0`.

Recorded scope — fauna knowledge rows

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 190).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — fauna knowledge rows
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 190) · `N189`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 46) · Walk planetary fauna rows
  Traverses manager planet range and resolves and deduplicates NPC pointers.

## RVA 0x00f8be60

**manufactured catalogue callback** · Level B · preferred VA `0x140f8be60`

Analysis labels recorded in the original sources are `FUN_140f8be60`.

Recorded scope — manufactured catalogue callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 226).

- **Inputs** — RCX callback closure; RDX AVIF
- **Outputs** — continues enumeration; admits IRES with knowledge true
- **Conditions** — Pinned retail 1.16.244.0; AVIF category and flag; IRES backpointer; live property sheet
- **Effects** — Reads AVIF +160/+15c/+148; appends candidate through 140f85f80
- **Mapped edges** — 140f859d0 -> this -> 140f85f80
- **Limits** — No runtime observation; lifetime/thread/failure guarantees bounded by native.md
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 226) · `N225`
- [fabricators · native](../experiments/fabricators/native.md) (line 38) · Admit generic Builder candidate
  Concrete callback uses AVIF/IRES backpointer and common property admission.
- [fabricators · report](../experiments/fabricators/report.md) (line 29)
  Original report discusses this roster entry under What the game implements.

## RVA 0x00f8c580

**Replay eligible pending production on object load** · Level B · preferred VA `0x140f8c580`

Analysis labels recorded in the original sources are `FUN_140f8c580`.

Conditionally dispatches pending production for the matching producer row.

In the mapped true object-loaded branch, the routine matches the current producer handle and refreshes cached eligibility. It sends a nonzero pending batch to 0x140f7d6a0 only when eligible, then clears the pending count either way. A missing row can lead to registration. Recovery of a stale sentinel row remains unqualified. For cargo, this is the other mapped direct caller of the production boundary, alongside the elapsed scheduler. Its admission does not represent a voyage debit.

Original records

- [fuel · native](../experiments/cargo-links/fuel/native.md) (line 124)
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 61)
- [resource retained population · d5ah extractor continuity](../experiments/resource-retained-population/d5ah-extractor-continuity.md) (line 83)
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 17)
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 31) · `S2-030`
- [local output links · saves](../experiments/local-output-links/saves.md) (line 43)
  Original report discusses this roster entry under saves.
- [resource retained population · d5ah extractor sources](../experiments/resource-retained-population/d5ah-extractor-sources.csv) (line 22) · `D5AH-XN021`

## RVA 0x00f8ce70

**flora planet range traversal** · Level B · preferred VA `0x140f8ce70`

Analysis labels recorded in the original sources are `FUN_140f8ce70`.

Recorded scope — flora planet range traversal

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 191).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — flora planet range traversal
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 191) · `N190`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 46) · Walk manager planet range
  Ranges subordinate keys under a numeric planet key; facility biome is not an operand.

## RVA 0x01308640

**full scan and currently eligible info completeness** · Level B · preferred VA `0x141308640`

Analysis labels recorded in the original sources are `FUN_141308640`.

Recorded scope — full scan and currently eligible info completeness

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 225).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — full scan and currently eligible info completeness
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 225) · `N224`

## RVA 0x01308d40

**evaluate ordered scanner keyword conditions** · Level B · preferred VA `0x141308d40`

Analysis labels recorded in the original sources are `FUN_141308d40`.

Recorded scope — evaluate ordered scanner keyword conditions

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 213).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — evaluate ordered scanner keyword conditions
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 213) · `N212`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 78) · Build scanner candidate rows
  Consumes inputs from the scanner candidate parent.

## RVA 0x01308ee0

**rebuild species eligible keyword cache** · Level B · preferred VA `0x141308ee0`

Analysis labels recorded in the original sources are `FUN_141308ee0`.

Recorded scope — rebuild species eligible keyword cache

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 214).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — rebuild species eligible keyword cache
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 214) · `N213`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 78) · Build scanner candidates
  Feeds the scanner candidate construction chain.

## RVA 0x0130a3e0

**species knowledge membership** · Level B · preferred VA `0x14130a3e0`

Analysis labels recorded in the original sources are `FUN_14130a3e0`.

Recorded scope — species knowledge membership

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 193).

- **Inputs** — Manager and planet/species/category/output-bool request
- **Outputs** — Knowledge membership
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads knowledge set
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 193) · `N192`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 51) · Query planetary species knowledge
  Uses planet/species/category and output bool pointer; absent default object defaults to true.

## RVA 0x0136ac90

**Almanac row vector queue** · Level B · preferred VA `0x14136ac90`

Analysis labels recorded in the original sources are `FUN_14136ac90`.

Recorded scope — Almanac row vector queue

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 173).

- **Inputs** — Model state; input vector
- **Outputs** — Deep copied queued row vector
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Allocates command and retains model
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 173) · `N172`
- [locations outpost · native and ui](../experiments/locations-outpost/native-and-ui.md) (line 52) · Queue the outpost maximum
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 18) · `n019` · owned asynchronous aggregate handoff

## RVA 0x0136c980

**Almanac outpost field binder** · Level B · preferred VA `0x14136c980`

Analysis labels recorded in the original sources are `FUN_14136c980`.

Recorded scope — Almanac outpost field binder

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 175).

- **Inputs** — UI map object
- **Outputs** — fProductionPerMin binding
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Binds UI data fields
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 175) · `N174`
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 23) · `n006` · OutpostEntry row fields
- [build budget · functions](../experiments/build-budget/functions.csv) (line 12)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 5)

## RVA 0x013da8f0

**Call the producer power-upgrade transition** · Level C · preferred VA `0x1413da8f0`

Recorded scope — Call the producer power-upgrade transition

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 107)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 6)

## RVA 0x0143f690

**build status snapshot queue** · Level B · preferred VA `0x14143f690`

Analysis labels recorded in the original sources are `FUN_14143f690`.

Recorded scope — build status snapshot queue

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 168).

- **Inputs** — Status model; optional Workshop
- **Outputs** — Queued summary payload
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Reads current or explicit Workshop; queues copy
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 168) · `N167`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 34)
- [build budget · report](../experiments/build-budget/report.md) (line 56)
  Original report discusses this roster entry under Causal path.

## RVA 0x0143f8a0

**build status value adapter** · Level B · preferred VA `0x14143f8a0`

Analysis labels recorded in the original sources are `FUN_14143f8a0`.

Recorded scope — build status value adapter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 169).

- **Inputs** — Summary and model
- **Outputs** — Production summary+8 to float UI field
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Copies values and marks UI dirty
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 169) · `N168`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 43)
- [build budget · report](../experiments/build-budget/report.md) (line 56)
  Original report discusses this roster entry under Causal path.
- [build budget · ui](../experiments/build-budget/ui.md) (line 40)
  Original report discusses this roster entry under Numerator, denominator and native cache.

## RVA 0x0143fb40

**Workshop status field binder** · Level B · preferred VA `0x14143fb40`

Analysis labels recorded in the original sources are `FUN_14143fb40`.

Recorded scope — Workshop status field binder

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 176).

- **Inputs** — UI map object
- **Outputs** — fProduction binding
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Binds UI data fields
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 176) · `N175`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 11)

## RVA 0x0143fdc0

**build status queued consumer** · Level B · preferred VA `0x14143fdc0`

Analysis labels recorded in the original sources are `FUN_14143fdc0`.

Recorded scope — build status queued consumer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 171).

- **Inputs** — Queued command
- **Outputs** — Adapter call with payload+18
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Releases retained model
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 171) · `N170`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 39)
- [build budget · report](../experiments/build-budget/report.md) (line 56)
  Original report discusses this roster entry under Causal path.
- [build budget · ui](../experiments/build-budget/ui.md) (line 40)
  Original report discusses this roster entry under Numerator, denominator and native cache.

## RVA 0x01582340

**builder menu data producer** · Level B · preferred VA `0x141582340`

Analysis labels recorded in the original sources are `FUN_141582340`.

Recorded scope — builder menu data producer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 198).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — builder menu data producer
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 198) · `N197`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 110) · Build facility directory data
  Produces WorkshopBuilderDirectoryData for facility selection.

## RVA 0x01583410

**apply selected resource AV** · Level B · preferred VA `0x141583410`

Analysis labels recorded in the original sources are `FUN_141583410`.

Recorded scope — apply selected resource AV

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 201).

- **Inputs** — Model; selected COBJ FormID
- **Outputs** — Changed resource AV/producer registration and queued refresh
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Mutates AVs; deregisters/registers; emits events and link pruning
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 201) · `N200`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 151) · Apply facility resource selection
  Requires model associations and resolved Workshop; changes AV and resource registration.

## RVA 0x01586950

**builder item UI field binding** · Level B · preferred VA `0x141586950`

Analysis labels recorded in the original sources are `FUN_141586950`.

Recorded scope — builder item UI field binding

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 199).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — builder item UI field binding
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 199) · `N198`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 120) · Bind workshop build-item data
  Maps resource rows to BuildItemData presentation.

## RVA 0x01716e70

**Parse facility selection ID** · Level C · preferred VA `0x141716e70`

Recorded scope — Used by the selection event handler.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 150)

## RVA 0x01717fd0

**UI ChangeBuildItem event consumer** · Level B · preferred VA `0x141717fd0`

Analysis labels recorded in the original sources are `FUN_141717fd0`.

Recorded scope — UI ChangeBuildItem event consumer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 200).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — UI ChangeBuildItem event consumer
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 200) · `N199`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 150) · Handle facility resource selection event
  Parses ID and dispatches directly or through an engine-thread queue.

## RVA 0x01719040

**Queue facility resource selection apply** · Level C · preferred VA `0x141719040`

Recorded scope — Engine-thread route used by selection event.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 151)

## RVA 0x017cab70

**Supply engine frame elapsed** · Level C · preferred VA `0x1417cab70`

Recorded scope — Part of the frame production-caller path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [fabricators · native](../experiments/fabricators/native.md) (line 200)

## RVA 0x017cbbe0

**Supply frame elapsed to production** · Level C · preferred VA `0x1417cbbe0`

Recorded scope — Part of the frame production-caller path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [fabricators · native](../experiments/fabricators/native.md) (line 200)
- [inorganic extractors · arithmetic clocks](../experiments/inorganic-extractors/arithmetic-clocks.md) (line 38)
  Original report discusses this roster entry under Frame elapsed, calendar progression and skipped time differ.
- [resource retained population · d5s query winner model](../experiments/resource-retained-population/d5s-query-winner-model.md) (line 100)
  Original report discusses this roster entry under Invocation lifetime and a retirement interval.
- [resource retained population · d5s sources](../experiments/resource-retained-population/d5s-sources.csv) (line 153) · `D5S-F1417cbbe0`

## RVA 0x017cc1d0

**Schedule the frame update callback** · Level C · preferred VA `0x1417cc1d0`

Recorded scope — The frame loop schedules 0x1417cbbe0 through task and dependency machinery. This scoped edge supplies no general threading or pause contract.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · arithmetic clocks](../experiments/inorganic-extractors/arithmetic-clocks.md) (line 38)

## RVA 0x017eb150

**Resolve crew actors in the inspected E2 callback** · Level C · preferred VA `0x1417eb150`

Recorded scope — Resolve crew actors in the inspected E2 callback

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 42)

## RVA 0x01800f20

**research material/progress completion** · Level B · preferred VA `0x141800f20`

Analysis labels recorded in the original sources are `FUN_141800f20`.

Recorded scope — research material/progress completion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 132).

- **Inputs** — Project state; actor; bench; requirements
- **Outputs** — Status2; optional product/XP/events
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — RSPJ NNAM0 bypasses insertion
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 132) · `N131`

## RVA 0x01801ee0

**recursive Research Project completion** · Level B · preferred VA `0x141801ee0`

Analysis labels recorded in the original sources are `FUN_141801ee0`.

Recorded scope — recursive Research Project completion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 131).

- **Inputs** — Research manager; project state
- **Outputs** — Supplies remaining requirements
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 141800f20
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 131) · `N130`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 37)

## RVA 0x018778e0

**calendar elapsed consumer** · Level B · preferred VA `0x1418778e0`

Analysis labels recorded in the original sources are `FUN_1418778e0`.

Recorded scope — calendar elapsed consumer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 153).

- **Inputs** — Calendar; elapsed in XMM1
- **Outputs** — Scaled hours and carried calendar fields
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Writes calendar globals and emits events
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 153) · `N152`
- [transport · functions](../experiments/cargo-links/transport/functions.csv) (line 66)

## RVA 0x01887c90

**main frame clock producer** · Level B · preferred VA `0x141887c90`

Analysis labels recorded in the original sources are `FUN_141887c90`.

Recorded scope — main frame clock producer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 148).

- **Inputs** — Main state
- **Outputs** — QPC milliseconds to engine frame seconds
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Updates engine frame state and commands
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 148) · `N147`
- [transport · functions](../experiments/cargo-links/transport/functions.csv) (line 43)
- [transport · timing](../experiments/cargo-links/transport/timing.md) (line 37)
  Original report discusses this roster entry under Script authority and native deadline.

## RVA 0x01954f20

**Handle cache and state follow-up after a perk transition** · Level C · preferred VA `0x141954f20`

Recorded scope — Handle cache and state follow-up after a perk transition

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 105)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 29)

## RVA 0x01958550

**Update dependent state after the perk transition** · Level C · preferred VA `0x141958550`

Recorded scope — Update dependent state after the perk transition

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 105)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 30)

## RVA 0x019ae7f0

**AV modifier total** · Level B · preferred VA `0x1419ae7f0`

Analysis labels recorded in the original sources are `FUN_1419ae7f0`.

Recorded scope — AV modifier total

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 138).

- **Inputs** — Modifier state and AV pointer
- **Outputs** — Binary32 sum of three modifier slots
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Locks modifier array
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 138) · `N137`
- [inorganic extractors · arithmetic production](../experiments/inorganic-extractors/arithmetic-production.md) (line 72) · Sum actor-value modifiers
  Sums three binary32 slots in a locked per-AV row.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 90)

## RVA 0x019aec20

**serialize base AV and modifiers** · Level B · preferred VA `0x1419aec20`

Analysis labels recorded in the original sources are `FUN_1419aec20`.

Recorded scope — serialize base AV and modifiers

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 211).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — serialize base AV and modifiers
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 211) · `N210`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 240) · Serialize reference actor values
  Writes identity and base-value state under the ExtraBF save path.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 71)
- [build budget · native](../experiments/build-budget/native.md) (line 144)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 38)

## RVA 0x019aeff0

**restore base AV and modifiers** · Level B · preferred VA `0x1419aeff0`

Analysis labels recorded in the original sources are `FUN_1419aeff0`.

Recorded scope — restore base AV and modifiers

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 212).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — restore base AV and modifiers
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 212) · `N211`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 242) · Restore reference actor values
  Restores explicit values and uses AVIF defaults for unflagged values.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 72)
- [build budget · native](../experiments/build-budget/native.md) (line 144)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 39)

## RVA 0x019af700

**explicit base AV lookup** · Level B · preferred VA `0x1419af700`

Analysis labels recorded in the original sources are `FUN_1419af700`.

Recorded scope — explicit base AV lookup

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 139).

- **Inputs** — Base-value array; AV; output pointer
- **Outputs** — Found Boolean and stored float bits
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Locks base-value array
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 139) · `N138`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 102)

## RVA 0x019af7c0

**upsert explicit base AV row** · Level B · preferred VA `0x1419af7c0`

Analysis labels recorded in the original sources are `FUN_1419af7c0`.

Recorded scope — upsert explicit base AV row

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 210).

- **Inputs** — Native context and field contracts documented in organic-facilities/native.md
- **Outputs** — upsert explicit base AV row
- **Conditions** — Pinned retail 1.16.244.0; same-context resolved operands
- **Effects** — Reads/allocates or mutates native state as specified in native.md; never invoked here
- **Mapped edges** — Scanner knowledge or selected-AV save/load path; organic-facilities/native.md
- **Limits** — Actual loaded values and general cache/lifetime/failure guarantees untested
- **Source assessment** — STATIC instructions and definition/save joins; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 210) · `N209`
- [organic facilities · native](../experiments/organic-facilities/native.md) (line 239) · Upsert actor base-value row
  Stores AV pointer and binary32 value in a stride-0x10 row.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 65)
- [build budget · native](../experiments/build-budget/native.md) (line 125)
  Original report discusses this roster entry under Mutations, movement and restored state.

## RVA 0x01a27d80

**travel skipped-time update** · Level B · preferred VA `0x141a27d80`

Analysis labels recorded in the original sources are `FUN_141a27d80`.

Recorded scope — travel skipped-time update

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 152).

- **Inputs** — Player and travel context
- **Outputs** — Caller input+7c converted to elapsed XMM6
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Advances calendar and simulation
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 152) · `N151`
- [fabricators · native](../experiments/fabricators/native.md) (line 202) · Supply elapsed from travel
  Converts elapsed time on the documented travel path.
- [transport · transit functions](../experiments/cargo-links/transport/transit-functions.csv) (line 198)
- [transport · transit](../experiments/cargo-links/transport/transit.md) (line 124)
  Original report discusses this roster entry under Elapsed producer and staged consumers.
- [resource retained population · d5v sources](../experiments/resource-retained-population/d5v-sources.csv) (line 48) · `V-S047`

## RVA 0x01a38840

**Finish the mapped wait-loop tail** · Level C · preferred VA `0x141a38840`

Recorded scope — The inspected tail clears player +0xdd4 and performs cleanup and event work. The complete instruction window shows no additional calendar or production-elapsed call in this tail.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · arithmetic clocks](../experiments/inorganic-extractors/arithmetic-clocks.md) (line 57)

## RVA 0x01a38ba0

**wait or sleep skipped-time update** · Level B · preferred VA `0x141a38ba0`

Analysis labels recorded in the original sources are `FUN_141a38ba0`.

Recorded scope — wait or sleep skipped-time update

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 151).

- **Inputs** — Player state; settings; calendar; body scalar
- **Outputs** — Converted elapsed supplied to production updater
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Advances calendar and simulation; produces items
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 151) · `N150`
- [fabricators · native](../experiments/fabricators/native.md) (line 201) · Supply skipped-time elapsed from wait
  Converts time chunks on the documented wait path.

## RVA 0x01fcc740

**Bind Actor AddPerk to its native path** · Level C · preferred VA `0x141fcc740`

Analysis labels recorded in the original sources are `FUN_141fcc740`.

Recorded scope — Bind Actor AddPerk to its native path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 79)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 42)

## RVA 0x0200e610

**Game IsResearchComplete callback** · Level B · preferred VA `0x14200e610`

Analysis labels recorded in the original sources are `FUN_14200e610`.

Recorded scope — Game IsResearchComplete callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 133).

- **Inputs** — Project FormID context
- **Outputs** — Existing status2 Boolean
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Manager1461e26a0
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 133) · `N132`

## RVA 0x02068a10

**AddTransferLink callback** · Level B · preferred VA `0x142068a10`

Analysis labels recorded in the original sources are `FUN_142068a10`.

Recorded scope — AddTransferLink callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 89).

- **Inputs** — R8 source; R9 destination
- **Outputs** — AL result and diagnostics
- **Conditions** — Pinned build; valid owned native context; resolved identities
- **Effects** — Reads native state; internal allocation/locks/reference bookkeeping or mutation as described
- **Mapped edges** — 140f85760 ->140f81200
- **Limits** — Mutator never invoked
- **Source assessment** — STATIC instruction/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 89) · `N88`
- [storage · functions](../experiments/storage/functions.csv) (line 6) · `S1-005` · ObjectReference AddTransferLink callback
- [storage · native](../experiments/storage/native.md) (line 92)
  Original report discusses this roster entry under Separate source and pair gates.

## RVA 0x0206e3e0

**GetActorBaseForResource callback** · Level B · preferred VA `0x14206e3e0`

Analysis labels recorded in the original sources are `FUN_14206e3e0`.

Recorded scope — GetActorBaseForResource callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 206).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — GetActorBaseForResource callback
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 206) · `N205`

## RVA 0x02070ff0

**GetFloraForResource callback** · Level B · preferred VA `0x142070ff0`

Analysis labels recorded in the original sources are `FUN_142070ff0`.

Recorded scope — GetFloraForResource callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 207).

- **Inputs** — Native context documented in organic-facilities/native.md
- **Outputs** — GetFloraForResource callback
- **Conditions** — Pinned retail 1.16.244.0; resolved same-context operands
- **Effects** — Reads/resolves context; allocations/mutations qualified in native.md
- **Mapped edges** — Organic selector/UI/producer path; organic-facilities/native.md
- **Limits** — Actual loaded values and general ABI/lifetime/failure guarantees untested
- **Source assessment** — STATIC instruction/dataflow; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 207) · `N206`

## RVA 0x0209ff50

**Register the crew-members callback** · Level C · preferred VA `0x14209ff50`

Recorded scope — The original registration binds the native callback for GetAllCrewMembers.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [inorganic extractors · stacking native](../experiments/inorganic-extractors/stacking-native.md) (line 41)

## RVA 0x021ba960

**statistics worker caller** · Level B · preferred VA `0x1421ba960`

Analysis labels recorded in the original sources are `FUN_1421ba960`.

Recorded scope — statistics worker caller

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 166).

- **Inputs** — Engine state
- **Outputs** — Processes one statistics request
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Services updater owner 145f5db08
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 166) · `N165`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 83)

## RVA 0x021f2680

**power-summary aggregation boundary** · Level B · preferred VA `0x1421f2680`

Analysis labels recorded in the original sources are `FUN_1421f2680`.

Recorded scope — power-summary aggregation boundary

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 163).

- **Inputs** — Workshop and scratch summaries
- **Outputs** — Power fields; production remains zero in mapped callback
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Parallel scratch work; no power totals reconstructed
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 163) · `N162`
- [power · native](../experiments/power/native.md) (line 265) · Refresh Workshop aggregate power pair
  Dispatches the Workshop's aggregation route.

## RVA 0x021f2890

**power callback field boundary** · Level B · preferred VA `0x1421f2890`

Analysis labels recorded in the original sources are `FUN_1421f2890`.

Recorded scope — power callback field boundary

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 164).

- **Inputs** — Thread summary context; reference handle
- **Outputs** — Writes summary +0/+4 only
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Resolves references; updates scratch power fields
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 164) · `N163`
- [power · native](../experiments/power/native.md) (line 265) · Aggregate object power data
  Uses generation and demand operands for aggregate display.

## RVA 0x021f2ac0

**Workshop statistics request sink** · Level B · preferred VA `0x1421f2ac0`

Analysis labels recorded in the original sources are `FUN_1421f2ac0`.

Recorded scope — Workshop statistics request sink

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 160).

- **Inputs** — Sink owner; event reference/type
- **Outputs** — Coalesced handle and refresh-mask request
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Locks and appends or ORs queue
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 160) · `N159`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 113)
- [build budget · ui](../experiments/build-budget/ui.md) (line 32)
  Original report discusses this roster entry under Numerator, denominator and native cache.
- [inorganic extractors · arithmetic ui](../experiments/inorganic-extractors/arithmetic-ui.md) (line 78)
  Original report discusses this roster entry under Cache producer and meaning of the rate.

## RVA 0x021f2cb0

**Workshop statistics cache updater** · Level B · preferred VA `0x1421f2cb0`

Analysis labels recorded in the original sources are `FUN_1421f2cb0`.

Recorded scope — Workshop statistics cache updater

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 161).

- **Inputs** — Request owner
- **Outputs** — Selective ExtraWorkshop summary refresh
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Pops request; resolves references; writes cache; emits events
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 161) · `N160`
- [power · native](../experiments/power/native.md) (line 271) · Refresh Workshop summary
  The power pair reaches ExtraWorkshop +0x7c and +0x80 via this refresh; production has a separate +0x84 field.
- [build budget · functions](../experiments/build-budget/functions.csv) (line 22)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 68)
- [build budget · report](../experiments/build-budget/report.md) (line 55)
  Original report discusses this roster entry under Causal path.
- [build budget · ui](../experiments/build-budget/ui.md) (line 24)
  Original report discusses this roster entry under Numerator, denominator and native cache.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 17)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 31)
- [build catalogue · production](../experiments/build-catalogue/production.md) (line 13)
  Original report discusses this roster entry under Actual expression and population.
- [build catalogue · ui](../experiments/build-catalogue/ui.md) (line 108)
  Original report discusses this roster entry under Footer gaps investigated.
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 7)

## RVA 0x021f34d0

**cargo summary field boundary** · Level B · preferred VA `0x1421f34d0`

Analysis labels recorded in the original sources are `FUN_1421f34d0`.

Recorded scope — cargo summary field boundary

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 165).

- **Inputs** — Workshop extra and summary context
- **Outputs** — Writes summary+c only
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — No mapped production contribution
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 165) · `N164`
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 10)
- [build catalogue · ui](../experiments/build-catalogue/ui.md) (line 108)
  Original report discusses this roster entry under Footer gaps investigated.
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 6)

## RVA 0x021f36b0

**nominal producer rate aggregate** · Level B · preferred VA `0x1421f36b0`

Analysis labels recorded in the original sources are `FUN_1421f36b0`.

Recorded scope — nominal producer rate aggregate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 162).

- **Inputs** — Resource map; accumulator and Workshop context
- **Outputs** — Sum of cached-eligible resolved producer rates
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Invalidates failed handles; no current reason recheck
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 162) · `N161`
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 8)
- [build catalogue · production](../experiments/build-catalogue/production.md) (line 13)
  Original report discusses this roster entry under Actual expression and population.

## RVA 0x022ccd40

**frame scale update** · Level B · preferred VA `0x1422ccd40`

Analysis labels recorded in the original sources are `FUN_1422ccd40`.

Recorded scope — frame scale update

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 146).

- **Inputs** — Scale in XMM1; branch flag R8B
- **Outputs** — Rescaled current frame seconds
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Writes frame-scale globals
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 146) · `N145`

## RVA 0x022cce10

**engine frame seconds update** · Level B · preferred VA `0x1422cce10`

Analysis labels recorded in the original sources are `FUN_1422cce10`.

Recorded scope — engine frame seconds update

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 145).

- **Inputs** — Frame context; integer milliseconds
- **Outputs** — Context+18 scaled seconds and +1c unscaled seconds
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Updates time history; freeze/clamp/smoothing
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 145) · `N144`

## RVA 0x022cd0c0

**nested time freeze leave** · Level B · preferred VA `0x1422cd0c0`

Analysis labels recorded in the original sources are `FUN_1422cd0c0`.

Recorded scope — nested time freeze leave

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 150).

- **Inputs** — Global clock state
- **Outputs** — Adjusted clock origin bookkeeping
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Changes nesting and timing origins
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 150) · `N149`

## RVA 0x022cd140

**nested time freeze enter** · Level B · preferred VA `0x1422cd140`

Analysis labels recorded in the original sources are `FUN_1422cd140`.

Recorded scope — nested time freeze enter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 149).

- **Inputs** — Global clock state
- **Outputs** — Adjusted clock origin bookkeeping
- **Conditions** — Pinned retail 1.16.244.0; current definition/extra/manager dependencies as documented
- **Effects** — Changes nesting and timing origins
- **Mapped edges** — Connected callers/consumers in arithmetic-report.md and linked contracts
- **Limits** — Current runtime operands and full exceptional/restoration/freshness coverage not observed
- **Source assessment** — STATIC instructions/definition or dataflow; strong within traced paths

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 149) · `N148`

## RVA 0x023ff640

**Obtain manager context for candidate resource reads** · Level C · preferred VA `0x1423ff640`

Recorded scope — Obtain manager context for candidate resource reads

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [organic facilities · native](../experiments/organic-facilities/native.md) (line 45)
