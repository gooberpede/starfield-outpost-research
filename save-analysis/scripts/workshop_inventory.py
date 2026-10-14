"""SPDX-License-Identifier: GPL-3.0-or-later
Offline population audit. Reads decoded bytes only; no files or target effects.
Stdlib/project readers. Conditional REFR prefixes are NOT construction proof.
Unknown records and identity failures remain in the unresolved ledger.
"""
import collections
import struct
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import Reader, iter_records
from validate_mature_outposts import directory


def reference_prefix(b, r, case):
    """Initial data, flag4 component envelope, self and optional saved flags.
    Native141833b20→14181cff0→1418663f0→141867470 precedes1405dfa40.
    Component payload is opaque; its queued references/strings are retained.
    """
    c = Reader(b, r['body'], r['end'])
    ri = 0
    def ref():
        nonlocal ri
        if ri >= len(r['refs']): raise ValueError('PREFIX_QUEUE_BOUNDS')
        t = r['refs'][ri]; ri += 1
        return t
    out = dict(case=case, base_token=None, disabled=None, deleted=None,
               saved_form_flags=None, saved_aux_flags=None)
    if case in (4,5,6):
        shape=c.take(1)[0]
        out.update(shape=shape, parent_token=ref(), xyz=list(struct.unpack('<3f',c.take(12))))
        for i in range(3):
            if shape & (1<<i): c.take(4)
        if not shape & 0x18: c.take(1)
        if case==5: out['base_token']=ref()
        if case==6:
            out['placement_parent_token']=ref()
            out['placement_indices']=list(struct.unpack('<2h',c.take(4)))
    elif case==7: out['initial_reference_token']=ref()
    else: raise ValueError('UNSUPPORTED_CASE')
    out['initial_end']=c.p
    if r['flags'] & 4:
        start=c.p; version=c.take(1)[0]
        nr, ns = struct.unpack('<HH',c.take(4)) if version>=4 else (0,0)
        size=c.count(); body=c.p
        c.take(size)
        component_refs=[ref() for _ in range(nr)]
        if ns>len(r['strings']): raise ValueError('COMPONENT_STRING_BOUNDS')
        out['component']=dict(start=start,end=c.p,version=version,size=size,body=body,
            references=component_refs, strings=r['strings'][:ns])
    out['self_reference_index']=ri
    out['self_token']=ref()
    if out['self_token']!=r['token']: raise ValueError('SELF_REFERENCE_MISMATCH')
    if r['flags'] & 1:
        out['saved_flags_offset']=c.p
        form,aux=struct.unpack('<IH',c.take(6))
        out.update(saved_form_flags=form,saved_aux_flags=aux,
                   disabled=bool(form&0x800),deleted=bool(form&0x20))
    out.update(form_prefix_end=c.p,next_reference_index=ri)
    return out


def linked_prefix(b, r, prefix):
    """Consume supported modern counted extras without byte searching.
    1419aeff0 BF masks; 140562ef0 keyed entries. Unknown trailing types retain
    decoded edges with NOT_DECODED status. CLOSED does not prove load defaults.
    """
    c = Reader(b, prefix['form_prefix_end'], r['end'])
    ri = prefix['next_reference_index']
    si=len(prefix.get('component',{}).get('strings',[]))
    def strings(n):
        nonlocal si
        if not 0<=n<=len(r['strings'])-si: raise ValueError('EXTRA_STRING_QUEUE_BOUNDS')
        si+=n
    def refs(n):
        nonlocal ri
        if not 0 <= n <= len(r['refs']) - ri: raise ValueError('EXTRA_QUEUE_BOUNDS')
        result = r['refs'][ri:ri+n]
        ri += n
        return result
    if r['flags'] & 0x80:
        refs(1)  # 140b29990 -> 1405631e0, no body bytes
        if not r['flags'] & 0xa6031f40: refs(1)
    if r['flags'] & 0x10: c.take(4)
    if not r['flags'] & 0xa6031f40: raise ValueError('NO_EXTRA_DISPATCH')
    types, alternate_groups, packin, entries = [], [], [], []
    extra_flags = None
    total = c.count()
    first_link = None
    def result(closed, gap=None):
        return dict(entries=entries, start=first_link, end=c.p, types=types,
            alternate_groups=alternate_groups, packin=packin,extra_flags=extra_flags,
            following_extras='CLOSED' if closed else 'NOT_DECODED',
            extra_count=total, decoded_extra_count=len(types)-(1 if gap else 0),
            following_gap=gap, next_reference_index=ri)
    for _ in range(total):
        start = c.p
        typ = c.take(1)[0]
        if typ in types: raise ValueError('DUPLICATE_EXTRA_TYPE_%02X' % typ)
        types.append(typ)
        if typ == 0x9c: extra_flags=int.from_bytes(c.take(4),'little')
        elif typ in (0x45, 0x83): refs(1)
        elif typ in (0x54,0x57): c.take(4)
        elif typ == 0x2a: c.take(4)
        elif typ == 0x1f: refs(2); c.take(1)
        elif typ == 0x0c:
            refs(c.count()); c.take(c.count())
        elif typ == 0x61: c.take(32)
        elif typ == 0x81:
            refs(1); c.take(4); refs(1); c.take(16)
        elif typ == 0xca:
            strings(c.count())  # qualified modern >=4 string-queue branch
        elif typ == 0xde:
            n=c.count()
            if n>len(r['refs'])-ri: raise ValueError('DE_GROUP_QUEUE_BOUNDS')
            for _ in range(n):
                refs(1); rows=c.count()
                if rows>(c.end-c.p)//8: raise ValueError('DE_ROW_BOUNDS')
                c.take(rows*8)
        elif typ == 0x30:
            refs(1)
            if c.count():
                gap='EXTRA_30_NONEMPTY_POLYMORPHIC_NODES'
                if first_link is not None: return result(False,gap)
                raise ValueError('LEADING_'+gap)
        elif typ == 0x96:
            flags=c.take(1)[0]
            for bit in (1,2,4):
                if flags&bit: refs(1)
            value=(c.count() if flags&0x80 else int.from_bytes(c.take(4),'little')) if flags&8 else 0xfffffffe
            if flags&0x10: c.take(2)
            if flags&6 and value==0xfffffffe:
                gap='EXTRA_96_RESOLUTION_DEPENDENT_STRING'
                if first_link is not None: return result(False,gap)
                raise ValueError('LEADING_'+gap)
            if not flags&6 and value==0xfffffffe: strings(1)
            if flags&0x20:
                n=c.count(); strings(n); c.take(n*4)
            if flags&0x40:
                n=c.count(); strings(n); refs(n)
        elif typ == 0xbc:
            n=int.from_bytes(c.take(4),'little')
            if n>(c.end-c.p)//4: raise ValueError('WORKSHOP_RESOURCE_GROUP_BOUNDS')
            for _ in range(n):
                refs(1); rows=int.from_bytes(c.take(4),'little')
                if rows>(c.end-c.p)//17: raise ValueError('WORKSHOP_RESOURCE_ROW_BOUNDS')
                refs(rows*2); c.take(rows*17)
            refs(c.count()); c.take(1); strings(1); c.take(24)
        elif typ == 0xcb:
            n=c.count(); refs(n); c.take(n*4)
        elif typ == 0xda:
            tokens=refs(4); flag_offset=c.p; flag=c.take(1)[0]
            tokens+=refs(1); word_offset=c.p; word=int.from_bytes(c.take(4),'little')
            packin.append(dict(tokens=tokens,flag68=flag,flag_offset=flag_offset,
                word64=word,word_offset=word_offset,start=start))
        elif typ == 0x84:
            n = c.count(); refs(n); c.take(n)
        elif typ == 0xbf:
            for bits in (1, 3):
                n = c.count()
                mask = c.take((bits*n + 7)//8)
                refs(n)
                c.take(4*sum(bool(mask[i//8] & (1 << (i%8))) for i in range(bits*n)))
        elif typ == 0x4c:
            if first_link is None: first_link=start
            n = c.count()
            if n > len(r['refs'][ri:])//2: raise ValueError('LINKED_QUEUE_BOUNDS')
            for i in range(n):
                keyword_index = ri
                key = refs(1)[0]
                flag_offset = c.p
                flag = c.take(1)[0]
                target = refs(1)[0]
                entries.append(dict(keyword_token=key, target_token=target,
                    keyword_queue_index=keyword_index, target_mode=flag,
                    flag_offset=flag_offset, entry_index=i))
        elif typ == 0x80:
            n=c.count()
            if n>len(r['refs'])-ri or n>(c.end-c.p)//4: raise ValueError('GROUP80_BOUNDS')
            for i in range(n):
                base=refs(1)[0]; offset=c.p
                group=int.from_bytes(c.take(4),'little')
                alternate_groups.append(dict(base_token=base, group_index=group,offset=offset))
        else:
            gap='EXTRA_%02X_UNSUPPORTED' % typ
            if first_link is not None: return result(False,gap)
            raise ValueError('LEADING_'+gap)
    if first_link is not None or alternate_groups:
        return result(True)
    raise ValueError('NO_LEADING_4C')


def audit(b, diagnostics=False):
    d = directory(b)
    plugins = plugin_tables(b)
    if plugins['version']!=153: raise ValueError('UNQUALIFIED_EXTRA_BUFFER_VERSION')
    a, _ = d['regions']['reference_u32']
    class Table:
        def __len__(self): return d['reference_count']
        def __getitem__(self, i):
            if not 0 <= i < len(self): raise IndexError(i)
            return struct.unpack_from('<I', b, a + 4 + 4*i)[0]
    table = Table()
    def resolve(t): return saved_form(token_value(t, table), plugins)
    rows = []
    counts = collections.Counter()
    for r in iter_records(b, *d['regions']['region_R3'], d['words'][9]):
        counts['framed_records'] += 1
        row = dict(token=r['token'], offset=r['offset'], end=r['end'],
                   ordinal=r['ordinal'], explicit_type=r['explicit_type'],
                   change_flags=r['flags'], offset_domain='DECODED_LOGICAL_STREAM',
                   association_status='UNRESOLVED', reason='TYPE_OR_INITIAL_REPRESENTATION',
                   body_offset=r['body'], reference_queue_offset=r['body']-3*len(r['refs'])-2*len(r['strings']),
                   string_queue_offset=r['body']-2*len(r['strings']),
                   refs=r['refs'], strings=r['strings'])
        try: row['saved_reference'] = resolve(r['token'])
        except ValueError as e: row['identity_error'] = str(e)
        row['resolved_refs'] = []
        for t in r['refs']:
            try: row['resolved_refs'].append(resolve(t))
            except ValueError as e: row['resolved_refs'].append(dict(error=str(e), token=t))
        dynamic = int(r['token'], 16) >> 22 == 2
        if dynamic and (r['explicit_type'] is None or 0x4a <= r['explicit_type'] <= 0x55):
            case = 5 if not r['flags'] & 0x8000 else 6 if r['flags'] & 0x02000008 else 4 if r['flags'] & 6 else 7
            try:
                p = reference_prefix(b, r, case)
                row['prefix'] = p
                row['reason'] = 'CONDITIONAL_PREFIX_NOT_CONSTRUCTION_PROOF'
                if p['base_token']: row['base_identity'] = resolve(p['base_token'])
                row['extra_body_offset'] = p['form_prefix_end']
                if diagnostics:
                    row['extra_body_hex'] = bytes(b[p['form_prefix_end']:r['end']]).hex()
                try:
                    row['linked_prefix'] = linked_prefix(b, r, p)
                    for e in row['linked_prefix']['entries']:
                        e['keyword_identity'] = resolve(e['keyword_token'])
                        e['target_identity'] = resolve(e['target_token'])
                    for e in row['linked_prefix']['alternate_groups']:
                        e['base_identity']=resolve(e['base_token'])
                    for e in row['linked_prefix']['packin']:
                        e['identities']=[resolve(t) for t in e['tokens']]
                except ValueError as e: row['linked_gap'] = str(e)
                counts['conditional_case_' + str(case)] += 1
            except ValueError as e:
                row['prefix_error'] = str(e)
                counts['prefix_errors'] += 1
        else: counts['other_representation'] += 1
        rows.append(row)
    return dict(schema='workshop-population-audit/1', plugins=plugins, records=rows,
                coverage=dict(counts), complete_player_population=False)


def ownership_ledger(result, context=None):
    """Saved DIRECT4C edges, never an exhaustive physical construction detector.
    Every framed record is retained either as a member or possible-missed row.
    Queue mentions are contextual leads only. No geometry/name/category filter.
    """
    records=result['records']
    ids=collections.Counter(r.get('saved_reference') for r in records)
    owners=[r for r in records if r.get('base_identity')=='starfield.esm:2c60e9']
    owner_ids={r['saved_reference'] for r in owners}
    members, unresolved=[],[]
    for r in records:
        entries=r.get('linked_prefix',{}).get('entries',[])
        edges=[e for e in entries if e.get('keyword_identity')=='starfield.esm:054ba6']
        row=dict(r)
        row.update(construction_status='UNRESOLVED_PHYSICAL_ROOT_OR_GENERATED_MEMBER',
                   load_getter_authority='NOT_ESTABLISHED_FOLLOWING_EXTRAS_OR_DEFAULTS',
                   editor_name=None, definition_provenance=[])
        if context and row.get('base_identity') in context['records']:
            matches=context['records'][row['base_identity']]
            row['definition_provenance']=matches
            if len(matches)==1: row['editor_name']=matches[0]['editor_id']
        row['ownership_evidence']=edges
        if not edges:
            row['reason']=row.get('linked_gap',row.get('prefix_error','NO_DECODED_DIRECT_WORKSHOP_ITEM_EDGE'))
            row['queued_workshop_keyword']='starfield.esm:054ba6' in row['resolved_refs']
            unresolved.append(row)
            continue
        # Preserve duplicates and competing evidence. Null/nonzero mode is not guessed.
        targets={e['target_identity'] for e in edges}
        row['owner_identity']=None
        if ids.get(row.get('saved_reference'),0)!=1:
            row['reason']='DUPLICATE_SAVED_REFERENCE_RECORDS'
        elif len(targets)!=1:
            row['reason']='CONFLICTING_DIRECT_OWNER_EDGES'
        elif next(iter(targets)) is None:
            row['reason']='NULL_DIRECT_OWNER'
        elif any(e['target_mode']!=0 for e in edges):
            row['reason']='NONZERO_TARGET_MODE_NOT_REFERENCE_QUALIFIED'
        elif next(iter(targets)) not in owner_ids:
            row['reason']='TARGET_NOT_QUALIFIED_ORDINARY_BEACON'
        elif ids.get(next(iter(targets)),0)!=1:
            row['reason']='DUPLICATE_OWNER_REFERENCE_RECORDS'
        else:
            row['association_status']='SAVED_DIRECT_WORKSHOP_MEMBER'
            row['reason']='DECODED_KEYWORD_TARGET_FIELDS_NOT_QUEUE_ADJACENCY'
            row['owner_identity']=next(iter(targets))
        row['parent_relations']=[e for e in entries if e.get('keyword_identity')=='starfield.esm:000192']
        members.append(row)
    members.sort(key=lambda r:(r.get('saved_reference') or '',r['offset']))
    unresolved.sort(key=lambda r:r['ordinal'])
    summaries=[]
    for r in sorted(owners,key=lambda r:r['saved_reference']):
        p=r['prefix']
        assigned=[m for m in members if m['owner_identity']==r['saved_reference']]
        summaries.append(dict(owner_identity=r['saved_reference'],token=r['token'],offset=r['offset'],
            saved_disabled=p['disabled'], saved_deleted_bit=p['deleted'],
            state='SAVED_DISABLED_SET' if p['disabled'] else 'SAVED_DISABLED_CLEAR' if p['disabled'] is False else 'UNKNOWN',
            direct_member_records=len(assigned),self_members=sum(m['token']==r['token'] for m in assigned),
            member_records_with_parent_relation=sum(bool(m['parent_relations']) for m in assigned),
            constructed_instance_count=None, completeness='NOT_ESTABLISHED'))
    return dict(schema='workshop-saved-membership/1', instances=members,
        unresolved_population=unresolved, owners=summaries, coverage=dict(result['coverage'],
        direct_member_records=len(members), unresolved_owner_members=sum(m['owner_identity'] is None for m in members),
        other_framed_records=len(unresolved), queued_keyword_without_edge=sum(r['queued_workshop_keyword'] for r in unresolved),
        complete_r3_record_scan=True, complete_constructed_population=False,
        complete_direct4c_detection=False),
        conclusion='SAVED_MEMBERSHIP_POSITIVE_CONSTRUCTION_INVENTORY_UNRESOLVED', plugins=result['plugins'])


def constructed_inventory(ledger, context=None):
    """Native item roots projected from CLOSED explicit saved member extras.

    This is not a reconstruction of default/inherited reverse4D populations.
    1421c71b0 filters 9C800+192; 140f366c0 groups effective191 replacements
    by dummy identity or DA+58; 1421cb740 selects an unreplaced dummy root.
    Every member is accounted for as a root, generated member, foundation or gap.
    Omitted ExtraFlags and incomplete extras never become proven single items.
    """
    members=ledger['instances']
    allrows=members+ledger['unresolved_population']
    index=collections.defaultdict(list)
    for r in allrows: index[r.get('saved_reference')].append(r)
    roles=[]; groups=collections.defaultdict(list); items=[]
    def relation(r,key):
        edges=[e for e in r.get('linked_prefix',{}).get('entries',[])
               if e.get('keyword_identity')==key]
        if any(e['target_mode'] not in (0,1) for e in edges): raise ValueError('RELATION_MODE')
        targets={e['target_identity'] for e in edges}
        if len(targets)>1: raise ValueError('CONFLICTING_RELATION')
        return next(iter(targets)) if targets else None
    def item(root,kind,peers,group=None):
        da=root['linked_prefix'].get('packin',[])
        definition=da[0]['identities'][0] if kind=='PACKIN_ROOT' else root.get('base_identity')
        definitions=context['records'].get(definition,[]) if context else []
        row=dict(instance_identity=root['saved_reference'],instance_token=root['token'],
            owner_identity=root['owner_identity'],base_identity=root.get('base_identity'),
            construction_definition=definition,root_kind=kind,group_identity=group,
            member_identities=sorted(r['saved_reference'] for r in peers),
            member_offsets=sorted(r['offset'] for r in peers),
            editor_name=definitions[0]['editor_id'] if len(definitions)==1 else None,
            definition_provenance=definitions,record_offset=root['offset'],record_end=root['end'],
            record_type=root['explicit_type'],offset_domain='DECODED_LOGICAL_STREAM',
            raw_position=root['prefix'].get('xyz'),
            saved_form_flags=root['prefix'].get('saved_form_flags'),
            saved_aux_flags=root['prefix'].get('saved_aux_flags'),
            saved_disabled=root['prefix']['disabled'],saved_deleted_bit=root['prefix']['deleted'],
            association_status='SAVED_EXPLICIT_NATIVE_ITEM_ROOT',
            reason='CLOSED_EXTRAS_UNIQUE_OWNER_AND_NATIVE_ROOT_INPUTS',
            completeness='COMPLETE_SUPPORTED_ROOT_PROJECTION_ONLY',
            member_population_complete=False,
            loaded_group_completeness='NOT_ESTABLISHED_DEFAULTS_REVERSE4D_OTHER_ENCODINGS')
        items.append(row)
    for r in members:
        role=dict(reference_identity=r.get('saved_reference'),token=r['token'],offset=r['offset'],
            owner_identity=r['owner_identity'],role='UNRESOLVED',reason=None,root_identity=None)
        roles.append(role)
        try:
            if not r['owner_identity']: raise ValueError(r['reason'])
            x=r['linked_prefix']
            if x['following_extras']!='CLOSED': raise ValueError('EXTRAS_NOT_CLOSED:'+str(x.get('following_gap')))
            if x.get('extra_flags') is None: raise ValueError('EXTRA_FLAGS_OMITTED_DEFAULT_UNKNOWN')
            foundation=relation(r,'starfield.esm:000192')
            if foundation and x.get('alternate_groups'):
                raise ValueError('ALTERNATE80_FOUNDATION_GETTER_UNRESOLVED')
            if x['extra_flags']&0x800 and foundation:
                if len(index[foundation])!=1: raise ValueError('FOUNDATION_TARGET_MISSING_OR_DUPLICATE')
                role.update(role='FOUNDATION_MEMBER',reason='NATIVE_9C800_AND_FOUNDATION192_FILTER')
                continue
            replacement=relation(r,'starfield.esm:000191')
            effective=r
            if replacement:
                if len(index[replacement])!=1: raise ValueError('REPLACEMENT_MISSING_OR_DUPLICATE')
                effective=index[replacement][0]
                if effective is r or relation(effective,'starfield.esm:000191'):
                    raise ValueError('REPLACEMENT_SELF_OR_CHAIN_UNSUPPORTED')
                if effective.get('owner_identity')!=r['owner_identity']: raise ValueError('REPLACEMENT_OWNER_UNRESOLVED_OR_CONFLICT')
                if effective.get('linked_prefix',{}).get('following_extras')!='CLOSED':
                    raise ValueError('REPLACEMENT_EXTRAS_NOT_CLOSED')
            da=effective.get('linked_prefix',{}).get('packin',[])
            if len(da)>1: raise ValueError('MULTIPLE_PACKIN_EXTRAS')
            group=(effective['saved_reference'] if effective.get('base_identity')=='starfield.esm:015804'
                   else da[0]['identities'][3] if da else None)
            if group:
                role['group_identity']=group
                if x.get('alternate_groups'): raise ValueError('ALTERNATE80_POSSIBLE_GROUP_CONTEXT_ONLY')
                role['role']='PENDING_GROUP'
                groups[(r['owner_identity'],group)].append((r,role))
            else:
                if x.get('alternate_groups'): raise ValueError('ALTERNATE80_GETTER_PRECEDENCE_SINGLE')
                if replacement: raise ValueError('REPLACEMENT_WITHOUT_GROUP')
                if da: raise ValueError('PACKIN_WITHOUT_GROUP_OR_DUMMY')
                role.update(role='SINGLE_ROOT',reason='NATIVE_NO_GROUP_SINGLE_ITEM_PATH',root_identity=r['saved_reference'])
                item(r,'SINGLE_ROOT',[r])
        except ValueError as e: role['reason']=str(e)
    for (owner,group), pairs in sorted(groups.items()):
        roots=[r for r,_ in pairs if r.get('base_identity')=='starfield.esm:015804'
               and relation(r,'starfield.esm:000191') is None]
        gap=None
        if len(pairs)<2: gap='SINGLETON_GROUP_NATIVE_PEER_POPULATION_UNRESOLVED'
        elif len(roots)!=1: gap='MISSING_OR_AMBIGUOUS_UNREPLACED_DUMMY_ROOT'
        elif not roots[0]['linked_prefix'].get('packin'): gap='DUMMY_CONSTRUCTION_DEFINITION_OMITTED'
        elif roots[0]['linked_prefix'].get('alternate_groups'): gap='ALTERNATE80_GETTER_PRECEDENCE_ROOT'
        # A different dummy cannot select this group: dummy groupID is SELF.
        # >=2 qualified peers proves the compound branch without claiming the
        # saved forward projection contains every reverse4D/default member.
        if gap:
            for _,role in pairs: role.update(role='UNRESOLVED',reason=gap)
        else:
            root=roots[0]
            item(root,'PACKIN_ROOT',[r for r,_ in pairs],group)
            for r,role in pairs:
                role.update(role='PACKIN_ROOT' if r is root else 'GENERATED_PACKIN_MEMBER',
                    reason='NATIVE_GROUP_ID_AND_UNREPLACED_DUMMY_SELECTOR',root_identity=root['saved_reference'])
    items.sort(key=lambda r:(r['owner_identity'],r['instance_identity'],r['record_offset']))
    roles.sort(key=lambda r:(r['reference_identity'] or '',r['offset']))
    for owner in ledger['owners']:
        owner['supported_constructed_roots']=sum(i['owner_identity']==owner['owner_identity'] for i in items)
        owner['root_role_counts']=dict(collections.Counter(r['role'] for r in roles if r['owner_identity']==owner['owner_identity']))
    ledger.update(constructed_instances=items,member_roles=roles,
        root_representation='CLOSED_EXPLICIT_SAVED_WORKSHOP_NATIVE_ITEM_PROJECTION/1',
        conclusion='SCOPED_NATIVE_ITEM_ROOT_POSITIVE_UNIVERSAL_POPULATION_UNRESOLVED')
    ledger['coverage'].update(supported_constructed_roots=len(items),member_role_counts=dict(collections.Counter(r['role'] for r in roles)),
        complete_supported_root_projection=True,complete_loaded_native_item_population=False)
    return ledger
