"""SPDX-License-Identifier: GPL-3.0-or-later
Offline corpus challenge, stdlib only. Reads frozen identity manifests, verified
ignored copies and two inspected ESM definition summaries. Archives missing
copies by SHA-256, never overwrites. Reads originals for integrity/copy only.
Writes fresh ignored numeric receipts, no decoded payload or target effects.
128MiB physical/64MiB decoded and existing 40GB C/D guards; no dependencies.
No prior classification, name, JSON network or quest outcome feeds classifier.
Plugin mapping below is an explicitly conditional hypothesis, not load remapping.
"""
from pathlib import Path
import argparse, collections, json, re, shutil, struct, sys, time
from investigate_active_outposts import specs
from inventory_historical_saves import identity, guard, framing, transform, MAX_PHYSICAL, MAX_DECODED, sha
from outpost_membership import classify

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--definitions', type=Path, required=True)
    ap.add_argument('--labels', help='optional comma-separated identity labels; never classifier inputs')
    args = ap.parse_args()
    if not re.fullmatch('[a-z0-9-]+', args.run):
        raise ValueError('run name')
    out = ROOT / '.local-work/membership-completion' / args.run
    out.mkdir(exist_ok=False)
    guard(out)
    started = time.monotonic()
    tool_paths = [Path(sys.executable), args.definitions] + sorted(Path(__file__).parent.glob('*.py'))
    tools_before = [identity(p) for p in tool_paths]
    archive = ROOT / '.local-work/membership-completion/archive'
    archive.mkdir(exist_ok=True)
    # Existing verified archives preferred; no second large copy by label.
    archived = {}
    for p in (ROOT / '.local-work').rglob('*.sfs'):
        v = identity(p)
        archived.setdefault(v['sha256'], p)
    definitions = json.loads(args.definitions.read_text())
    rows, preservation, cache = [], [], {}
    for s in specs():
        if args.labels and s['label'] not in args.labels.split(','):
            continue
        if time.monotonic() - started > 1800:
            raise ValueError('SCAN_TIME_BOUND')
        guard(out)
        expected = s['copy']
        source = Path(s['source']['path'])
        before = identity(source)
        if before['sha256'] != expected['sha256'] or before['size'] != expected['size']:
            raise ValueError('source mismatch: ' + s['label'])
        p = archived.get(expected['sha256'])
        if p is None:
            p = archive / (expected['sha256'] + '.sfs')
            with source.open('rb') as src, p.open('xb') as dst:
                shutil.copyfileobj(src, dst)
            archived[expected['sha256']] = p
        copy_before = identity(p)
        if copy_before['sha256'] != expected['sha256']:
            raise ValueError('copy mismatch')
        h = expected['sha256']
        if h not in cache:
            physical = p.read_bytes()
            if sha(physical) != h:
                raise ValueError('in-memory mismatch')
            r = dict(status='INDETERMINATE')
            try:
                if len(physical) > MAX_PHYSICAL:
                    raise ValueError('PHYSICAL_SIZE_LIMIT')
                f, sp = framing(physical)
                if f['declared_decoded_size'] > MAX_DECODED:
                    raise ValueError('DECODED_SIZE_LIMIT')
                b = transform(physical, sp, True)
                # Only a lead: regex occurrence sequence is not a plugin-table decoder.
                plugins = [x.decode('ascii') for x in re.findall(rb'[A-Za-z0-9_ -]+\.(?:esm|esp|esl)', b[:8192])]
                catalog = dict(direct_bases={}, templates={})
                for name, definition in definitions.items():
                    if name not in plugins:
                        continue
                    slot = plugins.index(name)
                    if slot > 0xfd:
                        continue
                    for d in definition['definitions']:
                        catalog['direct_bases'][(slot << 24) | (d['formid'] & 0xffffff)] = d['editor_id']
                    for t in definition['templates']:
                        base = t['base_formid'] & 0xffffff
                        catalog['templates'][(slot << 24) | (t['formid'] & 0xffffff)] = (slot << 24) | base
                r = classify(b, catalog)
                r.update(decoded_sha256=sha(b), conditional_plugin_sequence=plugins)
                del b
            except (ValueError, struct.error) as e:
                r.update(reason_codes=[str(e)], candidate_count=None)
            cache[h] = r
        rows.append(dict(label=s['label'], source_sha256=h, source_size=before['size'], result=cache[h]))
        after, copy_after = identity(source), identity(p)
        if before != after or copy_before != copy_after:
            raise ValueError('input changed')
        preservation.append(dict(label=s['label'], source_before=before, source_after=after,
                                 copy_before=copy_before, copy_after=copy_after))
        if len(rows) % 50 == 0:
            print('processed', len(rows), flush=True)
    tools_after = [identity(p) for p in tool_paths]
    if tools_before != tools_after:
        raise ValueError('tool/input definition changed')
    for name, data in [('features-frozen.json', rows), ('preservation.json', preservation),
                       ('tools.json', dict(before=tools_before, after=tools_after, argv=sys.argv))]:
        with (out / name).open('x', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, indent=2)
            f.write('\n')
    print(json.dumps(dict(labels=len(rows), unique_hashes=len(cache),
        framed=sum('coverage' in r['result'] for r in rows),
        states=dict(collections.Counter(r['result']['status'] for r in rows)),
        isdeleted_set=sum(len(r['result'].get('isdeleted_set_records', [])) for r in rows))))


if __name__ == '__main__':
    main()
