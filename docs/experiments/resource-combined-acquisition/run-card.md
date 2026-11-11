# D5B proposed Phase B: one Feynman V session

**PHASE B NOT AUTHORIZED. DO NOT LAUNCH OR ATTACH TO STARFIELD.**

2026-10-25, Australia/Sydney. Prepared under the [Phase A brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5B_combined_construction_mask_consumer_acquisition.md`). This is a proposal for separate explicit maintainer approval. Independent Phase A ACCEPT does not approve execution. [Native contract](native.md), [result classes](report.md), [qualification/review](review.md).

## Exact target and information value

One prospective Steam-launched Starfield process, one Save52 load, direct ordinary travel to the active **second Feynman V outpost**, one Build Mode entry. Saved Workshop bytes are `b0e207c2dee2c1b6`, saved beacon token `84e101`, saved frame `0x2b`, owner/body FormID `0x0005e0de`. Qualified interior chart 0 and descriptor (37536,20928) must select **only** source `0:37536:20928:0029d20e`. Installed chain is SFTR `0x00168814` -> SFPT `0x0023ddf3` -> SFBK `0x0029d20e`, BIOM `0x00145440`. Machine identity contract is `research/resource-combined-acquisition/target.json`.

Ordinary candidates are IL `0x000057d4`, Fluorine `0x000057d0`, Copper `0x000057cf`, main-file identities required. Fixed masks 0/3 have different weight vectors and geometry, although both predict all three names. No resource name or screenshot label chooses the mask.

A positively source-bound original construction query and sampled ordinary mask is useful **construction-only** evidence. A current Workshop-bound ACCEPT and same-evaluation transfer adds **consumption** evidence. Their shared geographic source is not a population-epoch join. Retail linkage and historical first query remain UNKNOWN. A correctly captured contrary mask or resource sequence is retained as a contradiction, not discarded to fit either alternative.

Normal revisits may reuse cached sources and never construct this source. Consumer-only then establishes current accepted geometry, not a historical construction mask. No hit leaves the primary question unresolved. A same-planet or neighboring-source construction is unrelated and must not trigger successful STOP. No guaranteed generation trigger is claimed.

## Frozen build, inputs and guards

Reviewed executable/source pins are supplied by the final manifest recorded in [review.md](review.md), under `.local-work/resource-combined-acquisition/`. The exact manifest and controller hashes below must match that reviewed package before any approval is issued:

| Artifact | SHA-256 |
|---|---|
| Combined build manifest | 584b7003712e953682e31b40473f90bb9bffdb36751d9fad8cc25c262eab8a2e |
| Retail controller | 5b3a915b24928be1facf7f546ff3a3c283f76e1e7df615ef2b6fa91d39ecfa48 |
| Synthetic fixture | a6abb42d4551a41d6d64bcbad6bfa34fad2f032e40a5641fa6b738de763663b0 |

The manifest pins every authored controller/wrapper source, both fixtures, inherited decoder/transport/header inputs and installed MSVC setup. The final review manifest additionally pins this card, target JSON and schemas. A changed source, binary or card requires fresh qualification/review; no silent replacement of these pins is permitted.

Retail inputs are fixed independently:

- Starfield.exe 1.16.244.0: `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
- Starfield.esm: `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
- PlanetData BA2: `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`.
- Save52/HIST-0267: `6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.

All loaded definition files, plugin/load-order/INI configuration and protected prior evidence must equal the reviewed installed baseline. Unknown or changed configuration is NO-GO, never an automatic rebaseline. No plugin installation, hook, native call, injected observer or game configuration change is part of this proposal.

The actual module base must be measured in SESSION. Preferred static base `0x140000000` is never used as the runtime base. [Native.md](native.md) specifies all 15 observed instruction sites and register/stack ownership. `preflight.py` independently reads their 16-byte on-disk guards and checks updater/callback/transfer call destinations; the controller checks runtime instruction bytes against the pinned PE again. Runtime pointers, FormIDs, source ordinals, saved tokens and file offsets remain separate domains.

## Strict preflight GO/NO-GO

Before requesting live approval, rerun the complete required synthetic roster on the exact reviewed build with fresh ignored output. Its build hash must equal the reviewed manifest and all mandatory scenarios must pass. Preserve every failed attempt. Reuse no stale live gate or PID.

Require Starfield absent, both C: and D: caller-available free space at least 40000000000 bytes, qualified source/frame/Workshop selection, independent readback transport and repaired terminal STOP. The preflight audits installed definitions/configuration, all designated research/manual/quicksaves and historical backups. It creates fresh independently hashed master copies outside game/Steam/Cloud write paths and rehearses Save52 restoration **only to a scratch file**. It never overwrites an original or sole backup.

Apply [SAVE_PROTECTION](../../SAVE_PROTECTION.md): reliably classified active autosaves/exitsaves are diagnostic churn and nonblocking; ambiguous save names fail closed. Explicit research designation overrides kind; `funclist.sfs` remains protected. Archived backup corpus is always strict. Verify Documents, Steam remote Saves and remotecache namespaces, and reject unexpected reparse/sync ancestry. The operator must freshly confirm Steam Cloud disabled through postflight. A file receipt cannot establish the UI setting; UNKNOWN is NO-GO. Do not change it automatically.

Offline commands, using fresh names, are:

```powershell
$d5bPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $d5bPython -B research/resource-combined-acquisition/qualify.py --build .local-work/resource-combined-acquisition/REVIEWED_BUILD --output .local-work/resource-combined-acquisition/FRESH_QUALIFICATION
& $d5bPython -B research/resource-combined-acquisition/preflight.py --build .local-work/resource-combined-acquisition/REVIEWED_BUILD --qualification .local-work/resource-combined-acquisition/FRESH_QUALIFICATION/summary.json --name FRESH_PREFLIGHT
```

Replace placeholders with the exact reviewed build and fresh lower-case output names. Placeholders must be resolved from the exact reviewed manifest; the original Phase A paths are in review.md. Any failed guard, backup comparison, malformed receipt, missing independent review or unclassified save prevents approval/attachment. Full save hashing is offline before launch and after exit. During play use only the bounded namespace/size/health checks unless a specific integrity incident justifies a full rescan.

## Separate approval and single session

The maintainer must explicitly approve this exact card/build/preflight for **one** session and confirm Cloud disabled. Retain that instruction verbatim with its UTC time and card/build/preflight SHA-256 pins in an exclusive approval receipt. The optional `--stop-after-construction` mode requests ACK-controlled disposal immediately after the primary result; its boolean must be explicitly bound as `stop_after_construction` in the approval receipt. Otherwise the operator can request construction-only STOP through the STOP file. Required fields are `status=GO_PHASE_B`, `human_instruction`, `card_sha256`, `build_sha256`, `preflight_sha256`, `cloud_disabled_confirmed=true`, `used=false`. The wrapper writes a non-overwritable consumed-gate receipt before attachment. A gate records authority; generating a JSON file never creates authority.

After that separate approval and successful admission:

1. Record UTC immediately before launching exactly one process through ordinary Steam `steam://rungameid/1716740`. Record PID, process start UTC and image path. Do not launch the executable directly. The controller must be started as the same ordinary user; do not elevate, enable privileges or alter security settings.
2. Attach the pinned controller to that newly Steam-launched disposable process before the single Save52 load. Record the measured module base, original debug state and instruction guards. Debugger attachment, all-stop pauses, DR execution breakpoints and RF resumption can alter timing; this is not an intervention-free experiment.
3. Load Save52 once. Travel directly by normal gameplay to the specified second Feynman V outpost, then enter Build Mode once. Record load/travel/Build Mode UTC times, displayed site/body identity, screenshots if useful, and any anomaly. The saved identity checks, not display labels, determine admission.
4. Do not teleport, force regeneration, invalidate caches, call console/native functions, change saves or repeat a load/Build Mode entry. Do not visit another outpost to improve the hit rate. If normal play yields no constructor, preserve current cached-consumer evidence and classify it accordingly.
5. The wrapper switches to consumer capture after a durably acknowledged qualified construction. An independently bound current consumer can complete the combined-unlinked result and trigger ACK-controlled STOP. The operator may request STOP once the useful construction-only result is durably acknowledged, or after the one normal sequence ends without it. A construction from any other key cannot trigger successful STOP.

The future attachment command, **not to be executed under Phase A**, is:

```powershell
& $d5bPython -B research/resource-combined-acquisition/collect.py --retail-pilot --approval .local-work/resource-combined-acquisition/APPROVED_GATE.json --preflight .local-work/resource-combined-acquisition/FRESH_PREFLIGHT/preflight.json --build .local-work/resource-combined-acquisition/REVIEWED_BUILD --pid NEW_PID --launch-utc RECORDED_UTC --output .local-work/resource-combined-acquisition/FRESH_CAPTURE
```

## Stopping, durability and recovery

Each sample is bounded, written to a new SRO1 file, fsynced, closed, reopened and independently decoded before the numbered ACK. No automatic healthy-run deadline, event quota or evidence-volume cutoff applies. Preserve both-drive free-space, target identity, instruction guards, protected inputs, worker/transport integrity and explicit STOP. The ten-second terminal drain applies only after disposal, not to gameplay or scientific observation.

Creating the capture directory's `STOP` file requests controlled disposal. The wrapper also stops for disk protection. Invalid/refused/EOF ACK commits terminal intent before termination; no later SAMPLE, PHASE or breakpoint rearm is permitted. Drain pending Windows events to process exit. Do not detach/replay onto a dying process, suppress a game exception or restart it automatically.

Preserve outcomes separately: `NO_HIT` means no sampled evidence; `PARTIAL` means an incomplete qualified attempt; `UNBOUND` means wrong or unqualified identity; `INVALID` means failed reads/shape/receipt checks; `LOSS` records exception or observation gaps. Construction-only and consumer-only are distinct useful scopes. Observed zero calls or an empty transfer remain observations, not aliases for no hit. A crash before useful persisted evidence is not success; complete acknowledged evidence collected earlier survives a later crash and is reported separately from target survival. Retain truncated/refused evidence and debugger-induced failures.

After exit, verify the PID absent and perform full strict postflight before any recovery decision:

```powershell
& $d5bPython -B research/resource-combined-acquisition/postflight.py --preflight .local-work/resource-combined-acquisition/FRESH_PREFLIGHT/preflight.json --output .local-work/resource-combined-acquisition/FRESH_POSTFLIGHT.json
& $d5bPython -B research/resource-combined-acquisition/compare.py --receipts .local-work/resource-combined-acquisition/FRESH_CAPTURE --output .local-work/resource-combined-acquisition/FRESH_COMPARISON.json
```

The read-only comparator uses both unchanged D5A alternatives. No fit, retrospective mask substitution or historical epoch assertion is allowed. Verify active protected saves, fresh masters, archived backups, Steam namespace metadata, installed content/configuration and original evidence; preserve transient churn diagnostics. Preserve raw originals and seal a stream-verified lossless archive using the existing [phase-aware session tools](../../../runtime/session-tools/README.md) after offline postflight. Do not restore or delete anything automatically. Unexpected protected changes or corruption require a named maintainer recovery decision.

No automatic retry, second process, new source, extra outpost, historical mutation-bug reproduction, B6, product integration or publication follows. VI-b source `0:29568:10932:0006ce58` is only a designated future alternative; its retail test requires new maintainer review and explicit approval.
