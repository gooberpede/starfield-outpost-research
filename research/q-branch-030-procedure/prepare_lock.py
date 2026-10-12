# SPDX-License-Identifier: GPL-3.0-or-later
"""Read immutable local receipts/artifacts; write one exclusive ignored lock.
No build, downloads, process handle, installation, save edit or native execution.
"""
import argparse
import hashlib
import struct
from pathlib import Path
from procedure import ROOT,read,write,sha,pins,archive_check

BUILD_SHA='6bdadc78ebfe1552adae913bb75cd5c0d54fc44ab4a5a4d12eb2bb4742b222f7'
PAIRS=[(0xad0c36,0xf4ab80),(0xad0d36,0x96f5c0),(0xad93fa,0xad08d0),
       (0xad0ab5,0xb1e190),(0xad08f2,0xad5760),(0xad0903,0x5de3b0),
       (0xad092c,0xaccad0),(0xad0976,0x96efb0),(0xad0986,0x96fb40),
       (0xad0ae5,0x96eb90),(0xad0b08,0x96f940)]

def prepare(output):
    buildpath=ROOT/'.local-work/native-oracle-030/builds/qualification-02/build.json'
    if sha(buildpath)!=BUILD_SHA:raise ValueError('unreviewed_build_receipt')
    build=read(buildpath);base=buildpath.parent
    baseline=read(ROOT/'.local-work/q-branch-030-procedure/baseline.json')
    locked=dict(baseline['protected'])
    def pin(path,expected=None):
        path=Path(path).resolve(strict=True);actual=sha(path)
        if expected and actual!=expected:raise ValueError('pin_mismatch:'+str(path))
        locked[str(path)]=actual
    for n,s in build['sources'].items():pin(ROOT/n,s)
    for n,s in build['protected'].items():pin(n,s)
    pin(buildpath,BUILD_SHA);pin(base/'SorNativePositionOracle-0.3.0.zip',build['zip_sha256'])
    pin(base/'SorNativePositionOracle.dll',build['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256'])
    pin(ROOT/'.local-work/q-branch-030-procedure/release-lock-02.json','16dad23320df928e63e0c7a1ffc9d00c5b65ae0008d4270f0a14173c3c164e5f')
    # ZIP is the authoritative package; do not assume a separately extracted tree.
    import zipfile
    with zipfile.ZipFile(base/'SorNativePositionOracle-0.3.0.zip') as z:
        for n,item in build['files'].items():
            if hashlib.sha256(z.read(n)).hexdigest()!=item['sha256']:raise ValueError('package_pin')
    pin(build['sfse_path'],build['sfse_hash'])
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    loader={'sfse_1_16_244.dll':build['sfse_hash'],'sfse_loader.exe':'16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526'}
    for n,s in loader.items():pin(game/n,s)
    manifest=ROOT/'.local-work/native-oracle-020/operations/continuation-live-evidence-manifest-01.json'
    pin(manifest)
    for row in read(manifest)['files']:pin(ROOT/row['path'],row['sha256'])
    attempt=ROOT/'.local-work/q-branch-030-procedure/live-20261012T043048Z-41899f5124cc4e4cac16ee0687ea2182/final-evidence-manifest.json'
    pin(attempt)
    for row in read(attempt)['files']:pin(row['path'],row['sha256'])
    pin(ROOT/'docs/implementation-briefs/CODEX_BRIEF_SOR_Q030_external_module_inventory_fix.md')
    save=Path('C:/Users/User/Documents/My Games/Starfield/Saves')
    for filename,expected in [
        ('Save27_D6036588M417474696C61204B6972616C79_000252_20261012011118_4_0_4.sfs','9615df728ab073bd24661fdc8abc65e0d0196b5abe532ab1b611bbe7ef7fc66c'),
        ('Save28_D6036588M417474696C61204B6972616C79_000258_20261012011827_4_0_4.sfs','7360ce427b2a51aa94efb776d09dfaa30654c44ba08c60259b52c639cde2a35c')]:
        pin(save/filename,expected);pin(ROOT/'.local-work/q-to-e/saved-correspondence-04'/filename,expected)
    for n in ['.local-work/recon/durable-center-04.tsv','.local-work/recon/engine-oracle-04.tsv',
              '.local-work/q-to-e/saved-correspondence-04/receipt.json',
              'docs/implementation-briefs/CODEX_BRIEF_SOR_Q_branch_030_live_acquisition_procedure.md']:
        pin(ROOT/n)
    for p in Path(__file__).parent.glob('*.py'):pin(p)
    for n in ['qualification.txt','branch-qualification.txt','inspection-tests.txt','branch-inspection-tests.txt','branch-decoder-qualification.txt']:
        pin(base/n)
    data=(game/'Starfield.exe').read_bytes()
    import sys
    sys.path.insert(0,str(ROOT/'research/exp0002'))
    from prepare import pe_layout,file_offset
    _,_,sections=pe_layout(data)
    calls=[]
    for rva,target in PAIRS:
        off=file_offset(sections,rva,5);raw=data[off:off+5]
        if raw[0]!=0xe8 or rva+5+struct.unpack_from('<i',raw,1)[0]!=target:raise ValueError('original_call_target')
        calls.append(dict(rva=rva,sha256=hashlib.sha256(raw).hexdigest(),target_rva=target))
    lock=dict(version='0.3.0',schema=3,module_inventory_source='UNCHANGED_030_WORKER_COOPERATIVE_INVENTORY',pins=locked,zip=str(base/'SorNativePositionOracle-0.3.0.zip'),
              package={n:v['sha256'] for n,v in build['files'].items()},game_dir=str(game),save_dir=str(save),
              live_root=str(ROOT/'.local-work/native-oracle-live'),installed_loader=loader,calls=calls,
              dll_sha256=build['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256'],
              game_sha256=build['game_hash'],sfse_sha256=build['sfse_hash'],
              schema_sha256=build['sources']['runtime/native-oracle-030/schema.md'],build_sha256=BUILD_SHA)
    pins(lock);archive_check(lock);write(output,lock)
    print(str(output));print(sha(output));print('pins',len(locked))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    prepare(p.parse_args().output)
