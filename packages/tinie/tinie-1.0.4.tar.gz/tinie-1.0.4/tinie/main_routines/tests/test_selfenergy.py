#!/usr/bin/env python3

import unittest

import numpy as np
from tinie.main_routines.selfenergy import SelfEnergy


class TestSelfEnergy(unittest.TestCase):
    def test_real_coupling(self):
        """Testing self energy for a simple real-valued coupling test case"""

        E = np.array([1.0, 1.0])
        V = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=np.complex128)
        sigma_anal = np.array(
            [
                [1.0 - 1e-7j, 0.0, 1.0 - 1e-7j],
                [0.0, 1.0 - 1e-7j, 0.0],
                [1.0 - 1e-7j, 0.0, 1.0 - 1e-7j],
            ],
            dtype=np.complex128,
        )
        gamma_anal = np.array(
            [[2e-7, 0.0, 2e-7], [0.0, 2e-7, 0.0], [2e-7, 0.0, 2e-7]],
            dtype=np.complex128,
        )

        selfE = SelfEnergy(E, V, eta=1e-7)
        selfE.set_omega(2.0)

        # Checking that the shape of the self energy is correct:
        np.testing.assert_equal(selfE.retarded().shape, sigma_anal.shape)

        # Checking that self energy is equal to analytical result:
        np.testing.assert_allclose(selfE.retarded(), sigma_anal)

        # Checking that advanced and retarded self energies are
        # complex conjugates of each other:
        np.testing.assert_allclose(
            selfE.advanced(), np.conjugate(np.transpose(selfE.retarded()))
        )

        # Checking that gamma is equal to the analytical result:
        np.testing.assert_allclose(selfE.get_gamma(), gamma_anal)

    def test_imag_coupling(self):
        """Testing self energy for a simple complex-valued coupling
        test case"""

        E = np.array([1.0, 1.0])
        V = np.array([[1.0j, 1.0, 1.0j], [1.0, 1.0j, 1.0]],
                     dtype=np.complex128)
        sigma_anal = np.array(
            [
                [2.0 - 2e-7j, 0.0, 2.0 - 2e-7j],
                [0.0, 2.0 - 2e-7j, 0.0],
                [2.0 - 2e-7j, 0.0, 2.0 - 2e-7j],
            ],
            dtype=np.complex128,
        )
        gamma_anal = np.array(
            [[4e-7, 0.0, 4e-7], [0.0, 4e-7, 0.0], [4e-7, 0.0, 4e-7]],
            dtype=np.complex128,
        )
        selfE = SelfEnergy(E, V, eta=1e-7)
        selfE.set_omega(2.0)

        # Checking that the shape of the self energy is correct:
        np.testing.assert_equal(selfE.retarded().shape, sigma_anal.shape)

        # Checking that self energy is equal to analytical result:
        np.testing.assert_allclose(selfE.retarded(), sigma_anal)

        # Checking that advanced and retarded self energies are complex
        # conjugates of each other:
        np.testing.assert_allclose(
            selfE.advanced(), np.conjugate(np.transpose(selfE.retarded()))
        )

        # Checking that gamma is equal to the analytical result:
        np.testing.assert_allclose(selfE.get_gamma(), gamma_anal)

    def test_harder_coupling(self):
        """Testing a slightly more complicated coupling case"""

        E = np.array([1.0, 2.0, 4.0, 8.0])
        V = np.array(
            [
                [1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j],
                [1.0 - 1.0j, 1.0 + 1.0j, 1.0 + 1.0j],
                [1.0 - 1.0j, 1.0 - 1.0j, 1.0 + 1.0j],
                [1.0 - 1.0j, 1.0 - 1.0j, 1.0 - 1.0j],
            ],
            dtype=np.complex128,
        )
        sigma_anal = np.array([[0.6 - 4.58e-7j,
                                -1.3999998 + 1.999999742j,
                                0.6000004 - 5.799999991e-8j,
                                ],
                               [-1.4000002 - 2.000000258j,
                                0.6 - 4.58e-7j,
                                2.6000002 - 2.000000258j],
                               [0.5999996 - 5.800000014e-8j,
                                2.5999998 + 1.999999742j,
                                0.6 - 4.58e-7j],
                               ],
                              dtype=np.complex128,
                              )
        gamma_anal = np.array(
            [
                [9.16e-7, 5.160000003e-7 + 3.999999998e-7j, 1.16e-7 + 8.0e-7j],
                [
                    5.160000003e-7 - 3.999999998e-7j,
                    9.16e-7,
                    5.159999996e-7 + 4.000000002e-7j,
                ],
                [1.16e-7 - 8.0e-7j, 5.159999996e-7 - 4.000000002e-7j, 9.16e-7],
            ],
            dtype=np.complex128,
        )
        selfE = SelfEnergy(E, V, eta=1e-7)
        selfE.set_omega(3.0)

        # Checking that the shape of the self energy is correct:
        np.testing.assert_equal(selfE.retarded().shape, sigma_anal.shape)

        # Checking that self energy is equal to analytical result:
        np.testing.assert_allclose(selfE.retarded(), sigma_anal)

        # Checking that advanced and retarded self energies are
        # complex conjugates of each other:
        np.testing.assert_allclose(
            selfE.advanced(), np.conjugate(np.transpose(selfE.retarded()))
        )

        # Checking that gamma is equal to the analytical result:
        np.testing.assert_allclose(selfE.get_gamma(), gamma_anal)

    def test_overlapping_energy_coupling(self):
        """Testing coupling case with overlapping reservoir
        energies and omega"""

        E = np.array([1.0, 2.0, 4.0, 8.0])
        V = np.array(
            [
                [1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j],
                [1.0 - 1.0j, 1.0 + 1.0j, 1.0 + 1.0j],
                [1.0 - 1.0j, 1.0 - 1.0j, 1.0 + 1.0j],
                [1.0 - 1.0j, 1.0 - 1.0j, 1.0 - 1.0j],
            ],
            dtype=np.complex128,
        )
        sigma_anal = np.array(
            [
                [
                    1.166666667 - 2.0e7j,
                    0.1666667167 - 1.9999999e7j,
                    2.000000017e7 + 0.9999999653j,
                ],
                [
                    0.1666666167 - 2.0000001e7j,
                    1.166666667 - 2.0e7j,
                    2.000000117e7 - 8.472222215e-8j,
                ],
                [
                    -1.999999983e7 - 1.000000035j,
                    -1.999999883e7 - 8.472222215e-8j,
                    1.166666667 - 2.0e7j,
                ],
            ],
            dtype=np.complex128,
        )
        gamma_anal = np.array(
            [
                [4.0e7, 4.0e7 + 9.999999984e-8j, 6.94444442e-8 + 4.0e7j],
                [4.0e7 - 9.999999984e-8j, 4.0e7, 1.694444443e-7 + 4.0e7j],
                [6.94444442e-8 - 4.0e7j, 1.694444443e-7 - 4.0e7j, 4.0e7],
            ],
            dtype=np.complex128,
        )
        selfE = SelfEnergy(E, V, eta=1e-7)
        selfE.set_omega(4.0)

        # Checking that the shape of the self energy is correct:
        np.testing.assert_equal(selfE.retarded().shape, sigma_anal.shape)

        # Checking that self energy is equal to analytical result:
        np.testing.assert_allclose(selfE.retarded(), sigma_anal)

        # Checking that advanced and retarded self energies are
        # complex conjugates of each other:
        np.testing.assert_allclose(
            selfE.advanced(), np.conjugate(np.transpose(selfE.retarded()))
        )

        # Checking that gamma is equal to the analytical result:
        np.testing.assert_allclose(selfE.get_gamma(), gamma_anal)
