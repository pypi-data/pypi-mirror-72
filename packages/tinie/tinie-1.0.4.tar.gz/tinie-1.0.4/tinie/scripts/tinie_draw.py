#!/usr/bin/env python3
"""
Command line script for drawing the transmission-energy figures.
"""

import argparse
import os
import sys

import h5py
from matplotlib import rc
from scipy.optimize import curve_fit
from tinie.main_routines.calculator import Calculator
from tinie.main_routines.misc import *
from tinie.systems.central_region.custom_center import CustomCenter
from tinie.systems.couplings.custom_coupling import CustomCoupling
from tinie.systems.leads.custom_lead import CustomLead
from tinie.systems.read_write.system_read import SystemRead
from tinie.systems.read_write.system_write import SystemWrite


def main():
    CWD = os.getcwd()

    rc('font', **{'family': 'serif'})
    rc('text', usetex=True)

    parser = argparse.ArgumentParser(description="""A script for plotting 
    the results of the transport calculations. Check README.md for more 
    details.""")
    parser.add_argument('--input-file', '-i', type=str,
                        default=CWD + "/tinie.h5",
                        help="Input file to read coupling data from.")
    parser.add_argument('--input-dos-file', '-idos', type=str,
                        default=CWD + "/tinie_dos.h5",
                        help="Input file to read DOS data from.")
    parser.add_argument('--output-file', '-o', type=str,
                        default=CWD + "/tinie_draw.pdf",
                        help="Output file to write data to.")
    parser.add_argument('--energy-range', '-E', nargs=2, type=float,
                        default=[0.0, 5.0], help="Range of energies to plot.")

    parser.add_argument('--transmission', dest='transmission', action='store_true',
                        help="Plot transmission as a function of probe energy.")
    parser.add_argument('--conductance', dest='conductance', action='store_true',
                        help="Plot conductance as a function of probe energy.")
    parser.add_argument('--backscattering', dest='backscattering', action='store_true',
                        help="Plot backscatterring as a function of probe energy.")
    parser.add_argument('--partial-currents', dest='partial_currents', action='store_true',
                        help="Plot partial currents as a function of probe energy.")
    parser.add_argument('--total-currents', dest='total_currents', action='store_true',
                        help="Plot total currents as a function of probe energy.")
    parser.add_argument('--dos', dest='dos', action='store_true',
                        help="Plot density of states as a function of probe energy.")
    parser.add_argument('--ldos', dest='ldos', action='store_true',
                        help="Plot local density of states")

    parser.add_argument('--no-transmission', dest='transmission', action='store_false',
                        help="Don't plot transmission as a function of probe energy.")
    parser.add_argument('--no-conductance', dest='conductance', action='store_false',
                        help="Don't plot conductance as a function of probe energy.")
    parser.add_argument('--no-backscattering', dest='backscattering', action='store_false',
                        help="Don't plot backscatterring as a function of probe energy.")
    parser.add_argument('--no-partial-currents', dest='partial_currents', action='store_false',
                        help="Don't plot partial currents as a function of probe energy.")
    parser.add_argument('--no-total-currents', dest='total_currents', action='store_false',
                        help="Don't plot total currents as a function of probe energy.")
    parser.add_argument('--no-dos', dest='dos', action='store_false',
                        help="Don't plot density of states as a function of probe energy.")
    parser.add_argument('--no-ldos', dest='ldos', action='store_false',
                        help="Don't plot local density of states.")

    parser.add_argument('--norm-ldos', dest='norm_ldos', action='store_true',
                        help="Normalize LDOS, so that max LDOS value is 1.")
    parser.add_argument('--no-norm-ldos', dest='norm_ldos', action='store_false',
                        help="Don't normalize LDOS.")
    parser.add_argument('--ldos-E', type=float,
                        help="Evaluate LDOS at the probe energy that "
                             "is the closest to the one specified.")
    parser.add_argument('--ldos-idx', type=int,
                        help="Evaluate LDOS at the specified probe energy "
                             "index.")

    parser.add_argument('--stability', dest='stability', action='store_true',
                        help="Make numerical stability figures of the transport code.")
    parser.add_argument('--no-stability', dest='stability', action='store_false',
                        help="Don't numerical stability figures of the transport code.")

    parser.set_defaults(transmission=False)
    parser.set_defaults(conductance=False)
    parser.set_defaults(backscattering=False)
    parser.set_defaults(partial_currents=False)
    parser.set_defaults(total_currents=False)
    parser.set_defaults(dos=False)
    parser.set_defaults(ldos=False)
    parser.set_defaults(stability=False)

    args = parser.parse_args()
    omega_range = args.energy_range
    filepath_read = args.input_file
    filepath_dos_read = args.input_dos_file
    filepath_write = args.output_file
    plot_tr = args.transmission
    plot_G = args.conductance
    plot_bs = args.backscattering
    plot_pI = args.partial_currents
    plot_tI = args.total_currents
    plot_dos = args.dos
    plot_ldos = args.ldos
    norm_ldos = args.norm_ldos
    ldos_E = args.ldos_E
    ldos_idx = args.ldos_idx
    plot_num_stability = args.stability

    if not (plot_tr or plot_pI or plot_tI or plot_bs or plot_G
            or plot_dos or plot_ldos or plot_num_stability):
        print("Quitting the program since there is nothing to plot.")
        sys.exit(0)

    # Read the input file:
    try:
        if not os.path.exists(filepath_read):
            raise ValueError("Error: file " + filepath_read + " does not exist.")
        file = h5py.File(filepath_read, 'r')
        if file.attrs["type"] != "TINIEFile":
            raise ValueError("Error: file must be a TINIEFile type.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    if plot_dos or plot_ldos:

        try:
            if not os.path.exists(filepath_read):
                raise ValueError(
                        "Error: file " + filepath_read + " does not exist.")
            file_dos = h5py.File(filepath_dos_read, 'r')
            if file_dos.attrs["type"] != "TINIEDOSFile":
                raise ValueError("Error: file must be a TINIEDOSFile type.")
        except ValueError as e:
            print(e)
            sys.exit(1)

    # Extract the data:
    omega = file["omega_values"][:]
    chem_pot = file.attrs["evaluated_chemical_potential"]
    V_bias = file.attrs["evaluated_bias_voltage"]
    temperature = file.attrs["evaluated_temperature"]
    num_couplings = file.attrs["number_of_couplings"]
    eta = file.attrs["eta"]
    data = r"$\mu=" + str(chem_pot) + r",V_{\mathrm{bias}}=" + str(list(V_bias)) + ",T=" + \
           str(temperature) + r",\eta=" + str(eta) + "$"

    if plot_tr:
        print("Plotting transmission...")
        T = file["transmission"][:]
        fig_T = get_figure(500)
        ax_T = fig_T.add_subplot(111)

        for i in range(num_couplings):
            for j in range(num_couplings):
                if i != j:
                    label = r'$\mathcal{T}_{' + str(i) + str(j) + '}$'
                    ax_T.plot(omega, T[i, j, :], linewidth=0.4, label=label)

        ax_T.set_xlim(omega_range[0], omega_range[1])
        ax_T.legend()
        ax_T.set_xlabel(r'$\omega$, probe energy (a.u.)')
        ax_T.set_ylabel(r'$\mathcal{T}$, transmission')
        ax_T.set_title(r'Transmission, ' + data)

        axes_real_aspect_ratio_to_golden(ax_T)

        fig_T.tight_layout(pad=1)
        plotpath = filepath_write.split('.')
        plotpath = plotpath[0] + "_transmission." + plotpath[1]
        plt.savefig(plotpath)
        print("Transmission plot saved at " + plotpath)

    if plot_G:
        print("Plotting conductance...")
        G = file["conductance"][:]
        fig_G = get_figure(500)
        ax_G = fig_G.add_subplot(111)

        for i in range(num_couplings):
            for j in range(num_couplings):
                if i != j:
                    label = r'$\mathcal{G}_{' + str(i) + str(j) + '}$'
                    ax_G.plot(omega, G[i, j, :], linewidth=0.4, label=label)

        ax_G.set_xlim(omega_range[0], omega_range[1])
        ax_G.legend()
        ax_G.set_xlabel(r'$\omega$, probe energy (a.u.)')
        ax_G.set_ylabel(r'$\mathcal{G}$, conductance')
        ax_G.set_title(r'Conductance, ' + data)

        axes_real_aspect_ratio_to_golden(ax_G)

        fig_G.tight_layout(pad=1)
        plotpath = filepath_write.split('.')
        plotpath = plotpath[0] + "_conductance." + plotpath[1]
        plt.savefig(plotpath)
        print("Conductance plot saved at " + plotpath)

    if plot_bs:
        print("Plotting backscattering...")
        T = file["transmission"][:]
        fig_T = get_figure(500)
        ax_T = fig_T.add_subplot(111)

        for i in range(num_couplings):
            label = r'$\mathcal{T}_{' + str(i) + str(i) + '}$'
            ax_T.plot(omega, T[i, i, :], linewidth=0.4, label=label)

        ax_T.set_xlim(omega_range[0], omega_range[1])
        ax_T.legend()
        ax_T.set_xlabel(r'$\omega$, probe energy (a.u.)')
        ax_T.set_ylabel(r'$\mathcal{T}$, backscattering')
        ax_T.set_title(r'Backscattering, ' + data)

        axes_real_aspect_ratio_to_golden(ax_T)

        fig_T.tight_layout(pad=1)
        plotpath = filepath_write.split('.')
        plotpath = plotpath[0] + "_backscattering." + plotpath[1]
        plt.savefig(plotpath)
        print("Backscattering plot saved at " + plotpath)

    if plot_pI:
        print("Plotting partial currents...")
        energy_dependent_partial_currents = file["omega_dependent_partial_currents"][:]
        partial_currents = file["partial_currents"][:]
        fig_pI = get_figure(500)
        ax_pI = fig_pI.add_subplot(111)

        for i in range(num_couplings):
            for j in range(num_couplings):
                label = r"$i'_{" + str(i) + str(j) + "}, i_{" + \
                        str(i) + str(j) + "}=" + str(partial_currents[i, j]) + "$"
                ax_pI.plot(omega, energy_dependent_partial_currents[i, j, :],
                           linewidth=0.4, label=label)

        ax_pI.set_xlim(omega_range[0], omega_range[1])
        ax_pI.legend()
        ax_pI.set_xlabel(r'$\omega$, probe energy (a.u.)')
        ax_pI.set_ylabel(r"$i'$, partial current profile (a.u.)")
        ax_pI.set_title(r"Energy profile ($i'$) of partial current $i$, " + data)

        axes_real_aspect_ratio_to_golden(ax_pI)

        fig_pI.tight_layout(pad=1)
        plotpath = filepath_write.split('.')
        plotpath = plotpath[0] + "_partial_current." + plotpath[1]
        plt.savefig(plotpath)
        print("Partial currents plot saved at " + plotpath)

    if plot_tI:
        print("Plotting total currents...")
        energy_dependent_total_currents = file["omega_dependent_total_currents"][:]
        total_currents = file["total_currents"][:]
        fig_tI = get_figure(500)
        ax_tI = fig_tI.add_subplot(111)

        for i in range(num_couplings):
            label = r"$I'_{" + str(i) + "}, I_{" + \
                    str(i) + "}=" + str(total_currents[i]) + "$"
            ax_tI.plot(omega, energy_dependent_total_currents[i, :],
                       linewidth=0.4, label=label)

        ax_tI.set_xlim(omega_range[0], omega_range[1])
        ax_tI.legend()
        ax_tI.set_xlabel(r'$\omega$, probe energy (a.u.)')
        ax_tI.set_ylabel(r"$I'$, total current profile (a.u.)")
        ax_tI.set_title(r"Energy profile ($I'$) of total current $I$, " + data)

        axes_real_aspect_ratio_to_golden(ax_tI)

        fig_tI.tight_layout(pad=1)
        plotpath = filepath_write.split('.')
        plotpath = plotpath[0] + "_total_current." + plotpath[1]
        plt.savefig(plotpath)
        print("Total currents plot saved at " + plotpath)

    if plot_dos:
        print("Plotting density of states...")
        dos_values = file_dos["dos"][:]
        fig_g = get_figure(500)
        ax_g = fig_g.add_subplot(111)

        ax_g.plot(omega, dos_values, linewidth=0.4)

        ax_g.set_xlim(omega_range[0], omega_range[1])
        ax_g.set_xlabel(r'$\omega$, probe energy (a.u.)')
        ax_g.set_ylabel(r"DOS")
        ax_g.set_title(r'DOS, ' + data)

        axes_real_aspect_ratio_to_golden(ax_g)

        fig_g.tight_layout(pad=1)
        plotpath = filepath_write.split('.')
        plotpath = plotpath[0] + "_dos." + plotpath[1]
        plt.savefig(plotpath)
        print("Density of states plot saved at " + plotpath)

    if plot_ldos:
        print("Plotting local density of states...")
        ldos_values = file_dos["ldos"][:]
        ldos_omega = file_dos["omega_ldos"][:]
        x = file_dos["x"][:]
        y = file_dos["y"][:]

        if ldos_E is not None:
            idx = (np.abs(ldos_omega - ldos_E)).argmin()

        elif ldos_idx is not None:
            idx = ldos_idx

        fig_rho = get_figure(500)
        ax_rho = fig_rho.add_subplot(111)

        if norm_ldos:
            plt.pcolormesh(x, y, ldos_values[:, :, idx] / np.amax(ldos_values[:, :, idx]),
                           cmap=plt.cm.plasma, shading='gouraud')

        else:
            plt.pcolormesh(x, y, ldos_values[:, :, idx], cmap=plt.cm.plasma, shading='gouraud')

        plt.colorbar()
        ax_rho.set_xlabel(r'$x$ (a.u.)')
        ax_rho.set_ylabel(r'$y$ (a.u.)')
        ax_rho.set_title(r'LDOS, ' + data +
                         r', $\omega=$' + "{0:.4f}".format(ldos_omega[idx]))

        fig_rho.tight_layout(pad=1)
        plotpath = filepath_write.split('.')
        plotpath = plotpath[0] + "_ldos." + plotpath[1]
        plt.savefig(plotpath)
        print("Local density of states plot saved at " + plotpath)

    if plot_num_stability:
        print("Plotting numerical stability of a one-state system...")

        fig_num_1 = get_figure(500)
        ax_num_1 = fig_num_1.add_subplot(111)

        ctr = CustomCenter("tinie/test_files/HC_system_1_test.npy")
        ld0 = CustomLead(None, None, None, None,
                         "tinie/test_files/HL0_system_3_test.npy")
        ld1 = CustomLead(None, None, None, None,
                         "tinie/test_files/HL1_system_3_test.npy")
        cpl0 = CustomCoupling(ctr, ld0,
                              "tinie/test_files/VL0_system_3_test.npy")
        cpl1 = CustomCoupling(ctr, ld1,
                              "tinie/test_files/VL1_system_3_test.npy")
        sys = SystemWrite()
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)

        mu = 0.0
        T = 0.0
        VL = 750.0
        VR = 250.0

        calc = Calculator(mu, T, [VL, VR], sys, 1e-2, 1e-3, 1e-1)
        omega_vals = calc.get_omega_range()
        total_currents, total_currents_vs_energy, partial_currents, \
        partial_currents_vs_energy, transmat_vs_energy, omega_values = \
            calc.currents(mu, T, [VL, VR])
        deltas = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
        rtols = [0.0] * 7
        val_anal = total_currents[0]

        for i in np.arange(1, 8):
            sys.set_coupling_perturbation(deltas[i - 1])

            calc = Calculator(mu, T, [VL, VR], sys, 1e-2, 1e-3, 1e-1)
            omega_vals = calc.get_omega_range()
            total_currents, total_currents_vs_energy, partial_currents, \
            partial_currents_vs_energy, transmat_vs_energy, omega_values = \
                calc.currents(mu, T, [VL, VR])

            rtols[i - 1] = np.abs((val_anal - total_currents[0]) / val_anal)

        def fit(x, a, b):
            return a * x + b

        coeff = curve_fit(fit, np.log(deltas), np.log(rtols))[0]
        print("The convergence power is " + str(coeff[0]))
        ax_num_1.plot(deltas, rtols)
        ax_num_1.set_title(r"Numerical stability of a custom one-state system")
        ax_num_1.set_xlabel(r"Perturbation magnitude $\Delta$")
        ax_num_1.set_ylabel(r"Relative tolerance")

        axes_real_aspect_ratio_to_golden(ax_num_1)
        fig_num_1.tight_layout(pad=1)
        plt.savefig("figures/one_state_stability.pdf")
        print("One-state stability plot saved at figures/one_state_stability.pdf")

        print("Plotting numerical stability of a two-state system...")

        fig_num_2 = get_figure(500)
        ax_num_2 = fig_num_2.add_subplot(111)

        ctr = CustomCenter(
                "tinie/test_files/HC_system_2_test.npy")
        ld0 = CustomLead(None, None, None, None,
                         "tinie/test_files/HL0_system_2_test.npy")
        ld1 = CustomLead(None, None, None, None,
                         "tinie/test_files/HL1_system_2_test.npy")
        cpl0 = CustomCoupling(ctr, ld0,
                              "tinie/test_files/VL0_system_2_test.npy")
        cpl1 = CustomCoupling(ctr, ld1,
                              "tinie/test_files/VL1_system_2_test.npy")
        sys = SystemWrite()
        sys.add_central_region(ctr)
        sys.add_coupling_region(cpl0)
        sys.add_coupling_region(cpl1)

        mu = 0.0
        T = 0.0
        VL = 1000.0
        VR = 0.0

        calc = Calculator(mu, T, [VL, VR], sys, 1e-2, 1e-3, 1e-1)
        omega_vals = calc.get_omega_range()
        total_currents, total_currents_vs_energy, partial_currents, \
        partial_currents_vs_energy, transmat_vs_energy, omega_values = \
            calc.currents(mu, T, [VL, VR])
        deltas = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
        rtols = [0.0] * 7
        val_anal = total_currents[0]

        for i in np.arange(1, 8):
            sys.set_coupling_perturbation(deltas[i - 1])

            calc = Calculator(mu, T, [VL, VR], sys, 1e-2, 1e-3, 1e-1)
            omega_vals = calc.get_omega_range()
            total_currents, total_currents_vs_energy, partial_currents, \
            partial_currents_vs_energy, transmat_vs_energy, omega_values = \
                calc.currents(mu, T, [VL, VR])

            rtols[i - 1] = np.abs((val_anal - total_currents[0]) / val_anal)

        coeff = curve_fit(fit, np.log(deltas), np.log(rtols))[0]
        print("The convergence power is " + str(coeff[0]))
        ax_num_2.plot(deltas, rtols)
        ax_num_2.set_title(r"Numerical stability of a custom two-state system")
        ax_num_2.set_xlabel(r"Perturbation magnitude $\Delta$")
        ax_num_2.set_ylabel(r"Relative tolerance")

        axes_real_aspect_ratio_to_golden(ax_num_2)
        fig_num_2.tight_layout(pad=1)

        plt.savefig("figures/two_state_stability.pdf")
        print("Two-state stability plot saved at figures/two_state_stability.pdf")

        print("Plotting numerical stability of a real system...")

        fig_num_3 = get_figure(500)
        ax_num_3 = fig_num_3.add_subplot(111)

        sys = SystemRead()
        sys.set_file_path("tinie/test_files/tinie_prepare.h5")
        mu = 0.0
        T = 0.0
        VL = 750.0
        VR = 250.0
        calc = Calculator(mu, T, [VL, VR], sys, 1e-2, 1e-3, 1e-1)
        omega_vals = calc.get_omega_range()
        total_currents, total_currents_vs_energy, partial_currents, \
        partial_currents_vs_energy, transmat_vs_energy, omega_values = \
            calc.currents(mu, T, [VL, VR])
        deltas = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
        rtols = [0.0] * 7
        val_anal = total_currents[0]

        for i in np.arange(1, 8):
            sys = SystemRead()
            sys.set_file_path("tinie/test_files/tinie_prepare.h5")
            sys.set_coupling_perturbation(deltas[i - 1])

            calc = Calculator(mu, T, [VL, VR], sys, 1e-2, 1e-3, 1e-1)
            omega_vals = calc.get_omega_range()
            total_currents, total_currents_vs_energy, partial_currents, \
            partial_currents_vs_energy, transmat_vs_energy, omega_values = \
                calc.currents(mu, T, [VL, VR])

            rtols[i - 1] = np.abs((val_anal - total_currents[0]) / val_anal)

        coeff = curve_fit(fit, np.log(deltas), np.log(rtols))[0]
        print("The convergence power is " + str(coeff[0]))
        ax_num_3.plot(deltas, rtols)
        ax_num_3.set_title(r"Numerical stability of a system read from tinie_prepare file")
        ax_num_3.set_xlabel(r"Perturbation magnitude $\Delta$")
        ax_num_3.set_ylabel(r"Relative tolerance")

        axes_real_aspect_ratio_to_golden(ax_num_3)
        fig_num_3.tight_layout(pad=1)

        plt.savefig("figures/preptinie_stability.pdf")
        print("Real system stability plot saved at figures/preptinie_stability.pdf")

    file.close()


if __name__ == '__main__':
    main()