#!/usr/bin/env python3
"""
Command line parser for calculating transmission and partial currents of a
coupling system.
"""

import argparse
import os
import sys
from shutil import move

import h5py
from mpi4py import MPI
from tinie.main_routines.calculator import Calculator
from tinie.main_routines.misc import *
# Importing the main system:
from tinie.systems.read_write.system_read import SystemRead


def main():
    CWD = os.getcwd()

    parser = argparse.ArgumentParser(description="""A script for calculating 
    transmission and partial currents through a
    nanostructure connected to multiple leads. Check README.md for more details.""")

    parser.add_argument('--delta-omega', '-dw', type=float, default=1e-2,
                        help="Probe energy grid spacing.")
    parser.add_argument('-eta', type=float, default=1e-1,
                        help="Small imaginary constant eta.")
    parser.add_argument('--chem-pot', '-mu', type=float, default=1.0,
                        help="Chemical potential in the system.")
    parser.add_argument('--temperature', '-T', type=float, default=1.0,
                        help="Temperature of the system.")
    parser.add_argument('--lead-bias', '-V', nargs='+', type=float,
                        default=[0.5, 1.5],
                        help="Bias voltages of the leads.")

    parser.add_argument('--wide-band', dest='wide_band', action='store_true',
                        help="Use wide band approximation. Must provide own "
                             "self energy and rate operators.")
    parser.add_argument('--no-wide-band', dest='wide_band', action='store_false',
                        help="Don't use wide band approximation (default).")
    parser.add_argument('--self-energy', '-S', type=str, default="",
                        help="Path to the .npz file containing the self-energies"
                             " for the wide band approximation.")
    parser.add_argument('--rate-operator', '-G', type=str, default="",
                        help="Path to the .npz file containing the rate operators "
                             "for the wide band approximation. If empty and self "
                             "energy is not, calculates the rate operators based "
                             "on the formula involving self energies.")

    parser.add_argument('--input-file', '-i', type=str,
                        default=CWD + "/tinie_prepare.h5",
                        help="Input file to read coupling data from.")
    parser.add_argument('--output-file', '-o', type=str,
                        default=CWD + "/tinie.h5",
                        help="Output file to write data to.")

    parser.set_defaults(wide_band=False)

    # Reading and checking the parameters:
    args = parser.parse_args()
    delta_w = args.delta_omega
    eta = args.eta
    chem_pot = args.chem_pot
    T = args.temperature
    V_bias = args.lead_bias

    wide_band = args.wide_band
    self_energy_path = args.self_energy
    rate_operator_path = args.rate_operator

    filepath_read = args.input_file
    filepath_write = args.output_file

    comm = MPI.COMM_WORLD

    # Setting up the system:
    if comm.rank == 0:
        print("Initializing the transport calculator...")
    system = SystemRead(comm)
    system.set_file_path(filepath_read)
    delta_E = system.get_lead_energy_spacing()

    try:
        if len(V_bias) != system.get_num_leads():
            raise ValueError("Error: number of potentials inconsistent with the number of leads.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Setting up the calculator:
    calculator = Calculator(chem_pot, T, V_bias, system, delta_w, delta_E, eta,
                            comm, wide_band)

    if wide_band:

        try:
            if self_energy_path == "" and rate_operator_path == "":
                raise ValueError("Error: empty self energy and rate operator path, make sure to specify a "
                                 "path for either self energies or rate operators if you are using "
                                 "wide band approximation.")
        except ValueError as e:
            print(e)
            sys.exit(1)

        if self_energy_path != "" and rate_operator_path == "":
            wide_band_self_energy = np.load(self_energy_path)

            try:
                if len(wide_band_self_energy) != system.get_num_leads(): \
                        raise ValueError("Error: number of self energy matrices not the "
                                         "same as the number of leads.")
            except ValueError as e:
                print(e)
                sys.exit(1)

            wide_band_gamma = []

            for i in range(system.get_num_leads()):
                wide_band_gamma.append(1j * (wide_band_self_energy[i, :, :] -
                                             np.conj(wide_band_self_energy[i, :, :].T)))

        elif rate_operator_path != "" and self_energy_path == "":
            wide_band_gamma = np.load(rate_operator_path)

            try:
                if len(wide_band_gamma) != system.get_num_leads():
                    raise ValueError("Error: number of rate operator matrices not "
                                     "the same as the number of leads.")
            except ValueError as e:
                print(e)
                sys.exit(1)

            wide_band_self_energy = []

            for i in range(system.get_num_leads()):
                wide_band_self_energy.append(-0.5j * wide_band_gamma[i, :, :])

        else:
            wide_band_self_energy = np.load(self_energy_path)
            wide_band_gamma = np.load(rate_operator_path)

            try:
                if len(wide_band_gamma) != system.get_num_leads() or \
                        len(wide_band_self_energy) != system.get_num_leads():
                    raise ValueError("Error: number of rate operator or self energy "
                                     "matrices not the same as the number of leads.")
            except ValueError as e:
                print(e)
                sys.exit(1)

        calculator.set_wide_band_gamma(wide_band_gamma)
        calculator.set_wide_band_self_energy(wide_band_self_energy)

    comm.Barrier()

    if comm.rank == 0:
        print("Calculator is prepared, initializing coupling calculation...")

    total_currents, total_currents_vs_energy, \
    partial_currents, partial_currents_vs_energy, \
    transmat_vs_energy, G_vs_energy, omega_values = calculator.currents()

    comm.Barrier()

    if comm.rank == 0:
        print("Transport calculation complete, saving data...")

        if os.path.exists(filepath_write):
            old_filepath = filepath_write
            new_filepath = filepath_write.rsplit('.', 1)[0] + "_backup." + \
                           filepath_write.rsplit('.', 1)[1]
            print("File with same path detected, moving to " + new_filepath)
            move(old_filepath, new_filepath)

        # Setting up the hdf5 storage
        file = h5py.File(filepath_write, 'w')
        file.attrs["type"] = "TINIEFile"
        file.create_dataset("partial_currents", data=np.real(partial_currents),
                            chunks=True, compression="gzip")
        file.create_dataset("total_currents", data=np.real(total_currents),
                            chunks=True, compression="gzip")
        file.create_dataset("omega_dependent_partial_currents",
                            data=np.real(partial_currents_vs_energy),
                            chunks=True, compression="gzip")
        file.create_dataset("omega_dependent_total_currents",
                            data=np.real(total_currents_vs_energy),
                            chunks=True, compression="gzip")
        file.create_dataset("transmission", data=np.real(transmat_vs_energy),
                            chunks=True, compression="gzip")
        file.create_dataset("transmission_error", data=np.imag(transmat_vs_energy),
                            chunks=True, compression="gzip")
        file.create_dataset("conductance", data=np.real(G_vs_energy),
                            chunks=True, compression="gzip")
        file.create_dataset("omega_values", data=omega_values,
                            chunks=True, compression="gzip")
        file.attrs["evaluated_chemical_potential"] = chem_pot
        file.attrs["evaluated_bias_voltage"] = V_bias
        file.attrs["evaluated_temperature"] = T
        file.attrs["omega_spacing"] = delta_w
        file.attrs["lead_energy_spacing"] = delta_E
        file.attrs["number_of_couplings"] = system.get_num_leads()
        file.attrs["eta"] = eta
        print("Transport data saved at " + filepath_write)
        file.close()

    comm.Barrier()

if __name__ == '__main__':
    main()