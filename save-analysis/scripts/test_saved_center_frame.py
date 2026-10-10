"""SPDX-License-Identifier: GPL-3.0-or-later
Independent boundary/control expectations for EXP0020 saved-frame arithmetic.
"""
import unittest
from audit_saved_center_frame import selected_grid


class SavedCenterFrameTests(unittest.TestCase):
    def test_control_origin_frame(self):
        r = selected_grid((1,10464,21120), (1,10467,21144), 0x0b,
                          (356.8204040527344,2459.05859375,-31.89084243774414))
        self.assertEqual((r['tag'],r['x'],r['y']), (1,10467,21144))
        self.assertEqual(r['residual_x'],56.820404052734375)
        self.assertEqual(r['residual_y'],59.05859375)

    def test_site_frame_does_not_add_origin_twice(self):
        r = selected_grid((0,27168,36000), (0,27165,35995), 0x2b, (12,34,56))
        self.assertEqual((r['x'],r['y']), (27165,35995))

    def test_negative_floor(self):
        r = selected_grid((0,13152,45120), (0,13152,45120), 0x2b,
                          (-53.4358024597168,58.03339767456055,8.46107006072998))
        self.assertEqual((r['x'],r['y']), (13151,45120))
        self.assertAlmostEqual(r['residual_x'],46.5641975402832)

    def test_seam_and_disabled(self):
        r = selected_grid((0,0,0), (0,0,0), 0x2b, (-1,-1,999))
        self.assertEqual((r['tag'],r['x'],r['y']), (2,49151,49151))
        with self.assertRaisesRegex(ValueError,'DISABLED'):
            selected_grid((0,0,0), None, 0x3b, (0,0,0))
        with self.assertRaisesRegex(ValueError,'MISSING'):
            selected_grid((0,0,0), None, 0x2b, (0,0,0))
        with self.assertRaisesRegex(ValueError,'UNQUALIFIED'):
            selected_grid((0,0,0), None, 0x01, (0,0,0))


if __name__ == '__main__':
    unittest.main()
