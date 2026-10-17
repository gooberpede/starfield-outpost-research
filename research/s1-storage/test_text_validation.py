# SPDX-License-Identifier: GPL-3.0-or-later
"""Text-only regression tests; no game/save/native reads, writes or dependencies.
Run CPython -B -m unittest discover -s research/s1-storage -p test_text_validation.py.
"""
import unittest
from text_validation import validate_text, validate_authored


class TextValidationTests(unittest.TestCase):
    def test_valid_unicode(self):
        for text in ('ASCII', 'C \u2212 W', '41 \u00d7 1.8', 'caf\u00e9', '\u2014 \u2013 \u2019', '\u65e5\u672c\u8a9e'):
            self.assertEqual(validate_text(text.encode('utf8')), text)

    def test_wrong_decodings(self):
        for symbol in ('\u2212', '\u00d7', '\u2014', '\u2013', '\u2019', '\ufeff', '\U0001f600'):
            for encoding in ('cp1252', 'latin1'):
                try:
                    bad = symbol.encode('utf8').decode(encoding).encode('utf8')
                except UnicodeDecodeError:
                    continue
                with self.subTest(symbol=ascii(symbol), encoding=encoding):
                    with self.assertRaises(ValueError):
                        validate_text(bad)

    def test_observed_sequences(self):
        for bad in ('\u00e2\u02c6\u2019', '\u00c3\u2014'):
            with self.assertRaisesRegex(ValueError, 'suspected mojibake'):
                validate_text(bad.encode('utf8'))

    def test_invalid_utf8(self):
        with self.assertRaises(UnicodeDecodeError):
            validate_text(b'\xff')

    def test_bom_and_replacement(self):
        for bad in ('\ufefftext', 'text\ufffd', 'text\u0085'):
            with self.assertRaises(ValueError):
                validate_text(bad.encode('utf8'))

    def test_tracked_additions(self):
        for bad in ('\u00e2\u02c6\u2019', '\u00c3\u2014', '\u0085', '\ufffd'):
            with self.assertRaises(ValueError):
                validate_authored(('old\nadded ' + bad).encode('utf8'), 'tracked', b'old\n')

    def test_unchanged_legacy_is_excluded(self):
        prior = 'legacy \u00e2\u02c6\u2019\n'.encode('utf8')
        validate_authored(prior + 'new \u2212 \u00d7\n'.encode('utf8'), 'tracked', prior)


if __name__ == '__main__':
    unittest.main()
