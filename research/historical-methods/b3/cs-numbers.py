from pathlib import Path
import json,sys,struct,math,csv
R=Path.cwd();W=R/'.local-work/coordinate-sufficiency';sys.path.insert(0,str(R/'save-analysis/scripts'))
from stream_save import decoded_save
from saved_world_components import find_world_components
from outpost_planetary_location import body_catalog
from beacon_terrain_projection import split_local,grid_cell,to_square,grid_centre,f32
from position_quantizer_diagnostic import diagnose
cat=json.loads((R/'.local-work/save-capacity-location/esm-index-verified.json').read_text());bp,bi=body_catalog(cat['records']);keys={k:f'{v[0]["formid"]:08X}' for k,v in bp.items() if len(v)==1}
def write(p,x):p.open('x',encoding='utf8',newline='\n').write(json.dumps(x,indent=2)+'\n')
numbers=[];comparisons=[]
for label in ['37','38','39','25']:
 x=json.loads((W/('Save'+label+'.json')).read_text());de=json.loads((W/('Save'+label+'-descriptors.json')).read_text());descs=de['descriptors']
 parents={int(z['parent_token'],16) for z in x['extraction']['beacons']}
 with decoded_save(Path(x['source']['path']),W/'scratch',seconds=float('inf')) as (b,m):
  run=find_world_components(b,*x['extraction']['global_units']['6'],parents,keys,descs) if parents else None
 write(W/('Save'+label+'-worlds.json'),run)
 p=x['players'][0];r=p['record'];numbers.append(dict(sample='Save'+label,role='player',token=r['token'],record_offset=r['offset'],xyz_offset=p['xyz_offset'],parent=r['refs'][0],xyz=p['xyz'],frame=p['initial_flag'],site=p['points'],xyz_hex=p['xyz_hex']))
 for z in x['extraction']['beacons']:
  pt,=z['points'];co,=[v for v in run['rows'] if v['world']==z['parent_token']];ds,=[v for v in descs if v['world_token']==co['secondary'] and v['body']==co['body']]
  wp=z.get('workshop');assert wp and wp['delta_hex']=='000000000000000000000000'
  q=[split_local(v)[0] for v in z['local_xyz'][:2]];res=[split_local(v)[1] for v in z['local_xyz'][:2]]
  calculated=[ds['tag'],ds['x']+q[0],ds['y']+q[1]];assert calculated==list(pt['model_cell'])
  row=dict(sample='Save'+label,role='beacon',token=z['token'],parent=z['parent_token'],record_offset=z['record']['offset'],xyz_offset=z['xyz_offset'],xyz=z['local_xyz'],xyz_hex=z['xyz_hex'],frame=z['initial_flag'],site=pt,world=co,descriptor=ds,workshop=wp,q=q,residual_xy=res,calculated_cell=calculated,cell_equal=True)
  numbers.append(row)
  if label=='39':
   delta=[a-b for a,b in zip(z['local_xyz'],p['xyz'])];comparisons.append(dict(case='Save39 player to beacon',delta_xyz=delta,horizontal=math.hypot(*delta[:2]),distance=math.hypot(*delta),same_parent=z['parent_token']==r['refs'][0]))
 if label=='38':p38=p
 if label=='39':comparisons.append(dict(case='Save38 to39 player',delta_xyz=[a-b for a,b in zip(p['xyz'],p38['xyz'])],xy_hex_equal=p['xyz_hex'][:16]==p38['xyz_hex'][:16]))
fixed=json.loads((W/'fixed.json').read_text())['entries'][0];labcell=fixed['cell'];new=next(n for n in numbers if n['sample']=='Save39' and n['role']=='beacon')
old=[n for n in numbers if n['sample']=='Save25' and n['role']=='beacon']
for name,a,b in [('SOR002 to003',old[0],old[1])]:
 delta=[y-x for x,y in zip(a['xyz'],b['xyz'])];dc=[y-x for x,y in zip(a['calculated_cell'][1:],b['calculated_cell'][1:])];rem=[delta[i]-100*dc[i] for i in range(2)]
 comparisons.append(dict(case=name,delta_xyz=delta,delta_cell=dc,delta_cell_units=[100*k for k in dc],residual_error_xy=rem,max_quantization_delta_error_per_axis=100,horizontal=math.hypot(*delta[:2])))
comparisons.append(dict(case='Fixed Lab anchor to outpost anchor',delta_cell=[new['calculated_cell'][i]-labcell[i] for i in [1,2]],angular_delta=[new['site']['pair'][0]-fixed['longitude'],new['site']['pair'][1]-fixed['latitude']],not_marker_distance=True))
pp37=next(n for n in numbers if n['sample']=='Save37');pp38=next(n for n in numbers if n['sample']=='Save38');delta=[b-a for a,b in zip(pp37['xyz'],pp38['xyz'])]
comparisons.append(dict(case='Lab fast travel player to Save38',delta_xyz=delta,horizontal=math.hypot(*delta[:2]),distance=math.hypot(*delta),same_local_frame='CONDITIONAL; fixed to generated parent',scanner_lab_m=471,scanner_minus_local_distance=471-math.hypot(*delta)))
write(W/'numbers.json',dict(rows=numbers,comparisons=comparisons))
print(json.dumps(comparisons,indent=2));print('cells',[(n['sample'],n['token'],n.get('calculated_cell')) for n in numbers if n['role']=='beacon'])
