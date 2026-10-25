# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure offline receipt reduction; no target, file, save or Git effects.

Owned D5 geographic gate and D4A consumer ancestry are reused under SOR-P-0002.
Tokens describe observer invocations, never native population epochs.
"""
import importlib.util
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
SOURCE = '0:37536:20928:0029d20e'
BODY = 0x5e0de
WORKSHOP = 'b0e207c2dee2c1b6'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


gate = load('d5b_gate', 'research/resource-feynman-d5/source_gate.py')
consumer = load('d5b_consumer', 'research/resource-combined-acquisition/consumer.py')


def source_key(source, descriptor):
    """Decode only the qualified interior chart; unsupported charts fail closed."""
    if len(source) != 0x70 or len(descriptor) != 0x2c or descriptor[0] != 0:
        return None
    x, y = struct.unpack_from('<2i', source, 0x10)
    dx = sum(struct.unpack_from('<i', descriptor, o)[0] * m
             for o, m in ((4, 192), (0x14, 12), (0x24, 1)))
    dy = sum(struct.unpack_from('<i', descriptor, o)[0] * m
             for o, m in ((8, 192), (0x18, 12), (0x28, 1)))
    return f'0:{dx+x}:{dy+y}:{struct.unpack_from("<I", source)[0]:08x}'


class Tracker:
    """Retain contradictory constructions and independently bound consumption."""
    def __init__(self, synthetic_proof=None):
        self.session = None
        self.synthetic_proof = synthetic_proof
        self.links = []
        self.empty_transfers = []
        self.samples = 0
        self.invalid = False
        self.partial = False
        self.producer = gate.Tracker('0005e0de', dict(chart=0, descriptor=[37536, 20928], source_keys=[SOURCE]))
        self.consumer = consumer.Tracker()
        self.pending, self.entries = {}, {}
        self.constructions, self.consumptions, self.loss = [], [], []

    def feed(self, row):
        kind = row.get('kind')
        if kind == 'SESSION':
            if self.session is not None and self.session != row:
                raise ValueError('multiple sessions in one reduction')
            self.session = row
        if kind == 'ACK_ACCEPTED' and row.get('accepted') is True:
            for item in self.constructions + self.consumptions:
                if item.get('terminal_capture', item.get('transfer_capture')) == row['capture']:
                    item['acknowledged'] = True
        if kind in ('LOSS', 'EXCEPTION', 'PHASE', 'THREAD_END'):
            tid = row.get('tid')
            self.entries = {k: v for k, v in self.entries.items() if kind == 'THREAD_END' and k[1] != tid}
            self.pending = {k: v for k, v in self.pending.items() if kind == 'THREAD_END' and k[1] != tid}
            if kind != 'THREAD_END':
                self.loss.append(dict(kind=kind, capture=row.get('capture'), qualification='NO_LIFETIME_JOIN'))
            if kind == 'PHASE':
                self.producer.active.clear()
                self.producer.frames.clear()
                self.consumer.active.clear()
        if kind == 'SAMPLE':
            self.samples += 1
            self.invalid |= row.get('required_reads_complete') is not True
            key = (row['pid'], row['tid'], row['thread_lifetime'])
            if row.get('site') == 'provider_entry':
                self.pending[key] = dict(first=row, selected=None)
            pending = self.pending.get(key)
            if pending and 'initial_query_xy_i32' in row:
                pending['selected'] = row
            if row.get('site') == 'generation_entry':
                self.entries[key + (row['invocation_token'],)] = dict(entry=row, pending=pending, samples=[])
            inv = self.entries.get(key + (row.get('invocation_token'),))
            if inv:
                inv['samples'].append(row)
            prior = self.producer.active.get((row['tid'], row['thread_lifetime'], row.get('invocation_token')), {})
            zero_ready = (row.get('site') == 'provider_return' and prior.get('ok') is True
                          and row.get('frame_matches') is True and row.get('required_reads_complete') is True)
            ready = self.producer.observe(row) or zero_ready
            if inv and row.get('site') == 'generation_entry':
                inv['target_bound'] = self.producer.active.get((row['tid'], row['thread_lifetime'], row.get('invocation_token')), {}).get('ok') is True
            if inv and row.get('site') == 'provider_return' and inv.get('target_bound') and not ready:
                self.partial = True
            if ready and inv:
                positions = [r for r in inv['samples'] if 'construction_mask_position' in r]
                masks = [r for r in inv['samples'] if 'construction_mask_raw_u8' in r]
                pending = inv['pending'] or {}
                original = pending.get('first') or {}
                selected = pending.get('selected') or {}
                query = gate.raw(original, 'provider_entry_query_xy_i32', 8)
                same = (query is not None and query == gate.raw(selected, 'initial_query_xy_i32', 8)
                        and isinstance(inv['entry'].get('provider_token'), int) and inv['entry']['provider_token'] > 0
                        and original.get('provider_token') == inv['entry']['provider_token'] == inv['entry'].get('upstream_provider_token'))
                if len(positions) == 1:
                    same &= (gate.raw(positions[0], 'construction_mask_position', 0x18) == gate.raw(inv['entry'], 'source_descriptor', 0x18)
                             and gate.raw(row, 'source_at_return', 0x70) == gate.raw(inv['entry'], 'source', 0x70))
                if same and len(positions) == len(masks) == 1:
                    self.constructions.append(dict(context=list(key) + [row['invocation_token']],
                        provider_token=inv['entry']['provider_token'], source=SOURCE,
                        first_query_xy_i32_le=query.hex(), mask=masks[0]['construction_mask_raw_u8'],
                        geographic_operand=positions[0]['construction_mask_position'],
                        source_bytes=inv['entry']['source']['raw'],
                        output_prefix=row['output_map_prefix_at_return'],
                        synthetic_witness=row.get('synthetic_population_witness'),
                        synthetic_geometry=row.get('synthetic_population_geometry'),
                        calls=[dict(ires=r.get('ires'), weight_bits=r.get('effective_weight_bits'),
                                    mask=r.get('mask_register_raw'), ordinal=r.get('observed_resource_call_ordinal'))
                               for r in inv['samples'] if r.get('site') == 'resource_call'],
                        terminal_capture=row['capture'], acknowledged=False, classification='CONSTRUCTION_ONLY', population_epoch=None))
                    self.entries.pop(key + (row['invocation_token'],), None)
                    return 'CONSTRUCTION'
            if row.get('decision') in ('ACCEPT', 'REJECT'):
                context = row.get('source_context', {})
                try:
                    manager = bytes.fromhex(context.get('raw_manager') or '')
                    source = bytes.fromhex(context.get('raw_source') or '')
                    at = 0x1c0 if manager[0x20] == 3 else 0xc8
                    actual = source_key(source, manager[at:at+0x2c])
                    extra = bytes.fromhex(row['raw_binding_extra'])
                    valid = (actual == SOURCE and source_key(bytes(0x70), manager[at:at+0x2c]) == '0:37536:20928:00000000') and context.get('owner_key_u32') == BODY and extra[0x98:0xa0].hex() == WORKSHOP
                except (ValueError, KeyError, IndexError, struct.error):
                    valid = False
                if not valid:
                    row = dict(row, required_reads_complete=False)
        else:
            self.producer.observe(row)
        if row.get('ancestry') == 'BOUND_TRANSFER' and row.get('refresh_payload', {}).get('members') == []:
            self.empty_transfers.append(dict(capture=row['capture'], source_binding='UNKNOWN_NO_ACCEPTED_MEMBER'))
        if self.consumer.feed(row):
            self.consumptions.append(dict(accepted=self.consumer.last_match, transfer_capture=row['capture'],
                acknowledged=False, classification='CONSUMER_ONLY', source=SOURCE, population_epoch=None))
            accepted = self.consumer.last_match
            if self.synthetic_proof and row.get('synthetic') is True:
                for construction in self.constructions:
                    before = construction.get('synthetic_witness') or {}
                    after = accepted.get('synthetic_population_witness') or {}
                    try:
                        b = bytes.fromhex(before.get('raw') or '')
                        a = bytes.fromhex(after.get('raw') or '')
                        epoch = struct.unpack_from('<Q', b, 0x38)[0]
                        same = (len(b) == len(a) == 0x70 and a == b and epoch > 0
                                and struct.unpack_from('<Q', b, 0x30)[0] == 0x4453424c49464531
                                and struct.unpack_from('<Q', b, 0x40)[0] == 1
                                and struct.unpack_from('<Q', b, 0x60)[0] == 1
                                and before['address'] == after['address'] == accepted['selected']['source_wrapper']
                                and construction['synthetic_geometry'] == accepted['geometry']
                                and construction['source_bytes'] == accepted['source_context']['raw_source'])
                    except (ValueError, KeyError, struct.error):
                        same = False
                    if same:
                        self.links.append(dict(classification='SYNTHETIC_ONLY_LINKED',
                            applicability='PINNED_FIXTURE_SOLE_WRITER_AND_STACK_LIFETIME',
                            proof=self.synthetic_proof, lifetime=epoch,
                            construction_capture=construction['terminal_capture'],
                            transfer_capture=row['capture'], native_epoch=None))
            return 'CONSUMPTION'
        return None

    def result(self):
        constructions = [r for r in self.constructions if r.get('acknowledged')]
        consumptions = [r for r in self.consumptions if r.get('acknowledged')]
        if constructions and consumptions:
            status = 'CONSTRUCTION_AND_CONSUMPTION_UNLINKED'
        elif constructions:
            status = 'CONSTRUCTION_ONLY'
        elif consumptions:
            status = 'CONSUMER_ONLY'
        elif self.loss:
            status = 'LOSS'
        elif self.samples:
            status = 'INVALID' if self.invalid else 'PARTIAL' if self.partial or self.constructions or self.consumptions else 'UNBOUND'
        else:
            status = 'NO_HIT'
        return dict(schema='sor-d5b-reduction/1', session=self.session, status=status, constructions=constructions,
                    consumptions=consumptions, loss=self.loss, producer_consumer_link=None, synthetic_links=[link for link in self.links if any(r['transfer_capture']==link['transfer_capture'] for r in consumptions)],
                    unacknowledged_observations=[r for r in self.constructions+self.consumptions if not r.get('acknowledged')],
                    observed_empty_transfers=self.empty_transfers, historical_epoch=None, linked_route='NOT_IMPLEMENTED')
