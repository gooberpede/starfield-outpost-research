# SD1 review and delivery receipts

2026-10-19, SOR-EXP-0055 / SOR-EV-0063.
[Original eight criteria](../../implementation-briefs/CODEX_BRIEF_SOR_SD1_containers_displays_ownership_persistence.md),
[answer](report.md), [evidence](evidence.md), [methods](methods.md).
No mandatory acceptance criterion was amended. Independent review02 **ACCEPT**
passed all eight criteria; the final administrative snapshot is checked separately.

Review01 returned **REWORK** against package manifest SHA256
`bb85933b7e793484a6014ca38c84e9f27628ebc6cac1ae5eab1c18e7daa23a55`.
The actual verbatim result is retained in
`.local-work/sd1-containers/independent-review01.md`. Criteria 1/3/4/6/7 passed;
criteria 2/5/8 failed for wardrobe overinterpretation, missing construction-stock
suppression and prose/failure-record issues. No criterion was waived. The
reviewer independently passed 746 checks in verification-independent01.json,
SHA256 `021e971f85ac817733fa03a92b22a0ca26ca565aea17aeee07f7d41f54a94ff4`.
Its failed WindowsApps Python alias did not execute the checker; the explicit
installed executable succeeded. Source/patch/HEAD/index identities matched
before/after, and both patches passed independent reverse applicability.

Disposition: wardrobe now states only a **node-1 rule**, without declaring it
nonvisual; rule count alone does not establish visible mounts. New n070–076
follow construction preview/commit, explicit null-destination inventory clearing,
mannequin recognition and display reset; native.md now answers default CNTO
suppression rather than leaving it as another context. Existing source stock
and cleared per-reference state remain distinct. The constructed-case competing
branch was an omission, not an exhausted dependency or a reason for live access.

The first review01 packaging attempt stopped on mojibake in evidence.md before
writing patches: a numeric-spacing pass had used the Windows CP1252 default
when reading UTF-8 native/evidence prose. The author reversed that encoding
conversion, changed subsequent passes to explicit UTF-8 and reran validation
and exact patch checks successfully. The first spacing pass still missed several
joined words/numbers; the reviewer supplied concrete failures, now corrected
with identifier-aware prose review. An intermediate construction paragraph also
swapped two call addresses; n075 instruction windows corrected them before
resubmission (actor 1421dd2d7, nonactor 1421dd301). A context-mismatched text patch
failed atomically and was reapplied with exact context. These are authored
analysis/documentation failures, with no protected-input or target effects.

| Original criterion | Implementer assessment | Support / limit |
|---|---|---|
| 1. Classification | PASS; independent PASS | definitions.csv:111 qualified recipe/leaf/child/add-on rows; recursive census, material variants and unresolved master leaves explicitly bounded |
| 2. Admission/capacity | PASS; independent PASS | native.md: weight, native slot limits/include/exclude, actor effective capacity/equipment, actual bound menu filter; ordinary successful actions unmeasured |
| 3. Ownership/access | PASS; independent PASS | Four separate channels, access predicate, concrete mode/reason transfer ancestry, new display owner override and reuse distinction; no laundering/UI guarantee |
| 4. Display residence | PASS; independent PASS | Inventory-to-reference/snap/dropper/slot chain versus actor inventory/equipment; actual rendered reload explicitly unproven |
| 5. Lifecycle | PASS; independent PASS | Construction/move/removal/ordinary scrap transfer and DA1 reuse traced; actual bIsMannequin predicate binding, actor exceptions and controlled-conservation limit retained |
| 6. Persistence | PASS; independent PASS | Native writer/load/fixup and real H21 display joins; H256/H257 storage and mannequin equipment rows; bounded 255-original survey with capability failures |
| 7. Quality/limits | PASS; independent PASS | Answer-first records, pins, exact identity domains, controls/counterexamples and smallest proposed live acquisition; SD2/SD3 excluded |
| 8. Integrity/package/review | PASS; independent ACCEPT | Exact patches/checks and full eight-criterion independent review02; final administrative snapshot checked separately |

Scientific result: strong scoped native mechanisms with actual saved
correspondence. Ordinary gameplay success, final rendered reload, controlled
theft/conservation and every installed winning override remain unmeasured.
Engineering/integrity checks are separate from semantic confidence. Target
survival is NOT APPLICABLE: no game process was used. Raw inputs remain local;
authored package requires maintainer review and publication clearance.

`.local-work/sd1-containers/verification-first.json` records **744 executed
checks**: protected inputs, all 255 attempted original hashes, successful
pre/post source pins, 43-section component closure, exact slot/backlink/owner and
modification joins, mannequin row state and populated ammo-box controls, plus a
fresh original H256 byte reread of quantity/state/sentinel fields. Its limits
explicitly exclude a gameplay/rendering oracle. `preservation01.json` separately
confirms protected inputs after analysis, all 69 completed native export headers,
the independently reread five-byte UI getter, retired owned Ghidra worker,
decoder scratch cleanup and unchanged HEAD/index. Both drive guards passed.
No protected input/save or existing analysis content was changed.
The construction continuation used a fresh hidden read-only worker for n070–076,
then retired it normally. `preservation03.json` supersedes the first retirement
receipt for final delivery. `rework-check02.json` adds **19 passed checks**,
including fresh physical case-stock definitions and actor/nonactor null-destination
instruction windows. `prose-check03.json` records the identifier-aware UTF-8
spacing check; final export repeats encoding/whitespace/link and exact
reconstruction validation.
The retained preservation02 receipt's numeric request_count field mistakenly
said 69 despite its executed 76-request assertion and correct retirement text.
Preservation03 reran the protected-input/retirement checks with the corrected
scalar; the earlier receipt was preserved, not overwritten.

## Reworked independent iterations

During preliminary review, the independent reviewer read the original brief and primary native/save receipts
without editing files or running experiments. Three preliminary REWORK iterations
challenged ownership, ordinary reason ancestry, scrap destination and mannequin
persistence. They were substantive checks, not final acceptance of a changing tree.

The ownership critique falsified the initial fallback interpretation: n005
1413001cb skips ExtraDataList allocation, not the ownership setter reached at
141300236..252. The corrected new-reference override is in native.md/report.md.
Later acquisitions close mode/reason ancestry, equipment-state writer/reader/
restorer and the ordinary scrap caller. The completed survey also supersedes
the interim missing chest/mannequin positive result. Earlier local receipts and
review returns remain preserved. Independent review supplies no integration,
live-action, publication, staging, commit or push authority.

The final preliminary pointer-join challenge was addressed independently from
the pinned original EXE: virtual slot 144c567b8 points to 14038a050, whose complete
getter adds 28 hex. This proves the provider-to-property-array adjustment used
to bind the scrap actor predicate to `bIsMannequin`; see native.md/accessor01.json.

## Local review package

The ignored `.local-work/diffs/sd1-containers-review01-complete.diff` includes
every current changed/untracked text file since HEAD, including the unchanged
supplied brief. The task-only counterpart excludes that preexisting brief.
The baseline also happened to capture the newly authored plan; exporter
classification correctly treats that plan as task-authored, preserving the
baseline receipt unchanged. No unrelated tracked changes existed at intake.

`package-review01.json` and `status-review01.txt` under
`.local-work/sd1-containers/` record file inventories, hashes, exclusions,
forward/reverse applicability, exact reconstructed bytes and HEAD/index identity.
Disposable application trees live under `.local-work/review-patches/`, with Git
parent discovery stopped at `.local-work/`. Workspace files/index are never
patched. Ignored exclusions include private paths/original and decoded saves,
native/PEX/ESM payloads, local readers, tool/database/cache/log files and scratch.
Authored source/evidence tables contain locators/hashes/interpretation, not raw
game/script/decompiled/save payloads. Local verbatim reviewer returns are retained
as review evidence; their substantive decisions are recorded here.

## Independent disposition and final snapshot

The independent reviewer returned **ACCEPT** for all eight unchanged original
criteria against package-review02.json SHA256
`95b6eddef56a85c205ee0d21a10fd5960e682217348065bdb009829576c09263`.
The verbatim result is `.local-work/sd1-containers/independent-review02.md`.
Actual file inventories/hashes, HEAD/index and both patch hashes/reverse checks
matched independently before/after review. The reviewer independently executed
the earlier 746-check verifier; the 19 new checks and forward reconstruction were
inspected as implementer receipts, while the new native construction branches
were independently read from primary exports. These coverage distinctions remain.

The final delivery is package-review03.json, status-review03.txt and
`.local-work/diffs/sd1-containers-review03-complete.diff` /
`sd1-containers-review03-task-only.diff`. It adds only this administrative
disposition and refreshed source/check receipt metadata after accepted review02;
scientific conclusions and primary evidence are unchanged. The promised limited
snapshot re-review is retained as independent-review03.md. All earlier snapshots
and failed iterations remain preserved. No acceptance grants maintainer
integration, live-action or publication authority.

Suggested Conventional Commit:

`docs(research): map container display ownership and persistence`

Nothing was staged, committed or pushed. Maintainer critical diff review remains
required before integration; scientific acceptance does not clear publication.
