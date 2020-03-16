import unittest

import numpy as np

from ..utils import unpack_mono12_packed


class Utils_TestCase(unittest.TestCase):
    def test_unpack_mono12(self):
        packed_data = np.zeros((3,), dtype=np.uint8)

        packed_data[:] = (0xAB, 0xFC, 0XDE)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0xABC, 0xDEF))

        packed_data[:] = (0, 0x0F, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0x00F, 0))

        packed_data[:] = (0x0F, 0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0x0F0, 0))

        packed_data[:] = (0xF0, 0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0xF00, 0))

        packed_data[:] = (0, 0xF0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0, 0x00F))

        packed_data[:] = (0x0F, 0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0x0F0, 0))

        packed_data[:] = (0xF0, 0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0xF00, 0))


if __name__ == '__main__':
    unittest.main()
