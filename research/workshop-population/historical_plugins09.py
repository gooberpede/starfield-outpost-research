"""Observed buffer122 partial plugin header, original local reader.
Full list has u8 count and u16 strings WITHOUT modern per-name metadata flag.
Bound declared block but preserve remaining small/medium bytes as unresolved;
do not guess metadata grammar. Dynamic/full IDs resolve; others explicit unknown.
"""
from outpost_record_framing import Reader
from extractor_resources import saved_form as modern_saved_form
def plugin_tables(b):
 c=Reader(b,16+int.from_bytes(b[12:16],'little'),len(b));version=c.take(1)[0]
 def string(cursor):return cursor.take(int.from_bytes(cursor.take(2),'little')).decode('utf8')
 builds=[string(c),string(c)];n=int.from_bytes(c.take(4),'little');p=Reader(b,c.p,c.p+n)
 names=[string(p).lower() for _ in range(p.take(1)[0])]
 assert names and names[0]=='starfield.esm' and all(x.endswith(('.esm','.esp','.esl')) for x in names)
 return dict(groups=dict(full=names,small=[],medium=[]),version=version,builds=builds,start=c.p,end=p.end,parsed_end=p.p,unparsed_plugin_metadata=b[p.p:p.end].hex(),scope='PARTIAL_OLD_FULL_SLOTS_ONLY')
def saved_form(fid,plugins):
 try:return modern_saved_form(fid,plugins)
 except ValueError:return f'UNRESOLVED_OLD_PLUGIN_SLOT:{fid:08x}'
