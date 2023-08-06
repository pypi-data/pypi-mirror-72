#!/usr/bin/env python3

import unittest

import numpy as np
from tinie.systems.leads.custom_lead import CustomLead

filename = "tinie/test_files/custom_lead_test.npy"


class TestCustomLead(unittest.TestCase):
    def test_init(self):
        """Testing custom lead initialization"""

        ld = CustomLead(None, None, None, None, filename)

    def test_get_energies(self):
        """Testing correctness of retrieved eigenenergies"""

        ld = CustomLead(None, None, None, None, filename)
        H = ld.get_energies()
        H_anal = np.array([0.5, 1.0, 1.5])

        np.testing.assert_equal(H, H_anal)
