# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline ZIP-byte regression checks; temporary files only, no deployment."""
import hashlib,tempfile,unittest,zipfile
from pathlib import Path
from build import ROOT,verify_package

class PackageTests(unittest.TestCase):
    def check(self,config,dll=b'synthetic DLL'):
        with tempfile.TemporaryDirectory(prefix='sor-package-') as d:
            path=Path(d)/'test.zip'
            with zipfile.ZipFile(path,'x') as z:
                z.writestr('Data/SFSE/Plugins/SorExp0002.config',config)
                z.writestr('Data/SFSE/Plugins/SorExp0002.dll',dll)
            verify_package(path,hashlib.sha256(b'synthetic DLL').hexdigest())
    def test_lf_roundtrip(self):
        self.check((str(ROOT/'.local-work/exp0002-live')+'\n').encode('utf-8'))
    def test_windows_crlf_rejected(self):
        with self.assertRaisesRegex(ValueError,'Config'):
            self.check((str(ROOT/'.local-work/exp0002-live')+'\r\n').encode('utf-8'))
    def test_different_path_rejected(self):
        with self.assertRaisesRegex(ValueError,'Config'):self.check(b'D:\\other\\exp0002-live\n')
    def test_changed_dll_rejected(self):
        with self.assertRaisesRegex(ValueError,'DLL'):
            self.check((str(ROOT/'.local-work/exp0002-live')+'\n').encode('utf-8'),b'changed')

if __name__=='__main__':unittest.main()
