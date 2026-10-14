# Codex implementation brief — Starfield Save-Menu Identification Utility

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)

**Assignment:** Bounded, single-agent offline support utility. Start from the current committed/synced repository and existing save-reader infrastructure. **Do not spawn specialist or reviewer sub-agents for this assignment.** The maintainer and ChatGPT will review the finished diff.

## 1. Purpose and scope

The research corpus uses identifiers such as Save3, Save25, Save26, Save27, Save28 and Save52, but Starfield's Load menu shows a character-filtered collection of save labels, dates and other metadata. Similar Kreet entries are difficult to distinguish, creating a risk that an operator will load the wrong save during native experiments.

Build a small, deterministic, **read-only** tool that maps a known research save file to a concise, player-recognizable Load-menu identification line. It must be useful in future experiment run cards without requiring repeated confirmation of the same character, label and timestamp.

This is an **operational convenience task**, not a reconstruction of the game's complete save-menu implementation. Prefer an accurate, sufficient partial label over expensive pursuit of perfect parity.

## 2. Field priorities

1. **Essential:** Character name and the date/time as shown (or reliably matched) in the Load menu. Determine the source and timezone/formatting behavior rather than assuming filesystem timestamps equal menu timestamps.
2. **High-value, where accessible:** Displayed location (`Kreet - Outpost`, `Kreet - Landing Area`, etc.) and character level.
3. **Useful, inexpensive:** Save kind (`SAVE`, `AUTO SAVE`, `EXIT SAVE`), playtime.
4. **Provenance:** Research identifier, exact source path, save filename, SHA-256, extracted raw metadata and derivation/confidence for each displayed field.
5. **Exclude:** Dynamically assigned Load-menu ordinal and `[C]` Creation Club indicator. No need to reproduce these.

**Minimum satisfactory result:** A truthful, consistent mapping containing character name plus a menu-matching timestamp that distinguishes the current relevant research saves. If some metadata are unavailable, omit or mark them unknown; never invent the label or copy an unverified illustrative value into results.

## 3. Inputs and independent controls

- Reuse the existing save parser, metadata readers, corpus inventory, pinned archive copies and read-only provenance tooling. Inspect current code before implementing new parsing.
- Cover at least the relevant accessible Save3/Save25/Save26/Save27/Save28 lineage and mature Save52 where available. Account for distinct character lineages (for example Attila Kiraly versus Cao Tran) rather than assuming all Save52-like entries belong to one character.
- The maintainer previously supplied Load-menu screenshots including an Attila Kiraly save list. Seek already-present screenshots or documented verified transcriptions in repository evidence; if not available to Codex, explain the limitation. Do not claim screenshot-based verification if screenshots are absent.
- Compare recovered values to independent in-game screenshot/transcription data where available. Preserve exact display date/time and locale assumptions. A location label may require localization or game-record resolution; that is optional if the primary identification pair is sufficient.
- If two or more saves have indistinguishable visible menu labels, flag a **collision** and provide safe additional clues (e.g., filename, neighboring save timestamps) without pretending the menu displays an unsupported unique identifier.
- Do not rely on displayed menu order as a permanent identity. An operator may use the documented character filter.

## 4. Implementation deliverables

Provide a minimal command-line interface that accepts one or many exact save paths and/or an existing research identifier mapping, and produces:

- A concise human-readable Load-menu instruction, e.g. `Load Attila Kiraly Save25 — Kreet - Outpost — Level 4 — 10/9/26, 9:22:22 PM` **only if each displayed field is independently supported**.
- A structured JSON or CSV inventory preserving provenance, unknown-field states, original source values and collision warnings.
- A documented invocation example suitable for incorporation into future live run cards, with the operator told **which entry to load before gameplay**; avoid repeated after-the-fact confirmation absent genuine mismatch.
- Focused tests for parsing, time formatting, absent fields, multiple characters, collision detection and safe failure on malformed saves.
- A concise report describing recovered fields, validation against controls, limitations and where future save-label support should be extended if needed.

Prefer a small standalone module using existing repository dependencies. Never alter, rename, normalize or rewrite a `.sfs` file; no game execution or native instrumentation.

## 5. Effort boundary and completion contract

This task deliberately uses **practical sufficiency**, not universal completeness.

- Investigate save headers and the existing reader first. Pursue readily available metadata and minimal game-record lookup if needed.
- Do not expand into native Load-menu reverse engineering, whole-save format reconstruction, Creation Club indicators, full localization or exact playtime calculation merely to fill optional fields.
- When the essential character/timestamp pair is reliably recovered and the current save population can be distinguished (or ambiguities are accurately reported), complete the task even if optional labels are unavailable.
- If the essential fields cannot be recovered from available offline data, make a bounded, evidence-backed negative finding explaining the precise obstruction and best practical fallback; do not label unsupported values as exact. Resolve ordinary implementation/test errors within this assignment.
- No arbitrary time or evidence-volume hard stops; honor established 40,000,000,000-byte free-space safeguards on both drives for substantial processing.
- No additional user gameplay/screenshot requests are needed to implement the utility. If independent validation is genuinely impossible without a new screenshot, produce the useful offline output and clearly mark the validation gap rather than blocking unnecessarily.

## 6. Review and preservation

- **Single primary Codex agent only**. Do not invoke independent-review or specialist sub-agents for this maintenance/support assignment.
- Follow current `WORKFLOW.md` for preservation, traceability and review packaging except for this explicit sub-agent exception.
- Preserve save archives, executables, game databases, frozen predictions and prior research evidence byte-for-byte. Read-only inspection and new derived artifacts in ignored local-work directories are permitted.
- Produce both `-complete.diff` and `-task-only.diff` under `.local-work/diffs/`, including new text files; provide `git status --short`, file/sha manifest, exclusions and forward/reverse patch checks. Do not stage just to generate review diffs.
- No Starfield launch, Vortex changes, save creation, external debugger, publication, staging, commit or push.

## 7. Final handoff

Return the exact code/report locations, example *actually generated* labels for the controlled lineage, structured output location, comparison with available screenshot controls, collisions, test results and review-diff links. State **COMPLETE — PASS** when the sufficiency criteria are met, or provide a bounded documented limitation if essential metadata cannot be recovered.

**Do not propose a separate extended reverse-engineering phase just to make the labels perfect.** After maintainer review, the project returns to outpost inorganic-resource availability research, using the unplaced-beacon `Available Resources` panel as the key independent gameplay oracle.
