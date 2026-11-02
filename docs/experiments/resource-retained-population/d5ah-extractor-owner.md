# D5AH concrete extractor and saved Workshop owner

2026-11-02, Australia/Sydney. D5AH-Q3 and Stage B selection dependency.
Parent D5AH-CQ is BLOCKED. Native addresses use preferred static image base
`0x140000000` for retail 1.16.244.0; the offsets below are decimal locations in
the decompressed logical save stream, not compressed-file positions.

**Save52 explicitly associates the placed ionic-liquid extractor
`DYNAMIC:ff041387` with the ordinary beacon `DYNAMIC:ff04e101`, whose established
saved label is Feynman V Cu IL F.** This is a decoded, counted WorkshopItem
relationship, stronger than the earlier EXP0029 queued-context lead. The future
design can select this existing outpost and actual saved machine. Its current
loaded owner, operating state and geometry still require separate observation.

Confidence is PROVEN / SAVE for the specified byte fields and framing; the
ordinary WorkshopItem interpretation retains the independently reviewed
[membership contract](../workshop-membership/report.md#authoritative-saved-relationship).
Coverage is this explicit saved relationship and these two supported records,
not an exhaustive physical inventory or a loaded ownership guarantee. Sources
and method identities are in [the exact ledger](d5ah-extractor-owner-sources.csv).
Authored interpretation remains REVIEW-REQUIRED; raw saves and receipts remain
LOCAL-ONLY.

## Fresh primary-byte check

The [owned verifier](../../../research/resource-retained-population/d5ah-extractor-owner.py)
reads only the policy-pinned research copy of Save52. It validates source size
and SHA-256 before and after, validates the BCPS physical framing, and decodes
the complete stream into memory using the existing independent selected-block
decoder. No decompressed save file is created. The decoded SHA-256 is
`e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93`, matching
the prior qualified input. Saved plugin tables identify buffer version 153 and
embedded build strings 1.16.244.0. Embedded strings do not establish a new
executable baseline.

All 205,557 directory-declared R3 records are iterated to exact closure. The
target and owner tokens each occur once. The verifier then consumes the
qualified initial-reference/component prefix and full counted extras for both
selected records. It also independently checks the actual mode byte is zero,
rather than accepting only the parser's reported mode.

| Selected object or field | Observed value and location |
|---|---|
| Extractor record | Ordinal 27735, logical range 5034479–5034935; saved identity `DYNAMIC:ff041387`, inline CONT base `Starfield.esm:20a076`. |
| Explicit saved WorkshopItem edge | One counted Extra4C entry, keyword `Starfield.esm:054ba6`, target mode 0 at logical location 5034589, target `DYNAMIC:ff04e101`. Keyword queue index 5 is interpreted through this field grammar, not adjacency. |
| Extractor extras qualification | Seven counted extras close; no alternate Extra80 group. The single matching WorkshopItem entry is nonnull and uniquely identifies the recognized beacon. |
| Beacon record | Starts at logical location 5712362; saved identity `DYNAMIC:ff04e101`, inline ordinary-beacon base `Starfield.esm:2c60e9`. |
| Saved flags | Disabled/deleted bits are clear on both selected records. Current power, halt, eligibility and actual output do not follow from these bits. |
| Name provenance | Existing [membership owner table](../workshop-membership/owners.csv), row for `DYNAMIC:ff04e101`, names Feynman V Cu IL F at the same record location. The name supplies context; it does not establish the resource or ownership edge. |

The medium ionic-liquid definition chain is independently established in
[the extractor report](d5ah-extractor-continuity.md#saved-controls-and-a-concrete-future-candidate):
CONT `0x20a076` → AVIF `0x05ef20` → IRES `0x0057d4` → COBJ `0x05ef52` →
MISC `0x00557a`, all qualified to `Starfield.esm`. Membership is determined
through the explicit saved relationship above, not by the machine's name,
location proximity or that resource chain.

## Native meaning and retained limits

The previously reviewed [native membership dependencies](../workshop-membership/dependencies.md)
bind `WorkshopItem` DFOB `0x054bb8` to KYWD `0x054ba6`. GetWorkshop
`0x142073cf0` supplies this key to `0x140517d60`. Dispatcher
`0x140521620 → 0x140547c90 → 0x140562ef0` reads the counted key/mode/target
entry; mode 0 restores a handle while mode 1 retains a FormID. These native
contracts explain why the fresh decoded field is an explicit saved owner edge.

GetWorkshop can prefer Extra80 and loaded/default relationships. This target's
closed saved extras have no Extra80, but that does not prove every loaded
default or later mutation absent. Future preflight must resolve the actual
machine and beacon, check their current owner and frame, and qualify current
ordinary properties and production. That live validation remains necessary;
finding the saved owner is no longer a deferred investigative task.

Fresh receipts `.local-work/d5ah-extractor-owner/owner01.json` and
`owner02.json` preserve the initial primary check and the added independent raw
mode-byte check. Both pass with unchanged protected input and both-drive
40,000,000,000-byte free-space guards. This check strengthens concrete sample
selection; it does not establish complete geometry, a departure/return episode
or continuing production beneath changed deposits. No game, debugger, native
invocation, save mutation, original analysis-project operation, deployment or
Git integration occurred.
