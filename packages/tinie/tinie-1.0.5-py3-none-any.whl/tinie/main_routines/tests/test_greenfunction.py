#!/usr/bin/env python3

import unittest

import numpy as np
from tinie.main_routines.greenfunction import GreenFunction
from tinie.main_routines.selfenergy import SelfEnergy


class TestGreenFunction(unittest.TestCase):
    def test_inverse_retarded(self):
        """Testing correctness of the inverse retarded matrix"""

        # Setting up simple test system:
        HC = np.array([0.5, 1.5, 2.5])

        E1 = np.array([1.0, 2.0])
        E2 = np.array([3.0, 4.0, 5.0])

        V1 = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=np.complex128)
        V2 = np.array([[0.0, 1.0, 0.0], [1.0, 1.0j, 1.0], [
            0.0, 1.0, 0.0]], dtype=np.complex128)

        sigma1 = SelfEnergy(E1, V1, eta=1e-7)
        sigma2 = SelfEnergy(E2, V2, eta=1e-7)

        GF = GreenFunction(HC, [sigma1, sigma2])
        GF.set_omega(2.5)

        # Introducing the analytical value:
        Ginv_anal = np.array([[2.0 +
                               8.888888889e-8j, -
                               4.444444444e-8 +
                               0.6666666667j, 8.888888889e-8j, ], [4.444444444e-8 -
                                                                   0.6666666667j, 2.066666667 +
                                                                   8.604444444e-7j, 4.444444444e-8 -
                                                                   0.6666666667j, ], [8.888888889e-8j, -
                                                                                      4.444444444e-8 +
                                                                                      0.6666666667j, 8.888888889e-8j], ])

        np.testing.assert_almost_equal(GF._get_inverse_retarded(), Ginv_anal)

    def test_apply_retarded(self):
        """Testing whether retarded product solver works as intended"""

        # Setting up simple test system:
        HC = np.array([0.5, 1.5, 2.5])

        E1 = np.array([1.0, 2.0])
        E2 = np.array([3.0, 4.0, 5.0])

        V1 = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=np.complex128)
        V2 = np.array([[0.0, 1.0, 0.0], [1.0, 1.0j, 1.0], [
            0.0, 1.0, 0.0]], dtype=np.complex128)

        sigma1 = SelfEnergy(E1, V1, eta=1e-7)
        sigma2 = SelfEnergy(E2, V2, eta=1e-7)

        GF = GreenFunction(HC, [sigma1, sigma2])
        GF.set_omega(2.5)

        np.testing.assert_allclose(
            GF._get_inverse_retarded()
            @ GF.apply_retarded(GF.self_energies[0].get_gamma()),
            GF.self_energies[0].get_gamma(),
            rtol=1e-7,
            atol=1e-20,
        )

        np.testing.assert_allclose(
            GF._get_inverse_retarded()
            @ GF.apply_retarded(GF.self_energies[1].get_gamma()),
            GF.self_energies[1].get_gamma(),
            rtol=1e-7,
            atol=1e-20,
        )

    def test_apply_advanced(self):
        """Testing whether advanced product solver works as intended"""

        # Setting up simple test system:
        HC = np.array([0.5, 1.5, 2.5])

        E1 = np.array([1.0, 2.0])
        E2 = np.array([3.0, 4.0, 5.0])

        V1 = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=np.complex128)
        V2 = np.array([[0.0, 1.0, 0.0], [1.0, 1.0j, 1.0], [
            0.0, 1.0, 0.0]], dtype=np.complex128)

        sigma1 = SelfEnergy(E1, V1, eta=1e-7)
        sigma2 = SelfEnergy(E2, V2, eta=1e-7)

        GF = GreenFunction(HC, [sigma1, sigma2])
        GF.set_omega(2.5)

        np.testing.assert_allclose(
            np.conj(GF._get_inverse_retarded().T)
            @ GF.apply_advanced(GF.self_energies[0].get_gamma()),
            GF.self_energies[0].get_gamma(),
            rtol=1e-7,
            atol=1e-20,
        )

        np.testing.assert_allclose(
            np.conj(GF._get_inverse_retarded().T)
            @ GF.apply_advanced(GF.self_energies[1].get_gamma()),
            GF.self_energies[1].get_gamma(),
            rtol=1e-7,
            atol=1e-20,
        )
