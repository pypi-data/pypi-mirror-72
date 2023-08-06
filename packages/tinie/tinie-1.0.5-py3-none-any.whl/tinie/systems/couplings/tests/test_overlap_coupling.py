import unittest

import numpy as np
import scipy.special as sp
import tinie.systems.central_region.itp2d_center as ctr
import tinie.systems.couplings.overlap_coupling as cpl
import tinie.systems.leads.finite_harmonic_lead as ld
from findiff.vector import Laplacian
from mpi4py import MPI
from scipy.integrate import simps
from scipy.optimize import curve_fit

FILEPATH_SMALL = "tinie/test_files/lil_itp2d_test.h5"
FILEPATH_BIG = "tinie/test_files/big_itp2d_test.h5"


class TestOverlapCoupling(unittest.TestCase):
    def test_ctr_wf_normalization(self):
        """Testing the normalization of custom center QHO"""

        # Setting up test system:
        center = ctr.Itp2dCenter(FILEPATH_SMALL, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-10.0, -4.0], [-5.0, 5.0], [0.0, 5.0], 1.0, "left"
        )
        coupling = cpl.OverlapCoupling(center, lead, MPI.COMM_WORLD)

        # Now we set up 3 test wavefunctions:
        coupling._set_test_wf_qhm(0, 0)
        psi_1 = coupling._test_wave_function_center

        coupling._set_test_wf_qhm(1, 0)
        psi_2 = coupling._test_wave_function_center

        coupling._set_test_wf_qhm(1, 1)
        psi_3 = coupling._test_wave_function_center

        # Set up the grid...
        x, y = center.get_coordinate_ranges()

        # ...and finally, calculate total probabilities over the whole space,
        # which should be equal to 1.
        prob_tot_1 = simps(simps(np.abs(psi_1) ** 2, x=x, axis=0), x=y, axis=0)
        prob_tot_2 = simps(simps(np.abs(psi_2) ** 2, x=x, axis=0), x=y, axis=0)
        prob_tot_3 = simps(simps(np.abs(psi_3) ** 2, x=x, axis=0), x=y, axis=0)

        np.testing.assert_almost_equal(
            prob_tot_1, 1.0, decimal=5, verbose=True)
        np.testing.assert_almost_equal(
            prob_tot_2, 1.0, decimal=5, verbose=True)
        np.testing.assert_almost_equal(
            prob_tot_3, 1.0, decimal=5, verbose=True)

    def test_trial_wf(self):
        """Testing the custom QHO center function"""

        # Setting up test system:
        center = ctr.Itp2dCenter(FILEPATH_SMALL, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-10.0, -4.0], [-5.0, 5.0], [0.0, 5.0], 1.0, "left"
        )
        coupling = cpl.OverlapCoupling(center, lead, MPI.COMM_WORLD)

        # Now we set up 3 test wavefunctions:
        coupling._set_test_wf_qhm(0, 0)
        psi_1 = coupling._test_wave_function_center

        coupling._set_test_wf_qhm(1, 0)
        psi_2 = coupling._test_wave_function_center

        coupling._set_test_wf_qhm(1, 1)
        psi_3 = coupling._test_wave_function_center

        # And compare their values to the analytical ones at some points:
        np.testing.assert_almost_equal(psi_1[20, 33], 0.05304457106)
        np.testing.assert_almost_equal(psi_1[0, 11], 9.295724939e-12)
        np.testing.assert_almost_equal(psi_1[45, 26], 0.01346426008)
        np.testing.assert_almost_equal(psi_1[63, 57], 1.630963515e-13)

        np.testing.assert_almost_equal(psi_2[20, 33], -0.1617540086)
        np.testing.assert_almost_equal(psi_2[0, 11], -7.764439103e-11)
        np.testing.assert_almost_equal(psi_2[45, 26], 0.04819838989)
        np.testing.assert_almost_equal(psi_2[63, 57], 1.362294708e-12)

        np.testing.assert_almost_equal(psi_3[20, 33], -0.06433726295)
        np.testing.assert_almost_equal(psi_3[0, 11], 4.220658548e-10)
        np.testing.assert_almost_equal(psi_3[45, 26], -0.07029290469)
        np.testing.assert_almost_equal(psi_3[63, 57], 9.211439835e-12)

    def test_laplacian(self):
        """Testing whether Laplacian works as intended"""

        # Setting up test system:
        center = ctr.Itp2dCenter(FILEPATH_SMALL, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-10.0, -4.0], [-5.0, 5.0], [0.0, 5.0], 1.0, "left"
        )
        coupling = cpl.OverlapCoupling(center, lead, MPI.COMM_WORLD)

        # Now we set up 3 test wavefunctions...
        coupling._set_test_wf_qhm(0, 0)
        psi_1 = coupling._test_wave_function_center

        coupling._set_test_wf_qhm(1, 0)
        psi_2 = coupling._test_wave_function_center

        coupling._set_test_wf_qhm(1, 1)
        psi_3 = coupling._test_wave_function_center

        # ...calculate their Laplacians...
        x, y = center.get_coordinate_ranges()

        nabla = Laplacian(h=[x[1] - x[0], y[1] - y[0]], acc=4)

        L_1 = nabla(psi_1)
        L_2 = nabla(psi_2)
        L_3 = nabla(psi_3)

        # ...and compare their values to the analytical ones at some points
        np.testing.assert_allclose(L_1[30, 34], -0.8265774534, rtol=1e-3)
        np.testing.assert_allclose(L_1[45, 15], 0.002674210178, rtol=1e-3)
        np.testing.assert_allclose(L_1[0, 63], 2.70775852e-14, atol=1e-10)
        np.testing.assert_allclose(L_1[37, 11], 0.002840146259, rtol=1e-3)

        np.testing.assert_allclose(L_2[30, 34], 0.7152899828, rtol=1e-3)
        np.testing.assert_allclose(L_2[45, 15], 0.00820327977, rtol=1e-3)
        np.testing.assert_allclose(L_2[0, 63], -2.194960145e-13, atol=1e-10)
        np.testing.assert_allclose(L_2[37, 11], 0.003543431931, rtol=1e-3)

        np.testing.assert_allclose(L_3[30, 34], 0.7304042681, rtol=1e-3)
        np.testing.assert_allclose(L_3[45, 15], -0.02989858777, rtol=1e-3)
        np.testing.assert_allclose(L_3[0, 63], -1.879060082e-12, atol=1e-10)
        np.testing.assert_allclose(L_3[37, 11], -0.01600744035, rtol=1e-3)

    def test_laplacian_convergence(self):
        """Testing convergence of the Laplacian with bigger grids"""

        # We check value of the Laplacian of this function at (0,0):
        def f(x, y):
            return np.cos(x) * np.cos(y)

        val_anal = -2.0

        # Set up different grids:
        sizes = [99, 199, 299, 399, 499]
        midpoint = [49, 99, 149, 199, 249]
        spacings = [0.0, 0.0, 0.0, 0.0, 0.0]
        rtols = [0.0, 0.0, 0.0, 0.0, 0.0]
        i = 0

        for size in sizes:
            x_range = np.linspace(-6.0, 6.0, size)
            y_range = np.linspace(-6.0, 6.0, size)
            z = np.array([[f(xp, yp) for yp in y_range] for xp in x_range])
            dx = x_range[1] - x_range[0]
            dy = y_range[1] - y_range[0]
            nabla = Laplacian(h=[dx, dy], acc=4)
            L = nabla(z)
            val = L[midpoint[i], midpoint[i]]
            spacings[i] = dx
            rtols[i] = np.abs((val_anal - val) / val_anal)
            i += 1

        def f(x, a, b):
            return a * x + b

        coeff = curve_fit(f, np.log(spacings), np.log(rtols))[0]
        np.testing.assert_allclose(coeff[0], 4.0, rtol=0.01)

    def test_simps(self):
        """Testing the Simpson's rule integrator"""

        x_range = np.linspace(-6.0, 6.0, 370)
        y_range = np.linspace(-6.0, 6.0, 370)

        # Setting up custom test functions:
        def f_1(x, y):
            return np.cos(x + y)  # Purely real function

        def f_2(x, y):
            return np.exp(1j * (x + y))  # Real/imaginary function

        def f_3(x, y):
            return 1j * np.sin(x + y)  # Purely imaginary function

        def f_4(x, y):
            return np.cos(x) * np.cos(y)  # Symmetrical in x and y

        def f_5(x, y):
            return np.cos(x) * np.exp(y)  # Symmetrical in x

        def f_6(x, y):
            return np.exp(x) * np.cos(y)  # Symmetrical in y

        def f_7(x, y):
            return np.exp(x + y)  # Not symmetrical

        def f_8(x, y):
            return sp.legendre(5)(x + y)  # Legendre functions

        def f_9(x, y):
            return sp.j0(x) + 1j * sp.j1(y)  # Bessel functions

        z_1 = np.array([[f_1(xp, yp) for yp in y_range] for xp in x_range])
        z_2 = np.array([[f_2(xp, yp) for yp in y_range] for xp in x_range])
        z_3 = np.array([[f_3(xp, yp) for yp in y_range] for xp in x_range])
        z_4 = np.array([[f_4(xp, yp) for yp in y_range] for xp in x_range])
        z_5 = np.array([[f_5(xp, yp) for yp in y_range] for xp in x_range])
        z_6 = np.array([[f_6(xp, yp) for yp in y_range] for xp in x_range])
        z_7 = np.array([[f_7(xp, yp) for yp in y_range] for xp in x_range])
        z_8 = np.array([[f_8(xp, yp) for yp in y_range] for xp in x_range])
        z_9 = np.array([[f_9(xp, yp) for yp in y_range] for xp in x_range])

        val_1 = simps(simps(z_1, x=x_range, axis=0), x=y_range, axis=0)
        val_2 = simps(simps(z_2, x=x_range, axis=0), x=y_range, axis=0)
        val_3 = simps(simps(z_3, x=x_range, axis=0), x=y_range, axis=0)
        val_4 = simps(simps(z_4, x=x_range, axis=0), x=y_range, axis=0)
        val_5 = simps(simps(z_5, x=x_range, axis=0), x=y_range, axis=0)
        val_6 = simps(simps(z_6, x=x_range, axis=0), x=y_range, axis=0)
        val_7 = simps(simps(z_7, x=x_range, axis=0), x=y_range, axis=0)
        val_8 = simps(simps(z_8, x=x_range, axis=0), x=y_range, axis=0)
        val_9 = simps(simps(z_9, x=x_range, axis=0), x=y_range, axis=0)

        # Comparing calculated results to the analytical:
        np.testing.assert_allclose(val_1, 0.3122920825, rtol=1e-5)
        np.testing.assert_allclose(val_2, 0.3122920825, rtol=1e-5)
        np.testing.assert_allclose(val_3, 0.0, atol=1e-10)
        np.testing.assert_allclose(val_4, 0.3122920825, rtol=1e-5)
        np.testing.assert_allclose(val_5, -225.4471482, rtol=1e-5)
        np.testing.assert_allclose(val_6, -225.4471482, rtol=1e-5)
        np.testing.assert_allclose(val_7, 162752.7914, rtol=1e-5)
        np.testing.assert_allclose(val_8, 0.0, atol=1e-8)
        np.testing.assert_allclose(val_9, 16.94930937, rtol=1e-5)

    def test_simps_convergence(self):
        """Testing convergence of the Simpson's rule with bigger grids"""

        # We check value of the integral of this function at (0,0):
        def f_1(x, y):
            return np.exp(-np.abs(x) - np.abs(y))

        val_anal_1 = 3.9801945594360824454546733897861818789971930592730

        def f_2(x, y):
            return np.cos(4 * x + 2 * y + 3)

        val_anal_2 = -0.24052304498504700435350585980238394605701172470702

        def f_3(x, y):
            return (1 / (1 + (0.2 * x) ** 2)) * (1 / (1 + (0.2 * y) ** 2))

        val_anal_3 = 76.747770801790682791007016939095890959933301179927

        # Set up different grids:
        spacings = [2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]
        rtols_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rtols_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rtols_3 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        i = 0

        for space in spacings:
            x_range = np.arange(-6.0, 6.0 + space, space)
            y_range = np.arange(-6.0, 6.0 + space, space)
            self.assertAlmostEqual(x_range[-1], 6.0)
            self.assertAlmostEqual(y_range[-1], 6.0)

            z_1 = np.array([[f_1(xp, yp) for yp in y_range] for xp in x_range])
            z_2 = np.array([[f_2(xp, yp) for yp in y_range] for xp in x_range])
            z_3 = np.array([[f_3(xp, yp) for yp in y_range] for xp in x_range])

            val_1 = simps(simps(z_1, x=x_range, axis=0), x=y_range, axis=0)
            val_2 = simps(simps(z_2, x=x_range, axis=0), x=y_range, axis=0)
            val_3 = simps(simps(z_3, x=x_range, axis=0), x=y_range, axis=0)

            rtols_1[i] = np.abs((val_anal_1 - val_1) / val_anal_1)
            rtols_2[i] = np.abs((val_anal_2 - val_2) / val_anal_2)
            rtols_3[i] = np.abs((val_anal_3 - val_3) / val_anal_3)
            i += 1

        def fit(x, a, b):
            return a * x + b

        coeff_1 = curve_fit(fit, np.log(spacings), np.log(rtols_1))[0]
        coeff_2 = curve_fit(fit, np.log(spacings), np.log(rtols_2))[0]
        coeff_3 = curve_fit(fit, np.log(spacings), np.log(rtols_3))[0]
        np.testing.assert_allclose(
            np.mean([coeff_1[0], coeff_2[0], coeff_3[0]]), 4.0, rtol=0.1
        )

    def test_simps_laplacian(self):
        """Testing integration of a Laplacian"""

        x_range = np.linspace(-6.0, 6.0, 400)
        y_range = np.linspace(-6.0, 6.0, 400)
        dx = x_range[1] - x_range[0]
        dy = y_range[1] - y_range[0]

        # Setting up custom test functions:
        def f_1(x, y):
            return np.cos(x + y)  # Purely real function

        def f_2(x, y):
            return np.exp(1j * (x + y))  # Real/imaginary function

        def f_3(x, y):
            return 1j * np.sin(x + y)  # Purely imaginary function

        def f_4(x, y):
            return np.cos(x) * np.cos(y)  # Symmetrical in x and y

        def f_5(x, y):
            return np.cos(x) * np.exp(y)  # Symmetrical in x

        def f_6(x, y):
            return np.exp(x) * np.cos(y)  # Symmetrical in y

        def f_7(x, y):
            return np.exp(x + y)  # Not symmetrical

        def f_8(x, y):
            return sp.legendre(5)(x + y)  # Legendre functions

        def f_9(x, y):
            return sp.j0(x) + 1j * sp.j1(y)  # Bessel functions

        # Defining Laplacian operator:
        nabla = Laplacian(h=[dx, dy], acc=4)

        L_1 = nabla(np.array([[f_1(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_2 = nabla(np.array([[f_2(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_3 = nabla(np.array([[f_3(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_4 = nabla(np.array([[f_4(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_5 = nabla(np.array([[f_5(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_6 = nabla(np.array([[f_6(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_7 = nabla(np.array([[f_7(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_8 = nabla(np.array([[f_8(xp, yp)
                               for yp in y_range] for xp in x_range]))
        L_9 = nabla(np.array([[f_9(xp, yp)
                               for yp in y_range] for xp in x_range]))

        val_1 = simps(simps(L_1, x=x_range, axis=0), x=y_range, axis=0)
        val_2 = simps(simps(L_2, x=x_range, axis=0), x=y_range, axis=0)
        val_3 = simps(simps(L_3, x=x_range, axis=0), x=y_range, axis=0)
        val_4 = simps(simps(L_4, x=x_range, axis=0), x=y_range, axis=0)
        val_5 = simps(simps(L_5, x=x_range, axis=0), x=y_range, axis=0)
        val_6 = simps(simps(L_6, x=x_range, axis=0), x=y_range, axis=0)
        val_7 = simps(simps(L_7, x=x_range, axis=0), x=y_range, axis=0)
        val_8 = simps(simps(L_8, x=x_range, axis=0), x=y_range, axis=0)
        val_9 = simps(simps(L_9, x=x_range, axis=0), x=y_range, axis=0)

        # Comparing calculated results to the analytical:
        np.testing.assert_allclose(val_1, -0.6245841651, rtol=1e-5)
        np.testing.assert_allclose(val_2, -0.6245841651, rtol=1e-5)
        np.testing.assert_allclose(val_3, 0.0, rtol=1e-5, atol=1e-4)
        np.testing.assert_allclose(val_4, -0.6245841656, rtol=1e-5)
        np.testing.assert_allclose(val_5, 0.0, rtol=1e-5, atol=1e-4)
        np.testing.assert_allclose(val_6, 0.0, rtol=1e-5, atol=1e-4)
        np.testing.assert_allclose(val_7, 325505.5828, rtol=1e-5)
        np.testing.assert_allclose(val_8, 0.0, rtol=1e-5, atol=1e-4)
        np.testing.assert_allclose(val_9, 6.640412595, rtol=1e-5)

    def test_simps_laplacian_convergence(self):
        """Testing the convergence rate of Laplacian integration"""

        # Setting up custom test functions:
        def f_1(x, y):
            return np.cos(x + y)

        val_anal_1 = -0.62458416507003158138417882730551286732765138958174

        def f_2(x, y):
            return np.cos(x) * np.cos(y)

        val_anal_2 = -0.62458416507003158138417882730551286732765138958174

        def f_3(x, y):
            return np.exp(x + y)

        val_anal_3 = 325505.58285029626632266682931433818269802963357989

        def f_4(x, y):
            return sp.j0(x) + 1j * sp.j1(y)

        val_anal_4 = 6.6404125950615745961465952731076902097840470031744

        # Set up different grids:
        spacings = [2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]
        rtols_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rtols_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rtols_3 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rtols_4 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        i = 0

        for space in spacings:
            x_range = np.arange(-6.0, 6.0 + space, space)
            y_range = np.arange(-6.0, 6.0 + space, space)
            self.assertAlmostEqual(x_range[-1], 6.0)
            self.assertAlmostEqual(y_range[-1], 6.0)

            # Defining Laplacian operator:
            nabla = Laplacian(h=[space, space], acc=4)

            z_1 = np.array([[f_1(xp, yp) for yp in y_range] for xp in x_range])
            z_2 = np.array([[f_2(xp, yp) for yp in y_range] for xp in x_range])
            z_3 = np.array([[f_3(xp, yp) for yp in y_range] for xp in x_range])
            z_4 = np.array([[f_4(xp, yp) for yp in y_range] for xp in x_range])

            L_1 = nabla(z_1)
            L_2 = nabla(z_2)
            L_3 = nabla(z_3)
            L_4 = nabla(z_4)

            val_1 = simps(simps(L_1, x=x_range, axis=0), x=y_range, axis=0)
            val_2 = simps(simps(L_2, x=x_range, axis=0), x=y_range, axis=0)
            val_3 = simps(simps(L_3, x=x_range, axis=0), x=y_range, axis=0)
            val_4 = simps(simps(L_4, x=x_range, axis=0), x=y_range, axis=0)

            rtols_1[i] = np.abs((val_anal_1 - val_1) / val_anal_1)
            rtols_2[i] = np.abs((val_anal_2 - val_2) / val_anal_2)
            rtols_3[i] = np.abs((val_anal_3 - val_3) / val_anal_3)
            rtols_4[i] = np.abs((val_anal_4 - val_4) / val_anal_4)
            i += 1

        def fit(x, a, b):
            return a * x + b

        coeff_1 = curve_fit(fit, np.log(spacings), np.log(rtols_1))[0]
        coeff_2 = curve_fit(fit, np.log(spacings), np.log(rtols_2))[0]
        coeff_3 = curve_fit(fit, np.log(spacings), np.log(rtols_3))[0]
        coeff_4 = curve_fit(fit, np.log(spacings), np.log(rtols_4))[0]
        np.testing.assert_allclose(
            np.mean([coeff_1[0], coeff_2[0], coeff_3[0], coeff_4[0]]), 4.0, rtol=0.2
        )

    def test_coupling_integration_symm_asym(self):
        """Testing integration of symmetrical/asymmetrical functions"""

        # Setting up custom test functions:
        def f_1(x, y):
            return np.cos(x) * np.cos(y)  # Symmetrical in x and y

        def f_2(x, y):
            return np.cos(x) * np.exp(y)  # Symmetrical in x

        def f_3(x, y):
            return np.exp(x) * np.cos(y)  # Symmetrical in y

        def f_4(x, y):
            return np.exp(x + y)  # Not symmetrical

        # Setting up the system:
        center = ctr.Itp2dCenter(FILEPATH_BIG, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-10.0, 0.0], [-3 * np.pi / 2, 3 * np.pi / 2], [0.0, 5.0], 1.0, "left"
        )
        coupling = cpl.OverlapCoupling(center, lead, MPI.COMM_WORLD)

        # Now we calculate the couplings and compare them to the analytical
        # values:
        coupling._set_custom_test_wf_center(f_1)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_3)
        val_3 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_4)
        val_4 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(np.abs(val_1) ** 2, 182.3858857, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_2) ** 2, 25447.6759, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_3) ** 2, 5.517588586, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_4) ** 2, 769.8501756, rtol=5e-2)

        coupling._set_custom_test_wf_center(f_2)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_3)
        val_3 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_4)
        val_4 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(np.abs(val_1) ** 2, 0.0, atol=1e-9)
        np.testing.assert_allclose(np.abs(val_2) ** 2, 0.0, atol=1e-9)
        np.testing.assert_allclose(np.abs(val_3) ** 2, 0.0, atol=1e-9)
        np.testing.assert_allclose(np.abs(val_4) ** 2, 0.0, atol=1e-9)

        coupling._set_custom_test_wf_center(f_3)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_3)
        val_3 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_4)
        val_4 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(np.abs(val_1) ** 2, 0.0, atol=1e-9)
        np.testing.assert_allclose(np.abs(val_2) ** 2, 0.0, atol=1e-9)
        np.testing.assert_allclose(np.abs(val_3) ** 2, 0.0, atol=1e-9)
        np.testing.assert_allclose(np.abs(val_4) ** 2, 0.0, atol=1e-9)

        coupling._set_custom_test_wf_center(f_4)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_3)
        val_3 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_4)
        val_4 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(np.abs(val_1) ** 2, 769.8501756, rtol=5e-2)
        np.testing.assert_allclose(
            np.abs(val_2) ** 2, 9.538172602e6, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_3) ** 2, 774.5934744, rtol=5e-2)
        np.testing.assert_allclose(
            np.abs(val_4) ** 2, 9.596940405e6, rtol=5e-2)

    def test_coupling_integration_real_imag(self):
        """Testing integration of real/complex valued functions"""

        # Setting up custom test functions:
        def f_1(x, y):
            return np.cos(x + y)  # Purely real function

        def f_2(x, y):
            return np.exp(1j * (x + y))  # Real/imaginary function

        def f_3(x, y):
            return 1j * np.sin(x + y)  # Purely imaginary function

        # Setting up the system:
        center = ctr.Itp2dCenter(FILEPATH_BIG, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-10.0, 0.0], [-4.0, 4.0], [0.0, 5.0], 1.0, "left")
        coupling = cpl.OverlapCoupling(center, lead, MPI.COMM_WORLD)

        # Now we calculate the couplings and compare them to the analytical
        # values:
        coupling._set_custom_test_wf_center(f_1)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_3)
        val_3 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(np.abs(val_1) ** 2, 569.6472594, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_2) ** 2, 569.648751, rtol=5e-2)
        np.testing.assert_allclose(
            np.abs(val_3) ** 2,
            0.001491588856,
            rtol=1.5e-1)

        coupling._set_custom_test_wf_center(f_2)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_3)
        val_3 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(np.abs(val_1) ** 2, 569.648751, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_2) ** 2, 2304.0, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_3) ** 2, 582.3894591, rtol=5e-2)

        coupling._set_custom_test_wf_center(f_3)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_3)
        val_3 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(
            np.abs(val_1) ** 2,
            0.001491588856,
            rtol=1.5e-1)
        np.testing.assert_allclose(np.abs(val_2) ** 2, 582.3894591, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_3) ** 2, 582.3879676, rtol=5e-2)

    def test_coupling_integration_advanced(self):
        """Testing integration of some really complicated functions"""

        # Setting up custom test functions:
        def f_1(x, y):
            return sp.legendre(5)(x + y)  # Legendre functions

        def f_2(x, y):
            return sp.j0(x) + 1j * sp.y0(y)  # Bessel functions

        # Setting up the system:
        center = ctr.Itp2dCenter(FILEPATH_BIG, (0, 0))
        lead = ld.FiniteHarmonicLead(
            [-10.0, 0.0], [1.0, 5.0], [0.0, 5.0], 1.0, "left")
        coupling = cpl.OverlapCoupling(center, lead, MPI.COMM_WORLD)

        # Now we calculate the couplings and compare them to the analytical
        # values:
        coupling._set_custom_test_wf_center(f_1)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(
            np.abs(val_1) ** 2, 5.999904457e16, rtol=5e-2)
        np.testing.assert_allclose(
            np.abs(val_2) ** 2, 5.113055894e8, rtol=5e-2)

        coupling._set_custom_test_wf_center(f_2)

        coupling._set_custom_test_wf_lead(f_1)
        val_1 = coupling.get_coupling_matrix_element(0, 0, test=True)
        coupling._set_custom_test_wf_lead(f_2)
        val_2 = coupling.get_coupling_matrix_element(0, 0, test=True)

        np.testing.assert_allclose(
            np.abs(val_1) ** 2, 3.895563366e7, rtol=5e-2)
        np.testing.assert_allclose(np.abs(val_2) ** 2, 9.64679162, rtol=5e-2)
