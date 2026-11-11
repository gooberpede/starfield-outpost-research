# SPDX-License-Identifier: GPL-3.0-or-later
"""Selected HIST-0021 component/REFR joins for d5bt_reader."""
import sys

from d5bt_reader import ROOT, require, select, span, unique
from outpost_record_framing import Reader
from workshop_components import component_sections
from workshop_global_units import global_units

# The owned extra reader imports project modules but performs no input discovery.
sys.path.insert(0, str(ROOT / 'research/historical-methods/b3/sd1-containers'))
from extras_sd1 import extra_view


def sections(data):
    units = [row for row in global_units(data) if row['type'] == 6]
    require(len(units) == 1, 'DISPLAY_TYPE6_CARDINALITY')
    unit = units[0]
    require((unit['offset'], unit['body'], unit['end']) == (1321153, 1321161, 1603619),
            'DISPLAY_TYPE6_SPAN')
    cursor = Reader(data, unit['body'], unit['end'])
    count = int.from_bytes(cursor.take(4), 'little')
    for _ in range(count):
        cursor.take(6)
        cursor.take(int.from_bytes(cursor.take(4), 'little')).decode('utf-8')
    tables = component_sections(data, cursor.p, cursor.end, buffer_version=153,
                                activity_custom_payloads=True, pending_dialogue=True)
    require(len(tables) == 43, 'DISPLAY_SECTION_COUNT')
    return tables


def slot(row, offset, fixture_token, item_token):
    require((row['offset'], row['id_word'], row['index'], row['flag'], row['groups']) ==
            (offset, int(fixture_token, 16), 0, 1, [[int(item_token, 16)]]), 'DISPLAY_SLOT')


def zero_inventory(data, record, view, expected_offset):
    require(record['flags'] & 0x08000020, 'DISPLAY_INVENTORY_BRANCH')
    cursor = Reader(data, view['body_end'], record['end'])
    start = cursor.p
    require(start == expected_offset and cursor.count() == 0 and cursor.p == start + 1,
            'DISPLAY_INVENTORY_COUNT')
    return dict(count=0, span=(start, cursor.p))


def extras(data, record, prefix, resolve):
    view = extra_view(data, record, prefix, resolve)
    require(view['status'] == 'COUNT_CLOSED', 'DISPLAY_EXTRA_UNSUPPORTED')
    require(view['next_reference_index'] == view['queue_count'], 'DISPLAY_REFERENCE_CURSOR')
    return view


def backlink(view, fixture, offset):
    extra = unique(view['extras'], '36')
    require(extra['references'] == [fixture] and extra['byte'] == 1 and
            span(extra) == (offset, offset+2), 'DISPLAY_BACKLINK')
    links = unique(view['extras'], '4c')['entries']
    require([(e['keyword'], e['target'], e['mode']) for e in links] ==
            [('starfield.esm:1c5edd', fixture, 1)], 'DISPLAY_LINK_BACK')
    return span(extra)


def display(data, resolve):
    tables = sections(data)
    nested = [table for table in tables if table['name'] == '1412fe810-Nested']
    require(len(nested) == 1 and (nested[0]['offset'], nested[0]['end'], nested[0]['count']) ==
            (1579785, 1579819, 2), 'DISPLAY_NESTED_SPAN')
    selected = select(data, resolve, {'DYNAMIC:ff05bb' + suffix for suffix in ('90', '91', '92', '93')})
    rows = []
    for label, n, fixture_base, item_base, secondary, item_end in (
        ('helmet', 0, '363cc8', '026bf0', 'ff0436d1', 5861629),
        ('backpack', 1, '363cc6', '026bef', 'ff031755', 5861794),
    ):
        fixture, item = f'DYNAMIC:ff05bb{0x90+n:02x}', f'DYNAMIC:ff05bb{0x92+n:02x}'
        fixture_token, item_token = f'85bb{0x90+n:02x}', f'85bb{0x92+n:02x}'
        row = nested[0]['rows'][n]
        slot(row, 1579789 + n*15, fixture_token, item_token)
        require((resolve(fixture_token), resolve(item_token)) == (fixture, item), 'DISPLAY_TOKEN_JOIN')
        fr, fp = selected[fixture]
        ir, ip = selected[item]
        require((fr['token'], ir['token']) == (fixture_token, item_token), 'DISPLAY_RECORD_TOKEN')
        require((resolve(fp['base_token']), resolve(ip['base_token'])) ==
                ('starfield.esm:' + fixture_base, 'starfield.esm:' + item_base), 'DISPLAY_BASE')
        require(resolve(fp['parent_token']) == resolve(ip['parent_token']) == 'DYNAMIC:ff020801',
                'DISPLAY_PARENT')
        require(span(fr) == (5861284+n*92, 5861376+n*92) and
                span(ir) == ((5861468, 5861629)[n], item_end), 'DISPLAY_RECORD_SPAN')

        fv, iv = extras(data, fr, fp, resolve), extras(data, ir, ip, resolve)
        ownership = unique(fv['extras'], '1f')
        require(ownership['references'] == [None, 'starfield.esm:000014'] and ownership['byte'] == 0,
                'DISPLAY_FIXTURE_OWNERSHIP')
        require(unique(iv['extras'], '1f')['references'] == ['starfield.esm:000007', None],
                'DISPLAY_ITEM_OWNERSHIP')
        links = unique(fv['extras'], '4c')['entries']
        require([(edge['keyword'], edge['target'], edge['mode']) for edge in links] == [
            ('starfield.esm:054ba6', 'DYNAMIC:ff029ca0', 0),
            ('starfield.esm:1c5edd', 'DYNAMIC:' + secondary, 1),
        ], 'DISPLAY_WORKSHOP_LINK')
        modifications = len(unique(iv['extras'], '33')['modifications'])
        require(iv['count'] == 7 and iv['body_end'] == ir['end'] - 1 and modifications == 10,
                f'DISPLAY_ITEM_EXTRAS {label}: {iv["count"]}, {iv["body_end"]}, {modifications}')
        reverse = backlink(iv, fixture, item_end-9)
        fixture_types = [r['type'] for r in fv['extras']]
        item_types = [r['type'] for r in iv['extras']]
        require(fixture_types == ['84', 'bf', '9c', '4c', '1f'] and
                item_types == ['33', '96', 'bf', '1f', '36', '4c', '84'],
                'DISPLAY_EXTRA_SEQUENCE')
        inventory = zero_inventory(data, fr, fv, 5861374 + n*92)
        rows.append(dict(role=label, fixture=fixture, fixture_token=fixture_token,
                         fixture_base=fixture_base, fixture_record=span(fr),
                         fixture_owner=ownership['references'][1], workshop='DYNAMIC:ff029ca0',
                         slot_offset=row['offset'], component_id_word=row['id_word'],
                         section_index=tables.index(nested[0]), row_index=n, typed_index=row['index'],
                         inventory=inventory, item=item, item_token=item_token, item_base=item_base,
                         item_record=span(ir), item_owner='starfield.esm:000007',
                         backlink=reverse,
                         item_counted_end=iv['body_end'], item_reference_cursor=iv['next_reference_index'],
                         item_extra_types=item_types))
    return dict(section_count=len(tables), type6=(1321153, 1603619), rows=rows)
