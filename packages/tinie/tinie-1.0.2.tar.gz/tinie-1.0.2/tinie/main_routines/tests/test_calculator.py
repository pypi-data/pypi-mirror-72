#!/usr/bin/env python3

import unittest

import numpy as np
from mpi4py import MPI
from tinie.main_routines.calculator import Calculator
from tinie.systems.central_region.custom_center import CustomCenter
from tinie.systems.central_region.itp2d_center import Itp2dCenter
from tinie.systems.couplings.custom_coupling import CustomCoupling
from tinie.systems.couplings.overlap_coupling import OverlapCoupling
from tinie.systems.leads.custom_lead import CustomLead
from tinie.systems.leads.finite_harmonic_lead import FiniteHarmonicLead
from tinie.systems.read_write.system_write import SystemWrite


class TestCalculator(unittest.TestCase):
    def test_one_state_system(self):
        """Testing a simple one state system"""

        # Preparing the calculator:
        ctr = CustomCenter("tinie/test_files/HC_system_1_test.npy")
        ld0 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_1_test.npy"
        )
        ld1 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_1_test.npy"
        )
        cpl0 = CustomCoupling(
            ctr, ld0, "tinie/test_files/VL0_system_1_test.npy", MPI.COMM_WORLD
        )
        cpl1 = CustomCoupling(
            ctr, ld1, "tinie/test_files/VL1_system_1_test.npy", MPI.COMM_WORLD
        )
        sys = SystemWrite(MPI.COMM_WORLD)
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)

        mu = 250.0
        T = 0.0
        VL = 0.0
        V0 = 1e-5

        calc = Calculator(mu, T, [VL, -V0], sys, 1e-6,
                          1e-7, 1e-5, MPI.COMM_WORLD, True)
        gammaL = np.array([[0.25]])
        gammaR = np.array([[0.25]])
        selfenergyL = -0.5j * gammaL
        selfenergyR = -0.5j * gammaR
        calc.set_wide_band_gamma([gammaL, gammaR])
        calc.set_wide_band_self_energy([selfenergyL, selfenergyR])
        (
            total_currents,
            total_currents_vs_energy,
            partial_currents,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        gamma = gammaL + gammaR
        I_anal = ((-V0 / np.pi) * (gammaL * gammaR) /
                  ((mu - 500.0) ** 2 + (gamma / 2) ** 2))
        np.testing.assert_allclose(total_currents[0], -total_currents[1])
        np.testing.assert_allclose(
            transmat_vs_energy[0, 1, :], transmat_vs_energy[1, 0, :]
        )
        np.testing.assert_allclose(total_currents[0], I_anal[0, 0], rtol=1e-7)
        np.testing.assert_allclose(
            calc.transmission_matrix(mu, [VL, -V0])[0, 1],
            (-np.pi / V0) * I_anal[0, 0],
            rtol=1e-7,
        )

    def test_two_state_system(self):
        """Testing a more involved two state system"""

        # Preparing the calculator:
        ctr = CustomCenter("tinie/test_files/HC_system_2_test.npy")
        ld0 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_2_test.npy"
        )
        ld1 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_2_test.npy"
        )
        cpl0 = CustomCoupling(
            ctr, ld0, "tinie/test_files/VL0_system_2_test.npy", MPI.COMM_WORLD
        )
        cpl1 = CustomCoupling(
            ctr, ld1, "tinie/test_files/VL1_system_2_test.npy", MPI.COMM_WORLD
        )
        sys = SystemWrite(MPI.COMM_WORLD)
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)

        mu = 0.0
        T = 0.0
        VL = 1000.0
        VR = 0.0

        # Setting up test case 1:
        calc = Calculator(mu, T, [VL, VR], sys, 1e-1,
                          1e-2, 1.0, MPI.COMM_WORLD, True)
        gammaL = np.array([[1.0, 0.0], [0.0, 1.0]])
        gammaR = np.array([[1.0, 0.0], [0.0, 1.0]])
        selfenergyL = -0.5j * gammaL
        selfenergyR = -0.5j * gammaR
        calc.set_wide_band_gamma([gammaL, gammaR])
        calc.set_wide_band_self_energy([selfenergyL, selfenergyR])
        (
            total_currents_1,
            total_currents_vs_energy,
            partial_currents_1,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        np.testing.assert_allclose(total_currents_1[0], -total_currents_1[1])
        np.testing.assert_allclose(
            transmat_vs_energy[0, 1, :], transmat_vs_energy[1, 0, :]
        )
        np.testing.assert_allclose(total_currents_1[1], 1.997449443)

        # Setting up test case 2:
        gammaL = np.array([[1.0, 1.0], [1.0, 1.0]])
        gammaR = np.array([[1.0, 1.0], [1.0, 1.0]])
        selfenergyL = -0.5j * gammaL
        selfenergyR = -0.5j * gammaR
        calc.set_wide_band_gamma([gammaL, gammaR])
        calc.set_wide_band_self_energy([selfenergyL, selfenergyR])
        (
            total_currents_2,
            total_currents_vs_energy,
            partial_currents_2,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        np.testing.assert_allclose(total_currents_2[0], -total_currents_2[1])
        np.testing.assert_allclose(
            transmat_vs_energy[0, 1, :], transmat_vs_energy[1, 0, :]
        )
        np.testing.assert_allclose(
            total_currents_1, total_currents_2, rtol=5e-3)
        np.testing.assert_allclose(total_currents_2[1], 1.993186842, rtol=5e-3)

    def test_three_lead_system(self):
        """Testing a transport system with three leads"""

        # Preparing the calculator:
        ctr = CustomCenter("tinie/test_files/HC_system_2_test.npy")
        ld0 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_2_test.npy"
        )
        ld1 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_2_test.npy"
        )
        ld2 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_2_test.npy"
        )
        cpl0 = CustomCoupling(
            ctr, ld0, "tinie/test_files/VL0_system_2_test.npy", MPI.COMM_WORLD
        )
        cpl1 = CustomCoupling(
            ctr, ld1, "tinie/test_files/VL1_system_2_test.npy", MPI.COMM_WORLD
        )
        cpl2 = CustomCoupling(
            ctr, ld2, "tinie/test_files/VL0_system_2_test.npy", MPI.COMM_WORLD
        )

        sys = SystemWrite(MPI.COMM_WORLD)
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)
        sys.add_coupling_region(cpl2)

        mu = 1.0
        T = 1.0
        V0 = 200.0
        V1 = 400.0
        V2 = 600.0

        calc = Calculator(mu, T, [V0, V1, V2], sys,
                          1.0, 1e-1, 10.0, MPI.COMM_WORLD)
        (
            total_currents,
            total_currents_vs_energy,
            partial_currents,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        np.testing.assert_allclose(
            np.sum(
                transmat_vs_energy, axis=0), np.sum(
                transmat_vs_energy, axis=1))

    def test_four_lead_system(self):
        """Testing a transport system with four leads"""

        # Preparing the calculator:
        ctr = CustomCenter("tinie/test_files/HC_system_2_test.npy")
        ld0 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_2_test.npy"
        )
        ld1 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_2_test.npy"
        )
        ld2 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_2_test.npy"
        )
        ld3 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_2_test.npy"
        )
        cpl0 = CustomCoupling(
            ctr, ld0, "tinie/test_files/VL0_system_2_test.npy", MPI.COMM_WORLD
        )
        cpl1 = CustomCoupling(
            ctr, ld1, "tinie/test_files/VL1_system_2_test.npy", MPI.COMM_WORLD
        )
        cpl2 = CustomCoupling(
            ctr, ld2, "tinie/test_files/VL0_system_2_test.npy", MPI.COMM_WORLD
        )
        cpl3 = CustomCoupling(
            ctr, ld3, "tinie/test_files/VL1_system_2_test.npy", MPI.COMM_WORLD
        )

        sys = SystemWrite(MPI.COMM_WORLD)
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)
        sys.add_coupling_region(cpl2)
        sys.add_coupling_region(cpl3)

        mu = 1.0
        T = 1.0
        V0 = 200.0
        V1 = 400.0
        V2 = 600.0
        V3 = 800.0

        calc = Calculator(mu, T, [V0, V1, V2, V3], sys,
                          1.0, 1e-1, 10.0, MPI.COMM_WORLD)
        (
            total_currents,
            total_currents_vs_energy,
            partial_currents,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        np.testing.assert_allclose(
            np.sum(
                transmat_vs_energy, axis=0), np.sum(
                transmat_vs_energy, axis=1))

    def test_analytical_system(self):
        """Testing a simple analytical system"""

        # Preparing the calculator:
        ctr = CustomCenter("tinie/test_files/HC_system_1_test.npy")
        ld0 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_3_test.npy"
        )
        ld1 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_3_test.npy"
        )
        cpl0 = CustomCoupling(
            ctr, ld0, "tinie/test_files/VL0_system_3_test.npy", MPI.COMM_WORLD
        )
        cpl1 = CustomCoupling(
            ctr, ld1, "tinie/test_files/VL1_system_3_test.npy", MPI.COMM_WORLD
        )
        sys = SystemWrite(MPI.COMM_WORLD)
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)

        mu = 0.0
        T = 0.0
        VL = 750.0
        VR = 250.0

        HL0_anal = np.diag([500.0, 600.0, 700.0, 800.0, 900.0])
        HL1_anal = np.diag([100.0, 200.0, 300.0, 400.0, 500.0])
        VL0_anal = np.array([[0.1], [0.2], [0.3], [0.4], [0.5]])
        VL1_anal = np.array([[0.5], [0.6], [0.7], [0.8], [0.9]])

        # Setting up test case 1:
        calc = Calculator(mu, T, [VL, VR], sys, 1e-1,
                          1e-2, 1.0, MPI.COMM_WORLD)
        omega_vals = calc.get_omega_range()
        (
            total_currents,
            total_currents_vs_energy,
            partial_currents,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        T_anal = np.zeros((len(omega_vals),), dtype=np.complex128)
        I1 = np.eye(1)
        I5 = np.eye(5)

        for i, omega in enumerate(omega_vals):
            sigmaL_anal = (
                np.conj(VL0_anal.T)
                @ np.linalg.inv(I5 * omega - HL0_anal - I5 * VL + I5 * 1j)
                @ VL0_anal
            )
            sigmaR_anal = (
                np.conj(VL1_anal.T)
                @ np.linalg.inv(I5 * omega - HL1_anal - I5 * VR + I5 * 1j)
                @ VL1_anal
            )
            gammaL_anal = 1j * (sigmaL_anal - np.conj(sigmaL_anal.T))
            gammaR_anal = 1j * (sigmaR_anal - np.conj(sigmaR_anal.T))
            greenR_anal = np.linalg.inv(
                I1 * omega - I1 * 500.0 - (sigmaL_anal + sigmaR_anal)
            )
            T_anal[i] = np.trace(
                gammaL_anal @ greenR_anal @ gammaR_anal @ np.conj(
                    greenR_anal.T))

        np.testing.assert_allclose(transmat_vs_energy[0, 1, :], T_anal)

    def test_nonzero_temperatures_one_state(self):
        """Testing the non-zero temperature case for one state system"""

        # Preparing the calculator:
        ctr = CustomCenter("tinie/test_files/HC_system_1_test.npy")
        ld0 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_1_test.npy"
        )
        ld1 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_1_test.npy"
        )
        cpl0 = CustomCoupling(
            ctr, ld0, "tinie/test_files/VL0_system_1_test.npy", MPI.COMM_WORLD
        )
        cpl1 = CustomCoupling(
            ctr, ld1, "tinie/test_files/VL1_system_1_test.npy", MPI.COMM_WORLD
        )
        sys = SystemWrite(MPI.COMM_WORLD)
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)

        mu = 250.0
        T = 100.0
        VL = 0.0
        VR = 100.0

        calc = Calculator(mu, T, [VL, VR], sys, 1e-1,
                          1e-2, 1.0, MPI.COMM_WORLD, True)
        gammaL = np.array([[0.25]])
        gammaR = np.array([[0.75]])
        selfenergyL = -0.5j * gammaL
        selfenergyR = -0.5j * gammaR
        calc.set_wide_band_gamma([gammaL, gammaR])
        calc.set_wide_band_self_energy([selfenergyL, selfenergyR])
        (
            total_currents,
            total_currents_vs_energy,
            partial_currents,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        np.testing.assert_allclose(total_currents[0], -total_currents[1])
        np.testing.assert_allclose(
            transmat_vs_energy[0, 1, :], transmat_vs_energy[1, 0, :]
        )
        np.testing.assert_allclose(
            total_currents[0], -0.03996640881, rtol=1e-6)

    def test_nonzero_temperatures_two_state(self):
        """Testing the non-zero temperature case for two state system"""

        # Preparing the calculator:
        ctr = CustomCenter("tinie/test_files/HC_system_2_test.npy")
        ld0 = CustomLead(
            None, None, None, None, "tinie/test_files/HL0_system_2_test.npy"
        )
        ld1 = CustomLead(
            None, None, None, None, "tinie/test_files/HL1_system_2_test.npy"
        )
        cpl0 = CustomCoupling(
            ctr, ld0, "tinie/test_files/VL0_system_2_test.npy", MPI.COMM_WORLD
        )
        cpl1 = CustomCoupling(
            ctr, ld1, "tinie/test_files/VL1_system_2_test.npy", MPI.COMM_WORLD
        )
        sys = SystemWrite(MPI.COMM_WORLD)
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)

        mu = 0.0
        T = 500.0
        VL = 1000.0
        VR = 0.0

        calc = Calculator(mu, T, [VL, VR], sys, 2e-1,
                          2e-2, 2.0, MPI.COMM_WORLD, True)
        gammaL = np.array([[1.0, 0.0], [0.0, 1.0]])
        gammaR = np.array([[1.0, 0.0], [0.0, 1.0]])
        selfenergyL = -0.5j * gammaL
        selfenergyR = -0.5j * gammaR
        calc.set_wide_band_gamma([gammaL, gammaR])
        calc.set_wide_band_self_energy([selfenergyL, selfenergyR])
        (
            total_currents_1,
            total_currents_vs_energy,
            partial_currents_1,
            partial_currents_vs_energy,
            transmat_vs_energy,
            G,
            omega_values,
        ) = calc.currents()

        np.testing.assert_allclose(total_currents_1[0], -total_currents_1[1])
        np.testing.assert_allclose(
            transmat_vs_energy[0, 1, :], transmat_vs_energy[1, 0, :]
        )
        np.testing.assert_allclose(
            total_currents_1[0], 0.9230415488, rtol=1e-5)

    def test_reciprocity_one(self):
        """Testing reciprocity property of the transmission in magnetic
        field"""

        # Preparing the calculator:
        ctr0 = Itp2dCenter("tinie/test_files/itp2d_test_B1.h5", (0, 3))
        ctr1 = Itp2dCenter("tinie/test_files/itp2d_test_B-1.h5", (0, 3))
        ld0 = FiniteHarmonicLead(
            [-10.0, 1.0], [-5.0, 5.0], [0.0, 2.0], 5e-3, "left", 1.0, "dir"
        )
        ld1 = FiniteHarmonicLead(
            [1.0, 10.0], [-5.0, 5.0], [0.0, 2.0], 5e-3, "right", 1.0, "dir"
        )

        mu = 0.0
        T = 0.0
        VL = 0.0
        VR = 2.0

        ld0.set_magnetic_field_strength(1.0)
        ld1.set_magnetic_field_strength(1.0)
        cpl0 = OverlapCoupling(ctr0, ld0, MPI.COMM_WORLD)
        cpl1 = OverlapCoupling(ctr0, ld1, MPI.COMM_WORLD)

        sys0 = SystemWrite(MPI.COMM_WORLD)
        sys0.add_central_region(ctr0)
        sys0.add_coupling_region(cpl0)
        sys0.add_coupling_region(cpl1)

        calc_0 = Calculator(mu, T, [VL, VR], sys0,
                            5e-2, 5e-3, 5e-1, MPI.COMM_WORLD)
        transmat_vs_energy_0 = calc_0.currents()[4]

        ld0 = FiniteHarmonicLead(
            [-10.0, 1.0], [-5.0, 5.0], [0.0, 2.0], 5e-3, "left", 1.0, "dir"
        )
        ld1 = FiniteHarmonicLead(
            [1.0, 10.0], [-5.0, 5.0], [0.0, 2.0], 5e-3, "right", 1.0, "dir"
        )
        ld0.set_magnetic_field_strength(-1.0)
        ld1.set_magnetic_field_strength(-1.0)
        cpl0 = OverlapCoupling(ctr1, ld0, MPI.COMM_WORLD)
        cpl1 = OverlapCoupling(ctr1, ld1, MPI.COMM_WORLD)

        sys1 = SystemWrite(MPI.COMM_WORLD)
        sys1.add_central_region(ctr1)
        sys1.add_coupling_region(cpl0)
        sys1.add_coupling_region(cpl1)

        calc_1 = Calculator(mu, T, [VL, VR], sys1,
                            5e-2, 5e-3, 5e-1, MPI.COMM_WORLD)
        transmat_vs_energy_1 = calc_1.currents()[4]

        np.testing.assert_allclose(
            transmat_vs_energy_1[1, 0, :],
            np.transpose(transmat_vs_energy_0, (1, 0, 2))[1, 0, :],
            rtol=1e-7,
        )
        np.testing.assert_allclose(
            transmat_vs_energy_1[0, 1, :],
            np.transpose(transmat_vs_energy_0, (1, 0, 2))[0, 1, :],
            rtol=1e-7,
        )

    def test_reciprocity_two(self):
        """Testing reciprocity property of the transmission in magnetic
        field, mixed alignments (horizontal and vertical), non-zero
        temperature and chemical potential"""

        # Preparing the calculator:
        ctr0 = Itp2dCenter("tinie/test_files/itp2d_test_B1.h5", (0, 3))
        ctr1 = Itp2dCenter("tinie/test_files/itp2d_test_B-1.h5", (0, 3))
        ld0 = FiniteHarmonicLead(
            [-10.0, 1.0], [-5.0, 5.0], [0.0, 2.0], 5e-3, "left", 1.0, "dir"
        )
        ld1 = FiniteHarmonicLead(
            [-5.0, 5.0], [1.0, 10.0], [0.0, 2.0], 5e-3, "up", 1.0, "dir"
        )

        mu = 1.0
        T = 1.0
        VL = 0.0
        VR = 2.0

        ld0.set_magnetic_field_strength(1.0)
        ld1.set_magnetic_field_strength(1.0)
        cpl0 = OverlapCoupling(ctr0, ld0, MPI.COMM_WORLD)
        cpl1 = OverlapCoupling(ctr0, ld1, MPI.COMM_WORLD)

        sys0 = SystemWrite(MPI.COMM_WORLD)
        sys0.add_central_region(ctr0)
        sys0.add_coupling_region(cpl0)
        sys0.add_coupling_region(cpl1)

        calc_0 = Calculator(mu, T, [VL, VR], sys0,
                            5e-2, 5e-3, 5e-1, MPI.COMM_WORLD)
        transmat_vs_energy_0 = calc_0.currents()[4]

        ld0 = FiniteHarmonicLead(
            [-10.0, 1.0], [-5.0, 5.0], [0.0, 2.0], 5e-3, "left", 1.0, "dir"
        )
        ld1 = FiniteHarmonicLead(
            [-5.0, 5.0], [1.0, 10.0], [0.0, 2.0], 5e-3, "up", 1.0, "dir"
        )
        ld0.set_magnetic_field_strength(-1.0)
        ld1.set_magnetic_field_strength(-1.0)
        cpl0 = OverlapCoupling(ctr1, ld0, MPI.COMM_WORLD)
        cpl1 = OverlapCoupling(ctr1, ld1, MPI.COMM_WORLD)

        sys1 = SystemWrite(MPI.COMM_WORLD)
        sys1.add_central_region(ctr1)
        sys1.add_coupling_region(cpl0)
        sys1.add_coupling_region(cpl1)

        calc_1 = Calculator(mu, T, [VL, VR], sys1,
                            5e-2, 5e-3, 5e-1, MPI.COMM_WORLD)
        transmat_vs_energy_1 = calc_1.currents()[4]

        np.testing.assert_allclose(
            transmat_vs_energy_1[1, 0, :],
            np.transpose(transmat_vs_energy_0, (1, 0, 2))[1, 0, :],
            rtol=1e-6,
        )
        np.testing.assert_allclose(
            transmat_vs_energy_1[0, 1, :],
            np.transpose(transmat_vs_energy_0, (1, 0, 2))[0, 1, :],
            rtol=1e-6,
        )
