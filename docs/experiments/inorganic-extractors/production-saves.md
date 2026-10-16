# Candidate save inventory and conditional restoration card

Read-only save specialist and primary checker used the accepted
`save-analysis/scripts/save_menu.py` and hash-bound original source metadata in
`.local-work/manual-S0-S7C/manifest.json` (SHA-256
`2e7bf2412b8752c149a6ee75ad131915e2df975f362a9962c348612bfa417731`).
New receipt: `.local-work/e1-production/verification-02.json`. These are header,
saved inventory and menu-model results, not loaded-state observations.

**S4 is Save12. Literal Save4 is S0, the no-outpost baseline.** All five inspected
headers identify Attila Kiraly, level 3. Kreet saves display Kreet - Outpost.
Archive hashes were freshly verified; original named source paths are absent.

| Corpus label / filename prefix | Original menu time model, 7 October 2026, UTC+11 | Header playtime | Saved/control relevance |
|---|---|---|---|
| S0 / Save4 | 7:23:16 PM | 2h 15m | No outpost baseline, not extractor control |
| S3 / Save10 | 7:26:20 PM | 2h 17m | Iron placement; combat uncertainty |
| S3C / Save11 | 7:26:51 PM | 2h 18m | Simpler unlinked iron control candidate |
| S4 / Save12 | 7:27:46 PM | 2h 18m | Linked iron/storage candidate selected conditionally below |
| S4C / Save13 | 7:28:01 PM | 2h 19m | No-action linked control; same bytes as later L0 |

S4 archive, verified size 2,095,152 bytes, SHA-256
`feafd2bc55d90ae48c2c86c3ef28db44ddf8a8b875a767264a484bd51893aff1`:

```text
D:\Projects\starfield-outpost-research\.local-work\savegames\manual-S0-S7C\Save12_D6036588M417474696C61204B6972616C79_000218_20261007082746_3_0_4.sfs
```

Exact currently absent destination:

```text
C:\Users\User\Documents\My Games\Starfield\Saves\Save12_D6036588M417474696C61204B6972616C79_000218_20261007082746_3_0_4.sfs
```

Accepted inventory `workshop-inventory/final05/manual-S0-S7C-S4.json` (under
`.local-work/`) contains four supported roots / 15 direct members: beacon root
`ff022c64`, base `29a8c6`, dummy `015804`, owner `ff022c5d`;
storage `ff022d48`, base `23aed9`; extractor `ff022da9`, base `05ef19`;
solar `ff022dba`, base `2031e1`, same owner. Resource
reader `extractor-resource/run04/manual-S0-S7C-S4.json`, extractor decoded range
1301053–1301485, ordinal 10539, joins AV `05ef18` → IRES `0057c7` → COBJ `05ef53` →
item `00556e`. Saved producer payload at decoded offset 1299534 is retained opaque
in this continuation; no new float layout is guessed from it. Supported roots
are not an exhaustive live census or proof of enabled, powered, eligible output.

S3/S3C/S4/S4C retain this iron/four-root subset. S4 adds an outgoing transfer
link; it is not a modifier contrast. Later link saves L0C–L2 vary links, not
skills/crew. Save25–28 have no ready producer groups in the inspected reader
output; Save52's 63 qualified instances are a complex mature population without
a causal modifier contrast. S7's extractor is deleted. Therefore select S4 only
as the linked baseline **candidate**; qualify its loaded operation and establish
the proposed crew contrast before any GO. S3C is preferable if links are
unnecessary. No archived save pair currently proves a useful modifier contrast.

## Conditional future card — not executed or authorized

This fragment applies only if a separately approved live brief selects S4 and
explicitly authorizes the copy and any timestamp operation. It is not launch
clearance. The future brief must supply observation scope, finite stop condition,
save/output protection and reviewed observer contract first.

1. With the game exited, inventory/hash the current Saves directory and protected
   archive. Confirm the exact source filename, size/hash above. Confirm the exact
   destination is still absent; stop on collision, ambiguity, missing source or
   hash mismatch. Never overwrite or use a force copy.
2. Copy to the exact destination using exclusive create-new semantics. Rehash
   source and new destination against the stated hash. Preserve all other saves.
3. Timestamp choice must be explicit. Original `mtime_ns=1791361666135597800`
   models 7:27:46 PM at UTC+11. The archive's actual last-write time instead
   models 8:14:33 PM. A timestamp-preserving copy of the archive does **not**
   recreate the original menu time. If separately authorized, retime only the
   newly created destination to the hash-bound original nanosecond timestamp and
   verify it; otherwise regenerate the menu instruction from its actual mtime.
4. Run the accepted save-menu tool on the new destination, using actual timestamp
   provenance and the agreed timezone. Require Attila Kiraly / Kreet - Outpost /
   level 3 / 2h 18m, expected date/time under that choice and exact file identity.
   The timestamp is MENU_MTIME_MODEL, not a decoded header clock. Existing tool
   validation against 12 screenshot rows does not itself screenshot-verify S4.
   Stop if missing/ambiguous; never select by ordinal position or filename clock.
5. Only under separate launch authority, use that verified menu identity. Before
   contrast, qualify extractor/resource/owner, power, halt, eligibility, room for
   output and actual current modifier participants. A nonworking control stops
   the test; do not repair it silently or interpret no output as no modifier.
6. After the separately bounded attempt, exit normally, hash the archive and
   source protection set, inventory incidental outputs and preserve anomalies.
   Removal of the exact temporary copy requires the future cleanup authorization
   and unchanged-copy verification. Never delete changed/incidental/other saves;
   archive them under that future brief. Unexpected corruption stops cleanup.

No copy, retiming, restoration, load or save change was performed here.
