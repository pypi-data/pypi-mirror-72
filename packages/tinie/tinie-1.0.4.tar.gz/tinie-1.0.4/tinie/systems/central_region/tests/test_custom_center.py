#!/usr/bin/env python3

import unittest

import numpy as np
from tinie.systems.central_region.custom_center import CustomCenter

filename = "tinie/test_files/custom_center_test.npy"


class TestCustomCenter(unittest.TestCase):
    def test_init(self):
        """Testing custom central region initialization"""

        ctr = CustomCenter(filename)

    def test_get_energies(self):
        """Testing correctness of retrieved eigenenergies"""

        ctr = CustomCenter(filename)
        H = ctr.get_energies()
        H_anal = np.array([1.0, 2.0, 2.0, 3.0, 3.0])

        np.testing.assert_equal(H, H_anal)

    def test_get_potential(self):
        """Testing correctness of retrieved potnetial"""

        ctr = CustomCenter(filename)
        V = ctr.get_potential()
        V_anal = 0.0

        np.testing.assert_equal(V, V_anal)
