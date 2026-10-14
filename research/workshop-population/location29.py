"""Original exact DFOB literal join, installed38ESM pins from catalog22.
Reads/decompresses DFOB/TES4 only, no assets; exclusive local receipt.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import identity,guard
from extractor_resources import qualified
p=Path('.local-work/workshop-population-rework/specialist');c=json.loads((p/'location-definitions22.json').read_text());pins=c['sources'];flags={};masters={};rows=[];guard()
for pin in pins:
 path=Path(pin['path']);assert identity(path)==pin
 row,fs=next(esm_records(path,{b'TES4'},repeated=True));flags[path.name.lower()]=row['flags'];masters[path.name.lower()]=[v.rstrip(b'\0').decode().lower() for k,v in fs if k==b'MAST']
for pin in pins:
 path=Path(pin['path'])
 for row,fs in esm_records(path,{b'DFOB'},repeated=True):
  names=[v.rstrip(b'\0').decode() for k,v in fs if k==b'EDID']
  if 'ShipFastTravelMarkerRefTypeDO' not in names:continue
  rows.append(dict(plugin=path.name,record=row,fields=[(k.decode(),v.hex()) for k,v in fs],editor_id=names[0],qualified_u32={k.decode():qualified(path.name.lower(),int.from_bytes(v,'little'),masters[path.name.lower()],flags) for k,v in fs if len(v)==4}))
 assert identity(path)==pin
with (p/'location-default29.json').open('x',encoding='utf8') as f:json.dump(dict(schema='exact-DFOB-name/1',sources=pins,rows=rows),f,indent=2);f.write('\n')
print(rows)
