# Outpost defense technical reference

[Reader guide](../guides/defense.md) ·
[Claim and evidence map](../audits/remaining-guides-d5bc/claims.md) ·
[Input and address provenance](../experiments/outpost-defense/evidence.md#input-and-address-provenance)

STATIC paths use retail 1.16.244.0, installed definitions and shipped
compiled scripts. Native locators are preferred static VAs at image base
`0x140000000`. PEX member positions, decoded save-stream positions and
native object displacements use separate bases. The [source review](../experiments/outpost-defense/review.md)
qualifies sampled SAVE corroboration and offline checks.

## Opportunity, eligibility and quest lifecycle

| Branch | Writer, inputs and consumer | Scope and negative case |
| --- | --- | --- |
| Arm a check | Beacon ACTI `0x002c60e9` binds OutpostBeaconScript to quest `0x0007092c`. OnLoad and OnWorkshopObjectPlaced with nonempty GetValueResources arm timer ID 1 for 12–48 seconds. OnTimer calls CheckForAttack with ordinary arguments. | One-shot. The shipped range supersedes the commented alternative. No wait-hours replay or timer-side rearm in this script. |
| Apply shared gates | CheckForAttack reads AllowAttacks, current planet match and ancestor LocTypeMajorOrbital. Prior nonzero LastAttackRoll `0x0024f6a0` needs at least 0.04 game days and ordinary positive LastAttack `0x00127239` needs 7 game days. | Timestamps are on the ancestor planet location and use current game time. They are shared by qualifying outposts there. No universal orbit equivalence. |
| Try Armillary | MQ204 `0x002c6d74` stage 620 and outpost resource `0x001f36bf` ≥1 qualify the installed condition. A separate 0.5 draw can request event `0x00349c9e` and quest `0x00349c9c`. | A returned quest skips the ordinary roll and its roll stamp. CountsAsAttack is false. Prior ordinary cooldown still gates entry. The resource test differs from visual presence or a global location label. |
| Draw ordinary event | One random value chooses creatures at ≤0.08, otherwise humans at ≤`0.10 + 0.01R + 0.05C + S`. R is the positive sum from the installed 111-entry resource AV array, C is cargo AV `0x000a46ff`, and the installed special event supplies no S increment. | With zero operands this predicts about 8% creature and 2% human event requests per eligible ordinary draw. The ordinary branch stamps the roll even without a request. No defense subtraction is present. |
| Resolve encounter and target | The event passes the beacon. Human alias 231 resolves it and alias 232 creates an attack marker. Landing eligibility uses a 2000-native-unit bound from the beacon on the mapped quest. Arriving actors can invoke AttackOutpostObjects and StartAttack. | Landing distance describes spawn context. Event request, successful quest, arrival and actual damage are separate outcomes. |

[Exact script and definition trace](../experiments/outpost-defense/attacks.md#ordinary-causal-trace) ·
[Armillary branch](../experiments/outpost-defense/attacks.md#armillary-and-starborn)

Native attack targeting traverses reverse WorkshopItem links from the checked
beacon, selecting references with destructible-capability bit 24 set and
destroyed bit 23 clear. The human target-unload callback can call SetDestroyed
for targets without loaded 3D after attack start if attackers remain alive.
The mapped creature subclass lacks that human override. Cleanup checks
survivors and player planet when its event is delivered. The relative order
of unload and cleanup during travel was unobserved.
[Target and cleanup paths](../experiments/outpost-defense/attacks.md) ·
[Contributor matrix](../experiments/outpost-defense/defenses.md)

## Health, state flags and repair

- **Indicator.** `0x14158a6e0` resolves the selected reference and computes
  effective current Health divided by permanent Health when permanent is
  positive. Permanent can include section 0 modifiers over base. The native
  producer emits −1 otherwise and does not clamp the ratio. The card hides
  the invalid value. Actor turrets use actor Health dispatch. Qualified
  destructible nonactors have a component-derived base fallback even without
  explicit Health PRPS. Inspected ordinary stores and cargo compartments
  lack that destructible component.
  [Indicator and object matrix](../experiments/outpost-defense/integrity.md#indicator-and-definition-provider)
- **Damage and destruction.** A qualifying nonactor damage operation changes
  modifier section 2 and evaluates destruction stages. Terminal damage sets
  destroyed mask `0x00800000`. SetDestroyed can change that bit directly,
  so the bit need not encode a gradual damage history. Disabled `0x800`
  and deleted `0x20` are separate reference flags. Production and power
  check their own invalid-state gates. Partial damage does not scale ordinary
  production timing through this path.
  [Damage and consequences](../experiments/outpost-defense/integrity.md#damage-and-operational-consequences)
- **Repair.** HUD and Build Mode reach `0x1421e3f50` with Workshop owner,
  broken-state, recipe and NoRepair checks. The service resolves the
  construction's handles and restores qualifying damage and clears destroyed
  state on the existing reference. The mapped action neither checks nor
  spends ingredients and does not perform ordinary quota/budget insertion.
  The direct Papyrus repair binding has a separate entry and eligibility path.
  [Repair chain](../experiments/outpost-defense/integrity.md#repair-identity-and-accounting)

## Saved observations and access

HIST-0255 has five owned partially damaged devices in ExtraBF. The writer
and loader preserve applicable AV modifiers and restore destroyed state
through separate form flags. For saved `0xff0202dc` the decoded-stream
record starts at `0x4f51a9` (decimal 5198249) and the damage value is at
`0x4f5205` (decimal 5198341). The reported −144 and
same-base no-override control support a conditional 0.64 versus 1 comparison.
They leave the cause, time, encounter rate and repair history open.
The report also closes the prior explicit-owner gap for two historical
turrets through ExtraE6 framing, with later actor tails and loaded power/AI
outside that result. Historical quest/timer resumption remains untested.
[Saved contrasts and state matrix](../experiments/outpost-defense/persistence.md)

**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING.** Tracked paths support
inspection of the predicates and conditional arithmetic. Primary PEX/native
and protected save witnesses remain separate dependencies.
