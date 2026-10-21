"""Independent exact-dyadic check of B1 rectangle/disk coverage. Defines the
continuous extension of the actual binary32 .01 quantizer by rounding a real
reference coordinate to binary32, then native-order multiplication. Thresholds
are adjacent-float midpoints, not fitted epsilons. Reads model/map receipts;
writes exclusive ignored JSON. Native execution and radial float predicate
equivalence are not claimed; the requested nominal disk is mathematical.
"""
from pathlib import Path
from fractions import Fraction as F
import json,struct,math,hashlib
W=Path('.local-work/outpost-biomes')
def f(x):return struct.unpack('<f',struct.pack('<f',x))[0]
def key(x):
 b=struct.unpack('<I',struct.pack('<f',x))[0];return (~b&0xffffffff) if b>>31 else b|0x80000000
def value(k):
 b=k&0x7fffffff if k>>31 else ~k&0xffffffff;return struct.unpack('<f',struct.pack('<I',b))[0]
K=f(.01)
def lower(q):
 # Bounded local operand domain: |x|<4000; bracketing is proved by assertions.
 a=key(f(q*100-.01));b=key(f(q*100+.01));assert math.floor(f(value(a)*K))<q<=math.floor(f(value(b)*K))
 while a+1<b:
  c=(a+b)//2
  if math.floor(f(value(c)*K))>=q:b=c
  else:a=c
 assert b==a+1 and math.floor(f(value(a)*K))<q<=math.floor(f(value(b)*K))
 return (F(value(a))+F(value(b)))/2,(value(a),value(b))
j=json.loads((W/'model-r2.json').read_text());results=[];boundaries={};checks=[]
for row in j['rows']:
 cx,cy=map(F,row['center'][:2]);radius=F(150);cells=[]
 for qy in range(math.floor((cy-radius)/100)-1,math.floor((cy+radius)/100)+2):
  for qx in range(math.floor((cx-radius)/100)-1,math.floor((cx+radius)/100)+2):
   x0,xx=lower(qx);x1,_=lower(qx+1);y0,yy=lower(qy);y1,_=lower(qy+1)
   for q in [qx,qx+1,qy,qy+1]:
    z,neighbors=lower(q);boundaries[q]=dict(boundary=str(z),neighbors=neighbors,nominal_error=float(z-q*100))
   dx=max(x0-cx,F(0),cx-x1);dy=max(y0-cy,F(0),cy-y1)
   if dx*dx+dy*dy<radius*radius:cells.append([qx,qy])
 expected=sorted(c['q'] for c in row['cells']);assert sorted(cells)==expected
 results.append(dict(sample=row['sample'],token=row['token'],cells=cells,exact_quantizer_preimage_same_cells=True))
# Actual exact tangency: construct center one radius left of an exact boundary.
edge,_=lower(2);cx=edge-150;dx=edge-cx;assert dx*dx==F(150)**2
checks.append(dict(test='exact_quantizer_tangent_area_zero',passed=not(dx*dx<F(150)**2)))
checks.append(dict(test='positive_dyadic_cap_survives',passed=(dx-F(1,2**20))**2<F(150)**2))
checks.append(dict(test='negative_dyadic_gap_excluded',passed=not((dx+F(1,2**20))**2<F(150)**2)))
assert all(c['passed'] for c in checks)
out=dict(results=results,quantizer_constant_hex=struct.pack('<f',K).hex(),boundaries=boundaries,checks=checks,domain='RNE and gradual-underflow mathematical surrogate, including the tiny subnormal neighborhood of lower(0); examined local |x|<4000. Historical MXCSR FTZ/DAZ unmeasured. Exact surrogate intervals do not prove hardware equivalence. Selected case tangency margins exceed0.5 units; zero-neighborhood differences cannot alter these case cell lists.',source_sha256=hashlib.sha256((W/'model-r2.json').read_bytes()).hexdigest())
(W/'numeric-r2.json').open('x',encoding='utf8').write(json.dumps(out,indent=2)+'\n')
print('PASS exact rational quantizer preimages',len(results),'cases;',len(checks),'boundary controls; max shift',max(abs(x['nominal_error']) for x in boundaries.values()))
