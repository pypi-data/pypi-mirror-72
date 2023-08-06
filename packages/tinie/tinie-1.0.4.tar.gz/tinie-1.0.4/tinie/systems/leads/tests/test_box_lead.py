#!/usr/bin/env python3

import unittest

import numpy as np
import scipy.integrate as integrate
import tinie.systems.leads.box_lead as ld


class TestBoxLead(unittest.TestCase):
    def test_lead_wf_normalization(self):
        """Testing normalization of the lead function."""
        # Setting up the leads:

        lead_1 = ld.BoxLead([-10.0, -1.0], [-3.0, 7.0],
                            [0.0, 5.0], 0.0, "left")

        lead_2 = ld.BoxLead([-10.0, -4.0], [-6.0, 1.0],
                            [0.0, 5.0], 0.0, "left")

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
        np.testing.assert_allclose(val, val_anal, rtol=1e-4)

    def test_lead_alignment(self):
        """Testing different lead alignments"""
        lead_right = ld.BoxLead(
            [5.0, 12.0], [-5.0, 5.0], [0.0, 5.0], 0.0, "right")
        np.testing.assert_equal(lead_right.alignment, "right")

        lead_left = ld.BoxLead(
            [-50.0, -14.2], [-5.0, 5.0], [0.0, 5.0], 0.0, "left")
        np.testing.assert_equal(lead_left.alignment, "left")

        lead_up = ld.BoxLead(
            [-5.0, 5.0], [np.pi, 2 * np.pi], [0.0, 5.0], 0.0, "up")
        np.testing.assert_equal(lead_up.alignment, "up")

        lead_down = ld.BoxLead(
            [-5.0, 5.0], [-10.0, -7.0], [0.0, 5.0], 0.0, "down")
        np.testing.assert_equal(lead_down.alignment, "down")

    def test_eval_state(self):
        """Testing if lead wavefunction values correspond to analytical ones"""

        # Setting up leads:
        lead_right = ld.BoxLead(
            [5.0, 12.0], [-5.0, 5.0], [0.0, 5.0], 0.0, "right")
        lead_left = ld.BoxLead(
            [-50.0, -14.2], [-5.0, 5.0], [0.0, 5.0], 0.0, "left")
        lead_up = ld.BoxLead(
            [-5.0, 5.0], [np.pi, 2 * np.pi], [0.0, 5.0], 0.0, "up")
        lead_down = ld.BoxLead(
            [-5.0, 5.0], [-10.0, -7.0], [0.0, 5.0], 0.0, "down")

        # Evaluating some points in the lead:
        p_1 = (
            np.abs(
                np.sqrt(4 / (lead_right._Lx * lead_right._Ly))
                * lead_right.get_state_point(7.0, 0.0, 0)
            )
            ** 2
        )
        p_2 = (
            np.abs(
                np.sqrt(4 / (lead_left._Lx * lead_left._Ly))
                * lead_left.get_state_point(-10 * np.pi, 3.0, 1)
            )
            ** 2
        )
        p_3 = (
            np.abs(
                np.sqrt(4 / (lead_up._Lx * lead_up._Ly))
                * lead_up.get_state_point(-np.pi, 3 * np.pi / 2, 2)
            )
            ** 2
        )
        p_4 = (
            np.abs(
                np.sqrt(4 / (lead_down._Lx * lead_down._Ly))
                * lead_down.get_state_point(-0.05, -8.0, 3)
            )
            ** 2
        )

        np.testing.assert_allclose(p_1, 0.03492916954)
        np.testing.assert_allclose(p_2, 0.00005537653689)
        np.testing.assert_allclose(p_3, 0.1232110538)
        np.testing.assert_allclose(p_4, 0.0003942649343)
