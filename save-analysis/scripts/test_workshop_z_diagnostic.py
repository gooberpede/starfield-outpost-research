"""Independent scalar fixtures; synthetic restoration branches are not oracles."""
import struct
import unittest

from workshop_z_diagnostic import (center_z, convert_z, initial_load_z, prepared_z,
                                   restore_from_saved)


class ScalarContracts(unittest.TestCase):
    def test_genuine_native_centers(self):
        # 0.5.0 raw center observations 96 and112; captured compensation zero.
        for bits in ('54296940', '404318c1'):
            z = struct.unpack('<f', bytes.fromhex(bits))[0]
            self.assertEqual(center_z(z, (0, 0, 0))['z_hex'], bits)

    def test_relocation_control(self):
        # Independent earlier moved SOR003 reference/delta and pre-move center.
        z = struct.unpack('<f', bytes.fromhex('37db0cc2'))[0]
        d = struct.unpack('<f', bytes.fromhex('e0af5440'))[0]
        self.assertEqual(center_z(z, (18.966949462890625, 52.639892578125, d))['z_hex'],
                         '7220ffc1')

    def test_conversion_transition(self):
        self.assertEqual(convert_z(8, 0xa0, True, -3)['z'], 5)
        self.assertEqual(convert_z(8, 0xa2, False, 3)['flag_byte'], 0xa0)
        self.assertEqual(convert_z(8, 0xa2, True)['z'], 8)
        self.assertFalse(convert_z(8, 0xa2, True)['transitioned'])

    def test_missing_operands(self):
        self.assertEqual(convert_z(8, None, True, 3)['status'], 'UNKNOWN')
        self.assertEqual(convert_z(8, 0, True)['status'], 'UNKNOWN')
        self.assertEqual(prepared_z(8, True)['status'], 'UNKNOWN')
        self.assertEqual(prepared_z(8, None, 3)['status'], 'UNKNOWN')
        self.assertEqual(center_z(None, (0, 0, 0))['status'], 'UNKNOWN')
        self.assertEqual(center_z(1, (None, 0, 0))['status'], 'UNKNOWN')
        for z in (18.352506637573242, -31.89084243774414):
            self.assertEqual(restore_from_saved(z, {'fitted': 1})['status'], 'UNKNOWN')

    def test_preparation_branches(self):
        self.assertEqual(prepared_z(8, False)['z'], 8)
        self.assertEqual(prepared_z(8, True, 3)['z'], 5)

    def test_saved_frame_variants(self):
        self.assertEqual(initial_load_z(8, 0x0b)['z'], 8)
        self.assertEqual(initial_load_z(8, 0x2b)['status'], 'UNKNOWN')
        self.assertEqual(initial_load_z(8, 0x2b, -3)['z'], 5)
        self.assertEqual(initial_load_z(8, None)['status'], 'UNKNOWN')
        with self.assertRaises(ValueError):
            initial_load_z(8, 0x1b)

    def test_binary32_order_and_zero(self):
        # Ties-to-even at 2**24: adding1 rounds away before next operation.
        first = convert_z(16777216, 0, True, 1)['z']
        self.assertEqual(convert_z(first, 2, False, -16777216)['z'], 0)
        self.assertEqual(center_z(-0.0, (0, 0, 0))['z_hex'], '00000080')
        self.assertEqual(center_z(-0.0, (1, 0, 0))['z_hex'], '00000000')

    def test_unqualified_domain(self):
        for z in (float('nan'), float('inf'), 2**-149, 1e100):
            with self.assertRaises(ValueError):
                center_z(z, (0, 0, 0))
        with self.assertRaises(ValueError):
            convert_z(1, 0, 1, 2)


if __name__ == '__main__':
    unittest.main()
