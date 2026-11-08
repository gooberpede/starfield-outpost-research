# D5BF proposed release assets for Starfield 1.16.244.0

**Publication is NOT READY / NOT CLEARED.** The four groups below are the exact
local proposal under the [D5BF brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BF_Final_Evidence_Selection_Clearance_and_Release_Asset_Preparation.md).
The [release-asset ledger](release-assets.json) is the single proposal for
selection, byte identity and member roles. All asset URLs are `PENDING RELEASE`.
`APPROVED FOR PROPOSED RELEASE` means technically and policy-eligible for the
proposal. The maintainer still controls final selection, disclosure and timing.

| Group | Local recommendation | Exact comparison supported |
| --- | --- | --- |
| B4-F1 CORE | Include 25 original first-party saves, 104,046,934 bytes. | Controlled action and no-action saves, position controls and mature witnesses, including Save29, Save52/HIST-0267, Save41/HIST-0255 and HIST-0036. |
| B4-F1 ADDENDUM | Include as a separate optional reader download, with 14 original saves and 13 original JPEGs, 80,827,444 bytes. | Supplemental saved-state, action/control and visual evidence. Screenshot and save epochs are unjoined. |
| D5AS | Include the geometry derivative, 176,733 bytes. | All 30 qualified canonical bodies against two complete fixed references, including the attempt chronology, exclusion and replacement. |
| C19 | Include the native callback derivative, 189,747 bytes. | All 346 complete recorded input-to-row comparisons and their run context. |

## Exact payload and policy decisions

**F1.** Both chosen containers match F1's pinned sizes and SHA-256 digests.
Every member has its exact original basename and matches both its current
protected copy and the prior extracted member byte for byte. Save52 is
`B4-F040`/`HIST-0267` and Save41 is `B4-F051`/`HIST-0255`. CORE includes one
`B4-F032` member for S4C/L0, the anchor for the ADDENDUM L-series controls.
The two original ZIP basenames, including their `provisional` suffixes, are
the proposed handoff names. The packages were reused byte for byte. The review
confirmed Unix `0100644` mode bits and creator-system code 0 on the ZIP entries.
All 52 files retain F1's prior scoped producer, utility and privacy decisions.
Twenty-one older locators were absent, with every selected identity verified
against its available protected copy. The first-party policy accepts character
names and historical generic user-path provenance. The existing screens leave
opaque save fields and incidental fine screenshot details incompletely examined.
Donor `B4-F061`, the other withheld F1 identities, and the alternate codec ZIPs
remain outside the proposal. No selected F1 file requires a new hold.
[F1 decisions](../publication-readiness-b4/f1/file-dispositions.csv) ·
[Privacy scope](../publication-readiness-b4/f1/privacy-policy.md) ·
[Original independent review](../publication-readiness-b4/f1/review.md).

**D5AS.** The ZIP carries a bounded JSON manifest and 32 canonical bodies
for one target-source profile, including two fixed-mask reference bodies.
The canonical body domain is distinct from the frozen envelope, archived
observer payloads and A0 normalization. Qualified positions 7 and 13 match
fixed mask 0. The other 28 match fixed mask 3. Attempt 6's retired source
lifetime prevents qualification, and attempt 31 supplies the replacement.
Equality assigns a geometry class. Direct generating-mask observations from
other instrumented trials have their own evidence, and the generating mask and
winning request in these samples remain unknown. The body structure encodes
three resource FormIDs with region and point records. The 30 bodies were
reconstructed from the sealed captures, and both references were checked
against four original controls. Manifest metadata covers the target source,
ordinals, admission outcomes and digests. The staged ZIP omits proprietary
source, executable material and whole game assets. These are bounded research
data under brief §2.2.
[D5BE method and source fidelity](../evidence-access-d5be/d5as.md) ·
[Original series closeout](../../experiments/resource-retained-population/d5as-series-closeout.md).

**C19.** The JSON carries ordered native common inputs, selected-append
observations, row identities and constructor/sequence information, using
equality aliases for pointer identities. All 346 folds agree with the recorded
rows, with 339 three-row updates and seven two-row updates. The census includes
one initial delivery, five set changes and 340 unchanged redeliveries. No
selected append occurs in this capture. Operator A/B/C labels are separate from
the native callback observations. Exact display timing and producer ancestry
remain unverified. The stable-run context summarizes the 35,573 preview
evaluations. The direct replay is scoped to the recorded 346 comparisons.
The source check rehashed the archived WAL and independently reconciled all
346 callback joins. The exact candidate retains the structured comparison and
phase labels. It omits account and private path metadata, the WAL, raw addresses
and compiled code. This is bounded evidence under brief §2.2. The distinct D1
incident remains outside this evidence route.
[D5BE method and source fidelity](../evidence-access-d5be/c19.md) ·
[Original independent review](../../experiments/continuous-beacon-preview/review.md).

The derivative inspection found no file-specific exception requiring a hold.
The bounded data are game-derived, and the original saves and JPEGs include
Bethesda content. The project's `GPL-3.0-or-later` terms cover authored research
and verifiers where contributors hold the necessary rights. The project claims
no ownership or sublicensing authority over upstream material. The maintainer's
policy supplies a project decision with residual legal uncertainty. Retain the
existing notices and credits for all four groups.
[Notices](../../../THIRD_PARTY_NOTICES.md) · [Credits](../../../CREDITS.md) ·
[Source provenance](../../SOURCES.md).

## Verification

Use CPython 3.10 or later. Supply each actual local file explicitly, keeping its
ledger basename. The verifier reads the ledger and the four files, streams ZIP
members without extracting to disk and writes a receipt to stdout. It compares
full container bytes, member paths, codecs, sizes and hashes, including the
whole-file member for C19. Its only dependencies are the Python standard
library and the explicit inputs. A missing input or mismatch exits nonzero.
The two standalone comparisons separately check the scientific evidence and
exercise the D5BE negative controls. Substitute actual file paths for the
placeholders below.

```text
python -I -S -B research/evidence-access/verify_release_assets.py docs/audits/release-assets-d5bf/release-assets.json --asset B4-F1-CORE "<CORE-path>" --asset B4-F1-ADDENDUM "<ADDENDUM-path>" --asset D5AS "<D5AS-path>" --asset C19 "<C19-path>"
python -I -B research/evidence-access/d5be/d5as_verify.py "<D5AS-path>" --sha256 d0d35ed2193527dd8215a647178614a5403e814bf14c3f9d1f0a448c53a1043c --negative-controls
python -I -S -B research/evidence-access/d5be/c19-verify.py "<C19-path>" --sha256 d37476dd5b33fca44423c1c0aaf239b43e8a98d8cf2ed97b15beaa4225906ada --negative-controls
python -I -S -B research/evidence-access/d5be/c19-verify.py --self-test
```

The ledger is portable planning metadata. It includes the approved original
basenames and repository source references. The private lookup receipt
`D5BF-LOCAL-INPUTS` maps the asset IDs to the retained files. The local delivery
index maps the other receipt IDs to exact hashes. Preserve and supply the four
proposed assets explicitly at B6. The verifier has no private-path lookup.

## Open evidence routes and maintainer decisions

These four assets prepare the original and bounded derivative routes. Agree
the claim matrix and verification tiers before any release freeze. The
[D5AX claim graph](../publication-architecture-d5ax/claim-evidence-dependencies.csv)
and [evidence access assessment](../publication-architecture-d5ax/evidence-access.md)
identify the outstanding edges. Hold any stronger selected claim with an
indispensable unresolved edge until the maintainer approves a verified route,
a narrower claim or exclusion.

| Route outside these four assets | Consequence for scope approval |
| --- | --- |
| B4-C19 D1 incident contrasts, including the header-rejected H249 control | The 346 callback comparisons leave the exact D1 historical save comparison unresolved. |
| B4-C07 historical three-load power observations, B4-C09/C23 cargo timing and private network/VM records, and B4-C18's broader frozen position inputs | Save29 and the F1 cargo and position controls support their own saved-state checks. Exact historical runtime and broader corpus replay still need distinct routes at that tier. |
| Full historical detections for B4-C06/C14 and other withheld component witnesses in F1 coverage | Retained originals support named examples. Tracked C14 rows can recompute the reported census at the derivative tier. Raw-corpus verification would require additional lawful inputs and readers. |
| D5AS original qualification custody, D5AK/D5AL cause and lifetime joins and D5AO/D5AQ historical chronology or exact native controls, if selected | The D5AS asset compares complete bodies in its domain. Assess any claim depending on raw qualification witnesses, other events or native methods separately. D5AT needs the Save52 original plus lawful pinned definitions and qualified grid/descriptor methods. |
| B3 lawful pinned game inputs, selectors and methods, and any selected creator prerequisites | Assets supply only their declared operands. Verify applicable input availability, tools, safety and effects under the B3, B5 and B6 gates. |

1. Approve the exact claim matrix, tiers, exclusions, four-asset selection and
   file-specific rights/privacy, contributor wording, credits and excerpt
   boundaries. Decide any archival changes separately and resolve remaining
   indispensable routes before freezing the candidate.
2. Freeze the exact commit, tree, public refs and reachable history, claims,
   assets and clearance records. Authorize independent B6 preflight in a truly
   isolated checkout with explicit staged inputs.
3. After B6 acceptance, separately approve the exact release identifier, tag,
   Git transfer, draft, upload inventory and disclosure recipient. Verify hosted
   bytes, member inventories and changed surfaces from actual draft URLs.
4. Separately approve visibility, exposure and timing. After authorized
   publication, verify public URLs and downloads, tag/commit and notices.

Record decisions and receipts in the [publication run card](../../PUBLICATION_RUN_CARD.md).
The D5BF snapshot is local preparation. B6 and every release action remain pending.
