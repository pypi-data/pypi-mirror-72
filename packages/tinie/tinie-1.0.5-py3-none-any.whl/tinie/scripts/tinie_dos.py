#!/usr/bin/env python3
"""
Command line parser for calculating DOS and LDOS of a coupling system.
"""

import argparse
import os
import sys
from shutil import move

import h5py
import tinie as tc
from mpi4py import MPI
from tinie.main_routines.calculator import Calculator
from tinie.main_routines.misc import *
from tinie.systems.central_region.itp2d_center import Itp2dCenter
# Importing the main system:
from tinie.systems.read_write.system_read import SystemRead


def main():
    CWD = os.getcwd()

    parser = argparse.ArgumentParser(description="""A script for calculating 
    density of states and local density of states through a
    nanostructure connected to multiple leads. Check README.md for more 
    details.""")

    parser.add_argument('--omega-ldos', '-w', nargs='+', type=float, default=[0.0, 1.0, 2.0],
                        help="Energies to evaluate LDOS at.")
    parser.add_argument('--delta-omega', '-dw', type=float, default=1e-2,
                        help="Probe energy grid spacing.")
    parser.add_argument('-eta', type=float, default=1e-1,
                        help="Small imaginary constant eta.")
    parser.add_argument('--chem-pot', '-mu', type=float, default=1.0,
                        help="Chemical potential of the system.")
    parser.add_argument('--temperature', '-T', type=float, default=1.0,
                        help="Temperature of the system.")
    parser.add_argument('--lead-bias', '-V', nargs='+', type=float, default=[0.5, 1.5],
                        help="Bias voltages of the leads.")

    parser.add_argument('--input-file', '-i', type=str,
                        default=CWD + "/tinie_prepare.h5",
                        help="Input file to read coupling data from.")
    parser.add_argument('--wf-file', '-psi', type=str, default=tc.__path__[0] + "/test_files/itp2d_test.h5",
                        help="Path to the file that contains wavefunctions "
                             "required for LDOS computation.")
    parser.add_argument('--wf-range', nargs=2, type=int, default=[0, 4],
                        help="Range of states to extract from the wavefunction "
                             "file required for LDOS.")
    parser.add_argument('--output-file', '-o', type=str,
                        default=CWD + "/tinie_dos.h5",
                        help="Output file to write data to.")

    parser.add_argument('--dos', dest='dos', action='store_true',
                        help="Evaluate DOS (default).")
    parser.add_argument('--ldos', dest='ldos', action='store_true',
                        help="Evaluate LDOS (default).")
    parser.add_argument('--no-dos', dest='dos', action='store_false',
                        help="Don't evaluate DOS.")
    parser.add_argument('--no-ldos', dest='ldos', action='store_false',
                        help="Don't evaluate LDOS.")

    parser.set_defaults(dos=True)
    parser.set_defaults(ldos=True)

    # Reading and checking the parameters:
    args = parser.parse_args()
    w = np.array(args.omega_ldos)
    delta_w = args.delta_omega
    eta = args.eta
    eval_dos = args.dos
    eval_ldos = args.ldos

    chem_pot = args.chem_pot
    T = args.temperature
    V_bias = args.lead_bias

    filepath_read = args.input_file
    filepath_dos_write = args.output_file

    filepath_wf = args.wf_file
    wf_range = args.wf_range

    comm = MPI.COMM_WORLD

    # Setting up the system:
    if comm.rank == 0:
        print("Initializing the transport calculator...")
    system = SystemRead(comm)
    system.set_file_path(filepath_read)
    delta_E = system.get_lead_energy_spacing()

    try:
        if system.get_center_type() != "Itp2dCenter":
            raise ValueError("Error: currently, only Itp2dCenter center objects are LDOS compatible.")
        if comm.size != 1 and eval_ldos:
            raise ValueError("Error: currently, LDOS is not parallelised.")
        if len(V_bias) != system.get_num_leads():
            raise ValueError("Error: number of potentials inconsistent with the number of leads.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Setting up the calculator:
    calculator = Calculator(chem_pot, T, V_bias, system, delta_w, delta_E, eta,
                            comm, False)

    comm.Barrier()

    if comm.rank == 0:
        print("Calculator is prepared, initializing DOS/LDOS calculation...")

    omega_values = calculator.get_omega_range()
    if eval_dos:
        dos_values = calculator.get_dos()
    else:
        dos_values = np.array([])

    if eval_ldos:
        if comm.rank == 0:
            ctr = Itp2dCenter(filepath_wf, tuple(wf_range))
            psi = ctr.get_states()
            x, y = ctr.get_coordinate_ranges()
            x_size = len(x)
            y_size = len(y)
            num_states = wf_range[1] - wf_range[0] + 1
        else:
            x_size = None
            y_size = None
            num_states = None

        x_size = comm.bcast(x_size, root=0)
        y_size = comm.bcast(y_size, root=0)
        num_states = comm.bcast(num_states, root=0)

        comm.Barrier()

        if comm.rank != 0:
            psi = np.zeros((x_size, y_size, num_states), dtype=np.complex128)

        comm.Bcast(psi, root=0)
        comm.Bcast(x, root=0)
        comm.Bcast(y, root=0)

        comm.Barrier()

        ldos_values_partial = calculator.get_ldos(psi, w)
        ldos_values = np.zeros(ldos_values_partial.shape)
        comm.Reduce(ldos_values_partial, ldos_values, MPI.SUM, 0)

    else:
        x = np.array([])
        y = np.array([])
        ldos_values = np.array([])

    comm.Barrier()

    if comm.rank == 0:
        print("DOS/LDOS calculation complete, saving data...")

        if os.path.exists(filepath_dos_write):
            old_filepath = filepath_dos_write
            new_filepath = filepath_dos_write.rsplit('.', 1)[0] + "_backup." + \
                           filepath_dos_write.rsplit('.', 1)[1]
            print("File with same path detected, moving to " + new_filepath)
            move(old_filepath, new_filepath)

        # Setting up the hdf5 storage
        file = h5py.File(filepath_dos_write, 'w')
        file.attrs["type"] = "TINIEDOSFile"

        file.create_dataset("dos", data=dos_values,
                            chunks=True, compression="gzip")
        file.create_dataset("ldos", data=ldos_values,
                            chunks=True, compression="gzip")
        file.create_dataset("x", data=x,
                            chunks=True, compression="gzip")
        file.create_dataset("y", data=y,
                            chunks=True, compression="gzip")
        file.create_dataset("omega_dos", data=omega_values,
                            chunks=True, compression="gzip")
        file.create_dataset("omega_ldos", data=w, chunks=True,
                            compression="gzip")
        print("DOS/LDOS data saved at " + filepath_dos_write)
        file.close()

    comm.Barrier()

if __name__ == '__main__':
    main()
