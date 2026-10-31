# SPDX-License-Identifier: GPL-3.0-or-later
"""Render D5Z causal graphs from authored machine-readable backing data.

Stdlib only. Reads a supplied JSON graph file; writes SVGs to a fresh output
directory. No target, native code, save, database, network or Git operations.
Node positions are layout coordinates, not geographical or temporal axes.
Evidence links are relative to the tracked d5z/ SVG destination.
"""
from html import escape
import json
from pathlib import Path
import sys

COLORS = {'static':'#125c70', 'observed':'#28643b', 'inferred':'#926000', 'open':'#9a3d65', 'contradicted':'#7f4b40'}

def render(graph):
    width, height = graph['size']
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 Z" fill="context-stroke"/></marker></defs>',
        '<rect width="100%" height="100%" fill="#f7f8fa"/>',
        '<g font-family="Segoe UI,Arial,sans-serif">',
        f'<text x="32" y="42" font-size="26" font-weight="700" fill="#192b38">{escape(graph["title"])}</text>',
        f'<text x="32" y="72" font-size="15" fill="#374e60">{escape(graph["subtitle"])}</text>']
    legend = 'Solid blue: static conditional path | Green: B1 witness | Dashed amber: inference | Dashed rose: historical gap | Brown: contradicted scoped claim'
    parts.append(f'<text x="32" y="100" font-size="13" fill="#374e60">{escape(legend)}</text>')
    nodes = {n['id']:n for n in graph['nodes']}
    for edge in graph['edges']:
        points = edge['points']
        color = COLORS[edge['class']]
        dash = ' stroke-dasharray="8 5"' if edge['class'] in ('open','inferred') else ''
        route = ' '.join(f'{x},{y}' for x,y in points)
        parts.append(f'<a href="{escape(edge["evidence"],quote=True)}"><title>{escape(edge["claim"])}</title><polyline points="{route}" fill="none" stroke="{color}" stroke-width="2.5"{dash} marker-end="url(#arrow)"/></a>')
        if edge.get('label'):
            x,y = edge['label_at']
            label = escape(edge['label'])
            parts.append(f'<text x="{x}" y="{y}" font-size="13" fill="{color}" paint-order="stroke" stroke="#f7f8fa" stroke-width="5" stroke-linejoin="round">{label}</text>')
    for node in nodes.values():
        x,y,w,h = node['box']
        color = COLORS[node['class']]
        parts.append(f'<a href="{escape(node["evidence"],quote=True)}"><title>{escape(node["claim"])}</title><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="white" stroke="{color}" stroke-width="2"/>')
        for i,line in enumerate(node['lines']):
            size, weight = (17,700) if i==0 else (15,400)
            parts.append(f'<text x="{x+16}" y="{y+29+i*24}" font-size="{size}" font-weight="{weight}" fill="#192b38">{escape(line)}</text>')
        parts.append('</a>')
    for i,line in enumerate(graph['notes']):
        parts.append(f'<text x="32" y="{height-50+(i*22)}" font-size="14" fill="#374e60">{escape(line)}</text>')
    return '\n'.join(parts+['</g></svg>'])+'\n'

def main():
    source, out = map(Path, sys.argv[1:])
    graphs = json.loads(source.read_text(encoding='utf8'))['graphs']
    out.mkdir(parents=True,exist_ok=False)
    for graph in graphs:
        assert graph['file'].endswith('.svg') and '/' not in graph['file']
        (out/graph['file']).write_text(render(graph),encoding='utf8',newline='\n')
    print(f'Rendered {len(graphs)} graphs to {out}')

if __name__ == '__main__':
    main()
