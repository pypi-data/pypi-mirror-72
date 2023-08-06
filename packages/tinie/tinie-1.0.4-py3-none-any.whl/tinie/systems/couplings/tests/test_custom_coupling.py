#!/usr/bin/env python3

import unittest

import numpy as np
from mpi4py import MPI
from tinie.systems.central_region.custom_center import CustomCenter
from tinie.systems.couplings.custom_coupling import CustomCoupling
from tinie.systems.leads.custom_lead import CustomLead

filename_ctr = "tinie/test_files/custom_center_test.npy"
filename_ld = "tinie/test_files/custom_lead_test.npy"
filename_cpl = "tinie/test_files/custom_coupling_test.npy"


class TestCustomCoupling(unittest.TestCase):
    def test_init(self):
        """Testing custom coupling initialization"""

        ctr = CustomCenter(filename_ctr)
        ld = CustomLead(None, None, None, None, filename_ld)
        cpl = CustomCoupling(ctr, ld, filename_cpl, MPI.COMM_WORLD)

    def test_get_coupling_matrix(self):
        """Testing correctness of retrieved coupling matrix"""

        ctr = CustomCenter(filename_ctr)
        ld = CustomLead(None, None, None, None, filename_ld)
        cpl = CustomCoupling(ctr, ld, filename_cpl, MPI.COMM_WORLD)
        V = cpl.get_coupling_matrix()
        V_anal = np.array(
            [
                [0.1, 0.2j, 0.1 + 0.2j, 0.2j, 0.1],
                [0.5, 0.3 + 0.01j, 0.7j, 0.8, 0.1],
                [0.3, 0.3, 0.3, 0.3, 0.3j],
            ]
        )

        np.testing.assert_equal(V, V_anal)
