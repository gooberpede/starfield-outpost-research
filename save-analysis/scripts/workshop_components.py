"""SPDX-License-Identifier: GPL-3.0-or-later
Pinned native type6 component grammar for save-format27/buffer153.
Original project research: consumes mapped bytes, returns local evidence fields.
No I/O, dependencies, target, database or network effects. Caller qualifies the
build, native-dispatch receipt and StarbornManager-zero activity format. A body
closure proves framing only; owner/population semantics are separate joins.
See docs/experiments/workshop-population/schema.md and specialist native37-78.
"""
from outpost_record_framing import Reader


def component_sections(b, start, end, *, buffer_version, activity_custom_payloads,
                       pending_dialogue=False):
    if buffer_version != 153 or activity_custom_payloads is not True:
        raise ValueError('UNQUALIFIED_COMPONENT_CONTEXT')
    c=Reader(b,start,end);sections=[];activity_leads=[]
    def u(n):return int.from_bytes(c.take(n),'little')
    def string():return c.take(u(4)).decode('utf8')
    def table(name,payload,size=None):
     at=c.p;n=u(4);rows=[];section=dict(name=name,offset=at,count=n);sections.append(section)
     for _ in range(n):
      entry=c.p
      if name in ('1414128c0','141413780'):
       raw=c.take(30 if name=='1414128c0' else 10);rows.append(dict(offset=entry,bytes=raw.hex()));continue
      word=u(4);index=u(2)
      if payload=='fixed':raw=c.take(size);rows.append(dict(offset=entry,id_word=word,index=index,payload=raw.hex()))
      elif payload=='string':
       s=string();raw=c.take(size);rows.append(dict(offset=entry,id_word=word,index=index,text=s,payload=raw.hex()))
      elif payload=='strings5':
       ss=[string() for _ in range(5)];rows.append(dict(offset=entry,id_word=word,index=index,texts=ss,payload=c.take(4).hex()))
      elif payload=='galaxy337':
       flags=u(4);version=u(2);value=u(4);ids=[u(4) for _ in range(u(4))];nested=[]
       if flags&8:
        for _ in range(u(8)):
         nr=dict(id_word=u(4),byte_a=u(1));nr['byte_b']=u(1) if version>1 else None
         nr['ids']=[u(4) for _ in range(u(8))] if version else [];nested.append(nr)
       raw=c.take(u(8)*12).hex() if version>2 else None
       rows.append(dict(offset=entry,id_word=word,index=index,flags=flags,version=version,value=value,ids=ids,nested=nested,raw_tail=raw))
      elif payload=='referenced-cell':
       rows.append(dict(offset=entry,id_word=word,index=index,cell_a=u(4),cell_b=u(4),name=string(),state=u(1),value=u(4),has_mapping=u(1)))
      elif payload=='cell-packin':
       ids=[u(4) for _ in range(6)];has=u(1);extra=[u(4),u(4)] if has else []
       rows.append(dict(offset=entry,id_word=word,index=index,ids=ids,has_mapping=has,extra=extra))
      elif payload=='worldclone':
       ids=[u(4) for _ in range(3)];pairs=[[u(4),u(4)] for _ in range(u(8))]
       rows.append(dict(offset=entry,id_word=word,index=index,ids=ids,pairs=pairs))
      elif payload=='middle':
       first=u(4);a=[u(4) for _ in range(u(4))];second=u(4);bb=[u(4) for _ in range(u(4))]
       rows.append(dict(offset=entry,id_word=word,index=index,first=first,first_ids=a,second=second,second_ids=bb))
      elif payload=='ids32':
       rows.append(dict(offset=entry,id_word=word,index=index,ids=[u(4) for _ in range(u(4))]))
      elif payload=='ids16':
       rows.append(dict(offset=entry,id_word=word,index=index,ids=[u(4) for _ in range(u(2))]))
      elif payload=='color':
       flag=u(1);saved_count=u(4);count=min(saved_count,3)
       rows.append(dict(offset=entry,id_word=word,index=index,flag=flag,saved_count=saved_count,colors=c.take(count*12).hex()))
      elif payload=='blob':
       count=u(4);blob=c.take(count).hex();refs=[c.take(3).hex() for _ in range(u(2))] if count else []
       rows.append(dict(offset=entry,id_word=word,index=index,blob=blob,inline_refs=refs))
      elif payload=='nested16':
       flag=u(1);groups=[[u(4) for _ in range(u(2))] for _ in range(u(2))]
       rows.append(dict(offset=entry,id_word=word,index=index,flag=flag,groups=groups))
      elif payload=='effects':
       groups=[]
       for _ in range(u(4)):
        groups.append(dict(raw_words=[u(4) for _ in range(u(4))],a=u(4),b=u(4),c=u(4)))
       rows.append(dict(offset=entry,id_word=word,index=index,groups=groups))
      elif payload=='finalA':
       raw=c.take(34).hex();values=[dict(value=u(4),ids=[u(4) for _ in range(4)]) for _ in range(u(2))];last=u(1)
       rows.append(dict(offset=entry,id_word=word,index=index,raw=raw,values=values,last=last))
      elif payload=='finalB':
       first=u(4);flag=u(1);values=[]
       for _ in range(u(8)):
        nr=dict(id_word=u(4),value=u(4));nr['saved_color_count']=u(4);nr['colors']=c.take(min(nr['saved_color_count'],3)*12).hex();values.append(nr)
       rows.append(dict(offset=entry,id_word=word,index=index,first=first,flag=flag,values=values,last=u(4)))
      elif payload=='600cc0':
       data=[]
       for _ in range(u(2)):
        nr=dict(id_word=u(4),value=u(2));nr['entries']=[]
        for _ in range(u(2)):
         entry_data=dict(raw=c.take(12).hex(),text=string())
         activity_leads.append(dict(offset=c.p,name=entry_data['text'],raw=entry_data['raw']))
         name=entry_data['text']
         vector={'Harvest','Barter','Consume','Craft','Dock Ship','Land Planet','LootContainer','Lose Enemy','Scan Surface','ShipBuilder','ShipCollection'}
         empty={'Kill','Bleedout','Research Completed','Cripple Limb','Destroy Ship','Grav Jump','Location Discovered','Produce','Reload Weapon','Scan Planet','Lockpick','Speech Challenge','Take Actor Damage','Take Hit Damage'}
         if name in vector:entry_data['derived_ids']=[u(4) for _ in range(u(4))]
         elif name in ('Build Workshop Item','Player Pickpocket'):
          entry_data['derived_ids']=[u(4) for _ in range(u(4))];entry_data['derived_ids_b']=[u(4) for _ in range(u(4))]
         elif name in ('Actor Value','Sprint'):entry_data['derived_raw']=c.take(9).hex()
         elif name=='Apply Magic Effect':
          entry_data['derived_ids']=[u(4) for _ in range(u(4))];entry_data['derived_pairs']=[[u(2),u(4)] for _ in range(u(4))]
         elif name not in empty:raise ValueError(('ACTIVITY_READER_UNQUALIFIED',name,c.p))
         entry_data['common_activity_runtime']=dict(counter=u(4),status=u(1))
         nr['entries'].append(entry_data)
        nr['ids_a']=[u(4) for _ in range(u(4))];nr['ids_b']=[u(4) for _ in range(u(4))];data.append(nr)
       rows.append(dict(offset=entry,id_word=word,index=index,data=data))
      else:raise ValueError(('PAYLOAD_UNQUALIFIED',name,n,entry))
     section.update(end=c.p,rows=rows)
    for name,payload,size in [('141411680','fixed',16),('1414118e0','string',25),('141411ba0','fixed',1),('141411da0','fixed',4),('141411fa0','string',1),('141412170','fixed',4),('141412370','fixed',4),('141412570','fixed',4),('141412700','fixed',8),('1414128c0','fixed',None),('14140c8c0-marker','fixed',0),('14140c8c0-celestial','fixed',25),('141412c50','fixed',4),('141412e50','fixed',60),('1414130d0','fixed',12),('141413320','strings5',None),('141413570','galaxy337',None),('141413780','fixed',None)]:
     table(name,payload,size)
    table('1409647c0-ReferencedCell','referenced-cell')
    table('140923480-CellPackIn','cell-packin')
    for name in ('140923480-markerA','140923480-markerB','140923480-markerC'):table(name,'fixed',0)
    table('140bc4280-WorldClone','worldclone')
    # SD1 verified the typed u32 payload for the selected HIST-0021 context.
    table('140d4ae40', 'fixed' if pending_dialogue else 'unknown', 4)
    at=c.p;dynamic=[]
    while True:
     word=u(4)
     if not word:break
     dynamic.append(dict(id_word=word,other=u(4),value_a=u(4),value_b=u(4),parent=u(4),flag=u(1),raw=c.take(16).hex()))
    sections.append(dict(name='140ad6150-WRLD-sentinel',offset=at,count=len(dynamic),rows=dynamic,end=c.p))
    table('14182e280-middle','middle')
    table('140602460','600cc0')
    table('141309900','fixed',9)
    table('141310be0','fixed',12)
    at=c.p;module=u(4);sections.append(dict(name='1424b57a0-module',offset=at,module=module,count=1,end=c.p))
    for name,size in [('14140d8c0-A',96),('14140d8c0-B',88),('141414e70',180),('141415060',104)]:table(name,'fixed',size)
    table('14140d8c0-C','ids32')
    table('141327270-Color','color')
    table('1412fe810-Blob','blob')
    table('1412fe810-Nested','nested16')
    table('14182f010-CalculatedPackinData','ids16')
    table('14214cf70-SpaceshipEffects','effects')
    table('14131c220','finalA')
    table('141311410','finalB')
    if c.p!=c.end:raise ValueError(('TYPE6_CLOSURE',c.p,c.end))
    return sections
