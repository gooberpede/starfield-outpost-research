# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic regression fixtures; no raw evidence or file writes."""
import json
from pathlib import Path
import unittest
import screen

class Screening(unittest.TestCase):
    def test_defects(self):
        fixtures=json.loads(Path(__file__).with_name('fixtures.json').read_text(encoding='utf8'))
        for text,rule in fixtures['defective']:
            with self.subTest(text=text):self.assertIn(rule,[r for r,_ in screen.line_rules(text)])

    def test_valid(self):
        fixtures=json.loads(Path(__file__).with_name('fixtures.json').read_text(encoding='utf8'))
        for text in fixtures['valid']:
            with self.subTest(text=text):self.assertEqual(screen.line_rules(text),[])

    def test_changed_lines_only(self):
        self.assertEqual(screen.scan(Path('x.md'),'all1296calls\nReadable prose.\n',{2}),[])

    def test_suppression_requires_reason(self):
        text='all1296calls <!-- editorial: allow JOINED_PROSE -- quoted defect fixture -->'
        self.assertEqual(screen.scan(Path('x.md'),text),[])
        self.assertTrue(screen.scan(Path('x.md'),'all1296calls <!-- editorial: allow JOINED_PROSE -->'))

    def test_local_link(self):
        self.assertEqual(screen.scan(Path('x.md'),'See [proof](never-created-file.md).')[0]['rule'],'LOCAL_LINK')

    def test_fences(self):
        self.assertEqual(screen.scan(Path('x.md'),'```text\nall1296calls\n```\n'),[])
        self.assertEqual(screen.scan(Path('x.md'),'```\n')[0]['rule'],'MARKDOWN_FENCE')

    def test_python_explanations(self):
        text='"""Readable prose."""\nx="all1296calls"\n# all1296calls\n'
        self.assertEqual([d['line'] for d in screen.scan(Path('x.py'),text)],[3])

    def test_csv_structure_and_labels(self):
        text='source_id,path,sha256,role\nC1H-S01,docs/foo.md,abc123,Readable role\n'
        self.assertEqual(screen.scan(Path('x.csv'),text),[])
        bad='source_id,role\nC1H-S01,all1296calls\n'
        self.assertEqual(screen.scan(Path('x.csv'),bad)[0]['rule'],'JOINED_PROSE')
        self.assertEqual(screen.scan(Path('x.csv'),bad)[0]['line'],2)

if __name__=='__main__':unittest.main()
