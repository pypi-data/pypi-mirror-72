#!/usr/bin/env python3

import unittest

import numpy as np
import scipy.integrate as integrate
from tinie.systems.central_region.itp2d_center import Itp2dCenter


class TestItp2dCenter(unittest.TestCase):
    def test_init(self):
        """Testing itp2d central region initialization"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

    def test_get_energies(self):
        """Testing correctness of retrieved eigenenergies"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        energies = f.get_energies()

        self.assertEqual(len(energies), 5)

        exact_energies = np.array([1.0, 2.0, 2.0, 3.0, 3.0, 3.0])
        for i in range(len(energies)):
            self.assertAlmostEqual(energies[i], exact_energies[i])

    def test_get_potential(self):
        """Testing correctness of retrieved potential"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        potential = f.get_potential()
        x, y = f.get_coordinate_ranges()

        self.assertEqual(potential.shape, (64, 64))

        exact_potential = np.array(
            [[0.5 * (xp ** 2 + yp ** 2) for yp in y] for xp in x]
        )
        np.testing.assert_allclose(potential, exact_potential)

    def test_get_state(self):
        """Testing that the shape of the wavefunction is correct"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        state = f.get_state(3)

        self.assertEqual(state.shape, (64, 64),
                         "States are not in correct shape")

    def test_get_states(self):
        """Testing that the shape of the states is correct"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        states = f.get_states()

        self.assertEqual(states.shape, (64, 64, 5),
                         "States are not in correct shape")

    def test_sliced_states(self):
        """Testing of the proper slicing of get_sliced_state and
        get_sliced_states functions"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        psi_1 = f.get_sliced_states(0.5, "right")[:, :, 0]
        psi_2 = f.get_sliced_states(1.0, "left")[:, :, 1]
        psi_3 = f.get_sliced_state(2, 5.0, "up")
        psi_4 = f.get_sliced_state(3, 10.0, "down")

        self.assertAlmostEqual(np.abs(psi_1[0, 30]) ** 2, 1.5336808e-14)
        self.assertAlmostEqual(np.abs(psi_1[0, 32]) ** 2, 1.6453992e-14)
        self.assertAlmostEqual(np.abs(psi_1[-1, 30]) ** 2, 3.7654110e-16)
        self.assertAlmostEqual(np.abs(psi_1[-1, 32]) ** 2, 4.0396963e-16)

        self.assertAlmostEqual(np.abs(psi_2[0, 30]) ** 2, 5.8504126e-14)
        self.assertAlmostEqual(np.abs(psi_2[0, 32]) ** 2, 6.2796733e-14)
        self.assertAlmostEqual(np.abs(psi_2[-1, 30]) ** 2, 2.5929611e-10)
        self.assertAlmostEqual(np.abs(psi_2[-1, 32]) ** 2, 2.7829896e-10)

        self.assertAlmostEqual(np.abs(psi_3[30, 0]) ** 2, 0.1807134)
        self.assertAlmostEqual(np.abs(psi_3[30, -1]) ** 2, 5.8508830e-15)
        self.assertAlmostEqual(np.abs(psi_3[32, 0]) ** 2, 0.2263852)
        self.assertAlmostEqual(np.abs(psi_3[32, -1]) ** 2, 6.2801692e-15)

        self.assertAlmostEqual(np.abs(psi_4[30, 0]) ** 2, 2.7149446e-13)
        self.assertAlmostEqual(np.abs(psi_4[30, -1]) ** 2, 5.6452517e-6)
        self.assertAlmostEqual(np.abs(psi_4[32, 0]) ** 2, 3.0816327e-13)
        self.assertAlmostEqual(np.abs(psi_4[32, -1]) ** 2, 5.3795889e-6)

    def test_boundary_state(self):
        """Testing if the wavefunctions on the boundary are extracted
        properly"""

        center = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        psi_bound_1 = center.get_state(0)[0, :]  # left boundary
        psi_bound_2 = center.get_state(1)[-1, :]  # right boundary
        psi_bound_3 = center.get_state(2)[:, -1]  # upper boundary
        psi_bound_4 = center.get_state(3)[:, 0]  # lower boundary

        np.testing.assert_array_equal(
            psi_bound_1, center.get_boundary_state(
                0, "left"))
        np.testing.assert_array_equal(
            psi_bound_2, center.get_boundary_state(1, "right")
        )
        np.testing.assert_array_equal(
            psi_bound_3, center.get_boundary_state(2, "up"))
        np.testing.assert_array_equal(
            psi_bound_4, center.get_boundary_state(
                3, "down"))

    def test_coordinate_ranges(self):
        """Testing that the shape of coordinate ranges is correct"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        x, y = f.get_coordinate_ranges()

        self.assertTrue(
            len(x) == 64 and len(y) == 64, "Wrong length of coordinate ranges"
        )

    def test_coordinates(self):
        """Testing if the coordinates are generated correctly"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        X, Y = f.get_coordinates()

        state = f.get_state(3)

        self.assertEqual(state.shape, X.shape)

        self.assertEqual(X[0, 0], -5.90625)
        self.assertEqual(X[-1, 0], 5.90625)
        self.assertEqual(X[0, -1], -5.90625)
        self.assertEqual(X[-1, -1], 5.90625)

        self.assertEqual(Y[0, 0], -5.90625)
        self.assertEqual(Y[-1, 0], -5.90625)
        self.assertEqual(Y[0, -1], 5.90625)
        self.assertEqual(Y[-1, -1], 5.90625)

    def test_slice_coordinates(self):
        """Testing if the sliced coordinates are taken correctly"""

        f = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        # Check if all boundary types work as intended:
        X, Y = f.get_slice_coordinates(0.4, "right")
        self.assertEqual(X[0, 0], 5.53125)
        self.assertEqual(X[-1, 0], 5.90625)
        self.assertEqual(X[0, -1], 5.53125)
        self.assertEqual(X[-1, -1], 5.90625)

        self.assertEqual(Y[0, 0], -5.90625)
        self.assertEqual(Y[0, -1], 5.90625)
        self.assertEqual(Y[-1, 0], -5.90625)
        self.assertEqual(Y[-1, -1], 5.90625)

        X, Y = f.get_slice_coordinates(0.6, "left")
        self.assertEqual(X[0, 0], -5.90625)
        self.assertEqual(X[-1, 0], -5.34375)
        self.assertEqual(X[0, -1], -5.90625)
        self.assertEqual(X[-1, -1], -5.34375)

        self.assertEqual(Y[0, 0], -5.90625)
        self.assertEqual(Y[0, -1], 5.90625)
        self.assertEqual(Y[-1, 0], -5.90625)
        self.assertEqual(Y[-1, -1], 5.90625)

        X, Y = f.get_slice_coordinates(1.0, "up")
        self.assertEqual(X[0, 0], -5.90625)
        self.assertEqual(X[-1, 0], 5.90625)
        self.assertEqual(X[0, -1], -5.90625)
        self.assertEqual(X[-1, -1], 5.90625)

        self.assertEqual(Y[0, 0], 4.96875)
        self.assertEqual(Y[0, -1], 5.90625)
        self.assertEqual(Y[-1, 0], 4.96875)
        self.assertEqual(Y[-1, -1], 5.90625)

        X, Y = f.get_slice_coordinates(10.0, "down")
        self.assertEqual(X[0, 0], -5.90625)
        self.assertEqual(X[-1, 0], 5.90625)
        self.assertEqual(X[0, -1], -5.90625)
        self.assertEqual(X[-1, -1], 5.90625)

        self.assertEqual(Y[0, 0], -5.90625)
        self.assertEqual(Y[0, -1], 4.03125)
        self.assertEqual(Y[-1, 0], -5.90625)
        self.assertEqual(Y[-1, -1], 4.03125)

    def test_state_normalization(self):
        """Testing if states in the test file are properly normalized"""

        center = Itp2dCenter("tinie/test_files/itp2d_test.h5", states=(0, 4))

        # Set up test wavefunctions:
        psi_1 = center.get_state(0)
        psi_2 = center.get_state(1)
        psi_3 = center.get_state(2)
        psi_4 = center.get_state(3)
        psi_5 = center.get_state(4)

        # Set up the grid...
        x = center.get_coordinates()[0]
        y = center.get_coordinates()[1]
        dx = x[1, 0] - x[0, 0]
        dy = y[0, 1] - y[0, 0]

        # ...and finally, calculate total probabilities over the whole space,
        # which should be equal to 1.
        prob_tot_1 = integrate.simps(
            integrate.simps(np.abs(psi_1) ** 2, x[:, 0], dx=dx, axis=0),
            y[0, :],
            dx=dy,
            axis=0,
        )
        prob_tot_2 = integrate.simps(
            integrate.simps(np.abs(psi_2) ** 2, x[:, 0], dx=dx, axis=0),
            y[0, :],
            dx=dy,
            axis=0,
        )
        prob_tot_3 = integrate.simps(
            integrate.simps(np.abs(psi_3) ** 2, x[:, 0], dx=dx, axis=0),
            y[0, :],
            dx=dy,
            axis=0,
        )
        prob_tot_4 = integrate.simps(
            integrate.simps(np.abs(psi_4) ** 2, x[:, 0], dx=dx, axis=0),
            y[0, :],
            dx=dy,
            axis=0,
        )
        prob_tot_5 = integrate.simps(
            integrate.simps(np.abs(psi_5) ** 2, x[:, 0], dx=dx, axis=0),
            y[0, :],
            dx=dy,
            axis=0,
        )

        np.testing.assert_almost_equal(
            prob_tot_1, 1.0, decimal=5, verbose=True)
        np.testing.assert_almost_equal(
            prob_tot_2, 1.0, decimal=5, verbose=True)
        np.testing.assert_almost_equal(
            prob_tot_3, 1.0, decimal=5, verbose=True)
        np.testing.assert_almost_equal(
            prob_tot_4, 1.0, decimal=5, verbose=True)
        np.testing.assert_almost_equal(
            prob_tot_5, 1.0, decimal=5, verbose=True)
