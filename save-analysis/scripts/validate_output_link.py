"""Bounded L0-L2C archive/analysis, invoked output-link brief only.

Reads named live saves for copy/hash/metadata only; parses verified local copies.
Reuses project-authored S0-S7C decoder/diff and unchanged candidate definitions.
Writes exclusively new local manifest, preregistration and analysis artifacts.
Installed CPython standard library only; no target/process/database effects.
Run from repo root: <python> save-analysis/scripts/validate_output_link.py
Stops on missing input, prior provenance mismatch, existing output or bad framing.
"""
from pathlib import Path
import datetime as dt
import argparse
import json
import re
import sys
import zlib

from archive_manual_corpus import metadata, sha as file_sha
from analyze_manual_corpus import decode, regions, compare, hits, sha
from probe_manual_candidates import MAIN, TOKENS, LINK

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/output-link-L0-L2C'
ARCHIVE = ROOT / '.local-work/savegames/output-link-L0-L2C'
PRIOR = ROOT / '.local-work/manual-S0-S7C'
BRIEF = ROOT / 'docs/implementation-briefs/CODEX_RESEARCH_BRIEF_output_link_validation_L0-L2C.md'
SOURCE = Path.home() / 'Documents/My Games/Starfield/Saves'


def write_json(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def archive():
    specs = re.findall(r'^(L[0-2]C?|exit) - (.+)\n([^\n]+\.sfs)$',
                       BRIEF.read_text(encoding='utf-8'), re.M)
    if [x[0] for x in specs] != ['L0', 'L0C', 'L1', 'L1C', 'L2', 'L2C', 'exit']:
        raise ValueError('Unexpected brief corpus')
    prior_manifest = json.loads((PRIOR / 'manifest.json').read_text())
    prior_analysis = json.loads((PRIOR / 'analysis-01/analysis.json').read_text())
    prior_candidates = json.loads((PRIOR / 'analysis-01/candidates.json').read_text())
    if (prior_candidates['link_motif'] != LINK.hex() or
            prior_candidates['main_signatures'] != MAIN or
            prior_candidates['tokens'] != TOKENS):
        raise ValueError('Candidate definitions changed')
    OUT.mkdir(parents=True, exist_ok=False)
    scripts = [Path(__file__), *(Path(__file__).parent / name for name in
               ('archive_manual_corpus.py', 'analyze_manual_corpus.py', 'probe_manual_candidates.py'))]
    write_json(OUT / 'preregistration.json', dict(
        recorded_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        link_motif=LINK.hex(), main_signatures=MAIN, tokens=TOKENS,
        prediction=['PRESENT', 'PRESENT', 'ABSENT', 'ABSENT', 'PRESENT', 'PRESENT'],
        prior_candidate_sha256=file_sha(PRIOR / 'analysis-01/candidates.json'),
        prior_report_sha256=file_sha(ROOT / 'docs/experiments/manual-save-corpus-S0-S7C.md'),
        script_hashes={str(p.relative_to(ROOT)): file_sha(p) for p in scripts},
        brief_sha256=file_sha(BRIEF)))
    ARCHIVE.mkdir(parents=True, exist_ok=False)
    samples = []
    classifications = ['HISTORICAL_LINKED_ANCHOR', 'NEW_SESSION_LINKED_BASELINE_CONTROL',
                       'UNLINK_ACTION', 'UNLINKED_NO_ACTION_CONTROL', 'RELINK_ACTION',
                       'RELINKED_NO_ACTION_CONTROL', 'INCIDENTAL_TERMINAL_SAMPLE']
    for index, (label, description, name) in enumerate(specs):
        source = SOURCE / name
        before = metadata(source)
        if label == 'L0':
            old = next(x for x in prior_manifest['samples'] if x['label'] == 'S4C')
            if name != old['filename'] or before['sha256'] != old['copy']['sha256']:
                raise ValueError('Historical anchor provenance mismatch')
            dest = Path(old['copy']['path']).resolve()
            if not dest.is_relative_to((ROOT / '.local-work/savegames/manual-S0-S7C').resolve()):
                raise ValueError('Historical copy outside archive')
            sample_id = old['sample_id']
        else:
            dest = ARCHIVE / name
            with source.open('rb') as src, dest.open('xb') as dst:
                while chunk := src.read(1024 * 1024):
                    dst.write(chunk)
            sample_id = f'SOR-SAMPLE-{22+index:04}'
        copied, after = metadata(dest), metadata(source)
        if (len({before['sha256'], copied['sha256'], after['sha256']}) != 1 or
                len({before['size'], copied['size'], after['size']}) != 1 or
                before['mtime_ns'] != after['mtime_ns']):
            raise ValueError(f'Copy/preservation failure: {label}')
        samples.append(dict(label=label, sample_id=sample_id, description=description,
                            filename=name, classification=classifications[index],
                            source_before=before, copy=copied, source_after=after, verified=True))
    write_json(OUT / 'manifest.json', dict(samples=samples, python=sys.version,
        executable=sys.executable, executable_sha256=file_sha(Path(sys.executable)),
        zlib_runtime=zlib.ZLIB_RUNTIME_VERSION,
        prior_manifest_sha256=file_sha(PRIOR / 'manifest.json'),
        preregistration_sha256=file_sha(OUT / 'preregistration.json')))
    print('All seven source/copy/source checks passed; L0 archive reused.', flush=True)
    return samples


def analyze(samples, out):
    out.mkdir(exist_ok=False)
    data, partitions, entries = {}, {}, []
    for sample in samples:
        label = sample['label']
        compressed = Path(sample['copy']['path']).read_bytes()
        if sha(compressed) != sample['copy']['sha256']:
            raise ValueError('Copy changed before analysis')
        raw, chunks = decode(compressed)
        with (out / f'{label}.decoded.bin').open('xb') as stream:
            stream.write(raw)
        if label == 'L0':
            prior_analysis = json.loads((PRIOR / 'analysis-01/analysis.json').read_text())
            old = next(x for x in prior_analysis['samples'] if x['label'] == 'S4C')
            if sha(raw) != old['decoded_sha256']:
                raise ValueError('Historical decoded anchor mismatch')
        data[label], partitions[label] = raw, regions(raw)
        candidates = {}
        for role, signature in MAIN.items():
            offsets = hits(raw, bytes.fromhex(signature))
            candidates[role] = dict(main_offsets=offsets,
                token_offsets=hits(raw, bytes.fromhex(TOKENS[role])),
                window_512_sha256=[sha(raw[pos:pos+512]) for pos in offsets])
        motifs = hits(raw, LINK)
        entry = dict(label=label, decoded_size=len(raw), decoded_sha256=sha(raw),
            chunks=chunks, candidates=candidates, motif_offsets=motifs,
            build_string_offsets=hits(raw, b'1.16.244.0'),
            motif_state='PRESENT' if motifs else 'ABSENT')
        entries.append(entry)
        print(label, entry['motif_state'], motifs,
              {k: v['main_offsets'] for k, v in candidates.items()}, flush=True)
    transitions = []
    for i in range(6):
        a, b = samples[i]['label'], samples[i+1]['label']
        result = compare(data[a], data[b], partitions[a], partitions[b])
        result.update(before=a, after=b,
            classification=['CROSS_SESSION_RELOAD_ELAPSED_TIME', 'UNLINK_ACTION',
                            'UNLINKED_CONTROL', 'RELINK_ACTION', 'RELINKED_CONTROL',
                            'INCIDENTAL_TERMINAL'][i],
            seconds=(samples[i+1]['source_before']['mtime_ns'] - samples[i]['source_before']['mtime_ns'])/1e9,
            file_delta=samples[i+1]['copy']['size']-samples[i]['copy']['size'],
            decoded_delta=len(data[b])-len(data[a]))
        transitions.append(result)
        print(a, b, result['region_count'], result['after_unmatched_bytes'], flush=True)
    write_json(out / 'analysis.json', dict(samples=entries, transitions=transitions,
        manifest_sha256=file_sha(OUT / 'manifest.json'), script_sha256=file_sha(Path(__file__))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', help='Analyze existing manifest into a fresh run directory; no recopy')
    args = parser.parse_args()
    if args.run and not re.fullmatch(r'[a-zA-Z0-9_-]+', args.run):
        raise ValueError('Simple run name required')
    samples = json.loads((OUT / 'manifest.json').read_text())['samples'] if args.run else archive()
    analyze(samples, OUT / (args.run or 'analysis-01'))


if __name__ == '__main__':
    main()
