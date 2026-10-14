"""Original bounded follow-on: resolve exact DFOB DATA definition, no writes
to sources. Uses project selective38ESM context with exclusive local output.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from workshop_definition_context import context
p=Path('.local-work/workshop-population-rework/specialist');d=json.loads((p/'location-default29.json').read_text());ids={r['qualified_u32']['DATA'] for r in d['rows']};assert ids=={'starfield.esm:2521c2'}
paths=[Path(s['path']) for s in d['sources']];result=context(paths,ids)
with (p/'location-selector30.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
print(result['records'])
