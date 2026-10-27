# SPDX-License-Identifier: GPL-3.0-or-later
"""Enumerate competing installed anchors at selected boundary query cells.

Reads pinned restored D5 corpus; native-derived fill/edge/corner support and
concrete Y-edge slots. Writes a fresh ignored receipt only. Does not assume that
an installed anchor is admitted, an index is populated, or a request occurs.
No native calls, target or analysis DB writes. Stdlib; SOR-P-0002 corpus lineage.
"""
import itertools
import json
from pathlib import Path
import sys
from domains import load
from audit import LOCAL, write


def contributors(c, query):
    body=c['bodies']['0005e0de']; max_x=max(w-4 for w,h in c['source_blocks'].values());max_y=max(h-4 for w,h in c['source_blocks'].values())
    qx,qy=query; result=[]; tiles=[]; seen=set()
    # Any anchor whose padded rectangle contains the cell must lie in these
    # inclusive bounds. Whole installed FNAM anchor entries are then inspected,
    # rather than an inverse base selector sampled at the candidate query.
    axlo,axhi=qx-max_x-1,qx+2;aylo,ayhi=qy-max_y-1,qy+2
    for cx in range(axlo//192,axhi//192+1):
        for cy in range(aylo//192,ayhi//192+1):
            tilekey=f'0:{cx}:{cy}';tile=body['tiles'][tilekey];assert tile[1]==8
            tiles.append(dict(key=tilekey,pattern=tile[0],flags=tile[1]))
            for slot,(block,flags) in enumerate(c['patterns'][tile[0]]):
                if not flags&8:continue
                sx,sy=divmod(slot,16);ax,ay=cx*192+sx*12,cy*192+sy*12
                w,h=(v-4 for v in c['source_blocks'][block]);dx,dy=qx-ax,qy-ay
                if not (-2<=dx<w+2 and -2<=dy<h+2):continue
                key=f'0:{ax}:{ay}:{block}';assert (ax,ay) not in seen;seen.add((ax,ay))
                kind='fill' if 0<=dx<w and 0<=dy<h else 'edgeY' if 0<=dx<w else 'other'
                slotfield='0x18' if kind=='fill' else '0x18' if kind=='edgeY' and dy<0 else '0x20' if kind=='edgeY' else 'UNRESOLVED'
                edgeflag=2 if kind=='edgeY' and dy<0 else 1 if kind=='edgeY' else 0
                result.append(dict(source=key,anchor=[ax,ay],nominal_dimensions=[w,h],relative_query=[dx,dy],
                    sfpt=tile[0],entry=slot,flags=flags,cell_kind=kind,edge_flag=edgeflag,setter_slot=slotfield,
                    source_local_raw_query=[dx+2,dy+2],raw_bounds_pass=0<=dx+2<w+4 and 0<=dy+2<h+4))
    outcomes=[]
    for ordering in itertools.permutations(result):
        assert all(r['cell_kind'] in ('fill','edgeY') and r['raw_bounds_pass'] for r in ordering)
        assert len({r['cell_kind'] for r in ordering})==1
        slots={}
        for row in ordering:slots.setdefault(row['setter_slot'],row['source'])
        outcomes.append(dict(order=[r['source'] for r in ordering],slots=slots,
            emitted=[slots[k] for k in sorted(slots)]))
    return dict(query=query,anchor_search_inclusive=[axlo,axhi,aylo,ayhi],max_nominal=[max_x,max_y],
        complete_tiles=tiles,contributors=result,permutation_outcomes=outcomes,
        selected_retained_in_all_orders=all('0:37536:20928:0029d20e' in r['emitted'] for r in outcomes),
        dedup='No repeated anchor among contributing installed entries; unrelated descriptors cannot dedup this anchor',
        qualification='Conditional on these installed descriptors reaching an ordinary completed index that contains the queried cells; does not prove first miss')


def main():
    output=Path(sys.argv[1]).resolve();assert output.is_relative_to(LOCAL) and not output.exists()
    c=load('.local-work/resource-feynman-d5/build04/normalized.json','97aa50e0eb6bc7a2d5157bffbb311942fd84e7c01e6bd2ef3ea28a4e9bd9e0f9')
    rows=[contributors(c,[37540,20927]),contributors(c,[37540,20929])]
    assert all(r['selected_retained_in_all_orders'] for r in rows)
    write(output,dict(rows=rows,actual_first_miss_proved=False))
    print(json.dumps(rows,indent=2))


if __name__=='__main__':main()
