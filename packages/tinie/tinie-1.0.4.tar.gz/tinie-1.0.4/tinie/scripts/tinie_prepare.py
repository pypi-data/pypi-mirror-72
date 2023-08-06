#!/usr/bin/env python3
"""
Command line parser for calculating coupling and hamiltonians of a transport
system.
"""

import argparse
import os
import sys

import tinie as tc
from mpi4py import MPI
from tinie.main_routines.misc import *
from tinie.systems.central_region.custom_center import CustomCenter
# Importing the center region types:
from tinie.systems.central_region.itp2d_center import Itp2dCenter
from tinie.systems.couplings.custom_coupling import CustomCoupling
from tinie.systems.couplings.one_layer_coupling import OneLayerCoupling
# Importing the coupling region types:
from tinie.systems.couplings.overlap_coupling import OverlapCoupling
from tinie.systems.couplings.tight_binding_coupling import TightBindingCoupling
from tinie.systems.leads.box_lead import BoxLead
from tinie.systems.leads.custom_lead import CustomLead
# Importing the lead region types:
from tinie.systems.leads.finite_harmonic_lead import FiniteHarmonicLead
# Importing the main system:
from tinie.systems.read_write.system_write import SystemWrite


def main():
    CWD = os.getcwd()

    ctr = {'itp2d': Itp2dCenter,
           'custom': CustomCenter}

    ld = {'finharm': FiniteHarmonicLead,
          'box': BoxLead,
          'custom': CustomLead}

    cpl = {'overlap': OverlapCoupling,
           'tightbind': TightBindingCoupling,
           'onelayer': OneLayerCoupling,
           'custom': CustomCoupling}



    parser = argparse.ArgumentParser(description="""A script for calculating 
    Hamiltonains and couplings of a transport system. Check README.md for more 
    details.""")

    parser.add_argument('--delta-E', '-dE', type=float, default=1e-3,
                        help="Lead region energy grid spacing.")
    parser.add_argument('-B', type=float, default=0.0,
                        help="Magnetic field strength.")
    parser.add_argument('--x-axis-limits', '-xlim', nargs='+',
                        type=str, default=["[-10.0, -4.0]", "[4.0, 10.0]"],
                        help="Lead x-axis boundaries, specified as pairs of "
                             "floats of the form '[xmin, xmax]'.")
    parser.add_argument('--y-axis-limits', '-ylim', nargs='+',
                        type=str, default=["[-5.0, 5.0]", "[-5.0, 5.0]"],
                        help="Lead y-axis boundaries, specified as pairs of "
                             "floats of the form '[ymin, ymax]'.")
    parser.add_argument('--energy-limits', '-Elim', nargs='+',
                        type=str, default=["[0.0, 2.0]", "[0.0, 2.0]"],
                        help="Lead energy boundaries, specified as pairs of "
                             "floats of the form '[Emin, Emax]'.")
    parser.add_argument('--center-type', '-ctr', type=str,
                        default="itp2d(" + tc.__path__[0] +
                                "/test_files/itp2d_test.h5,(0,4))",
                        help="""Central region type, takes a string as input and 
                        currently supports the following: (1) 
                        'itp2d(FILENAME,STATES)': import of the central region 
                        states from itp2d software package, FILENAME is the full 
                        path to the itp2d .h5 file, and STATES is a pair of 
                        integers of form (state_init, state_fin) that defines the 
                        range of states to be imported. (2) 'custom(FILENAME)': 
                        import of the custom central region Hamiltonian, FILENAME 
                        is the full path to a .npy file containing the Hamiltonian 
                        array. Check README.md for more details.""")
    parser.add_argument('--lead-number', '-l', type=int, default=2,
                        help="Number of leads in the simulation.")
    parser.add_argument('--lead-types', '-ld', nargs='+', type=str,
                        default=["finharm(left, 1.0, dir)",
                                 "finharm(right, 1.0, dir)"],
                        help="""Types of leads in the simulation, with their 
                        additional arguments, typed as a sequence of strings 
                        corresponding to the lead types. 
                        Currently supports the following: 
                        (1) 'finharm(ALIGNMENT,W0,BOUNDARY)': finite harmonic 
                        lead with particle-in-a-box potential in one 
                        dimension and harmonic oscillator potential of 
                        frequency W0 in the other, with ALIGNMENT 
                        corresponding to position of the lead in relation 
                        to the central region (up/down/left/right), and 
                        BOUNDARY (dir/neu) corresponding to 
                        Dirichlet/Neumann boundary conditions used for the 
                        eigenfunctions. (2) 'box(ALIGNMENT)': lead that is 
                        confined with a particle-in-a-box potential in 
                        both x- and y-dimensions, with ALIGNMENT parameter 
                        similar to that of finharm. (3) 'custom(FILENAME)': 
                        custom lead Hamiltonian imported from the .npy 
                        file located at FILENAME. Check README.md for more 
                        details.""")
    parser.add_argument('--coupling-types', '-cpl', nargs='+', type=str,
                        default=["overlap()", "overlap()"],
                        help="""Types of the coupling regions for the leads. Typed 
                        as a sequence of strings corresponding to the overlap type 
                        between each lead and the center. The following are currently 
                        supported: (1) 'overlap()': coupling based on computing the 
                        overlap integral between the lead and the central region, 
                        so they must spatially overlap. (2) 'tightbind()': 
                        calculates coupling using the tight binding method, for 
                        which the lead and center regions must not overlap. 
                        (3) 'onelayer()': version of the tight binding coupling 
                        method optimised for computing coupling between two 1D 
                        layers of the lead and central region, which must not 
                        overlap. (4) 'custom(FILENAME)': import custom coupling 
                        matrix from a .npy file located at FILENAME. Check 
                        README.md for more details.""")
    parser.add_argument('--output-file', '-o', type=str,
                        default=CWD + '/tinie_prepare.h5',
                        help="Output file to write data to.")

    # Reading and checking the parameters:
    args = parser.parse_args()
    ld_num = args.lead_number
    delta_E = args.delta_E
    B = args.B

    xlims = []
    for arg in args.x_axis_limits:
        xlims.append(handle_list_string(arg))
    ylims = []
    for arg in args.y_axis_limits:
        ylims.append(handle_list_string(arg))
    Elims = []
    for arg in args.energy_limits:
        Elims.append(handle_list_string(arg))
    ctr_args = handle_function_string(args.center_type)
    ld_args = args.lead_types
    cpl_args = args.coupling_types

    # Some input sanity checks:
    try:
        if len(xlims) != ld_num:
            raise ValueError("Error: number of x-axis boundaries inconsistent with number of leads.")
        if len(ylims) != ld_num:
            raise ValueError("Error: number of y-axis boundaries inconsistent with number of leads.")
        if len(Elims) != ld_num:
            raise ValueError("Error: number of energy boundaries inconsistent with number of leads.")
        if ld_num == False:
            raise ValueError("Error: invalid number of leads, only integer values!")
        if len(ld_args) != ld_num:
            raise ValueError("Error: lead parameters inconsistent with number of leads.")
        if ld_num != len(cpl_args):
            raise ValueError("Error: number of coupling regions inconsistent with number of lead regions.")
        if ctr_args[0] not in ctr.keys():
            raise ValueError("Error: invalid central region type.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    filename_write = args.output_file

    # Setting up the communicator:
    comm = MPI.COMM_WORLD

    # Setting up the system:
    if comm.rank == 0:
        print("Initializaing the coupling system...")

    system = SystemWrite(comm)
    system.set_file_path(filename_write)
    center = ctr[ctr_args[0]](*ctr_args[1:])
    system.add_central_region(center)

    comm.Barrier()

    for i in range(ld_num):
        ld_params = handle_function_string(ld_args[i])
        cpl_params = handle_function_string(cpl_args[i])

        try:
            if ld_params[0] not in ld.keys():
                raise ValueError("Error: invalid Lead %s region type." % i)
            if cpl_params[0] not in cpl.keys():
                raise ValueError("Error: invalid Coupling %s region type." % i)
        except ValueError as e:
            print(e)
            sys.exit(1)

        lead = ld[ld_params[0]](xlims[i], ylims[i], Elims[i], delta_E,
                                *ld_params[1:])
        lead.set_magnetic_field_strength(B)

        coupling = cpl[cpl_params[0]](center, lead, *cpl_params[1:], comm)
        system.add_coupling_region(coupling)

    comm.Barrier()

    if comm.rank == 0:
        print("System prepared, initializing coupling calculation...")

    system.dump()

    comm.Barrier()

    if comm.rank == 0:
        print("Coupling calculation complete, data saved at " + filename_write)

if __name__ == '__main__':
    main()