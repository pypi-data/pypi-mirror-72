import unittest

import tinie.systems.central_region.itp2d_center as ctr
import tinie.systems.couplings.tight_binding_coupling as cpl
import tinie.systems.leads.finite_harmonic_lead as ld
from mpi4py import MPI

FILEPATH_SMALL = "tinie/test_files/lil_itp2d_test.h5"
FILEPATH_BIG = "tinie/test_files/big_itp2d_test.h5"


class TestTightBindingCoupling(unittest.TestCase):
    def test_small_grid_coupling(self):
        """Testing coupling value calculation on a small grid"""

        center = ctr.Itp2dCenter(FILEPATH_SMALL, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-20.0, -7.0], [-5.0, 5.0], [0.0, 5.0], 1.0, "left"
        )
        coupling = cpl.TightBindingCoupling(center, lead, MPI.COMM_WORLD)

    def test_big_grid_coupling(self):
        """Testing coupling value calculation on a bigger grid"""

        center = ctr.Itp2dCenter(FILEPATH_BIG, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-10.0, -7.0], [-5.0, 5.0], [0.0, 5.0], 1.0, "left"
        )
        coupling = cpl.TightBindingCoupling(center, lead, MPI.COMM_WORLD)
