#!/usr/bin/env python3

import unittest

import tinie.systems.central_region.itp2d_center as ctr
import tinie.systems.couplings.overlap_coupling as cpl
import tinie.systems.leads.finite_harmonic_lead as ld
from mpi4py import MPI
from tinie.systems.read_write.system_write import SystemWrite

filepath = "tinie/test_files/itp2d_test.h5"

# Set up the test system
center = ctr.Itp2dCenter(filepath, (0, 4))
lead_left = ld.FiniteHarmonicLead(
    [-10.0, -4.0], [-5.0, 5.0], [0.0, 1.0], 1.0, "left")
lead_right = ld.FiniteHarmonicLead(
    [4.0, 10.0], [-5.0, 5.0], [0.0, 1.0], 1.0, "right")
coupling_left = cpl.OverlapCoupling(center, lead_left, MPI.COMM_WORLD)
coupling_right = cpl.OverlapCoupling(center, lead_right, MPI.COMM_WORLD)

# Initialize the system calculator
system = SystemWrite(MPI.COMM_WORLD)
system.add_central_region(center)
system.add_coupling_region(coupling_left)
system.add_coupling_region(coupling_right)


class TestSystemWrite(unittest.TestCase):
    def test_system_central_region(self):
        """Testing proper initialization of the central region of a system"""

        assert system.center == center

    def test_system_lead_region(self):
        """Testing proper initialization of the lead region of a system"""

        assert system.get_num_leads() == 2
        assert system.couplings[0].Lead_object == lead_left
        assert system.couplings[1].Lead_object == lead_right

    def test_system_coupling_region(self):
        """Testing proper initialization of the coupling region of a system"""

        assert system.couplings[0] == coupling_left
        assert system.couplings[1] == coupling_right
