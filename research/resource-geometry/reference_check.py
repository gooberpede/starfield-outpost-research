# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent arithmetic check of RG1 qualified source predictions.

Reads one local qualification receipt and maintainer-owned explicit MT source;
writes only an unused --output under ignored .local-work. No game/process/save/
analysis effects, installs or network. Uses double geometry, libm sin/cos and a
distance/slab predicate, independently of geometry.py's polynomial/Fraction
implementation. Inputs remain conditional; agreement is STATIC mathematical
cross-validation, never a newly observed native geometry oracle.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys,zlib,struct


R=Path(__file__).resolve().parents[2]
OWNED=Path('D:/Projects/starfield-resource-reproducer/src')
sys.path.insert(0,str(OWNED))
from starfield_resource_reproducer.prng import StarfieldRng


def bound(points):
    b=points[0][:];previous=b[3]
    for p in points[1:]:
        if p[3]>0:
            w=max(previous,p[3]);d=math.dist(b[:3],p[:3]);dr=w-b[3]
            if d>abs(dr):
                factor=(d-dr)/(2*d)
                b=[p[i]+factor*(b[i]-p[i]) for i in range(3)]+[(w+d+b[3])/2]
            elif dr>=0:b=p[:3]+[w]
        previous=p[3]
    return b


def contains(points,q,b=None):
    """Independent Euclidean-distance/slab route, no polygon cross-product test."""
    if not points:return False
    b=bound(points) if b is None else b
    if math.dist(q,b[:2])>max(.5,b[3]):return False
    if any(p[3]>0 and math.dist(q,p[:2])<=p[3] for p in points):return True
    for a,c in zip(points,points[1:]):
        dx,dy=c[0]-a[0],c[1]-a[1];length=math.hypot(dx,dy)
        if not length:continue
        along=((q[0]-a[0])*dx+(q[1]-a[1])*dy)/length
        across=abs((q[0]-a[0])*dy-(q[1]-a[1])*dx)/length
        if 0<=along<=length and across<=max(a[3],c[3]):return True
    return False


def reference(req):
    paths=[];gate_count=0
    for resource in req['ordered_resources']:
        block=resource['block'];identity=resource['resource']
        for x in range(req['cell_bounds'][0],req['cell_bounds'][1]):
            for y in range(req['cell_bounds'][2],req['cell_bounds'][3]):
                key=req['packed_keys'][f'{x},{y}']
                seed=zlib.crc32(struct.pack('<QI',key,req['owner_key']),0xffffffff)^0xffffffff
                rng=StarfieldRng(seed)
                def u():return rng.next_float01()
                def between(a,b):return a+(b-a)*u()
                if 100*u()>=resource['weight']*block[7]:continue
                gate_count+=1
                raw=between(block[0],block[1]);n=math.floor(raw)
                n+=raw-n>=u()
                if not n:continue
                angle=u()*math.tau;points=[]
                for _ in range(n):
                    w=between(block[2],block[3])
                    if not points:
                        p=[x*100+u()*100+req['origin'][0],y*100+u()*100+req['origin'][1],0,w]
                    else:
                        turn=u()*math.pi/180*block[6]
                        angle+=-turn if u()<.5 else turn
                        step=between(block[4],block[5])
                        p=[points[-1][0]+step*math.cos(-angle),points[-1][1]+step*math.sin(-angle),0,w]
                    if any(abs(p[i]-req['clip_center'][i])>req['clip_half'][i]+w for i in range(3)):continue
                    samples=[(p[0]+i*w,p[1]+j*w) for i in (-1,0,1) for j in (-1,0,1)]
                    if any(prior['resource']!=identity and any(contains(prior['points'],q,prior['bound']) for q in samples) for prior in paths):continue
                    points.append(p)
                if points:paths.append(dict(resource=identity,cell=[x,y],points=points,bound=bound(points)))
    return paths,gate_count


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    assert not args.output.exists() and args.output.resolve().is_relative_to((R/'.local-work').resolve())
    data=args.input.read_bytes();source=json.loads(data);max_error=0;bound_error=0;regions=0;gates=0;all_paths=[]
    for s in source['sources']:
        paths,count=reference(s['request']);expected=s['regions'];gates+=count
        assert len(paths)==len(expected),(s['source']['id'],len(paths),len(expected))
        for p,e in zip(paths,expected):
            assert (p['resource'],p['cell'],len(p['points']))==(e['resource'],e['cell'],len(e['points']))
            max_error=max(max_error,max(abs(a-b) for q,v in zip(p['points'],e['points']) for a,b in zip(q,v)))
            bound_error=max(bound_error,max(abs(a-b) for a,b in zip(p['bound'],e['native_bound'])))
        regions+=len(paths);all_paths+=paths
    assert max_error<.01,('coordinate difference exceeds declared tolerance',max_error)
    for row in source['fixed_queries']:
        actual=sorted({p['resource'] for p in all_paths if contains(p['points'],row['point'],p['bound'])})
        assert actual==row['resources'],(row,actual)
    assert bound_error<.01,bound_error
    result=dict(status='PASS_STATIC_ALTERNATE_ARITHMETIC',native_spatial_observation=False,input=dict(path=str(args.input),sha256=hashlib.sha256(data).hexdigest()),method=dict(path=str(Path(__file__)),sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),owned_mt=dict(path=str(OWNED/'starfield_resource_reproducer/prng.py'),sha256=hashlib.sha256((OWNED/'starfield_resource_reproducer/prng.py').read_bytes()).hexdigest()),regions=regions,chance_pass_cells=gates,max_coordinate_width_error=max_error,max_bound_component_error=bound_error,coordinate_tolerance=.01,queries=len(source['fixed_queries']),positive_queries=sum(bool(x['resources']) for x in source['fixed_queries']),negative_queries=sum(not x['resources'] for x in source['fixed_queries']))
    assert args.input.read_bytes()==data
    args.output.open('x',encoding='utf8',newline='\n').write(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
