#!/usr/bin/env python3

import unittest

import numpy as np
import tinie.systems.central_region.itp2d_center as ctr
import tinie.systems.couplings.overlap_coupling as cpl
import tinie.systems.leads.finite_harmonic_lead as ld
from mpi4py import MPI
from tinie.systems.read_write.system_read import SystemRead
from tinie.systems.read_write.system_write import SystemWrite

filepath_ctr = "tinie/test_files/itp2d_test.h5"
filepath_dump = "tinie/test_files/tinie_prepare_test.h5"

# Set up the test system
center = ctr.Itp2dCenter(filepath_ctr, (0, 4))
lead_left = ld.FiniteHarmonicLead(
    [-10.0, -4.0], [-5.0, 5.0], [0.0, 1.0], 1.0, "left")
coupling_left = cpl.OverlapCoupling(center, lead_left, MPI.COMM_WORLD)

# Initialize the system calculator...
system_dump = SystemWrite(MPI.COMM_WORLD)
system_dump.add_central_region(center)
system_dump.add_coupling_region(coupling_left)

# Now, we initialize the SystemRead for the test file, that contains the
# same information:
system_fetch = SystemRead(MPI.COMM_WORLD)
system_fetch.set_file_path(filepath_dump)


class TestSystemRead(unittest.TestCase):
    def test_region_number(self):
        """Testing that the numbers of regions are correct"""

        np.testing.assert_equal(system_fetch.get_num_leads(), 1)

    def test_center_hamiltonian(self):
        """Testing retrieval of central region Hamiltonian"""

        np.testing.assert_equal(
            system_fetch.get_center_energies(),
            system_dump.get_center_energies())

    def test_center_potential(self):
        """Testing retrieval of central region potential"""

        x, y = center.get_coordinate_ranges()
        exact_potential = np.array(
            [[0.5 * (xp ** 2 + yp ** 2) for yp in y] for xp in x]
        )

        np.testing.assert_equal(
            system_fetch.get_center_potential(),
            exact_potential)

    def test_lead_hamiltonian(self):
        """Testing retrieval of lead region Hamiltonian"""

        np.testing.assert_equal(
            system_fetch.get_lead_energies(0), system_dump.get_lead_energies(0)
        )

    def test_coupling_matrix(self):
        """Testing retrieval of the coupling matrix"""

        np.testing.assert_almost_equal(
            system_fetch.get_center_lead_coupling_mat(0),
            system_dump.get_center_lead_coupling_mat(0),
        )
