# D1 public-source ledger

Consulted **2026-10-16, Australia/Sydney**. SOR-S-0151–0158 below are
SOURCE-REPORTED evidence, independently distinct from Bethesda executable
instructions and project save analysis. Paraphrases only; no third-party code,
images, saves or substantial source text is incorporated. No issue/comment,
permission request or evidence upload was sent. Reports are credited at use.

| Source record / original source | Date/build and actual access | Observation, workaround and evidentiary limit |
|---|---|---|
| SOR-S-0151 — [Reddit 16jwju9](https://www.reddit.com/r/Starfield/comments/16jwju9/is_anybody_else_noticing_outpost_resource_sources/) and its participants | 2023-09-16 supplied date; page accessible; individual builds unknown | Andraphon He-3 loss, old extractors reportedly operating, new placement blocked. Replies describe different replacements and inconsistent restart/reload recovery. These are heterogeneous reports, not one demonstrated trigger or cache diagnosis. |
| SOR-S-0152 — [Reddit 169ko1k](https://www.reddit.com/r/Starfield/comments/169ko1k/mineral_veins_disappearing/) and its participants | 2023-09-04 supplied date; page accessible; builds unknown | Post-load vein loss and placement restrictions; variable resource lists and reload outcomes. Power-wiring advice is uncontrolled, with no demonstrated native power→region dependency. |
| SOR-S-0153 — Constellation-VASCO, [SFCP #703](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues/703) and [reporter follow-up](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues/703#issuecomment-1837113174) | Opened 2023-11-29; reported 1.8.86.0; HTML, connector issue metadata and all one comment inspected | Kaptyen I: Nickel loss/Platinum→Nickel, installed extractors reportedly continue. Some travel sequences changed veins, others did not; occasional save reload recovery. This is a limited reporter sequence, not deterministic independent reproduction. |
| SOR-S-0154 — [Reddit 1blg5g6](https://www.reddit.com/r/Starfield/comments/1blg5g6/) | March 2024 supplied date; search excerpt accessible, direct opens failed | Iron/Copper loss; replies suggest checking actual extractor output and variable reload success. Uses the brief summary plus search excerpt, not a claimed full-thread inspection. No output test performed here. |
| SOR-S-0155 — [Reddit 1i90iio](https://www.reddit.com/r/Starfield/comments/1i90iio/) | 2025-01-24 search excerpt; direct opens failed; builds unknown | Distinguishes depletion from intermittent reassignment; old extractors reportedly remain. No verified depletion or generation mechanism supplied. |
| SOR-S-0156 — Berto5690 and replies, [Reddit 1svi772](https://www.reddit.com/r/Starfield/comments/1svi772/outpost_resource_vein_disappeared/) | 2026; brief says April, fetched rendering says “4mo ago”; exact posting date unverified; page accessible | Lead lost after a supplies trip; reload/wait did not restore it for the poster, a reply reports later reappearance. Date ambiguity retained rather than silently accepting the brief's month. |
| SOR-S-0157 — Bethesda official notes: [1.10.31, 2024-03-19](https://bethesda.net/en-US/news/starfield-update-1-10-31-march-19-2024), [1.11.36, 2024-05-15](https://bethesda.net/en-US/news/starfield-update-1-11-36-may-15-2024), [1.16.236, 2026-04-07](https://bethesda.net/zh-TW/game/starfield/news/starfield-free-lanes-update-notes), [1.16.242, 2026-05-14](https://bethesda.net/en-US/news/starfield-update-1-16-242-may-14-2026), [1.16.244, 2026-06-11](https://bethesda.net/en-US/news/starfield-update-1-16-244-june-2026) | First two and last two pages opened; 1.16.236 official-domain indexed release text inspected; attempted guessed English 236 URL failed | March 2024 includes a local Gagarin harvesting correction; May 2024 has other outpost fixes. Free Lanes adds outpost features; 242/244 list other fixes. None of the inspected text identifies or repairs D1's general changing/departing-deposit mechanism. This is not an audit of every patch ever released. |
| SOR-S-0158 — [Steam ore-patch discussion](https://steamcommunity.com/app/1716740/discussions/0/3824174193414859655/), [Reddit 172yone](https://www.reddit.com/r/Starfield/comments/172yone/), [Reddit 177c4kx](https://www.reddit.com/r/Starfield/comments/177c4kx/) | 2023 search excerpts; Steam direct fetch failed; versions unknown | More substitution/loss reports and speculation that seeds are not saved. No code, save-byte proof or accepted fix accompanies the inspected claims. Seed speculation was not promoted to a finding. |

SFCP current connector result: **open**, `closed_at=null`, last update
`2023-12-02T10:24:59Z`, one comment. Current returned labels are
`Platform: PC (Steam)` and `Type: Outposts`; **Needs Vetting was not returned**. This corrects
the brief's label statement for the fetched state. HTML Development shows no
branches/PRs. The connector comment contains a reload suggestion, not a fix.
Full API timeline could not be accessed through the web tool, so historical label
transitions and every possible cross-referenced PR are not claimed audited.
Local public-connector-receipt.json retains exact metadata and the search scope.

## Broader search coverage

The following query families were executed through the public web tool, not
merely proposed. Search time is the access date above. Results were screened for
the specific disappearing/changing resource geometry symptom; unrelated cargo,
greenhouse, graphical-cache and other-game results were rejected.

| Exact search query | Inspected result / limitation |
|---|---|
| `Starfield disappearing resource veins bug fix Bethesda patch deposits changed` | User threads, SFCP #703 and unrelated outpost fixes; no inspected native diagnosis. |
| `Starfield resource veins disappearing fix 2025 2026` | 2025 depletion/reassignment thread, 2026 reports and unrelated mods; no verified general fix. |
| `site:github.com/Starfield-Community-Patch resource veins disappearing 703` | #703 inspected directly. |
| `site:github.com/Starfield-Community-Patch/Starfield-Community-Patch "resource" "disappearing"` | #703; unrelated repository search contamination rejected. |
| `site:github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues "veins"` | #703; supplemented by connector search below. |
| `site:github.com/Starfield-Community-Patch "703" "fix"` | #703 and unrelated version-number hits; no inspected fix. |
| `site:github.com/Starfield-Community-Patch/Starfield-Community-Patch "veins" "closed"` | No relevant documented closure among returned hits. |
| `site:starfieldpatch.dev "veins"`; `site:starfieldpatch.dev "resource" "veins"`; `site:starfieldpatch.dev "703"` | No useful accepted-fix page returned. This is search coverage, not a complete release changelog audit. |
| `site:bethesda.net Starfield update "veins"`; `site:help.bethesda.net Starfield "deposits" "outpost"` | Unrelated-game notes and general gathering support; no D1 explanation established. |
| `site:bethesda.net Starfield "1.16.244" update`; `site:bethesda.net/en "Starfield Update 1.16.244"` | Official June 2026 notes inspected. |
| `site:bethesda.net/en-US/news/starfield "outposts" "resources" "Fixed"` | Official March/May 2024 notes inspected. |
| `site:bethesda.net/en-US/news "1.16.236" "Outposts"` | Official Free Lanes release text; region URL above. |
| `Starfield disappearing veins fix cache seed explanation` | Steam seed speculation, Reddit reports, unrelated shader-cache advice. No native linkage verified. |
| Connector: `repo:Starfield-Community-Patch/Starfield-Community-Patch veins`, limit 20 | Two results: #703 and #37 (Caelumite harvesting difficulty, a different symptom). No third-party sample download or code reuse. |

Known-cause/fix conclusion: **not established by the inspected sources**.
Inconsistent reload/power advice and repeated reports are useful for choosing
observations, but cannot discriminate cache retention, changed descriptors,
placement logic or actual production. Search snippets and rendered relative
dates have weaker provenance than the directly fetched issue metadata.
