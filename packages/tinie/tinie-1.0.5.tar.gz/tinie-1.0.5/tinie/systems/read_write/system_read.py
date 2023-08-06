#!/usr/bin/env python3
"""
This file contains the implementation of SystemRead class, which is used to
read data from a SystemDump-generated hdf5 file and to pass that data on to
the transport calculator.
"""

import h5py
from mpi4py import MPI

if MPI.COMM_WORLD.Get_size() > 1 and not h5py.get_config().mpi:
    print("Your HDF5 is not compatible with MPI")
    exit(1)

import numpy as np
from tinie.systems.read_write.system import System


class SystemRead(System):
    """
    An interface for handling system-dependent code
    such as implementation of leads, lead-center coupling,
    center-region energies etc.
    """

    def __init__(self, comm):
        """
        Initializer method.
        """

        System.__init__(self)
        self.file = None
        self._comm = comm

        ################################
        #   DEBUGGING MODE VARIABLES   #
        self.coupling_perturbation = 0.0
        #       USE WITH CAUTION       #
        ################################

    def _check_read_file_path(self):
        """
        Checks whether user specified a read file path prior to any method
        calls.
        """

        assert self.file_path is not None, "Fetch file path not specified."

    def set_file_path(self, file_path):
        """
        Sets file path to fetch the file data from.
        """
        System.set_file_path(self, file_path)
        if self._comm.Get_size() > 1:
            self.file = h5py.File(file_path, "r", driver="mpio", comm=self._comm)
        else:
            self.file = h5py.File(file_path, "r")
        assert self.file.attrs["type"] == "PREPTINIEFile", "Invalid file type"

    def get_center_energies(self):
        """
        Returns energies of the central region in the transport setup.
        """
        self._check_read_file_path()

        return self.file["/center/hamiltonian"][:]

    def get_center_potential(self):
        """
        Returns potential energy at a grid of the central region.
        """

        return self.file["/center/potential"][:]

    def get_lead_energies(self, lead_nbr):
        """
        Returns energies of the lead 'lead_nbr' with discretization step
        `delta_energy`.
        """

        self._check_read_file_path()
        assert (
            lead_nbr < self.file["/leads"].attrs["num_leads"]
        ), "Invalid lead number specified"

        return self.file["/leads/lead_" + str(lead_nbr) + "/hamiltonian"][:]

    def get_center_lead_coupling_mat(self, cpl_nbr):
        """
        Returns the coupling matrix between central region and a lead.
        """

        self._check_read_file_path()
        assert (
            cpl_nbr < self.file["/couplings"].attrs["num_couplings"]
        ), "Invalid coupling number specified"

        return (self.file["/couplings/coupling_" +
                          str(cpl_nbr) +
                          "/coupling_matrix"][:] +
                self.coupling_perturbation)

    def get_num_leads(self):
        """
        Returns the number of leads.
        """

        self._check_read_file_path()

        return self.file["/leads"].attrs["num_leads"]

    def get_num_couplings(self):
        """
        Returns the number of couplings.
        """

        self._check_read_file_path()

        return self.file["/couplings"].attrs["num_couplings"]

    def get_center_type(self):
        """
        Returns type of the central region.
        """

        return self.file["/center"].attrs["type"]

    def get_lead_energy_spacing(self):
        """
        Returns average lead probe energy spacing.
        """

        delta_E = []

        for i in range(self.get_num_leads()):
            delta_E.append(self.file["leads/lead_" +
                                     str(i)].attrs["energy_spacing"])

        return np.mean(delta_E)

    ###########################################################################
    #                      DEBUGGING MODE ONLY CODE                           #
    def set_coupling_perturbation(self, delta):
        """
        Setting up small perturbation for the coupling for stability testing
        purposes.
        """

        self.coupling_perturbation = delta

    #                        PROCEED WITH CAUTION                             #
    ###########################################################################
