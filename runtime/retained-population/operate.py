# SPDX-License-Identifier: GPL-3.0-or-later
"""Phase B proposal helpers. No installation, launch, attachment or removal.

Preflight/postflight read installed inputs, archives and protected namespaces and
write new task receipts/copies through protect.py. READY writes only a nonce
request in the exact observer session after an explicit authorization receipt.
Requires CPython stdlib, retained owned preservation evidence and Windows process
metadata access. Never edits Vortex, game files, saves, configuration or Git.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
from build import ROOT, SRC, LOCAL, GAME, sha, guard, GAME_HASH, SFSE_HASH
from read_capture import inspect

DEPLOYED=GAME/'Data/SFSE/Plugins/SorRetainedPopulation.dll'
VORTEX=Path('C:/Users/User/AppData/Roaming/Vortex/starfield/mods')
CARD=ROOT/'docs/experiments/resource-retained-population/run-card-d5p-v1.md'


def write(path,value):
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n')


def package(build):
    manifest=json.loads((build/'build.json').read_text())
    assert manifest.get('schema')=='sor-d5p-build/1', 'Historical v1 operations do not authorize R1 schema 2'
    deployment=json.loads((build/'package.json').read_text())
    assert sha(build/'build.json')==deployment['build_sha256']
    assert sha(build/'qualification.json')==deployment['qualification_sha256']
    assert sha(deployment['zip'])==deployment['zip_sha256']
    assert sha(build/'SorRetainedPopulation.dll')==deployment['dll_sha256']==manifest['dll_sha256']
    assert all(sha(p)==h for p,h in manifest['sources'].items())
    return manifest,deployment


def absence():
    # Metadata query only. No process access with intervention rights.
    r=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process Starfield -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True,check=True)
    return r.stdout.strip()=='0'


def inventory():
    paths=list((GAME/'Data/SFSE/Plugins').glob('*RetainedPopulation*.dll'))
    paths+=list(VORTEX.glob('*/Data/SFSE/Plugins/*RetainedPopulation*.dll'))
    paths+=list(VORTEX.glob('*/SFSE/Plugins/*RetainedPopulation*.dll'))
    return {str(p):sha(p) for p in paths if p.is_file()}


def session_closed(session):
    return any((session/n).exists() for n in ('terminal.json','not-ready.json','worker-exception.json','STOP'))


def preserve(label):
    subprocess.run([sys.executable,'-B',str(SRC/'protect.py'),label],check=True)
    return json.loads((LOCAL/label/'protection.json').read_text())


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=('preflight','ready','postflight'))
    p.add_argument('--build',type=Path,required=True);p.add_argument('--name',required=True)
    p.add_argument('--session',type=Path);p.add_argument('--authorization',type=Path)
    p.add_argument('--preflight',type=Path);p.add_argument('--profile')
    a=p.parse_args();assert a.name.isascii() and a.name.replace('-','').isalnum()
    build=a.build.resolve();assert build.is_relative_to(LOCAL)
    manifest,deployment=package(build);free=guard()
    out=LOCAL/(a.name+'.json')
    if a.mode=='preflight':
        assert absence(),'Game must be absent during offline preflight'
        assert a.profile,'Record intended Vortex profile, to be confirmed by maintainer'
        protected=preserve(a.name+'-protection')
        write(out,dict(schema='sor-d5p-preflight/1',authority='NOT_AUTHORIZED',build=str(build),
                       package=deployment,protection=protected,existing_plugins=inventory(),
                       intended_profile=a.profile,profile_verification='REQUIRES_OPERATOR_CONFIRMATION',
                       card_sha256=sha(CARD),free=free))
    elif a.mode=='ready':
        assert a.authorization and a.session
        auth=json.loads(a.authorization.read_text())
        assert auth['phase']=='B' and auth['explicit_go'] is True and auth['steam_cloud_disabled'] is True
        assert auth['package_sha256']==deployment['zip_sha256'] and auth['card_sha256']==sha(CARD)
        session=a.session.resolve();assert session.is_relative_to(LOCAL/'live')
        for ancestor in (session,*session.parents):assert not ancestor.lstat().st_file_attributes & 0x400
        identity=json.loads((session/'identity.json').read_text());ready=json.loads((session/'ready.json').read_text())
        assert not identity.get('fixture') and identity['game_sha256']==GAME_HASH and identity['sfse_sha256']==SFSE_HASH
        assert identity['dll_sha256']==deployment['dll_sha256'] and all(ready[k]==v for k,v in identity.items())
        assert ready['ready'] is True and ready['hooks']==11 and sha(DEPLOYED)==deployment['dll_sha256']
        pid=int(identity['pid'])
        result=subprocess.run(['powershell','-NoProfile','-Command',f'(Get-Process -Id {pid} -ErrorAction Stop).StartTime.ToUniversalTime().ToFileTimeUtc()'],capture_output=True,text=True,check=True)
        assert int(result.stdout.strip())==identity['creation_filetime']
        nonce=uuid.uuid4().hex;temp=session/(nonce+'.request.tmp');temp.write_text(nonce,encoding='ascii')
        os.replace(temp,session/'request.txt')
        ack=session/('ack-'+nonce+'.json')
        # This command has no experiment deadline. Operator STOP or worker
        # failure ends the wait; a delayed operator is not a failed experiment.
        while not ack.exists():
            assert not session_closed(session)
            guard();time.sleep(0.2)
        receipt=json.loads(ack.read_text());assert all(receipt[k]==v for k,v in identity.items())
        assert not session_closed(session),'Session closed before READY admission'
        assert receipt['nonce']==nonce and receipt['hooks_intact'] is True
        assert receipt['capture_active'] is True and receipt['drops']==0
        evidence=inspect(session,deployment['dll_sha256'])
        assert not evidence['errors'] and evidence['independently_verified_durable_records']>=receipt['flushed']
        assert not session_closed(session),'Session closed during READY verification'
        write(out,dict(status='READY_AT_FRESH_ACK',identity=identity,nonce=nonce,ack_sha256=sha(ack),
                       authority_receipt_sha256=sha(a.authorization),evidence=evidence,free=guard()))
    else:
        assert absence(),'Postflight requires target exit; never terminates it'
        assert a.preflight
        before=json.loads(a.preflight.read_text());after=preserve(a.name+'-protection')
        fields=('save_policy_sha256','protected_live','save52','backups','definitions','config','installed','restore_rehearsal_sha256')
        checks={k:before['protection'][k]==after[k] for k in fields}
        residue=inventory();assert not residue,'Maintainer must remove/disable residue in Vortex; Codex must not delete it'
        if a.session:
            capture=inspect(a.session.resolve(),deployment['dll_sha256'])
        else:capture=None
        write(out,dict(status='POSTFLIGHT_PASS' if all(checks.values()) else 'POSTFLIGHT_FAIL',checks=checks,
                       after=after,plugin_residue=residue,capture=capture,free=guard()))
        assert all(checks.values()),checks
    print(out)


if __name__=='__main__':main()
