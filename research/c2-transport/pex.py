# SPDX-License-Identifier: GPL-3.0-or-later
"""Original finite C2 PEX inspection aid, CPython 3.14 -B/stdlib only.
Reads five already extracted installed members in ignored C2 evidence; writes
one exclusive ignored JSON. Parses only the observed v3.12/game4 grammar and
opcode shapes; no VM execution, source reconstruction/export to Git or general
PEX support promise. Bounds, declared object/file closure and branch controls
are integrity checks, not a proof of semantic equivalence. See README.md.
"""
import pathlib,struct,json
class P:
 def __init__(s,b):s.b=b;s.p=0;s.ss=[]
 def n(s,n):v=s.b[s.p:s.p+n];assert len(v)==n;s.p+=n;return v
 def u(s):return s.n(1)[0]
 def h(s):return struct.unpack('<H',s.n(2))[0]
 def i(s):return struct.unpack('<I',s.n(4))[0]
 def st(s):return s.n(s.h()).decode()
 def si(s):return s.ss[s.h()]
 def val(s):
  t=s.u()
  if t==0:return None
  if t in (1,2):return [t,s.si()]
  if t==3:return [t,struct.unpack('<i',s.n(4))[0]]
  if t==4:return [t,struct.unpack('<f',s.n(4))[0]]
  if t==5:return [t,s.u()]
  raise ValueError(('val',s.p,t))
 def func(s):
  ret,doc,uf,flags=s.si(),s.si(),s.i(),s.u()
  params=[(s.si(),s.si()) for _ in range(s.h())];locs=[(s.si(),s.si()) for _ in range(s.h())]
  ops=[]
  ar={0:0,1:3,2:3,3:3,4:3,5:3,6:3,7:3,8:3,9:3,10:2,11:2,12:2,13:2,14:2,15:3,16:3,17:3,18:3,19:3,20:1,21:2,22:2,23:3,24:2,25:3,26:1,27:3,28:3,29:3,30:2,31:2,32:3,33:3,34:4,35:4,36:4,37:1,38:3,39:4,40:4,41:3,42:3,43:2,44:3,45:2,46:4,47:3,48:4}
  for _ in range(s.h()):
   off=s.p;op=s.u();assert op in ar or op in (48,49),(off,op)
   if op in (48,49):
    count=s.val();assert count[0]==3;ops.append(dict(offset=off,op=op,args=[s.val() for _ in range(count[1])]))
    continue
   vals=[s.val() for _ in range(5 if op in (40,41) else ar[op])]
   if op in (23,24,25):
    count=s.val();assert count[0]==3;vals.append([s.val() for _ in range(count[1])])
   ops.append(dict(offset=off,op=op,args=vals))
  return dict(ret=ret,doc=doc,uf=uf,flags=flags,params=params,locals=locs,ops=ops)
 def parse(s):
  assert s.n(8)==bytes.fromhex('dec057fa030c0400');s.n(8);hdr=[s.st() for _ in range(3)];s.ss=[s.st() for _ in range(s.h())]
  if s.u():
   s.n(8)
   for _ in range(s.h()):
    s.si();s.si();s.si();s.u();s.n(2*s.h())
   # property groups: object,group,doc,userflags, property names
   for _ in range(s.h()):
    s.si();s.si();s.si();s.i();[s.si() for _ in range(s.h())]
   for _ in range(s.h()):
    s.si();s.si();[s.si() for _ in range(s.h())]
  uf=[(s.si(),s.u()) for _ in range(s.h())]
  objs=[]
  for _ in range(s.h()):
   name=s.si();size=s.i();end=s.p+size-4;parent=s.si();doc=s.si();const=s.u();flags=s.i();auto=s.si()
   structs=[]
   for _ in range(s.h()):
    sn=s.si();members=[]
    for _ in range(s.h()):members.append((s.si(),s.si(),s.i(),s.val(),s.u(),s.si()))
    structs.append((sn,members))
   variables=[]
   for _ in range(s.h()):variables.append((s.si(),s.si(),s.i(),s.val(),s.u()))
   guards=[s.si() for _ in range(s.h())]
   props=[]
   for _ in range(s.h()):
    pn,pt,pd,puf,pflag=s.si(),s.si(),s.si(),s.i(),s.u()
    if pflag&4:body=s.si()
    else:body=[s.func() for bit in (1,2) if pflag&bit]
    props.append((pn,pt,pflag,body))
   states=[]
   for _ in range(s.h()):
    state=s.si();fs=[]
    for _ in range(s.h()):
     fn=s.si();fs.append((fn,s.func()))
    states.append((state,fs))
   objs.append(dict(name=name,parent=parent,variables=variables,properties=props,states=states,guards=guards,constant=const,userflags=flags,end=s.p,declared_end=end))
   assert s.p==end,(name,s.p,end,s.b[s.p:s.p+40].hex())
  assert s.p==len(s.b),(s.p,len(s.b))
  return dict(header=hdr,objects=objs)
if __name__ == '__main__':
 import argparse,hashlib
 ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);a=ap.parse_args()
 assert a.run.isalnum()
 R=pathlib.Path(__file__).resolve().parents[2];W=R/'.local-work/c2-transport'
 import sys
 sys.path.insert(0,str(R/'save-analysis/scripts'))
 from inventory_historical_saves import guard
 guard()
 result={}
 for name in ('outpostcargolinkmarkerscript','sq_outpostcargolinkscript','sq_outpostcargolinkshipscript','pf_sq_outpostcargolinktravel_002457b0','pf_sq_outpostcargolinktravel_00255cc4'):
  b=(W/(name+'.pex')).read_bytes();j=P(b).parse()
  result[name]=dict(sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),decoded=j)
  for obj in j['objects']:
   for state,fs in obj['states']:
    for fn,f in fs:
     for i,op in enumerate(f['ops']):
      if op['op'] in (20,21,22):
       delta=op['args'][-1];assert delta[0]==3
       assert 0<=i+delta[1]<=len(f['ops']),(name,fn,i,delta)
 # Truncation and signature controls must fail, never produce partial success.
 failures=0
 for name in result:
  b=(W/(name+'.pex')).read_bytes()
  for bad in (b[:-1],b[:16],b'bad!'+b[4:]):
   try:P(bad).parse()
   except (AssertionError,IndexError,ValueError,struct.error,UnicodeDecodeError):failures+=1
   else:raise AssertionError('invalid input accepted')
 result['controls']=dict(invalid_inputs_rejected=failures,branch_targets_in_bounds=True)
 with (W/(a.run+'.json')).open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
 guard();print('PASS five closed members; 15 invalid inputs rejected; branch targets bounded')
