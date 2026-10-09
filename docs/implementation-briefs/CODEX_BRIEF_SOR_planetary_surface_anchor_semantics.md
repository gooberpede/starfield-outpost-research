# Codex Research Brief — SOR: Planetary Surface-Anchor Coordinate Semantics

## Objective and research posture

Determine what the **two saved double-precision values associated with an outpost's planetary overlay** mean and whether they allow a reproducible planetary surface location to be derived. Identify the **planetary placement of an outpost**—preferably latitude/longitude or an equivalent globally meaningful coordinate—as the primary objective. Body identity is already strongly supported and should be used as a foundation, not rediscovered from names.

Use the current committed `starfield-outpost-research` state and its durable evidence standard. Investigate competing explanations actively, prioritize discriminating evidence, and give the strongest supported answer with **confidence, coverage, and completeness** separated. Do not require universal coverage before reporting a strong result within demonstrated scope. A plausible numeric range alone does not prove angular units.

**Authority:** Offline analysis, public-source/prior-art research, Ghidra static inspection, xEdit/ESM inspection, and small reproducible numerical tests are authorized. **Do not launch Starfield, run a live debugger or SFSE plugin, modify game files or saves, stage, commit, or push.** If live validation becomes necessary, specify the smallest proposed experiment and return it for separate authorization.

## Phase 0 — Establish the evidence baseline

Before generating new hypotheses, read the committed reports, findings and state registers for:

- `save-capacity-and-planetary-location`, including the verified S1/S1C/L2C Kreet body association and the mature Save52 17/17 body/system matches;
- Save2 near the Lodge/New Atlantis; original A0/A0C runtime position evidence; prior local XYZ candidates;
- current ordinary beacon detector and saved beacon → parent/overlay → body/PNDT association;
- prior provenance, source, permission, evidence and methodology requirements.

Verify the actual source bytes and reference locations before using quoted numbers. The starting Kreet surface-anchor candidate reported previously was `(-0.2211059435912563, -0.5113105421317372)`; the Save2 Jemison-associated comparison was `(2.2810355988151545, 0.7111154993616507)`. These are **candidate** values and not already-proven latitude/longitude. Confirm from durable evidence rather than treating this brief as a data authority.

Preserve source hashes and frozen earlier analyses. Record the current installed Starfield/ESM build and any older-version limitations. Distinguish the immutable historical save from any later resave; regenerated tokens and offsets do not imply that an earlier file changed.

## Phase 1 — Prior work and community research: planetary tiling

**Make this a real research phase, not a token web search.** Survey publicly available prior work, discussions and technical experiments about Starfield planetary tiling, landing-area placement and coordinate systems. Search as relevant across modding communities, Nexus Mods, GitHub repositories/issues, Creation Kit documentation, Bethesda modding forums, Reddit, reverse-engineering writeups and other discoverable technical discussions.

Questions to pursue:

- How are planetary landing tiles/overlays identified, positioned and oriented? Is there evidence for a tile grid, projected map, spherical sampling, or local-to-body transforms?
- Has anyone located code, fields, game records or repeatable experiments for **planetary latitude/longitude**, tile origin, player landing point, outpost beacon position, poles or prime meridian?
- Are orbital appearance textures and resource overlays known to share a mapping, or do they use distinct projections/coordinate frames?
- Do community observations concern current Starfield or earlier versions, and are their conclusions experimentally supported?

Maintain a compact **prior-art register**: author, title/claim, URL, access date, publication/update date where available, game/tool version, precise evidence offered, relevance, confidence, and whether independently confirmed. Separate reported claims from project-verified results. Follow links to original sources where feasible. Distinguish primary technical evidence from discussion/speculation; include useful negative results and conflicting accounts.

**Permissions:** Reading and citing publicly accessible material is not permission to copy code or redistribute assets. Follow `THIRD_PARTY_POLICY.md`, `PERMISSIONS.md`, `SOURCES.md`, `PROVENANCE.md`, `CREDITS.md` and notices; do not incorporate third-party code without the required explicit permission decision and user approval. For maintainer-authored `gooberpede` repositories, apply the established reuse exception with exact provenance; third-party material embedded there is not exempt. Do not reproduce substantial copyrighted text, images or binary assets. Any usable technical ideas must be attributed and clearly marked *source-reported* until independently checked.

If prior work supplies a credible answer, **validate it against our saved pairs and installed executable/ESM evidence** rather than simply adopting it. If relevant material is unavailable or permission-restricted, document the lead without circumventing access restrictions.

## Phase 2 — Trace origin and consumption of the saved doubles

Use targeted Ghidra analysis of the pinned executable and selected xEdit/ESM records to trace the data flow of the body-associated double pair:

1. Locate and validate the serialization/deserialization path, types, record framing and association to beacon/overlay/landing-site references.
2. Identify code that creates, reads, transforms or consumes the pair; prioritize callers/callees that connect it to planet surface placement, tile/overlay creation and landing site selection.
3. Determine whether the pair is angles, normalized parameters, projection coordinates, body-relative values, tile keys, or something else. Test numeric encoding (double, endian, signedness), units, component order, wrap/range, axes and handedness.
4. Separate **planet/body identity**, **landing-area or overlay origin**, **beacon position**, and **local XYZ transform**. Do not conflate them just because they are linked.
5. Determine what fixes polar direction and a longitude zero/prime-meridian convention if the identified code exposes those rules. Do not impose Earth conventions in the absence of evidence.

For each significant function or data record, give a reproducible locator (RVA, FormID, EditorID, file/hash/build), relevant data flow and a concise evidence trail. Avoid broad unrelated decompilation.

## Phase 3 — Numerical and cross-case validation

Develop small offline calculations/tests to discriminate plausible coordinate interpretations. Prefer testable predictions over visual plausibility. Use independently established body associations and a diversity of anchors:

- S1/S1C/L2C on Kreet (same site, reload/resave), and S0/Save3 as controls where useful;
- Save52’s 17 outposts, particularly **different outposts on the same body** and different bodies within the same system;
- Save2 near the Lodge in New Atlantis on Jemison;
- verified fixed-location ESM cases such as New Atlantis, Akila City and Cydonia, where comparable coordinate fields can actually be established.

**Do not infer planet or location from the outpost name.** In Save52, the manually authored network JSON may be used to **cross-check** extracted associations, not as an input to the extraction logic. If matching entities by name to align datasets, explain that separately; the planetary conclusion must be based on save/ESM-derived identifiers.

Test repeatability of the double pair across same-site saves, differentiation among sites on the same body, component ranges, possible radians/degrees/projection models, and relationship to previously recorded local XYZ. If deriving lat/long, specify north/south sign, longitude zero, axis direction, normalizing/wrapping conventions, and whether the result is **site origin** versus **beacon position**. Record numeric error and ambiguities. Do not extrapolate from a single planet.

If the exact transformation requires missing runtime state or unproven terrain/tile origin, report precisely what additional observable would disambiguate it rather than pretending an approximate result is exact.

## Phase 4 — Opportunistic planetary-system leads (secondary)

While examining relevant functions and records, record promising leads about:

- orbital appearance texture overlays and their surface orientation;
- inorganic-resource overlays / distributions and whether they share planetary coordinates;
- landing tile boundaries, tile selection and procedural terrain frame;
- poles, rotation axis, prime meridian, sphere/projection transformations.

These are **lead-register entries**, not deliverables demanding full investigation. Record exact locator, observation, hypothesis, relationship to the main task, version and a focused follow-up question. **Do not expand into a general planetary-generation or resource-overlay research programme.** If a secondary lead is necessary to decode the pair, it may be pursued as part of the main evidence chain; state why.

## Results and stopping standard

Deliver separately assessable results:

**A. Meaning of the saved pair.** Best-supported semantic interpretation, direct data-flow support, numeric tests, confidence and tested coverage. A valid result may be a landing-site anchor rather than beacon coordinates.

**B. Planetary coordinate representation.** If supported, a reproducible equation or procedure with component order, units, axis/origin convention, examples and error checks. If not resolved, give concrete incompatible hypotheses, decisive observations already made, and the *specific* missing mechanism/evidence; do not stop at “the coordinates are mysterious.”

**C. Bridge to beacon.** Explain whether and how the site/overlay coordinate relates to actual beacon local XYZ, distinguishing established from hypothesized steps.

**D. Prior-art register and planetary leads.** Proper attribution, versioning, confidence and proposed later follow-ups, without taking on those investigations.

**E. Next experiment only if essential.** Propose the smallest controlled Save3 or runtime test that would distinguish remaining coordinate conventions, and await separate user authorization. No live testing in this task.

Use the prospective project methodology: lead with the best-supported answer; differentiate observed/proven, strong, provisional and unresolved claims; track scope/coverage independently of confidence; present concrete counterexamples; do not reopen established body identity merely on speculative grounds. A genuinely unresolved coordinate conversion is acceptable only with a persuasive, reproducible account of what remains inaccessible and why the authorized evidence cannot currently distinguish competing models.

## Documentation, safety and review

- Write a durable experiment report, reproducible evidence indexes and a small prior-art/lead register. Update findings, hypotheses and research state only to the degree new evidence warrants; do not silently rewrite previously reviewed results or promote provisional claims without evidence.
- Follow the 40,000,000,000-byte free-space guard for relevant C:/D: activity, avoid huge unbounded outputs and preserve all raw saves, Ghidra databases and installation files. Do not track raw saves, decompressed blobs or third-party assets.
- Reuse existing offline tools and tests. New scripts should be narrow, read-only, documented and self-tested. No in-game mods or debugger sessions.
- Validate source hashes, `git diff --check`, internal links and `git status --short`. Provide task-only and complete diffs if feasible. No staging, commit or push.

### Return for review

Provide (1) best-supported coordinate interpretation, (2) decisive static/data-flow evidence and locators, (3) numerical test matrix across bodies/sites and fixed POIs, (4) confidence/coverage/completeness, (5) prime meridian/pole/axis findings or precise gaps, (6) site-origin versus beacon-position distinction, (7) prior-art sources and permissions/provenance, (8) secondary leads, (9) remaining concrete blockers and smallest next experiment, (10) files changed, checks, Git status and full diff.

Suggested commit title **only if later approved**:

`research: investigate planetary surface-anchor coordinate semantics`
