# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.

import unittest

import numpy as np

from ..utils import (
    unpack_mono_xx_p, unpack_mono10_p, unpack_mono12_p, unpack_mono12_packed
)


class Utils_TestCase(unittest.TestCase):
    def test_unpack_mono12packed(self):
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

        packed_data[:] = (0, 0, 0x0F)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0, 0x0F0))

        packed_data[:] = (0, 0, 0xF0)
        unpacked_data = np.frombuffer(
            unpack_mono12_packed(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0, 0xF00))

    def test_unpack_mono12p(self):
        packed_data = np.zeros((3,), dtype=np.uint8)

        packed_data[:] = (0xBC, 0xFA, 0xDE)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0xABC, 0xDEF))

        packed_data[:] = (0x0F, 0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0x00F, 0))

        packed_data[:] = (0xF0, 0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0x0F0, 0))

        packed_data[:] = (0, 0x0F, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0xF00, 0))

        packed_data[:] = (0, 0xF0, 0)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0, 0x00F))

        packed_data[:] = (0, 0, 0x0F)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0, 0x0F0))

        packed_data[:] = (0, 0, 0xF0)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0, 0xF00))

        packed_data = np.zeros((5,), dtype=np.uint8)

        packed_data[:] = (0xBC, 0xFA, 0xDE, 0x23, 0x01)
        unpacked_data = np.frombuffer(
            unpack_mono12_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(tuple(unpacked_data), (0xABC, 0xDEF, 0x123))

    def test_unpack_mono10p(self):
        packed_data = np.zeros((5,), dtype=np.uint8)

        packed_data[:] = (0xAB, 0xCD, 0xEF, 0x0A, 0xBC)
        unpacked_data = np.frombuffer(
            unpack_mono10_p(packed_data), dtype=np.uint16)
        self.assertTupleEqual(
            tuple(unpacked_data), (0x1AB, 0x3F3, 0x0AE, 0x2F0))

    def test_unpack_mono_xx_p(self):
        packed_data = np.zeros((3,), dtype=np.uint8)

        with self.assertRaises(ValueError):
            unpack_mono_xx_p(packed_data, 8)

        with self.assertRaises(ValueError):
            unpack_mono_xx_p(packed_data, 16)


if __name__ == '__main__':
    unittest.main()
