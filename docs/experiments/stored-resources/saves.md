# Historical search and item-level correspondence

[Answer](report.md), [corpus census](corpus.csv), [selected cases](cases.csv),
[methods](methods.md). All offsets below are **decimal decoded logical stream
offsets**. Dynamic identities are save-local FormIDs, not current runtime handles.

The fresh survey visits all **278** canonical historical locators: **255**
accessible originals, **23** missing. Of accessible originals, **147** support
the strict envelope/typed REFR-family reader and **108** fail supported framing or
build qualification. No unsupported input supports an absence claim. Every
accessible original is hashed before and after its attempt. All originals remain
unchanged. Corpus.csv retains each outcome, original hash and qualification error.

All 147 supported inputs report buffer version **153** and both build strings
**1.16.244.0** in their decoded plugin context, including HIST-0036. Matching
build strings do not establish that historical plugin contents equal the current
installed ESMs; current-definition joins retain that distinction.

Within the supported inline-base reference subset, **29,582 candidate record
occurrences** match the S1/SD1 base sets, ordinary beacon or shared fixture.
These are correlated occurrences, not independent outposts or a complete
constructed-object population. Prefix gaps and missing inherited/default
representations remain recorded per original. The source set includes ordinary
storage/output/cargo/transfer bases, SD1 CONT/NPC fixtures and shared access bases;
it does not pretend to decode the player's SD2 backing-inventory segment.

The approved owned S1 inventory reader requires a closed leading-extra section
and supports empty stack-extra lists. It follows native saved order: queued item
identity, compact stack count, each stack's extra list and signed count, then
bookkeeping. Nonempty stack extras, leading unknown extras and actor tails remain
explicit gaps. A missing inventory-change branch can inherit defaults; it is not
an empty-inventory finding. Counts reported here are decoded serialized stack
units, not complete post-load effective inventories or measured UI counts.

## Positive mature mixed-source witness

HIST-0036 SHA-256:
`7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37`.
Fresh saved-HIST-0036.json supplies source record, item-stack and Extra4C
WorkshopItem joins. The owner resolves to an actual ordinary beacon in that same
decoded original; case-definitions01 physically rereads its ACTI definition and
all 43 other selected case definitions. No outpost name or screenshot is a join key.

| Actual saved relation | Positive item evidence | Discrimination / supported scope |
|---|---|---|
| Beacon ff04ba51, record 5598838; incoming ff018b7c/base219173, record 2985440 | MISC 0057df Caesium, **375**, stack 2985557 -> IRES 0057e0 | Incoming base AV 1; conditional eligible source |
| Same beacon; outgoing ff018b73/base219171, record 2984588 | Same Caesium, **375**, stack 2984705 | Outgoing base omits AV. Excluded if effective AV 0 despite real stock and membership |
| Same beacon; liquid store ff018b61/base2c5913 | Caesium **94**, stack 2981573 | A separate eligible source contributes additional units; not duplicate suppression by item form |
| Same beacon; medium extractor ff05632a/base20a079 | Caesium **12**, stack 6101151 | Extractor buffer is another distinct source; nominal production is not the quantity |
| Beacon ff01a510, record 3037357; greenhouse ff01a5c5/base2965f7 | Lubricant **15**, stack 3058631 -> IRES 0777f9 | Organic output buffer and solid store ff01a506 holding **150** Lubricant show resource-key merge across source classes |
| Same beacon; incoming ff059263 and warehouse ff0592cd | Reactive Gauge **25** + **50** -> IRES 24577b | Manufactured physical items are admitted through their resource association |
| Beacon ff04fc98, record 5793175; warehouse ff01a9f3/base29b453 | Aldumite Drilling Rig **1**, stack 3076697 -> IRES 202f59 | Independent manufactured class/owner witness |

Cases.csv contains **27 exact item rows at three owner beacons**, including
extractors, storage, greenhouse, builder and cargo. The conditional subtotal of
the listed Caesium incoming/store/extractor rows at ff04ba51 is **481**; adding
the excluded outgoing 375 would produce **856**. These are deliberately partial
serialized-source contrasts under stated predicates, **not** an exhaustive
outpost/UI total, and no settled loaded AV/resolution state is inferred.

Industrial bases may have CNTO marker entries. The decoded ordinary resource
stacks above remain exact serialized observations; no default marker is silently
added to their resource quantities. Construction-preview clearing is established
by SD1, while current winning definitions/load reconstruction remain separate.

An additional all-supported-receipt search for a closed decoded non-CVPA item in
an AV 1, positively joined main-game source found **zero** witnesses
(negative01.json). This is a qualified search bound, not proof that such stock
cannot exist. Native equipment/nonresource exclusion and the positive outgoing
stock contrast supply differentiated controls; no physical nonresource example
is fabricated to compensate for unsupported stack extras.

## Screenshots remain non-joins

`1716740_66.jpg` is a UI witness: SCHROD II AD shows Adaptive Frame 5,
Adhesive 7, Aldumite 47, Aldumite Drilling Rig 2, Alkanes 38, Aluminum 64,
Amino Acids 10 and Analgesic 31 in the visible portion. `1716740_62.jpg` shows
KREET OUTPOST 1 with Iron 1. Both original files are freshly hashed. Neither is
assigned to HIST-0036, Save52 or an arbitrary historical epoch. The mismatch
between screenshot Rig 2 and this saved Rig 1 is not a production delta or error.
No screenshot is copied into tracked documentation.

Broad source search and positive mixed-source joins satisfy the bounded saved
correspondence objective without decoding all player-held shared stock. Actual
post-load amounts, current eligibility and UI freshness remain unmeasured;
[one proposed test](aggregation.md#three-separate-freshness-boundaries) is retained
without live execution or new-save authority.
