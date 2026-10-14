"""Bounded continuation of original location23; adds exact native104 bitmaps.
Reads same pinned inputs, exclusive new receipt; prior failed script preserved.
"""
from pathlib import Path
source=Path(__file__).with_name('location23.py').read_text()
source=source.replace("if f&(1<<25):raise ValueError(('KEYWORD_COMPONENT_PENDING',hex(f),r['offset'],c.p,qi))", """if f&(1<<25):
   n=c.count();bitmap=c.take((n+7)//8);fields['188']=[{'reference':ref(),'value':u(4) if bitmap[j//8]&(1<<(j%8)) else None} for j in range(n)]
   n=c.count();bitmap=c.take((3*n+7)//8);fields['198']=[{'reference':ref(),'values':[u(4) if bitmap[(3*j+k)//8]&(1<<((3*j+k)%8)) else None for k in range(3)]} for j in range(n)]""")
source=source.replace('location-census23.json','location-census24.json').replace('scratch23','scratch24')
exec(compile(source,str(__file__),'exec'))
