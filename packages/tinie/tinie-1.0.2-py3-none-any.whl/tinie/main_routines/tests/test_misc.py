#!/usr/bin/env python3

import unittest

import numpy as np
from tinie.main_routines.misc import fd


class TestMisc(unittest.TestCase):
    def test_fermi_dirac(self):
        """Testing Fermi-Dirac distribution implementation"""

        np.testing.assert_allclose(
            [
                fd(500, 1000),
                fd(1.0, 0.0),
                fd(-1.0, 0.0),
                fd(20, 38),
                fd(1, 100),
                fd(211, 673),
            ],
            [0.3775406688, 1.0, 0.0, 0.3713765808, 0.4975000208, 0.4222554032],
            rtol=1e-10,
        )
