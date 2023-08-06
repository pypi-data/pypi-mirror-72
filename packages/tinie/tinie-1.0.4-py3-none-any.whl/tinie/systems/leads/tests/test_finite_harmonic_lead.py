#!/usr/bin/env python3

import unittest

import numpy as np
import scipy.integrate as integrate
import tinie.systems.leads.finite_harmonic_lead as ld


class TestFiniteHarmonicLead(unittest.TestCase):
    def test_lead_wf_normalization(self):
        """Testing normalization of the lead function."""
        # Setting up the leads:

        # Lead with Dirichlet boundaries:
        lead_1 = ld.FiniteHarmonicLead(
            [-10.0, -1.0], [-3.0, 7.0], [0.0, 5.0], 1.0, "left", 1.0, "dir"
        )

        # Lead with von Neumann boundaries:
        lead_2 = ld.FiniteHarmonicLead(
            [-10.0, -4.0], [-6.0, 1.0], [0.0, 5.0], 1.0, "left", 1.0, "neu"
        )

        # Now we set 3 test wavefunctions for each:
        psi_1 = lead_1.get_state(100, 100, 0)
        psi_2 = lead_1.get_state(100, 100, 4)
        psi_3 = lead_1.get_state(100, 100, 10)

        psi_4 = lead_2.get_state(100, 100, 0)
        psi_5 = lead_2.get_state(100, 100, 4)
        psi_6 = lead_2.get_state(100, 100, 10)

        # Set up the grid...
        x1 = np.linspace(lead_1.x[0], lead_1.x[1], 100)
        y1 = np.linspace(lead_1.y[0], lead_1.y[1], 100)
        dx1 = x1[1] - x1[0]
        dy1 = y1[1] - y1[0]

        x2 = np.linspace(lead_2.x[0], lead_2.x[1], 100)
        y2 = np.linspace(lead_2.y[0], lead_2.y[1], 100)
        dx2 = x2[1] - x2[0]
        dy2 = y2[1] - y2[0]

        # ...and finally calculate total probabilities, over the whole space,
        # which should be equal to 1.
        prob_tot_1 = integrate.simps(
            integrate.simps(
                np.abs(psi_1) ** 2,
                x1,
                dx=dx1,
                axis=0),
            y1,
            dx=dy1,
            axis=0)
        prob_tot_2 = integrate.simps(
            integrate.simps(
                np.abs(psi_2) ** 2,
                x1,
                dx=dx1,
                axis=0),
            y1,
            dx=dy1,
            axis=0)
        prob_tot_3 = integrate.simps(
            integrate.simps(
                np.abs(psi_3) ** 2,
                x1,
                dx=dx1,
                axis=0),
            y1,
            dx=dy1,
            axis=0)
        prob_tot_4 = integrate.simps(
            integrate.simps(
                np.abs(psi_4) ** 2,
                x2,
                dx=dx2,
                axis=0),
            y2,
            dx=dy2,
            axis=0)
        prob_tot_5 = integrate.simps(
            integrate.simps(
                np.abs(psi_5) ** 2,
                x2,
                dx=dx2,
                axis=0),
            y2,
            dx=dy2,
            axis=0)
        prob_tot_6 = integrate.simps(
            integrate.simps(
                np.abs(psi_6) ** 2,
                x2,
                dx=dx2,
                axis=0),
            y2,
            dx=dy2,
            axis=0)

        val = [
            prob_tot_1,
            prob_tot_2,
            prob_tot_3,
            prob_tot_4,
            prob_tot_5,
            prob_tot_6]
        val_anal = [1.0] * 6
        np.testing.assert_allclose(val, val_anal, rtol=1e-3)

    def test_lead_alignment(self):
        """Testing different lead alignments"""
        lead_right = ld.FiniteHarmonicLead(
            [5.0, 12.0], [-5.0, 5.0], [0.0, 5.0], 1.0, "right"
        )
        np.testing.assert_equal(lead_right.alignment, "right")

        lead_left = ld.FiniteHarmonicLead(
            [-50.0, -14.2], [-5.0, 5.0], [0.0, 5.0], 1.0, "left"
        )
        np.testing.assert_equal(lead_left.alignment, "left")

        lead_up = ld.FiniteHarmonicLead(
            [-5.0, 5.0], [np.pi, 2 * np.pi], [0.0, 5.0], 1.0, "up"
        )
        np.testing.assert_equal(lead_up.alignment, "up")

        lead_down = ld.FiniteHarmonicLead(
            [-5.0, 5.0], [-10.0, -7.0], [0.0, 5.0], 1.0, "down"
        )
        np.testing.assert_equal(lead_down.alignment, "down")

    def test_get_state_point(self):
        """Testing if lead wavefunction values correspond to analytical ones"""

        # Setting up leads:
        lead_right = ld.FiniteHarmonicLead(
            [5.0, 12.0], [-5.0, 5.0], [0.0, 5.0], 1.0, "right", 1.0
        )
        lead_left = ld.FiniteHarmonicLead(
            [-50.0, -14.2], [-5.0, 5.0], [0.0, 5.0], 1.0, "left", 5.0, "neu"
        )
        lead_up = ld.FiniteHarmonicLead(
            [-5.0, 5.0], [np.pi, 2 * np.pi], [0.0, 5.0], 1.0, "up", 1e-3
        )
        lead_down = ld.FiniteHarmonicLead(
            [-5.0, 5.0], [-10.0, -7.0], [0.0, 1000.0], 1.0, "down", 100.0, "neu"
        )

        # Evaluating some points in the lead:
        p_1 = (
            np.abs(
                lead_right.normalization(0) *
                lead_right.get_state_point(
                    7.0,
                    0.0,
                    0)) ** 2)
        p_2 = (
            np.abs(
                lead_left.normalization(4)
                * lead_left.get_state_point(-10 * np.pi, 3.0, 4)
            )
            ** 2
        )
        p_3 = (
            np.abs(
                lead_up.normalization(8)
                * lead_up.get_state_point(-np.pi, 3 * np.pi / 2, 8)
            )
            ** 2
        )
        p_4 = (
            np.abs(
                lead_down.normalization(5500)
                * lead_down.get_state_point(-0.05, -8.0, 5500)
            )
            ** 2
        )

        np.testing.assert_allclose(p_1, 0.1434299865)
        np.testing.assert_allclose(p_2, 9.848598103e-22)
        np.testing.assert_allclose(p_3, 0.002640913489)
        np.testing.assert_allclose(p_4, 0.01396425704)
