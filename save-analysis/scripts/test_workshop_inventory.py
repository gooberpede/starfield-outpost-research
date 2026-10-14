"""SPDX-License-Identifier: GPL-3.0-or-later
Original synthetic native-contract/adversarial tests. Stdlib/project only;
no file writes, target effects or private fixtures. Expected fields authored
from native contracts, not by invoking the detector under test.
"""
import struct
import unittest
from extractor_resources import saved_form
from workshop_inventory import audit, reference_prefix, linked_prefix, ownership_ledger, constructed_inventory


def fixture(extras=b'\x04\x4c\x04\0', refs=None, flags=0x41, saved=0, component=b''):
    body=b'\0'+struct.pack('<3f',1,2,3)+b'\0'+component
    if flags&1: body+=struct.pack('<IH',saved,0)
    start=len(body)
    body+=extras
    r=dict(body=0,end=len(body),offset=0,ordinal=0,token='800001',flags=flags,
        refs=refs or ['800004','400077','800001','454ba6','800002'],strings=[])
    return body,r,start


def ledger_row(token='800001', identity='DYNAMIC:ff000001', base='UNKNOWN', target='DYNAMIC:ff000002', mode=0):
    return dict(token=token,saved_reference=identity,base_identity=base,offset=0,ordinal=0,
        end=20,explicit_type=0x4a,resolved_refs=[],prefix=dict(disabled=False,deleted=False),linked_prefix=dict(following_extras='CLOSED',extra_flags=0x800,alternate_groups=[],packin=[],entries=[
            dict(keyword_identity='starfield.esm:054ba6',target_identity=target,target_mode=mode)]))


def ledger(rows):
    return ownership_ledger(dict(records=rows,coverage={},plugins={}))


def owner():
    r=ledger_row('800002','DYNAMIC:ff000002','starfield.esm:2c60e9',target='DYNAMIC:ff000002')
    r['ordinal']=1
    return r


class InventoryTests(unittest.TestCase):
    def test_mixed_explicit_nonreference_decoy_not_a_member(self):
        from unittest.mock import patch
        b,r,_=fixture()
        good=dict(r,explicit_type=0x4a)
        decoy=dict(r,explicit_type=0x2a,token='800009',ordinal=1,refs=list(r['refs']))
        decoy['refs'][2]='800009'
        d=dict(reference_count=0,regions=dict(reference_u32=(0,4),region_R3=(0,len(b))),words=[0]*9+[2])
        plugins=dict(version=153,groups=dict(full=['starfield.esm'],small=[],medium=[]))
        with patch('workshop_inventory.directory',return_value=d),patch('workshop_inventory.plugin_tables',return_value=plugins),patch('workshop_inventory.iter_records',return_value=iter([good,decoy])):
            raw=audit(b)
        x=ownership_ledger(raw)
        self.assertEqual(raw['coverage']['framed_records'],2)
        self.assertEqual([r['token'] for r in x['instances']],['800001'])
        self.assertEqual(x['unresolved_population'][0]['token'],'800009')
        self.assertNotIn('prefix',x['unresolved_population'][0])

    def test_native_key_byte_target(self):
        b,r,start=fixture();p=reference_prefix(b,r,5);x=linked_prefix(b,r,p)
        self.assertEqual(p['xyz'],[1,2,3]);self.assertEqual(x['entries'][0]['target_token'],'800002')
        self.assertEqual(x['entries'][0]['flag_offset'],start+3)

    def test_flag4_component_precedes_self_and_flags(self):
        # Version153, one ref/string, payload3; component refs precede self.
        block=b'\x99\x01\0\x01\0\x0cXYZ'
        b,r,_=fixture(flags=0x45,saved=0x800,component=block,
            refs=['800004','400077','400099','800001','454ba6','800002'])
        r['strings']=[17]
        p=reference_prefix(b,r,5)
        self.assertEqual(p['component']['references'],['400099'])
        self.assertEqual(p['component']['strings'],[17]);self.assertTrue(p['disabled'])
        self.assertEqual(linked_prefix(b,r,p)['entries'][0]['keyword_queue_index'],4)

    def test_old_component_version_has_no_counts(self):
        b,r,_=fixture(flags=0x45,component=b'\x03\x04X')
        self.assertEqual(reference_prefix(b,r,5)['component']['size'],1)

    def test_component_queue_underflow(self):
        b,r,_=fixture(flags=0x45,component=b'\x99\xff\xff\0\0\0')
        with self.assertRaises(ValueError): reference_prefix(b,r,5)

    def test_proper_prefix_truncations(self):
        b,r,_=fixture(flags=0x45,component=b'\x99\0\0\0\0\x0cXYZ')
        end=reference_prefix(b,r,5)['form_prefix_end']
        for n in range(end):
            with self.subTest(n=n),self.assertRaises(ValueError): reference_prefix(b[:n],dict(r,end=n),5)

    def test_unknown_leading_extra_cannot_be_byte_searched(self):
        b,r,_=fixture(extras=b'\x08\xee\x4c\x04\0')
        with self.assertRaisesRegex(ValueError,'EE'): linked_prefix(b,r,reference_prefix(b,r,5))

    def test_bf_mask_consumes_reference(self):
        b,r,_=fixture(extras=b'\x08\xbf\x04\x01'+struct.pack('<f',1)+b'\0\x4c\x04\0',
            refs=['800004','400077','800001','400032','454ba6','800002'])
        self.assertEqual(linked_prefix(b,r,reference_prefix(b,r,5))['entries'][0]['keyword_token'],'454ba6')

    def test_link_queue_underflow(self):
        b,r,_=fixture(refs=['800004','400077','800001','454ba6'])
        with self.assertRaises(ValueError): linked_prefix(b,r,reference_prefix(b,r,5))

    def test_group80_retains_index_before_direct4c(self):
        b,r,_=fixture(extras=b'\x08\x80\x04'+struct.pack('<I',38)+b'\x4c\x04\0',
            refs=['800004','400077','800001','400066','454ba6','800002'])
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertEqual(x['alternate_groups'][0]['group_index'],38)
        self.assertEqual(x['entries'][0]['keyword_token'],'454ba6')

    def test_omitted_saved_state_is_unknown(self):
        b,r,_=fixture(flags=0x40)
        self.assertIsNone(reference_prefix(b,r,5)['disabled'])

    def test_duplicate_bases_unknown_names_preserve_instances(self):
        a=ledger_row();b=ledger_row('800003','DYNAMIC:ff000003');b['ordinal']=2
        x=ledger([a,owner(),b])
        self.assertEqual(len(x['instances']),3)
        self.assertIsNone(x['instances'][0]['editor_name'])
        self.assertFalse(x['coverage']['complete_constructed_population'])

    def test_null_owner_is_unresolved(self):
        x=ledger([ledger_row(target=None),owner()])
        self.assertEqual(x['instances'][0]['reason'],'NULL_DIRECT_OWNER')

    def test_conflicting_owners_are_not_chosen(self):
        r=ledger_row();r['linked_prefix']['entries'].append(dict(keyword_identity='starfield.esm:054ba6',target_identity='DYNAMIC:ff000009',target_mode=0))
        self.assertEqual(ledger([r,owner()])['instances'][0]['reason'],'CONFLICTING_DIRECT_OWNER_EDGES')

    def test_duplicate_target_owner_is_unresolved(self):
        x=ledger([ledger_row(),owner(),owner()])
        self.assertEqual(x['instances'][0]['reason'],'DUPLICATE_OWNER_REFERENCE_RECORDS')

    def test_nonzero_mode_is_not_assigned(self):
        self.assertEqual(ledger([ledger_row(mode=1),owner()])['instances'][0]['reason'],'NONZERO_TARGET_MODE_NOT_REFERENCE_QUALIFIED')

    def test_missing_edge_and_unrelated_mention_retained(self):
        r=ledger_row();r['linked_prefix']['entries']=[];r['resolved_refs']=['starfield.esm:054ba6']
        x=ledger([r,owner()]);self.assertEqual(len(x['unresolved_population']),1)
        self.assertTrue(x['unresolved_population'][0]['queued_workshop_keyword'])

    def test_historical_owner_kept(self):
        o=owner();o['prefix']['disabled']=True
        x=ledger([ledger_row(),o]);self.assertEqual(x['owners'][0]['state'],'SAVED_DISABLED_SET')
        self.assertEqual(x['owners'][0]['direct_member_records'],2)

    def test_identity_domains_do_not_collide(self):
        p=dict(groups=dict(full=['starfield.esm','full.esm'],medium=['medium.esm'],small=['small.esm']))
        self.assertEqual(len({saved_form(n,p) for n in [0x01000077,0xfd000077,0xfe000077,0xff000077]}),4)


    def test_trailing_da_and_flags_decoded(self):
        b,r,_=fixture(extras=b'\x0c\x4c\x04\0\xda\x01'+bytes(4)+b'\x9c'+struct.pack('<I',0x800),
            refs=['800004','400077','800001','454ba6','800002','400088','400088','000000','800007','400099'])
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertEqual(x['following_extras'],'CLOSED')
        self.assertEqual(x['packin'][0]['tokens'][3],'800007')
        self.assertEqual(x['extra_flags'],0x800)

    def test_trailing_group80_retained(self):
        b,r,_=fixture(extras=b'\x08\x4c\x04\0\x80\x04'+struct.pack('<I',38),
            refs=['800004','400077','800001','454ba6','800002','400066'])
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertEqual(x['alternate_groups'][0]['group_index'],38)

    def test_duplicate_extra_rejected(self):
        b,r,_=fixture(extras=b'\x08\x9c'+bytes(4)+b'\x9c'+bytes(4))
        with self.assertRaisesRegex(ValueError,'DUPLICATE_EXTRA'):linked_prefix(b,r,reference_prefix(b,r,5))

    def test_unknown_trailing_keeps_edge_withholds_root(self):
        b,r,_=fixture(extras=b'\x08\x4c\x04\0\xee')
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertEqual(len(x['entries']),1);self.assertEqual(x['following_extras'],'NOT_DECODED')
        a=ledger_row();a['linked_prefix']['following_extras']='NOT_DECODED'
        y=constructed_inventory(ledger([a,owner()]))
        self.assertFalse(any(i['instance_identity']==a['saved_reference'] for i in y['constructed_instances']))

    def test_native_compound_root_and_generated_members(self):
        o=owner();a=ledger_row();d=ledger_row('800007','DYNAMIC:ff000007','starfield.esm:015804')
        a['linked_prefix']['packin']=[dict(identities=['UNKNOWN_PKIN',None,None,d['saved_reference'],None])]
        d['linked_prefix']['packin']=[dict(identities=['UNKNOWN_PKIN',None,None,None,None])]
        x=constructed_inventory(ledger([a,d,o]))
        roots=[i for i in x['constructed_instances'] if i['root_kind']=='PACKIN_ROOT']
        self.assertEqual(len(roots),1);self.assertEqual(roots[0]['instance_identity'],d['saved_reference'])
        self.assertEqual(len(roots[0]['member_identities']),2)
        self.assertIsNone(roots[0]['editor_name'])

    def test_foundation_filter_requires_extra_flags(self):
        a=ledger_row();a['linked_prefix']['entries'].append(dict(keyword_identity='starfield.esm:000192',target_identity='DYNAMIC:ff000002',target_mode=1))
        x=constructed_inventory(ledger([a,owner()]));self.assertEqual(x['member_roles'][0]['role'],'FOUNDATION_MEMBER')
        a['linked_prefix']['extra_flags']=None
        x=constructed_inventory(ledger([a,owner()]));self.assertEqual(x['member_roles'][0]['role'],'UNRESOLVED')
        a['linked_prefix']['extra_flags']=0
        x=constructed_inventory(ledger([a,owner()]));self.assertEqual(x['member_roles'][0]['role'],'SINGLE_ROOT')

    def test_57_opaque_four_bytes_do_not_consume_reference(self):
        b,r,_=fixture(extras=b'\x08\x57'+bytes(4)+b'\x4c\x04\0')
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertEqual(x['following_extras'],'CLOSED')
        self.assertEqual(x['entries'][0]['keyword_token'],'454ba6')

    def test_modern_workshop_and_string_queue_before_links(self):
        b,r,_=fixture(extras=b'\x0c\xca\x04\xbc'+bytes(4)+b'\0\0'+bytes(24)+b'\x4c\x04\0')
        r['strings']=[7,8]
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertEqual(x['following_extras'],'CLOSED')
        self.assertEqual(x['entries'][0]['target_token'],'800002')
        r['strings']=[7]
        with self.assertRaisesRegex(ValueError,'STRING_QUEUE'):linked_prefix(b,r,reference_prefix(b,r,5))

    def test_de_and_empty30_native_queue_alignment(self):
        b,r,_=fixture(extras=b'\x0c\xde\x04\x04'+bytes(8)+b'\x30\0\x4c\x04\0',
            refs=['800004','400077','800001','400010','400020','454ba6','800002'])
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertEqual(x['entries'][0]['keyword_token'],'454ba6')
        self.assertEqual(x['following_extras'],'CLOSED')

    def test_nonempty30_is_not_scanned_for_links(self):
        b,r,_=fixture(extras=b'\x08\x4c\x04\0\x30\x04',
            refs=['800004','400077','800001','454ba6','800002','400020'])
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertIn('POLYMORPHIC',x['following_gap'])

    def test_96_resolution_dependent_string_not_guessed(self):
        b,r,_=fixture(extras=b'\x08\x4c\x04\0\x96\x02',
            refs=['800004','400077','800001','454ba6','800002','400020'])
        x=linked_prefix(b,r,reference_prefix(b,r,5))
        self.assertIn('RESOLUTION_DEPENDENT',x['following_gap'])

    def test_alternate80_cannot_prove_foundation_getter(self):
        a=ledger_row();a['linked_prefix']['entries'].append(dict(keyword_identity='starfield.esm:000192',target_identity='DYNAMIC:ff000002',target_mode=1))
        a['linked_prefix']['alternate_groups']=[dict(group_index=38)]
        x=constructed_inventory(ledger([a,owner()]))
        self.assertEqual(x['member_roles'][0]['reason'],'ALTERNATE80_FOUNDATION_GETTER_UNRESOLVED')

    def test_missing_foundation_target_unresolved(self):
        a=ledger_row();a['linked_prefix']['entries'].append(dict(keyword_identity='starfield.esm:000192',target_identity='DYNAMIC:ff000099',target_mode=1))
        x=constructed_inventory(ledger([a,owner()]))
        self.assertEqual(x['member_roles'][0]['reason'],'FOUNDATION_TARGET_MISSING_OR_DUPLICATE')

    def test_same_base_multiple_single_instances_and_owners(self):
        a=ledger_row();b=ledger_row('800003','DYNAMIC:ff000003')
        x=constructed_inventory(ledger([a,b,owner()]))
        self.assertEqual(len(x['constructed_instances']),3)
        self.assertEqual(len({r['instance_identity'] for r in x['constructed_instances']}),3)

    def test_replacement_missing_self_and_chain_unresolved(self):
        for target in ['DYNAMIC:ff000001','DYNAMIC:ff000099']:
            a=ledger_row();a['linked_prefix']['entries'].append(dict(keyword_identity='starfield.esm:000191',target_identity=target,target_mode=1))
            x=constructed_inventory(ledger([a,owner()]))
            self.assertEqual(x['member_roles'][0]['role'],'UNRESOLVED')

    def test_partial_group_is_not_complete_item(self):
        a=ledger_row();d=ledger_row('800007','DYNAMIC:ff000007','starfield.esm:015804')
        a['linked_prefix']['packin']=[dict(identities=['UNKNOWN_PKIN',None,None,d['saved_reference'],None])]
        a['linked_prefix']['following_extras']='NOT_DECODED'
        d['linked_prefix']['packin']=[dict(identities=['UNKNOWN_PKIN',None,None,None,None])]
        x=constructed_inventory(ledger([a,d,owner()]))
        self.assertFalse(any(i['root_kind']=='PACKIN_ROOT' for i in x['constructed_instances']))


if __name__=='__main__': unittest.main()
