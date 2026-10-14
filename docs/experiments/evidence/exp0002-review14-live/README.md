# SOR-EV-0004 — Review 14 primary controls and thread discrepancy

2026-10-06 Australia/Sydney. SOR-D-0013 / SOR-EXP-0002. [Run record](../../EXP0002-review14-run.md). Authored index REVIEW-REQUIRED; raw artifacts LOCAL-ONLY. A0/A0C completed and two manual saves were archived. The sequence stopped before construction/A1 because A0 ran on a different thread from the loader-identified main thread. No selected-reference query, debugger, observer code modification or automatic retry. Game exited normally and observer retired through user-managed Vortex.

Local paths below are relative to ignored `.local-work/exp0002-review14-live/`. Exact private source/save locators are retained only in JSON manifests. Original files and archives preserve exact bytes; no normalization or save semantics inferred. The original A0C save observation remains REQUIRES_REVIEW because it included the later incidental exit save; post-exit.json explicitly resolves the one manual/one incidental distinction using user confirmation and timestamps.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| preflight.json | 50092 | `aa858b9fa9e0127535e59ce7df2c3814aa08d7c307e66eb112eee3fee50bb455` |
| session-start.json | 584 | `eaf40a24f8aa0650569df5531d8bdd020dfe4815f366dfa447c7c3351c980369` |
| A0-capture.json | 674 | `6e33608ab819872e157ee5c8637ed981e0ba272abf5002ce0ff40e9d6fdb0245` |
| A0-save-observation.json | 570 | `1c75cb852659d862d9995845b44dbab0c4fea34920abb35acb2d2f760f232a1e` |
| A0C-capture.json | 676 | `ea8015965484eceaca9565a8b8a8447d22fe8c453e84f4c807b873a4d9e859ba` |
| A0C-save-observation.json | 875 | `7ece6a327d194243b4dafc795d993e8afdd8cd5b9c738cfca581f4a65ec73e0d` |
| post-exit.json | 89331 | `f318fc227c6b4ae8bef83b3b07b5dd502c480d65c79b58e6185d59aa8b8104e9` |
| archive/observer/A0-begin.json | 254 | `05ca14ce938eacc3acd23d73722991a01f1590508b016123668ae3ff8fbbdb17` |
| archive/observer/A0.json | 2156 | `27d89814a8a893603ce6a9f530e3fff9dbb08b20ea2856947ec7c2772c7fed34` |
| archive/observer/A0C-begin.json | 255 | `c68d21b9a1af718917998073c0cf9672d6b6928c68f4d2dadc520e4c3fb2f77b` |
| archive/observer/A0C.json | 2158 | `f763441b19202f0277b422d6e4905dfc0231cfdbeda4edca45b113bbf675f015` |
| archive/observer/modules.json | 4129 | `f35d550418f813f2d3a845c178422b38c8e6fd8801b141aebf45c72f308dbecb` |
| archive/observer/ready.json | 219 | `b474513ff9b575799b09d20a1d792dbf236ce600073de537afdef2120979507d` |
| archive/observer/request-A0.txt | 11 | `c85ce4e1b13c41a45e3a1910ab7ef022f69066bc39be057cdd5c2239c3419d8d` |
| archive/observer/request-A0C.txt | 12 | `02eed6b023d83420aad55f21688687cc398327ed189d9a0081dd31657e27af1f` |
| archive/sfse-logs/sfse.txt | 1088 | `91097ac62b339ab01ac5730f2f638173fbf19413784fd33590fc8d68f6c657a1` |
| archive/sfse-logs/sfse_loader.txt | 1293 | `4dd48c302f38a88e57fcbd61f40d606140a457f91ecc3a9525f49d7893ed32d5` |

Neutral save identities: SOR-SAMPLE-0002/A0 (2,082,992 bytes, SHA-256 `7d25e02cc0ac4bc81ab7d966a73c84ade0c6c795d154aa625d85b0aaf259fa66`); SOR-SAMPLE-0003/A0C (2,066,048 bytes, SHA-256 `875f2e8460d3e5adfdfc15de860a57b991139195905ffff461c43fdf59409d0c`); incidental exit (2,074,288 bytes, SHA-256 `adaf84c0708214ed2055148fb196c7d461427ba1f8641855eef40f8456d077a1`). Sources and copies matched with stable metadata. Previous exit-save filename disappeared from the game directory but its verified first-attempt archive remains available. Protected parent/backup hashes, sizes and mtimes unchanged.

Source SOR-S-0119 supplies read-only task-dispatch context; runtime thread IDs and loader log supply the direct discrepancy. Header/source inspection alone does not establish installed-binary scheduling or alternate-thread callback safety. Successful control capture validates neither atomicity nor outpost membership/reload semantics. Current live helpers `record.py` and `archive.py` describe their scoped reads/writes and never issue requests or modify source saves. Review artifacts in the same local root: review.diff, validation.json, status.txt, hashes.json. Full diff includes prior task work and the supplied private-path brief; not cleared for publication.
